"""
kyeong/dashboard.py - GUI 시각화 버전
시스템 정보를 보기 좋은 GUI로 표시합니다.
"""

import tkinter as tk
from tkinter import ttk
import platform
import sys
import os
from datetime import datetime


class DashboardGUI:
    """대시보드 GUI 클래스"""
    
    def __init__(self, root=None):
        if root is None:
            self.root = tk.Tk()
            self.is_standalone = True
        else:
            self.root = tk.Toplevel(root)
            self.is_standalone = False
            
        self.bg_color = "#ffc0cb"
        self.card_color = "#fff0f5"
        self.title_color = "#ff69b4"
        self.text_color = "#333333"
        
        self.setup_window()
        self.create_widgets()
        
        if self.is_standalone:
            self.root.mainloop()
    
    def setup_window(self):
        """윈도우 기본 설정"""
        self.root.title("📊 Terminal Helper Dashboard")
        self.root.geometry("700x600")
        self.root.configure(bg=self.bg_color)
        self.root.resizable(True, True)
        
        # 화면 중앙에 배치
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (700 // 2)
        y = (self.root.winfo_screenheight() // 2) - (600 // 2)
        self.root.geometry(f"+{x}+{y}")
    
    def create_widgets(self):
        """위젯 생성"""
        # 메인 컨테이너
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        # 헤더
        self.create_header(main_frame)
        
        # 스크롤 가능한 프레임 생성
        canvas_container = tk.Frame(main_frame, bg=self.bg_color)
        canvas_container.pack(fill="both", expand=True, pady=(20, 0))
        
        # Canvas 생성
        canvas = tk.Canvas(canvas_container, bg=self.bg_color, highlightthickness=0)
        scrollbar = tk.Scrollbar(canvas_container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.bg_color)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # 마우스 휠 스크롤 지원
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # 시스템 정보 수집
        info = self.get_system_info()
        
        # 정보 카드들 생성 (스크롤 가능한 프레임에)
        self.create_info_card(scrollable_frame, "💻 운영체제", info['os'], 0)
        self.create_info_card(scrollable_frame, "🐍 Python 버전", info['python'], 1)
        self.create_info_card(scrollable_frame, "📁 현재 디렉토리", info['directory'], 2)
        self.create_info_card(scrollable_frame, "🕐 시스템 시간", info['time'], 3)
        
        # 하단 버전 정보
        self.create_footer(main_frame)
    
    def create_header(self, parent):
        """헤더 생성"""
        header_frame = tk.Frame(parent, bg=self.bg_color)
        header_frame.pack(fill="x", pady=(0, 10))
        
        title = tk.Label(
            header_frame,
            text="Terminal Helper Dashboard",
            font=("맑은 고딕", 24, "bold"),
            bg=self.bg_color,
            fg=self.title_color
        )
        title.pack()
        
        subtitle = tk.Label(
            header_frame,
            text="시스템 정보 대시보드",
            font=("맑은 고딕", 11),
            bg=self.bg_color,
            fg=self.text_color
        )
        subtitle.pack()
    
    def create_info_card(self, parent, label, value, row):
        """정보 카드 생성"""
        # 카드 프레임
        card_frame = tk.Frame(parent, bg=self.bg_color)
        card_frame.pack(fill="x", pady=8, padx=10)
        
        # Canvas로 둥근 모서리 구현
        canvas = tk.Canvas(
            card_frame,
            bg=self.bg_color,
            highlightthickness=0,
            height=110
        )
        canvas.pack(fill="x")
        
        # 둥근 모서리 사각형 그리기
        def draw_rounded_rect(event=None):
            canvas.delete("all")
            w = canvas.winfo_width()
            h = 110
            r = 20  # 모서리 반경
            
            if w < 10:
                return
            
            # 외부 테두리 (그림자 효과)
            canvas.create_arc(2, 2, 2+r*2, 2+r*2, start=90, extent=90, fill="#ffb6c1", outline="")
            canvas.create_arc(w-2-r*2, 2, w-2, 2+r*2, start=0, extent=90, fill="#ffb6c1", outline="")
            canvas.create_arc(2, h-2-r*2, 2+r*2, h-2, start=180, extent=90, fill="#ffb6c1", outline="")
            canvas.create_arc(w-2-r*2, h-2-r*2, w-2, h-2, start=270, extent=90, fill="#ffb6c1", outline="")
            canvas.create_rectangle(2+r, 2, w-2-r, h-2, fill="#ffb6c1", outline="")
            canvas.create_rectangle(2, 2+r, 2+r, h-2-r, fill="#ffb6c1", outline="")
            canvas.create_rectangle(w-2-r, 2+r, w-2, h-2-r, fill="#ffb6c1", outline="")
            
            # 내부 카드
            canvas.create_arc(4, 4, 4+r*2, 4+r*2, start=90, extent=90, fill=self.card_color, outline="")
            canvas.create_arc(w-4-r*2, 4, w-4, 4+r*2, start=0, extent=90, fill=self.card_color, outline="")
            canvas.create_arc(4, h-4-r*2, 4+r*2, h-4, start=180, extent=90, fill=self.card_color, outline="")
            canvas.create_arc(w-4-r*2, h-4-r*2, w-4, h-4, start=270, extent=90, fill=self.card_color, outline="")
            canvas.create_rectangle(4+r, 4, w-4-r, h-4, fill=self.card_color, outline="")
            canvas.create_rectangle(4, 4+r, 4+r, h-4-r, fill=self.card_color, outline="")
            canvas.create_rectangle(w-4-r, 4+r, w-4, h-4-r, fill=self.card_color, outline="")
        
        canvas.bind("<Configure>", draw_rounded_rect)
        canvas.update()
        draw_rounded_rect()
        
        # 내용 프레임 (Canvas 위에)
        content_frame = tk.Frame(card_frame, bg=self.card_color)
        content_frame.place(x=24, y=18, relwidth=0.9, height=74)
        
        # 라벨
        label_widget = tk.Label(
            content_frame,
            text=label,
            font=("맑은 고딕", 12, "bold"),
            bg=self.card_color,
            fg=self.title_color,
            anchor="w"
        )
        label_widget.pack(fill="x", pady=(5, 2))
        
        # 값
        value_widget = tk.Label(
            content_frame,
            text=value,
            font=("맑은 고딕", 11),
            bg=self.card_color,
            fg=self.text_color,
            anchor="w",
            wraplength=600,
            justify="left"
        )
        value_widget.pack(fill="x", pady=(2, 5))
    
    def create_footer(self, parent):
        """푸터 생성"""
        footer_frame = tk.Frame(parent, bg=self.bg_color)
        footer_frame.pack(side="bottom", fill="x", pady=(10, 0))
        
        version = tk.Label(
            footer_frame,
            text="Version: v0.1.0",
            font=("맑은 고딕", 9),
            bg=self.bg_color,
            fg="#999999"
        )
        version.pack(side="left")
        
        # 닫기 버튼
        close_btn = tk.Button(
            footer_frame,
            text="닫기",
            command=self.root.destroy,
            bg="#ff69b4",
            fg="white",
            font=("맑은 고딕", 10, "bold"),
            relief="flat",
            padx=20,
            pady=8,
            cursor="hand2",
            borderwidth=0
        )
        close_btn.pack(side="right")
        
        # 호버 효과
        close_btn.bind("<Enter>", lambda e: close_btn.config(bg="#ff85a1"))
        close_btn.bind("<Leave>", lambda e: close_btn.config(bg="#ff69b4"))
    
    def get_system_info(self):
        """시스템 정보 수집"""
        return {
            'os': f"{platform.system()} {platform.release()} ({platform.machine()})",
            'python': sys.version.split()[0],
            'directory': os.getcwd(),
            'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }


# 기존 함수들 (호환성 유지)
def get_dashboard_text():
    lines = []
    lines.append("=" * 40)
    lines.append(" Terminal Helper")
    lines.append(" Version: v0.1.0")
    lines.append("=" * 40)
    lines.append(f"OS: {platform.system()} {platform.release()}")
    lines.append(f"Python: {sys.version.split()[0]}")
    lines.append(f"Current Directory: {os.getcwd()}")
    return "\n".join(lines)


def show_dashboard():
    """텍스트 대시보드 출력 (기존 함수)"""
    print(get_dashboard_text())


def show_dashboard_gui(parent=None):
    """GUI 대시보드 표시 (새 함수)"""
    DashboardGUI(parent)


if __name__ == "__main__":
    # GUI로 실행
    DashboardGUI()