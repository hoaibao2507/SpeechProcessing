import sys
import os

# Thêm thư mục gốc vào path để import các module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from . import stt_module
from . import denoise_module
from . import animal_module

__all__ = ['stt_module', 'denoise_module', 'animal_module']

