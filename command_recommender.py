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

        #주석 메인 창 오른쪽에 붙이기
        master.update_idletasks()
        x = master.winfo_x() + master.winfo_width() + 5
        y = master.winfo_y()
        self.geometry(f"420x300+{x}+{y}")

        #주석 메인 닫히면 같이 닫힘
        master.bind("<Destroy>", lambda e: self.destroy())

        #주석 자연어 입력 라벨
        tk.Label(
            self,
            text="🗣 자연어 입력",
            bg=BG_COLOR,
            fg=TEXT_COLOR,
            font=("Apple SD Gothic Neo", 13, "bold")
        ).pack(anchor="w", padx=20, pady=(15, 5))

        #주석 자연어 입력창 (둥근)
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

        #주석 출력 라벨
        tk.Label(
            self,
            text="📋 추천 결과",
            bg=BG_COLOR,
            fg=TEXT_COLOR,
            font=("Apple SD Gothic Neo", 13, "bold")
        ).pack(anchor="w", padx=20, pady=(15, 5))

        #주석 출력창 (둥근)
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
            15, 15, window=self.output_text, anchor="nw", width=350, height=95
        )

        self.output_text.insert(
            "end",
            "👉 자연어를 입력하면\n👉 여기에 추천 결과가 표시됩니다"
        )

    #주석 둥근 사각형
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
