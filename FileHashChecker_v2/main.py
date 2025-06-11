import argparse
from hashchecker.scanner import scan_directory
from hashchecker.snapshot import save_snapshot, load_snapshot, compare_snapshots
from hashchecker.reporter import print_report
from hashchecker.notifier import send_alert  # 선택 기능

def main():
    parser = argparse.ArgumentParser(description="FileHashChecker v2 - Directory hash scanner")
    parser.add_argument("dir", help="검사할 디렉토리 경로")
    parser.add_argument("-m", "--method", choices=["sha256","md5"], default="sha256")
    parser.add_argument("-s", "--snapshot", action="store_true", help="스냅샷 저장")
    parser.add_argument("-c", "--compare", help="비교할 스냅샷 파일 경로")
    parser.add_argument("-n", "--notify", action="store_true", help="변경 시 알림 전송")
    args = parser.parse_args()

    current = scan_directory(args.dir, method=args.method)

    if args.snapshot:
        snap_file = save_snapshot(current)
        print(f"스냅샷 저장됨: {snap_file}")
        return

    if args.compare:
        old = load_snapshot(args.compare)
        changed = compare_snapshots(old, current)
        print_report(changed)
        if args.notify and changed['modified']:
            print("modified")
            # send_alert(changed)
        return

    # 기본 동작: 즉시 출력
    for path, h in current.items():
        print(f"{path}: {h}")

if __name__ == "__main__":
    main()