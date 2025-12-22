import tkinter as tk

# 프로그램의 '메인 창'을 만든다
# 이게 없으면 화면 자체가 안 뜸
root = tk.Tk()

# 창 맨 위에 표시될 제목 설정
root.title("Terminal Helper")

# ===== 명령어 입력창 =====

# 한 줄짜리 입력칸을 만든다 (터미널에 명령어 치는 곳)
# root = 이 입력창이 메인 창 안에 들어간다는 뜻
# width = 글자 기준 너비
entry = tk.Entry(root, width=50)

# 화면에 실제로 배치한다
# padx, pady = 바깥 여백 (안 하면 너무 붙어 보임)
entry.pack(padx=10, pady=10)

# ===== 실행 버튼 =====

# 버튼을 만든다
# text="실행" → 버튼에 적힐 글자
button = tk.Button(root, text="실행")

# 버튼을 화면에 배치
button.pack(pady=5)

# ===== 설명 / 출력 창 =====

# 여러 줄 텍스트를 보여줄 수 있는 박스
# 명령어 설명이나 결과를 여기다 보여줄 예정
text = tk.Text(root, width=60, height=15)

# 화면에 배치
text.pack(padx=10, pady=10)

# ===== 프로그램 계속 실행 =====

# 이 줄이 있어야 창이 바로 안 꺼지고 계속 켜져 있음
# 사용자의 입력(클릭 등)을 계속 기다리는 상태
root.mainloop()

