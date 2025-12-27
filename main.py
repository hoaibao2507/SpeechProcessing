import sys
import os

# Thêm thư mục hiện tại vào đường dẫn tìm kiếm module để tránh lỗi ModuleNotFound
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.ui.main_window import MainWindow

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()