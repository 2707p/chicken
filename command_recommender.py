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
        self.geometry(f"420x300+{x}+{y}")

        # 메인 닫히면 같이 닫힘
        master.bind("<Destroy>", lambda e: self.destroy())

        # 자연어 입력 라벨
        tk.Label(
            self,
            text="🗣 자연어 입력",
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
            text="📋 추천 결과",
            bg=BG_COLOR,
            fg=TEXT_COLOR,
            font=("Apple SD Gothic Neo", 13, "bold")
        ).pack(anchor="w", padx=20, pady=(15, 5))

        # 출력창
        self.output_canvas = tk.Canvas(
            self, width=380, height=130,
            bg=BG_COLOR, highlightthickness=0
        )
        self.output_canvas.pack()

        self._rounded_box(self.output_canvas, 5, 5, 375, 125, 20)

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
            anchor="nw", width=350, height=95
        )

        self.output_text.insert(
            "end",
            "👉 자연어를 입력하고\n👉 Enter를 누르세요"
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
            self.output_text.insert(
                "end",
                f"✅ 추천 명령어\n\n{command}"
            )


print("### LOADED command_recommender.py ###")

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
# Natural Language → Command
# ==============================

def nlp_to_command(user_input: str) -> str:
    text = user_input.lower()

    # 1순위: 삭제 관련 (가장 구체적)
    if "강제로" in text and "삭제" in text:
        return "rm -rf"
    if "폴더" in text and "삭제" in text:
        return "rm -r"
    if "삭제" in text or "지워" in text or "제거" in text:
        return "rm"

    # 2순위: 생성/만들기 관련
    if "만들" in text and ("폴더" in text or "디렉토리" in text):
        return "mkdir"
    if "만들" in text and "파일" in text:
        return "touch"
    if "생성" in text and ("폴더" in text or "디렉토리" in text):
        return "mkdir"
    if "생성" in text and "파일" in text:
        return "touch"
    if "만들" in text or "생성" in text:
        return "mkdir"

    # 3순위: 파일 조작
    if "복사" in text or "copy" in text:
        return "cp"
    if ("이름" in text and "변경" in text) or "이동" in text and "파일" in text:
        return "mv"
    if "내용" in text or ("보여" in text and "파일" in text):
        return "cat"

    # 4순위: 이동/탐색
    if "이동" in text or "들어가" in text or "디렉토리 변경" in text:
        return "cd"
    if "위치" in text or "어디" in text or "현재 경로" in text:
        return "pwd"

    # 5순위: ls 관련 (자세히가 먼저)
    if "자세히" in text or "상세" in text or "detailed" in text:
        return "ls -l"
    if "목록" in text or "리스트" in text or "보여" in text:
        return "ls"
    
    # 6순위: 기타
    if "화면" in text or "정리" in text or "clear" in text:
        return "clear"
    if "실행" in text or "파이썬" in text:
        return "python"
    if "종료" in text or "kill" in text:
        return "kill"

    # 마지막: 파일/폴더만 단독으로 언급된 경우
    if "파일" in text or "폴더" in text:
        return "ls"

    return "UNKNOWN"