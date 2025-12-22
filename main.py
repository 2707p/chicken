import tkinter as tk
from PIL import Image, ImageTk
import json
import os
import subprocess
from tkinter import messagebox

root = tk.Tk()
root.configure(bg="#ffc0cb")
root.title("💕Terminal Helper💕")
root.geometry("700x600")

# 최근입력기록저장용리스트
recent_inputs = []

# 둥근 모서리 사각형 함수
def create_rounded_rect(canvas, x1, y1, x2, y2, radius=15, **kwargs):
    points = [
        x1+radius, y1,
        x2-radius, y1,
        x2, y1,
        x2, y1+radius,
        x2, y2-radius,
        x2, y2,
        x2-radius, y2,
        x1+radius, y2,
        x1, y2,
        x1, y2-radius,
        x1, y1+radius,
        x1, y1
    ]
    return canvas.create_polygon(points, smooth=True, **kwargs)

# commands.json 로드
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE_DIR, "data", "commands.json"), encoding="utf-8") as f:
    commands = json.load(f)

def get_command_info(cmd):
    if cmd in commands:
        return commands[cmd]
    base = cmd.split()[0]
    return commands.get(base)

# 입력창 배경
entry_canvas = tk.Canvas(root, bg="#ffc0cb", highlightthickness=0)
entry_canvas.place(relx=0.5, rely=0.08, anchor="center", relwidth=0.7, relheight=0.06)

def redraw_entry_bg(event=None):
    entry_canvas.delete("all")
    w = entry_canvas.winfo_width()
    h = entry_canvas.winfo_height()
    if w > 1 and h > 1:
        r = min(20, h // 2)
        create_rounded_rect(entry_canvas, 4, 4, w, h, r, fill="#ffa0ab")
        create_rounded_rect(entry_canvas, 2, 2, w-2, h-2, r, fill="white")

entry_canvas.bind("<Configure>", redraw_entry_bg)

# 입력창 (까만 테두리 제거)
entry = tk.Entry(
    root,
    bd=0,
    bg="white",
    fg="#333333",
    relief="flat",
    highlightthickness=0,
    insertbackground="#ff69b4"
)
entry.place(relx=0.5, rely=0.08, anchor="center", relwidth=0.66, relheight=0.045)

# 명령어 추천 박스 (원래 네가 만든 연파랑 박스 유지)
recommend_canvas = tk.Canvas(root, bg="#ffc0cb", highlightthickness=0)
recommend_canvas.place(relx=0.5, rely=0.23, anchor="center", relwidth=0.7, relheight=0.13)

def redraw_recommend_bg(event=None):
    recommend_canvas.delete("all")
    w = recommend_canvas.winfo_width()
    h = recommend_canvas.winfo_height()
    if w > 1 and h > 1:
        r = min(40, h // 2)
        create_rounded_rect(recommend_canvas, 4, 4, w, h, r, fill="#a0d5f0")
        create_rounded_rect(recommend_canvas, 2, 2, w-2, h-2, r, fill="lightblue")

recommend_canvas.bind("<Configure>", redraw_recommend_bg)

recommend_text = tk.Text(
    root,
    bd=0,
    bg="lightblue",
    fg="#2c5f7f",
    relief="flat",
    highlightthickness=0,
    wrap="word"
)
recommend_text.place(relx=0.5, rely=0.23, anchor="center", relwidth=0.64, relheight=0.09)

# 출력 / 주석 배경 (둥근 모서리)
text_canvas = tk.Canvas(root, bg="#ffc0cb", highlightthickness=0)
text_canvas.place(relx=0.5, rely=0.52, anchor="center", relwidth=0.82, relheight=0.35)

def redraw_text_bg(event=None):
    text_canvas.delete("all")
    w = text_canvas.winfo_width()
    h = text_canvas.winfo_height()
    if w > 1 and h > 1:
        create_rounded_rect(text_canvas, 2, 2, w-2, h-2, 20, fill="white")

text_canvas.bind("<Configure>", redraw_text_bg)

# 출력창
text = tk.Text(
    root,
    bd=0,
    bg="white",
    fg="#333333",
    relief="flat",
    highlightthickness=0,
    wrap="word",
    insertbackground="#ff69b4"
)
text.place(relx=0.5, rely=0.52, anchor="center", relwidth=0.78, relheight=0.32)

# 헬로키티 이미지 복구
try:
    img_top = ImageTk.PhotoImage(Image.open("hello_kitty_top.png").resize((50, 50)))
    img_bottom = ImageTk.PhotoImage(Image.open("hello_kitty_bottom.png").resize((50, 50)))

    tk.Label(root, image=img_top, bg="#ffc0cb").place(relx=0.02, rely=0.02)
    tk.Label(root, image=img_bottom, bg="#ffc0cb").place(relx=0.98, rely=0.98, anchor="se")
except:
    print("헬로키티 이미지 없음")

# 자동 주석 표시
def update_comment(event=None):
    recommend_text.delete(1.0, tk.END)
    cmd = entry.get().strip()
    info = get_command_info(cmd)
    if info:
        recommend_text.insert(
            tk.END,
            f"📌 {info['description']}\n"
            f"⚠️ 위험도: {info['danger']}\n"
            f"💡 예시: {info['example']}"
        )

entry.bind("<KeyRelease>", update_comment)

# 실행
def execute():
    cmd = entry.get().strip()
    if not cmd:
        return

    info = get_command_info(cmd)
    if not info:
        messagebox.showerror("차단", "허용되지 않은 명령어입니다.")
        return

    if info["danger"] == "high":
        if not messagebox.askyesno("경고", "위험한 명령어입니다.\n실행할까요?"):
            return

    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    text.insert(tk.END, f"> {cmd}\n")
    text.insert(tk.END, result.stdout or result.stderr)
    text.insert(tk.END, "\n")

    entry.delete(0, tk.END)

entry.bind("<Return>", lambda e: execute())

# 실행 버튼
button_canvas = tk.Canvas(root, bg="#ffc0cb", highlightthickness=0)
button_canvas.place(relx=0.5, rely=0.8, anchor="center", width=150, height=50)

def draw_button(hover=False):
    button_canvas.delete("all")
    color = "#ff69b4" if hover else "#ff85a1"
    create_rounded_rect(button_canvas, 2, 2, 148, 48, 15, fill=color)
    button_canvas.create_text(75, 25, text="✨ 실행 ✨", fill="white", font=("Arial", 12, "bold"))

draw_button()
button_canvas.bind("<Enter>", lambda e: draw_button(True))
button_canvas.bind("<Leave>", lambda e: draw_button(False))
button_canvas.bind("<Button-1>", lambda e: execute())

root.mainloop()
