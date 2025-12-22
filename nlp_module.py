import subprocess

def ask_ollama(user_input: str) -> str:
    try:
        result = subprocess.run(
            ["ollama", "run", "llama3"],
            input=user_input,
            text=True,
            encoding="utf-8",
            capture_output=True,
            timeout=10
        )
        return result.stdout.strip()
    except:
        return "UNKNOWN"

def nlp_to_command(user_input: str) -> str:
    """자연어 → 터미널 명령어"""
    text = user_input.lower()

    # 1️⃣ 옵션 있는 구체 규칙 (우선 처리)
    if "자세히" in text or "상세" in text:
        return "ls -l"
    if "숨김" in text:
        return "ls -a"
    if "몇 개" in text or "개수" in text:
        return ask_ollama(user_input)


    # 2️⃣ 기본 규칙 (dict)
    rules = {
        "rm": ["삭제", "지우기"],
        "touch": ["파일 만들기", "새 파일"],
        "cd": ["이동", "들어가"],
        "pwd": ["현재", "위치", "어디"],
        "ls": ["폴더", "목록"]
    }

    for command, keywords in rules.items():
        for kw in keywords:
            if kw in text:
                return command

    return ask_ollama(user_input)
