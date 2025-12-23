import tkinter as tk
from PIL import Image, ImageTk
import json
import os
import subprocess
import sys
from pathlib import Path
from tkinter import messagebox
from command_recommender import CommandRecommenderUI

root = tk.Tk()
root.configure(bg="#ffc0cb")
root.title("💕Terminal Helper💕")
root.geometry("700x600")

CommandRecommenderUI(root)

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

# ==================== 대시보드 함수 추가 ====================
def open_dashboard():
    #대시보드 GUI를 여는 함수"""
    try:
        # kyeong/dashboard.py의 DashboardGUI 클래스 import
        current_dir = Path(__file__).parent
        kyeong_path = current_dir / "kyeong"
        
        # kyeong 폴더를 sys.path에 추가
        if str(kyeong_path) not in sys.path:
            sys.path.insert(0, str(kyeong_path))
        
        # dashboard 모듈 import
        import dashboard
        
        # GUI 대시보드 실행
        dashboard.DashboardGUI(root)
        
    except Exception as e:
        # 에러 발생 시 메시지박스 표시
        messagebox.showerror("오류", f"대시보드를 열 수 없습니다.\n\n{str(e)}")

def create_dashboard_button(parent):
    #대시보드 함수
    normal_color = "#ff85a1"
    hover_color = "#ff69b4"
    
    button = tk.Button(
        parent,
        text="💻 현재 상태 확인",
        font=("맑은 고딕", 11, "bold"),
        bg=normal_color,
        fg="white",
        activebackground=hover_color,
        activeforeground="white",
        relief="flat",
        cursor="hand2",
        padx=20,
        pady=10,
        command=open_dashboard,
        borderwidth=0,
        highlightthickness=0
    )
    
    # 호버 효과
    def on_hover(e):
        button.config(bg=hover_color)
    
    def on_leave(e):
        button.config(bg=normal_color)
    
    button.bind("<Enter>", on_hover)
    button.bind("<Leave>", on_leave)
    
    return button
# ==================== 대시보드 함수 끝 ====================

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


def add_entry_placeholder(entry, placeholder):
    entry.insert(0, placeholder)
    entry.config(fg="gray")

    def on_focus_in(event):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.config(fg="#333333")  # 원래 글자색

    def on_focus_out(event):
        if entry.get() == "":
            entry.insert(0, placeholder)
            entry.config(fg="gray")

    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)

add_entry_placeholder(entry, "명령어를 입력하세요. 명령어는 실제로 작동합니다.")

# 주석나오느대
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

def add_text_placeholder(text_widget, placeholder):
    text_widget.insert(1.0, placeholder)
    text_widget.config(fg="gray")

    def on_focus_in(event):
        if text_widget.get(1.0, tk.END).strip() == placeholder:
            text_widget.delete(1.0, tk.END)
            text_widget.config(fg="#2c5f7f")  # 원래 글자색

    def on_focus_out(event):
        if text_widget.get(1.0, tk.END).strip() == "":
            text_widget.insert(1.0, placeholder)
            text_widget.config(fg="gray")

    text_widget.bind("<FocusIn>", on_focus_in)
    text_widget.bind("<FocusOut>", on_focus_out)

add_text_placeholder(recommend_text, "명령어 입력 후 실시간으로 출력되는 설명을 확인하세요.")


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

text.insert(tk.END, "여기는 출력창입니다.\n")


# ==================== 대시보드 버튼 추가 ====================
dashboard_btn = create_dashboard_button(root)
dashboard_btn.place(relx=0.5, rely=0.75, anchor="center")
# ==================== 대시보드 버튼 끝 ====================

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

#안뇽
root.mainloop()