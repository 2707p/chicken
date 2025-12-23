print("### LOADED kyeong/command_recommender.py ###")

# ==============================
# Command Knowledge Base (JSON 기반)
# ==============================

COMMANDS = {
    "ls": {"danger": "low"},
    "ls -l": {"danger": "low"},
    "pwd": {"danger": "low"},
    "cd": {"danger": "low"},
    "mkdir": {"danger": "medium"},
    "touch": {"danger": "medium"},
    "cp": {"danger": "medium"},
    "mv": {"danger": "medium"},
    "cat": {"danger": "low"},
    "clear": {"danger": "low"},
    "python": {"danger": "medium"},
    "rm": {"danger": "high"},
    "rm -r": {"danger": "high"},
    "rm -rf": {"danger": "high"},
    "kill": {"danger": "high"},
}

# ==============================
# Natural Language → Command
# ==============================

def nlp_to_command(user_input: str) -> str:
    text = user_input.lower()

    # 1️⃣ 삭제 계열 (위험 우선)
    if "강제로" in text:
        return "rm -rf"
    if "폴더" in text and "삭제" in text:
        return "rm -r"
    if "삭제" in text or "지워" in text:
        return "rm"

    # 2️⃣ 옵션 명령
    if "자세히" in text or "상세" in text:
        return "ls -l"

    # 3️⃣ 기본 명령
    if "목록" in text or "파일" in text or "폴더" in text:
        return "ls"
    if "위치" in text or "어디" in text or "현재" in text:
        return "pwd"
    if "이동" in text or "들어가" in text:
        return "cd"
    if "만들" in text:
        return "mkdir"
    if "복사" in text:
        return "cp"
    if "이름" in text or "변경" in text:
        return "mv"
    if "내용" in text or "보기" in text:
        return "cat"
    if "화면" in text or "정리" in text:
        return "clear"
    if "실행" in text:
        return "python"

    return "UNKNOWN"
