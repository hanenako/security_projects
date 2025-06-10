import hashlib  # 해쉬값 계산을 위한 라이브러리 import
import argparse # 인자 처리용 라이브러리
import sys  # sys
import os   # 디렉토리 읽어오기용 라이브러리
import csv  # csv 파일 처리
import json # json 파일 처리
from collections import defaultdict

# all_hashes
# { "ALGORITHM" : { "FILENAME" : "HASHVALUE" } }
# { "SHA256" : { "test.txt" : "asd1231dax12334e" } }

# file_based_result
# { "FILENAME" : { "ALGORITHM" : "HASHVALUE"} }
# { "test.txt" : { "SHA256" : "asd1231dax12334e" } }


# argparse 설정
parser = argparse.ArgumentParser(description="해시값 취득 프로그램")

# 기본 인자들
parser.add_argument("file_path", nargs="?", help="해시값 취득할 파일 경로")  # --list만 사용할 때를 위해 text도 optional로 처리
parser.add_argument("-c", "--check", help="지정 파일과 입력한 해시값을 비교", default=None)
parser.add_argument("-f", "--check-file", nargs="*", help="지정 파일 여러개의 해시값을 비교하여 동일 파일인지 확인", default=None, dest="check_file")
parser.add_argument("-a", "--algorithm", help="선택적 해시 알고리즘 (예: sha256)", default=None)
parser.add_argument("-o", "--output", help="결과를 저장할 파일 경로(.TXT, .CSV, .JSON, .MD 등)", default=None)
parser.add_argument("--list-algorithms", action="store_true", help="사용 가능한 해시 알고리즘 목록 출력")
parser.add_argument("-r", "--recursive", action="store_true", help="하위 디렉토리, 파일의 해쉬값을 취득", default=None)
            
args = parser.parse_args()

# 알고리즘 리스트(--list-algorithms)
available_algorithms = sorted(hashlib.algorithms_available)

# 프로그램상 기본 알고리즘 리스트
default_algorithms = ['md5', 'sha1', 'sha256', 'sha512']

if args.list_algorithms:
    print('사용 가능한 해시 알고리즘 목록:')
    for algo in available_algorithms:
        print(f'- {algo}')
    sys.exit(0)
    
if args.file_path is None and (not args.check_file or len(args.check_file) == 0):
    print('[오류] 파일을 지정하세요')
    parser.print_help()
    sys.exit(1)

#해시값 취득 함수
def calculate_hashes(file_path, algo):
    result = {}
    try:
        if os.path.isfile(file_path):
            # 파일 1개 처리
            result_hash = hashlib.new(algo)
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    result_hash.update(chunk)
            result[os.path.basename(file_path)] = result_hash.hexdigest()

        else:
            # 디렉토리 처리
            if args.recursive:
                # 하위 디렉토리까지 탐색
                for root, dirs, files in os.walk(file_path):
                    for file in files:
                        full_path = os.path.join(root, file)
                        if os.path.isfile(full_path):
                            result_hash = hashlib.new(algo)
                            with open(full_path, "rb") as f:
                                for chunk in iter(lambda: f.read(4096), b""):
                                    result_hash.update(chunk)
                            # 기준 디렉토리 기준 상대 경로
                            relative_path = os.path.relpath(full_path, file_path)
                            result[relative_path] = result_hash.hexdigest()
            else:
                # 현재 디렉토리의 파일만 처리
                for file in os.listdir(file_path):
                    full_path = os.path.join(file_path, file)
                    if os.path.isfile(full_path):
                        result_hash = hashlib.new(algo)
                        with open(full_path, "rb") as f:
                            for chunk in iter(lambda: f.read(4096), b""):
                                result_hash.update(chunk)
                        result[file] = result_hash.hexdigest()

        return result
    
    except ValueError:
        print(f"[오류] 지원되지 않는 알고리즘: {algo}")
        print("다음 중에서 선택하세요:")
        print(", ".join(default_algorithms))
        sys.exit(1)
        
    except Exception as e:
        print(f"Error : {e}")
        
    return None
    
    
# 결과 저장용
final_results = []

# 알고리즘 리스트
algorithms = [args.algorithm] if args.algorithm else default_algorithms # args.algorithm 입력받지 않은 경우, default_algorithms를 저장

# 해시값 계산 및 결과 저장
all_hashes = {}
for algo in algorithms:
    hash_result = calculate_hashes(args.file_path, algo)    # hash_result에 해시값 계산 결과를 저장(딕셔너리)
    if hash_result:
        all_hashes[algo] = hash_result
        
# [출력 형식 변경]
# 파일 기준으로 재구성
file_based_result = defaultdict(dict)  # {파일명: {알고리즘: 해시값}}

for algo, hash_dict in all_hashes.items():
    for fname, hval in hash_dict.items():
        file_based_result[fname][algo] = hval
        
final_results = []
for fname in sorted(file_based_result):
    full_path = os.path.join(args.file_path, fname) if os.path.isdir(args.file_path) else fname
    size_kb = os.path.getsize(full_path) / 1024
    
    final_results.append(f"FileName: {fname}")
    final_results.append(f"FileSize: {size_kb:.2f} KB")
    
    for algo in sorted(file_based_result[fname]):
        final_results.append(f"{algo} : {file_based_result[fname][algo]}")
    final_results.append("")  # 줄 바꿈

if args.check:
    found_match = False
    for fname, algos in file_based_result.items():
        for algo, hval in algos.items():
            if hval.lower() == args.check.lower():
                print(f"[일치] {algo} 해시값이 '{fname}'과 일치합니다.")
                found_match = True
    if not found_match:
        print("[불일치] 일치하는 해시값이 없습니다.")
    sys.exit(0)
    
if args.check_file:
    check_file_hashes = {}
    for path in args.check_file:
        if not os.path.isfile(path):
            print(f"[오류] 파일이 존재하지 않습니다: {path}")
            continue
        try:
            if args.algorithm:
                check_algo = args.algorithm
            else:
                check_algo = "sha256"
            result_hash = hashlib.new(args.algorithm if args.algorithm else "sha256")
            with open(path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    result_hash.update(chunk)
            check_file_hashes[os.path.basename(path)] = result_hash.hexdigest()
            
        except Exception as e:
            print(f"[오류] 파일 비교 실패: {path} -> {e}")
            
    print(f"\n[check file result] : {check_algo}")
    for fname, hval in check_file_hashes.items():
        print(f"{fname}: {hval}")
        
    if(len(set(check_file_hashes.values()))) == 1:
        print("모든 파일의 해쉬 값이 동일합니다.")
    else:
        print("파일의 해시값이 동일하지 않습니다.")      
    sys.exit(0)
    
#콘솔 출력
if final_results:
    for line in final_results:
        print(line)
else:
    print('[오류] 해시값 취득에 실패했습니다.')

# 결과를 파일로 출력(-o, --output)
if args.output:
    try:
        # csv파일 출력
        if args.output.lower().endswith('.csv'):
            with open(args.output, "w", newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["FileName", "Algorithm", "HashValue"])
                for fname, hash_dict in sorted(file_based_result.items()):
                    for algo, hval in hash_dict.items():
                        writer.writerow([fname, algo, hval])
            print(f"\n결과가 파일에 저장됨: {args.output}")
            
        # json 파일 출력
        elif args.output.lower().endswith('.json'):
            with open(args.output, "w", encoding='utf-8') as f:
                json.dump(file_based_result, f, ensure_ascii=False, indent=4)
            print(f"\n결과가 파일에 저장됨: {args.output}")
        
        # md 파일 출력    
        elif args.output.endswith('.md'):
            with open(args.output, "w", encoding='utf-8') as f:
                f.write("# 해시값 검사 결과\n\n")
                f.write("| FileName | Algorithm | HashValue |\n")
                f.write("|----------|-----------|-----------|\n")
                for fname in sorted(file_based_result):
                    for algo in sorted(file_based_result[fname]):
                        hash_value = file_based_result[fname][algo]
                        f.write(f"| {fname} | {algo.upper()} | `{hash_value}` |\n")
            print(f"\n결과가 파일에 저장됨: {args.output}")
                
                            
        # 그 외 파일 처리
        else:
            with open(args.output, "w", encoding='utf-8') as f:
                f.write('\n'.join(final_results))
            print(f"\n결과가 파일에 저장됨: {args.output}")   

    except Exception as e:
        print(f"[오류] 파일 저장 실패: {e}")