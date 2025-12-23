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
        self.title_color = "#ff85a1"
        self.text_color = "#333333"
        
        self.setup_window()
        self.create_widgets()
        
        if self.is_standalone:
            self.root.mainloop()
    
    def setup_window(self):
        """윈도우 기본 설정"""
        self.root.title("📊 Terminal Helper Dashboard")
        self.root.geometry("700x500")
        self.root.configure(bg=self.bg_color)
        self.root.resizable(False, False)
        
        # 화면 중앙에 배치
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (700 // 2)
        y = (self.root.winfo_screenheight() // 2) - (500 // 2)
        self.root.geometry(f"+{x}+{y}")
    
    def create_widgets(self):
        """위젯 생성"""
        # 메인 컨테이너
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        # 헤더
        self.create_header(main_frame)
        
        # 정보 카드 컨테이너
        cards_frame = tk.Frame(main_frame, bg=self.bg_color)
        cards_frame.pack(fill="both", expand=True, pady=20)
        
        # 시스템 정보 수집
        info = self.get_system_info()
        
        # 정보 카드들 생성
        self.create_info_card(cards_frame, "💻 운영체제", info['os'], 0)
        self.create_info_card(cards_frame, "🐍 Python 버전", info['python'], 1)
        self.create_info_card(cards_frame, "📁 현재 디렉토리", info['directory'], 2)
        self.create_info_card(cards_frame, "🕐 시스템 시간", info['time'], 3)
        
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
        card = tk.Frame(
            parent,
            bg=self.card_color,
            relief="flat",
            borderwidth=0
        )
        card.pack(fill="x", pady=8)
        
        # 그림자 효과를 위한 테두리
        card.config(highlightbackground="#ffb6c1", highlightthickness=2)
        
        # 라벨
        label_widget = tk.Label(
            card,
            text=label,
            font=("맑은 고딕", 12, "bold"),
            bg=self.card_color,
            fg=self.title_color,
            anchor="w"
        )
        label_widget.pack(fill="x", padx=20, pady=(15, 5))
        
        # 값
        value_widget = tk.Label(
            card,
            text=value,
            font=("맑은 고딕", 11),
            bg=self.card_color,
            fg=self.text_color,
            anchor="w",
            wraplength=600
        )
        value_widget.pack(fill="x", padx=20, pady=(0, 15))
    
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