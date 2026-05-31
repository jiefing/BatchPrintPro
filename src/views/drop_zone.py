"""
拖拽区域组件
支持文件/文件夹拖拽
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt, Signal, QEvent
from PySide6.QtGui import QDragEnterEvent, QDropEvent


class DropZoneWidget(QWidget):
    """拖拽区域组件"""
    
    # 信号定义
    files_dropped = Signal(list)  # 拖拽文件信号
    
    def __init__(self, parent=None):
        """初始化拖拽区域
        
        Args:
            parent: 父窗口
        """
        super().__init__(parent)
        self.init_ui()
        
    def init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # 设置拖拽区域样式
        self.setStyleSheet("""
            DropZoneWidget {
                border: 3px dashed #aaa;
                border-radius: 15px;
                background-color: #fafafa;
                min-height: 180px;
            }
            DropZoneWidget:hover {
                border-color: #4CAF50;
                background-color: #f0f9f0;
            }
        """)
        
        # 图标和提示文本
        self.icon_label = QLabel("📁")
        self.icon_label.setAlignment(Qt.AlignCenter)
        self.icon_label.setStyleSheet("font-size: 64px; margin-bottom: 10px;")
        layout.addWidget(self.icon_label)
        
        self.hint_label = QLabel("拖拽文件/文件夹至此")
        self.hint_label.setAlignment(Qt.AlignCenter)
        self.hint_label.setStyleSheet("font-size: 18px; color: #666; font-weight: bold;")
        layout.addWidget(self.hint_label)
        
        # 额外提示
        self.hint_label2 = QLabel("支持图片 (.jpg, .png, .bmp) 和文档 (.pdf, .doc, .docx)")
        self.hint_label2.setAlignment(Qt.AlignCenter)
        self.hint_label2.setStyleSheet("font-size: 12px; color: #999; margin-top: 5px;")
        layout.addWidget(self.hint_label2)
        
        # 设置接受拖拽
        self.setAcceptDrops(True)
        
    def dragEnterEvent(self, event: QDragEnterEvent):
        """拖拽进入事件"""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            # 改变样式
            self.setStyleSheet(self.styleSheet().replace("#fafafa", "#e8f5e8"))
            
    def dragLeaveEvent(self, event: QEvent):
        """拖拽离开事件"""
        # 恢复样式
        self.setStyleSheet(self.styleSheet().replace("#e8f5e8", "#fafafa"))
            
    def dropEvent(self, event: QDropEvent):
        """拖拽释放事件"""
        urls = event.mimeData().urls()
        file_paths = [url.toLocalFile() for url in urls]
        
        # 发送信号
        self.files_dropped.emit(file_paths)
        
        # 恢复样式
        self.setStyleSheet(self.styleSheet().replace("#e8f5e8", "#fafafa"))
        
    def show_event(self, event: QEvent):
        """显示事件 - 根据任务列表是否为空切换显示"""
        # 这里可以根据任务列表是否为空来切换显示内容
        pass
