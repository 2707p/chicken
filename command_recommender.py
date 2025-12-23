import tkinter as tk

BG_COLOR = "#ffc0cb"     # 메인 배경
BOX_COLOR = "#e6f2ff"    # 연파랑
TEXT_COLOR = "#333333"


class CommandRecommenderUI(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)

        self.title("💡 명령어 추천")
        self.configure(bg=BG_COLOR)
        self.resizable(False, False)

        # 메인 창 오른쪽에 붙이기
        master.update_idletasks()
        x = master.winfo_x() + master.winfo_width() + 5
        y = master.winfo_y()
        self.geometry(f"420x400+{x}+{y}")

        # 메인 닫히면 같이 닫힘
        master.bind("<Destroy>", lambda e: self.destroy())

        # 자연어 입력 라벨
        tk.Label(
            self,
            text="🗣 사용하고 싶은 명령어를 설명하세요.",
            bg=BG_COLOR,
            fg=TEXT_COLOR,
            font=("Apple SD Gothic Neo", 13, "bold")
        ).pack(anchor="w", padx=20, pady=(15, 5))

        # 자연어 입력창
        self.input_canvas = tk.Canvas(
            self, width=380, height=45,
            bg=BG_COLOR, highlightthickness=0
        )
        self.input_canvas.pack()

        self._rounded_box(self.input_canvas, 5, 5, 375, 40, 18)

        self.input_entry = tk.Entry(
            self.input_canvas,
            bd=0,
            highlightthickness=0,
            bg=BOX_COLOR,
            fg=TEXT_COLOR,
            font=("Apple SD Gothic Neo", 12)
        )
        self.input_canvas.create_window(
            15, 22, window=self.input_entry, anchor="w", width=350
        )

        # ⭐ 엔터 → 추천 실행
        self.input_entry.bind("<Return>", self.recommend_command)

        # 출력 라벨
        tk.Label(
            self,
            text="📋 추천 명령어",
            bg=BG_COLOR,
            fg=TEXT_COLOR,
            font=("Apple SD Gothic Neo", 13, "bold")
        ).pack(anchor="w", padx=20, pady=(15, 5))

        # 출력창 (높이 증가)
        self.output_canvas = tk.Canvas(
            self, width=380, height=230,
            bg=BG_COLOR, highlightthickness=0
        )
        self.output_canvas.pack()

        self._rounded_box(self.output_canvas, 5, 5, 375, 225, 20)

        self.output_text = tk.Text(
            self.output_canvas,
            bd=0,
            highlightthickness=0,
            bg=BOX_COLOR,
            fg=TEXT_COLOR,
            font=("Apple SD Gothic Neo", 11),
            wrap="word"
        )
        self.output_canvas.create_window(
            15, 15, window=self.output_text,
            anchor="nw", width=350, height=195
        )

        self.output_text.insert(
            "end",
            "👉 설명을 입력하고\n👉 Enter를 누르세요"
        )

    # 둥근 사각형
    def _rounded_box(self, canvas, x1, y1, x2, y2, r):
        points = [
            x1+r, y1, x2-r, y1, x2, y1,
            x2, y1+r, x2, y2-r, x2, y2,
            x2-r, y2, x1+r, y2, x1, y2,
            x1, y2-r, x1, y1+r, x1, y1
        ]
        canvas.create_polygon(
            points, smooth=True, fill=BOX_COLOR, outline=BOX_COLOR
        )

    # ⭐ 추천 로직 연결
    def recommend_command(self, event=None):
        user_input = self.input_entry.get().strip()
        if not user_input:
            return

        command = nlp_to_command(user_input)

        self.output_text.delete("1.0", "end")
        if command == "UNKNOWN":
            self.output_text.insert(
                "end",
                "❓ 이해하지 못했어요.\n다시 입력해 주세요."
            )
        else:
            result = f"✅ 추천 명령어\n\n{command}"
            self.output_text.insert("end", result)


print("### LOADED command_recommender.py ###")

# ==============================
# Command Knowledge Base
# ==============================

COMMANDS = {
    "ls": {
        "description": "현재 폴더에 있는 파일과 폴더 목록을 보여준다.",
        "example": "ls",
        "keywords": ["목록", "리스트", "보기", "확인", "list"]
    },
    "ls -l": {
        "description": "파일 목록을 상세 정보(권한, 크기, 날짜)와 함께 보여준다.",
        "example": "ls -l",
        "keywords": ["자세히", "상세", "detailed", "디테일"]
    },
    "pwd": {
        "description": "현재 내가 위치한 폴더의 전체 경로를 출력한다.",
        "example": "pwd",
        "keywords": ["위치", "어디", "경로", "현재", "where"]
    },
    "cd": {
        "description": "다른 폴더로 이동한다.",
        "example": "cd Documents",
        "keywords": ["이동", "들어가", "변경", "change"]
    },
    "mkdir": {
        "description": "새로운 폴더를 생성한다.",
        "example": "mkdir test_folder",
        "keywords": ["폴더", "디렉토리", "만들", "생성", "folder"]
    },
    "touch": {
        "description": "빈 파일을 새로 생성한다.",
        "example": "touch hello.txt",
        "keywords": ["파일", "만들", "생성", "create"]
    },
    "cp": {
        "description": "파일이나 폴더를 복사한다.",
        "example": "cp a.txt b.txt",
        "keywords": ["복사", "copy", "복제"]
    },
    "mv": {
        "description": "파일이나 폴더를 이동하거나 이름을 변경한다.",
        "example": "mv old.txt new.txt",
        "keywords": ["이름", "변경", "rename", "move"]
    },
    "cat": {
        "description": "텍스트 파일의 내용을 터미널에 출력한다.",
        "example": "cat readme.txt",
        "keywords": ["내용", "읽기", "출력", "read"]
    },
    "clear": {
        "description": "터미널 화면을 깨끗하게 지운다.",
        "example": "clear",
        "keywords": ["화면", "정리", "지우기", "clear"]
    },
    "python": {
        "description": "파이썬 파일을 실행한다.",
        "example": "python main.py",
        "keywords": ["실행", "파이썬", "run", "python"]
    },
    "rm": {
        "description": "파일을 삭제한다. 삭제된 파일은 휴지통으로 가지 않는다.",
        "example": "rm test.txt",
        "keywords": ["삭제", "지우기", "제거", "delete", "remove"]
    },
    "rm -r": {
        "description": "폴더와 그 안의 모든 파일을 삭제한다.",
        "example": "rm -r test_folder",
        "keywords": ["폴더삭제", "디렉토리삭제"]
    },
    "rm -rf": {
        "description": "확인 없이 파일이나 폴더를 강제로 삭제한다. 매우 위험하다.",
        "example": "rm -rf test_folder",
        "keywords": ["강제", "강제삭제", "force"]
    },
    "kill": {
        "description": "실행 중인 프로세스를 종료한다.",
        "example": "kill 1234",
        "keywords": ["종료", "프로세스", "kill", "중지"]
    }
}

# ==============================
# Natural Language → Command
# ==============================

def nlp_to_command(user_input: str) -> str:
    text = user_input.lower()

    # 1순위: 삭제 관련 (가장 위험하고 구체적)
    if any(kw in text for kw in ["강제", "강제로"]) and any(kw in text for kw in ["삭제", "지워"]):
        return "rm -rf"
    if any(kw in text for kw in ["폴더", "디렉토리"]) and any(kw in text for kw in ["삭제", "지워", "제거"]):
        return "rm -r"
    if any(kw in text for kw in COMMANDS["rm"]["keywords"]):
        return "rm"

    # 2순위: 생성/만들기 관련 (구체적 → 일반)
    if any(kw in text for kw in ["만들", "생성"]):
        if any(kw in text for kw in ["폴더", "디렉토리"]):
            return "mkdir"
        if any(kw in text for kw in ["파일"]):
            return "touch"
        # "만들"만 있으면 기본적으로 폴더
        return "mkdir"

    # 3순위: 파일 조작
    if any(kw in text for kw in COMMANDS["cp"]["keywords"]):
        return "cp"
    if any(kw in text for kw in COMMANDS["mv"]["keywords"]) and ("이름" in text or "rename" in text):
        return "mv"
    if any(kw in text for kw in COMMANDS["cat"]["keywords"]) and ("파일" in text or "텍스트" in text):
        return "cat"

    # 4순위: 이동/탐색
    if any(kw in text for kw in COMMANDS["cd"]["keywords"]):
        return "cd"
    if any(kw in text for kw in COMMANDS["pwd"]["keywords"]):
        return "pwd"

    # 5순위: ls 관련 (자세히가 먼저)
    if any(kw in text for kw in COMMANDS["ls -l"]["keywords"]):
        return "ls -l"
    if any(kw in text for kw in COMMANDS["ls"]["keywords"]):
        return "ls"
    
    # 6순위: 기타
    if any(kw in text for kw in COMMANDS["clear"]["keywords"]):
        return "clear"
    if any(kw in text for kw in COMMANDS["python"]["keywords"]):
        return "python"
    if any(kw in text for kw in COMMANDS["kill"]["keywords"]):
        return "kill"

    # 마지막: 기본값
    if "파일" in text or "폴더" in text:
        return "ls"

    return "UNKNOWN"