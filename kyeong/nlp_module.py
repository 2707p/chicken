print("### LOADED kyeong/nlp_module.py ###")

# ==============================
# Command Knowledge Base
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
# 1️⃣ Intent Classification
# ==============================

def classify_intent(text: str) -> str:
    if "삭제" in text or "지워" in text:
        return "DELETE"
    if "목록" in text or "보여" in text or "확인" in text:
        return "LIST"
    if "이동" in text or "들어가" in text:
        return "MOVE"
    if "만들" in text:
        return "CREATE"
    if "복사" in text:
        return "COPY"
    if "이름" in text or "변경" in text:
        return "RENAME"
    if "위치" in text or "현재" in text:
        return "WHERE"
    if "실행" in text:
        return "RUN"
    return "UNKNOWN"

# ==============================
# 2️⃣ Intent → Command Mapping
# ==============================

def intent_to_command(intent: str, text: str) -> str:
    if intent == "DELETE":
        if "강제로" in text:
            return "rm -rf"
        if "폴더" in text:
            return "rm -r"
        return "rm"

    if intent == "LIST":
        if "자세히" in text or "상세" in text:
            return "ls -l"
        return "ls"

    if intent == "MOVE":
        return "cd"

    if intent == "CREATE":
        return "mkdir"

    if intent == "COPY":
        return "cp"

    if intent == "RENAME":
        return "mv"

    if intent == "WHERE":
        return "pwd"

    if intent == "RUN":
        return "python"

    return "UNKNOWN"

# ==============================
# 3️⃣ Natural Language → Command
# ==============================

def nlp_to_command(user_input: str) -> str:
    text = user_input.lower()
    intent = classify_intent(text)
    return intent_to_command(intent, text)