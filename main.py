import tkinter as tk
from PIL import Image, ImageTk

root = tk.Tk()
root.configure(bg="#ffc0cb")
root.title("💕Terminal Helper💕")
root.geometry("700x600")

# 최근입력기록저장용리스트
recent_inputs = []

# 둥근 모서리 사각형 함수
def create_rounded_rect(canvas, x1, y1, x2, y2, radius=15, **kwargs):
    points = [x1+radius, y1,
              x1+radius, y1,
              x2-radius, y1,
              x2-radius, y1,
              x2, y1,
              x2, y1+radius,
              x2, y1+radius,
              x2, y2-radius,
              x2, y2-radius,
              x2, y2,
              x2-radius, y2,
              x2-radius, y2,
              x1+radius, y2,
              x1+radius, y2,
              x1, y2,
              x1, y2-radius,
              x1, y2-radius,
              x1, y1+radius,
              x1, y1+radius,
              x1, y1]
    return canvas.create_polygon(points, **kwargs, smooth=True)

# 폰트 크기 계산 함수
def get_scaled_font_size(base_size):
    scale = min(root.winfo_width() / 700, root.winfo_height() / 600)
    return max(8, int(base_size * scale))

# 명령어입력창
entry_canvas = tk.Canvas(root, bg="#ffc0cb", highlightthickness=0)
entry_canvas.place(relx=0.5, rely=0.08, anchor="center", relwidth=0.7, relheight=0.06)

def redraw_entry_bg(event=None):
    entry_canvas.delete("all")
    width = entry_canvas.winfo_width()
    height = entry_canvas.winfo_height()
    if width > 1 and height > 1:
        radius = min(20, height // 2)
        create_rounded_rect(entry_canvas, 4, 4, width, height, radius=radius, fill="#ffa0ab", outline="")
        create_rounded_rect(entry_canvas, 2, 2, width-2, height-2, radius=radius, fill="white", outline="#ffb0bb", width=2)

entry_canvas.bind("<Configure>", redraw_entry_bg)

entry = tk.Entry(root, bg="white", bd=0, relief="flat", highlightthickness=0, fg="#333333", insertbackground="#ff69b4")
entry.place(relx=0.5, rely=0.08, anchor="center", relwidth=0.66, relheight=0.045)

# 추천명령어박스
recommend_canvas = tk.Canvas(root, bg="#ffc0cb", highlightthickness=0)
recommend_canvas.place(relx=0.5, rely=0.23, anchor="center", relwidth=0.7, relheight=0.13)

def redraw_recommend_bg(event=None):
    recommend_canvas.delete("all")
    width = recommend_canvas.winfo_width()
    height = recommend_canvas.winfo_height()
    if width > 1 and height > 1:
        radius = min(40, height // 2)
        create_rounded_rect(recommend_canvas, 4, 4, width, height, radius=radius, fill="#a0d5f0", outline="")
        create_rounded_rect(recommend_canvas, 2, 2, width-2, height-2, radius=radius, fill="lightblue", outline="#80c0e0", width=3)

recommend_canvas.bind("<Configure>", redraw_recommend_bg)

recommend_text = tk.Text(root, bg="lightblue", bd=0, relief="flat", highlightthickness=0, wrap="word", fg="#2c5f7f", insertbackground="#5090b0")
recommend_text.place(relx=0.5, rely=0.23, anchor="center", relwidth=0.64, relheight=0.09)

# 설명/출력창
text_canvas = tk.Canvas(root, bg="#ffc0cb", highlightthickness=0)
text_canvas.place(relx=0.5, rely=0.52, anchor="center", relwidth=0.82, relheight=0.35)

def redraw_text_bg(event=None):
    text_canvas.delete("all")
    width = text_canvas.winfo_width()
    height = text_canvas.winfo_height()
    if width > 1 and height > 1:
        create_rounded_rect(text_canvas, 4, 4, width, height, radius=20, fill="#f0f0f0", outline="")
        create_rounded_rect(text_canvas, 2, 2, width-2, height-2, radius=20, fill="white", outline="#ffb0bb", width=2)

text_canvas.bind("<Configure>", redraw_text_bg)

text = tk.Text(root, bg="white", bd=0, relief="flat", highlightthickness=0, wrap="word", fg="#333333", insertbackground="#ff69b4")
text.place(relx=0.5, rely=0.52, anchor="center", relwidth=0.78, relheight=0.32)

# 키티 이미지
try:
    img_top = Image.open("hello_kitty_top.png").resize((50, 50))
    img_top_tk = ImageTk.PhotoImage(img_top)
    img_bottom = Image.open("hello_kitty_bottom.png").resize((50, 50))
    img_bottom_tk = ImageTk.PhotoImage(img_bottom)
    
    top_label = tk.Label(root, image=img_top_tk, bg="#ffc0cb")
    top_label.image = img_top_tk
    top_label.place(relx=0.02, rely=0.02)
    
    bottom_label = tk.Label(root, image=img_bottom_tk, bg="#ffc0cb")
    bottom_label.image = img_bottom_tk
    bottom_label.place(relx=0.98, rely=0.98, anchor="se")
except:
    print("이미지 파일을 찾을 수 없습니다.")

# 버튼 클릭 함수
def show_text():
    user_input = entry.get()
    if not user_input.strip():
        return
    
    text.insert(tk.END, f"{user_input} #설명 : 여기에 명령어 설명 표시\n")
    recent_inputs.append(user_input)
    
    recommend_text.delete(1.0, tk.END)
    recommend_text.insert(tk.END, f"{user_input}_추천1\n{user_input}_추천2\n")
    
    entry.delete(0, tk.END)

# Canvas 기반 버튼 생성
button_canvas = tk.Canvas(root, bg="#ffc0cb", highlightthickness=0)
button_canvas.place(relx=0.5, rely=0.78, anchor="center", width=150, height=50)

def draw_button(canvas, hover=False):
    canvas.delete("all")
    color = "#ff69b4" if hover else "#ff85a1"
    create_rounded_rect(canvas, 2, 2, 148, 48, radius=15, fill=color, outline="")
    canvas.create_text(75, 25, text="✨ 실행 ✨", font=("Arial", 12, "bold"), fill="white")

draw_button(button_canvas)

def on_enter(e):
    draw_button(button_canvas, hover=True)

def on_leave(e):
    draw_button(button_canvas, hover=False)

def on_click(event):
    show_text()

button_canvas.bind("<Enter>", on_enter)
button_canvas.bind("<Leave>", on_leave)
button_canvas.bind("<Button-1>", on_click)

# 폰트 크기 업데이트
def update_fonts(event=None):
    entry_font_size = get_scaled_font_size(11)
    recommend_font_size = get_scaled_font_size(10)
    text_font_size = get_scaled_font_size(10)
    button_font_size = get_scaled_font_size(12)
    
    entry.config(font=("Arial", entry_font_size))
    recommend_text.config(font=("Arial", recommend_font_size))
    text.config(font=("Arial", text_font_size))
    # Canvas 버튼은 텍스트 그리기 때문에 따로 font update 필요 없음

root.bind("<Configure>", update_fonts)
update_fonts()

root.mainloop()
