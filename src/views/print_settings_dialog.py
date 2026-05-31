"""
打印设置对话框
为单个打印任务提供设置界面
"""

from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, 
                              QLabel, QSpinBox, QComboBox, 
                              QPushButton, QGroupBox, QCheckBox)
from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtGui import QFont


class PrintSettingsDialog(QDialog):
    """打印设置对话框"""
    
    settings_applied = Signal(dict)  # 设置应用信号
    
    def __init__(self, task, parent=None):
        """初始化打印设置对话框
        
        Args:
            task: 打印任务对象
            parent: 父窗口
        """
        super().__init__(parent)
        self.task = task
        self.init_ui()
        
    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle("打印设置")
        self.setMinimumWidth(450)
        self.setModal(True)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # 标题
        title_label = QLabel(f"打印设置 - {self.task.file_name}")
        title_label.setFont(QFont("Microsoft YaHei", 12, QFont.Bold))
        title_label.setStyleSheet("color: #333; margin-bottom: 10px;")
        title_label.setWordWrap(True)
        layout.addWidget(title_label)
        
        # 1. 打印份数
        copies_group = QGroupBox("打印份数")
        copies_layout = QHBoxLayout(copies_group)
        copies_layout.setContentsMargins(15, 20, 15, 15)
        
        copies_label = QLabel("份数:")
        copies_label.setMinimumWidth(80)
        copies_layout.addWidget(copies_label)
        
        self.copies_spinbox = QSpinBox()
        self.copies_spinbox.setMinimum(1)
        self.copies_spinbox.setMaximum(99)
        self.copies_spinbox.setValue(self.task.copies)
        self.copies_spinbox.setMinimumWidth(100)
        copies_layout.addWidget(self.copies_spinbox)
        
        copies_layout.addStretch()
        layout.addWidget(copies_group)
        
        # 2. 色彩模式
        color_group = QGroupBox("色彩模式")
        color_layout = QHBoxLayout(color_group)
        color_layout.setContentsMargins(15, 20, 15, 15)
        
        color_label = QLabel("模式:")
        color_label.setMinimumWidth(80)
        color_layout.addWidget(color_label)
        
        self.color_combo = QComboBox()
        self.color_combo.addItems(["彩色", "黑白"])
        self.color_combo.setCurrentIndex(0 if self.task.color_mode == "color" else 1)
        self.color_combo.setMinimumWidth(120)
        color_layout.addWidget(self.color_combo)
        
        color_layout.addStretch()
        layout.addWidget(color_group)
        
        # 3. 缩放模式
        scale_group = QGroupBox("缩放模式")
        scale_layout = QHBoxLayout(scale_group)
        scale_layout.setContentsMargins(15, 20, 15, 15)
        
        scale_label = QLabel("模式:")
        scale_label.setMinimumWidth(80)
        scale_layout.addWidget(scale_label)
        
        self.scale_combo = QComboBox()
        self.scale_combo.addItems(["适应纸张", "原始大小"])
        self.scale_combo.setCurrentIndex(0 if self.task.scale_mode == "fit" else 1)
        self.scale_combo.setMinimumWidth(120)
        scale_layout.addWidget(self.scale_combo)
        
        scale_layout.addStretch()
        layout.addWidget(scale_group)
        
        # 4. 朝向
        orientation_group = QGroupBox("朝向")
        orientation_layout = QHBoxLayout(orientation_group)
        orientation_layout.setContentsMargins(15, 20, 15, 15)
        
        orientation_label = QLabel("方向:")
        orientation_label.setMinimumWidth(80)
        orientation_layout.addWidget(orientation_label)
        
        self.orientation_combo = QComboBox()
        self.orientation_combo.addItems(["自动", "纵向", "横向"])
        orientation_index = 0 if self.task.orientation == "auto" else (1 if self.task.orientation == "portrait" else 2)
        self.orientation_combo.setCurrentIndex(orientation_index)
        self.orientation_combo.setMinimumWidth(120)
        orientation_layout.addWidget(self.orientation_combo)
        
        orientation_layout.addStretch()
        layout.addWidget(orientation_group)
        
        # 5. 双面打印（全局设置）
        self.duplex_checkbox = QCheckBox("双面打印（全局设置）")
        self.duplex_checkbox.setChecked(self.parent().viewmodel.global_duplex if self.parent() else False)
        layout.addWidget(self.duplex_checkbox)
        
        layout.addStretch()
        
        # 6. 按钮区
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.addStretch()
        
        ok_button = QPushButton("确定")
        ok_button.setMinimumHeight(40)
        ok_button.setMinimumWidth(100)
        ok_button.setFont(QFont("Microsoft YaHei", 10, QFont.Bold))
        ok_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 6px;
                padding: 8px 20px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        ok_button.clicked.connect(self.accept)
        button_layout.addWidget(ok_button)
        
        cancel_button = QPushButton("取消")
        cancel_button.setMinimumHeight(40)
        cancel_button.setMinimumWidth(100)
        cancel_button.setFont(QFont("Microsoft YaHei", 10))
        cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border-radius: 6px;
                padding: 8px 20px;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
        """)
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)
        
        layout.addLayout(button_layout)
        
    def get_settings(self) -> dict:
        """获取设置
        
        Returns:
            dict: 设置字典
        """
        return {
            'copies': self.copies_spinbox.value(),
            'color_mode': 'color' if self.color_combo.currentIndex() == 0 else 'monochrome',
            'scale_mode': 'fit' if self.scale_combo.currentIndex() == 0 else 'original',
            'orientation': ['auto', 'portrait', 'landscape'][self.orientation_combo.currentIndex()],
            'duplex': self.duplex_checkbox.isChecked()
        }
        
    def accept(self):
        """确定按钮回调"""
        # 发送设置应用信号
        settings = self.get_settings()
        self.settings_applied.emit(settings)
        
        # 应用设置到任务
        self.task.copies = settings['copies']
        self.task.color_mode = settings['color_mode']
        self.task.scale_mode = settings['scale_mode']
        self.task.orientation = settings['orientation']
        
        # 应用全局双面打印设置
        if self.parent() and hasattr(self.parent(), 'viewmodel'):
            self.parent().viewmodel.set_global_duplex(settings['duplex'])
        
        super().accept()
