import tkinter as tk
from PIL import Image, ImageTk

root = tk.Tk()
root.configure(bg="#ffc0cb")
root.title("Terminal Helper")
root.geometry("700x600")

# 명령어입력창
entry = tk.Entry(root, width=50, bg="white")
entry.pack(padx=10, pady=10)

# 추천명령어박스
recommend_canvas = tk.Canvas(root, width=500, height=80, bg="#ffc0cb", highlightthickness=0)
recommend_canvas.pack(padx=10, pady=5)

# 구름 모양 그리기 (여러 원을 겹쳐서)
recommend_canvas.create_oval(50, 30, 150, 70, fill="lightblue", outline="skyblue", width=2)
recommend_canvas.create_oval(120, 20, 220, 70, fill="lightblue", outline="skyblue", width=2)
recommend_canvas.create_oval(200, 25, 300, 70, fill="lightblue", outline="skyblue", width=2)
recommend_canvas.create_oval(280, 30, 380, 70, fill="lightblue", outline="skyblue", width=2)
recommend_canvas.create_oval(350, 35, 450, 70, fill="lightblue", outline="skyblue", width=2)

# 구름 하단부를 부드럽게 연결
recommend_canvas.create_oval(80, 40, 420, 75, fill="lightblue", outline="skyblue", width=2)

# Text 위젯 추가 (이 부분이 빠져있었어요!)
recommend_text = tk.Text(root, width=58, height=3, bg="lightblue", bd=0, 
                         font=("Arial", 10), relief="flat", highlightthickness=0)
recommend_canvas.create_window(250, 45, window=recommend_text)

# 설명/출력창
text = tk.Text(root, width=60, height=10, bg="white")
text.pack(padx=10, pady=10)

# 최근입력기록저장용리스트
recent_inputs = []

# 키티 ㅎㅎ (이미지경로는내가따로설정ㅋㅋ)
try:
    img_top = Image.open("hello_kitty_top.png").resize((50, 50))
    img_top_tk = ImageTk.PhotoImage(img_top)
    img_bottom = Image.open("hello_kitty_bottom.png").resize((50, 50))
    img_bottom_tk = ImageTk.PhotoImage(img_bottom)
    
    top_label = tk.Label(root, image=img_top_tk, bg="#ffc0cb")
    top_label.place(x=10, y=10)  # 좌측 상단
    
    bottom_label = tk.Label(root, image=img_bottom_tk, bg="#ffc0cb")
    bottom_label.place(relx=1.0, rely=1.0, anchor="se")  # 우측 하단
except:
    print("이미지 파일을 찾을 수 없습니다.")

# 버튼클릭함수
def show_text():
    user_input = entry.get()
    if not user_input.strip():
        return
    
    text.insert(tk.END, f"{user_input} #설명 : 여기에 명령어 설명 표시\n")
    recent_inputs.append(user_input)
    
    # 추천명령어표시
    recommend_text.delete(1.0, tk.END)
    recommend_text.insert(tk.END, f"{user_input}_추천1\n{user_input}_추천2\n")
    
    entry.delete(0, tk.END)

# 실행버튼 
button = tk.Button(root, text="실행", command=show_text)
button.pack(pady=5)

root.mainloop()