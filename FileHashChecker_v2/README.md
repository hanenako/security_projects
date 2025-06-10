# 🔐 FileHashChecker_v2

목표: 악성코드 탐지, 무결성 검사 기능 강화

기능	설명
📁 디렉토리 재귀 검사: 특정 폴더 전체의 해시를 저장/비교

📅 스냅샷 기능: 특정 시점 해시값 JSON 저장 & 비교

📉 해시 변경 리포트: 변경된 파일만 로그로 출력 (변경 전/후 SHA256 비교)

☁️ VirusTotal 연동: 의심 파일을 API로 자동 스캔 (API Key 필요)

📧 경고 알림: 해시 변조 시 이메일 or 슬랙 or Discord 알림

1. hashchecker/scanner.py에 scan_directory 함수를 먼저 구현
2. 스냅샷, 비교, 출력, 알림 기능을 module.py 파일로 분리해서 작성
3. main.py를 실행하여 기능이 올바른지 테스트
4. tests/test_scanner.py를 작성하여 기본 동작 자동화

FileHashChecker-v2/

├── hashchecker/

│   ├── __init__.py

│   ├── scanner.py         # 해시 계산 및 검사

│   ├── snapshot.py        # 스냅샷 저장/비교

│   ├── reporter.py        # 변화 리포트 출력

│   └── notifier.py        # 알림

├── snapshots/

│   └── 2025-06-10-snapshot.json

├── tests/

│   └── test_scanner.py

├── main.py                # CLI 실행 진입점

├── requirements.txt

└── README.md