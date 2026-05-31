"""
PrintTask 数据模型
定义打印任务的属性和行为
"""

import os
from PySide6.QtCore import QObject, Signal, Slot


class PrintTask(QObject):
    """打印任务数据模型"""
    
    # 信号定义
    status_changed = Signal(str)  # 状态改变信号
    settings_changed = Signal()     # 设置改变信号
    
    def __init__(self, file_path: str, parent=None):
        """初始化打印任务
        
        Args:
            file_path: 文件路径
            parent: 父对象
        """
        super().__init__(parent)
        self.file_path = file_path
        self.file_name = os.path.basename(file_path)
        self.file_type = self._detect_file_type(file_path)
        self.page_count = 0
        self.orientation = "auto"  # auto, portrait, landscape
        self.copies = 1
        self.color_mode = "color"  # color, monochrome
        self.scale_mode = "fit"     # fit, original
        self.status = "pending"      # pending, processing, completed, failed
        self.error_message = ""
        
    def _detect_file_type(self, file_path: str) -> str:
        """检测文件类型
        
        Args:
            file_path: 文件路径
            
        Returns:
            str: 文件类型 (image, pdf, word, unknown)
        """
        ext = os.path.splitext(file_path)[1].lower()
        if ext in ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif']:
            return "image"
        elif ext == '.pdf':
            return "pdf"
        elif ext in ['.doc', '.docx']:
            return "word"
        else:
            return "unknown"
            
    def update_status(self, status: str, error_msg: str = ""):
        """更新任务状态
        
        Args:
            status: 新状态
            error_msg: 错误信息
        """
        self.status = status
        self.error_message = error_msg
        self.status_changed.emit(status)
        
    def update_settings(self, **kwargs):
        """更新任务设置
        
        Args:
            **kwargs: 设置参数
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.settings_changed.emit()
        
    def __str__(self) -> str:
        """字符串表示"""
        return f"PrintTask(file={self.file_name}, type={self.file_type}, status={self.status})"
        
    def __repr__(self) -> str:
        """详细信息"""
        return self.__str__()
