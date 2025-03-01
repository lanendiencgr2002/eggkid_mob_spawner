import tkinter as tk
from tkinter import ttk
import pyperclip
import pyautogui
import time

class ClipboardFormatter:
    def __init__(self):
        self.last_text = ''
        
        # 创建主窗口
        self.root = tk.Tk()
        self.root.title("剪贴板格式清除工具")
        self.root.geometry("300x100")
        
        # 创建状态标签
        self.status_label = ttk.Label(
            self.root,
            text="等待检测剪贴板...\n复制带格式文本后会自动清除格式",
            anchor="center"
        )
        self.status_label.pack(pady=20)
        
        # 开始检查剪贴板
        self.check_clipboard()
        
    def check_clipboard(self):
        try:
            current_text = pyperclip.paste()
            
            # 检查剪贴板是否有变化
            if current_text != self.last_text and current_text:
                # 保存当前文本用于比较
                self.last_text = current_text
                
                # 清除格式后重新复制到剪贴板
                pyperclip.copy(current_text)
                
                # 更新状态
                self.status_label.config(
                    text=f"已清除格式 - {len(current_text)}字符\n"
                        f"时间: {time.strftime('%H:%M:%S')}"
                )
                
        except Exception as e:
            self.status_label.config(text=f"发生错误: {str(e)}")
            
        # 继续检查剪贴板
        self.root.after(500, self.check_clipboard)
        
    def run(self):
        self.root.mainloop()

if __name__ == '__main__':
    app = ClipboardFormatter()
    app.run()