def print_report(diff_result: dict):
    print("\n변경 사항 리포트:")
    print("-" * 40)

    if diff_result["added"]:
        print("추가된 파일:")
        for f in diff_result["added"]:
            print(f"  + {f}")
    if diff_result["removed"]:
        print("삭제된 파일:")
        for f in diff_result["removed"]:
            print(f"  - {f}")
    if diff_result["modified"]:
        print("변경된 파일:")
        for f, (old, new) in diff_result["modified"].items():
            print(f"  * {f}\n    - OLD: {old}\n    - NEW: {new}")

    if not any(diff_result.values()):
        print("변경 사항 없음.")
