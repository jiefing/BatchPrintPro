"""
任务列表组件
显示和管理打印任务列表
支持单选/多选，提供取消打印功能
"""
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QTableWidget,
                              QTableWidgetItem, QHeaderView, QPushButton,
                              QMenu, QMessageBox, QLabel)
from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtGui import QColor, QFont


class TaskListWidget(QWidget):
    """任务列表组件"""
    
    # 信号定义
    task_selected = Signal(int)       # 任务选中信号
    settings_requested = Signal(int)  # 设置请求信号
    task_removed = Signal(int)        # 单个任务移除信号（索引）
    tasks_remove_requested = Signal(list)  # 多个任务移除信号（索引列表）
    
    def __init__(self, parent=None):
        """初始化任务列表组件
        
        Args:
            parent: 父窗口
        """
        super().__init__(parent)
        self.init_ui()
        
    def init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # 创建表格部件（支持多选）
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(5)
        self.table_widget.setHorizontalHeaderLabels(["文件名", "类型", "页数", "状态", "操作"])
        
        # 设置为多选模式
        self.table_widget.setSelectionBehavior(QTableWidget.SelectRows)
        self.table_widget.setSelectionMode(QTableWidget.MultiSelection)
        self.table_widget.setAlternatingRowColors(True)
        self.table_widget.setShowGrid(True)
        
        # 设置表格样式
        self.table_widget.setStyleSheet("""
            QTableWidget {
                gridline-color: #ddd;
                font-size: 13px;
            }
            QTableWidget::item:selected {
                background-color: #4CAF50;
                color: white;
            }
            QTableWidget::item:hover {
                background-color: #f0f9f0;
            }
            QHeaderView::section {
                background-color: #f5f5f5;
                padding: 8px;
                font-weight: bold;
                border: 1px solid #ddd;
            }
        """)
        
        # 设置列宽
        header = self.table_widget.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        
        # 连接信号
        self.table_widget.cellDoubleClicked.connect(self._on_cell_double_clicked)
        
        # 右键菜单
        self.table_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table_widget.customContextMenuRequested.connect(self._on_context_menu)
        
        layout.addWidget(self.table_widget)

        # 底部操作提示
        self.hint_label = QLabel("提示：左键选中行，右键可取消打印")
        self.hint_label.setStyleSheet(
            "QLabel { color: #888888; font-size: 12px; padding: 4px 0px 0px 0px; }"
        )
        layout.addWidget(self.hint_label)

    def add_task(self, task):
        """添加任务到列表
        
        Args:
            task: 打印任务对象
        """
        row = self.table_widget.rowCount()
        self.table_widget.insertRow(row)
        
        # 文件名
        name_item = QTableWidgetItem(task.file_name)
        name_item.setFlags(name_item.flags() & ~Qt.ItemIsEditable)  # 不可编辑
        self.table_widget.setItem(row, 0, name_item)
        
        # 类型
        type_item = QTableWidgetItem(task.file_type.upper())
        type_item.setFlags(type_item.flags() & ~Qt.ItemIsEditable)
        type_item.setTextAlignment(Qt.AlignCenter)
        self.table_widget.setItem(row, 1, type_item)
        
        # 页数
        page_item = QTableWidgetItem(str(task.page_count))
        page_item.setFlags(page_item.flags() & ~Qt.ItemIsEditable)
        page_item.setTextAlignment(Qt.AlignCenter)
        self.table_widget.setItem(row, 2, page_item)
        
        # 状态
        status_item = QTableWidgetItem(task.status)
        self._set_status_color(status_item, task.status)
        status_item.setFlags(status_item.flags() & ~Qt.ItemIsEditable)
        status_item.setTextAlignment(Qt.AlignCenter)
        self.table_widget.setItem(row, 3, status_item)
        
        # 操作按钮
        settings_button = QPushButton("⚙️")
        settings_button.setFixedSize(32, 32)
        settings_button.setStyleSheet("""
            QPushButton {
                font-size: 16px;
                border: none;
                background-color: transparent;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
                border-radius: 4px;
            }
        """)
        settings_button.clicked.connect(lambda: self.settings_requested.emit(row))
        self.table_widget.setCellWidget(row, 4, settings_button)
        
    def update_task(self, task, index: int):
        """更新任务
        
        Args:
            task: 打印任务对象
            index: 任务索引
        """
        if 0 <= index < self.table_widget.rowCount():
            # 更新状态
            status_item = QTableWidgetItem(task.status)
            self._set_status_color(status_item, task.status)
            status_item.setFlags(status_item.flags() & ~Qt.ItemIsEditable)
            status_item.setTextAlignment(Qt.AlignCenter)
            self.table_widget.setItem(index, 3, status_item)
            
    def remove_task(self, index: int):
        """移除任务
        
        Args:
            index: 任务索引
        """
        if 0 <= index < self.table_widget.rowCount():
            self.table_widget.removeRow(index)
            
    def clear_all(self):
        """清空所有任务"""
        self.table_widget.setRowCount(0)
        
    def get_task_count(self) -> int:
        """获取任务数量
        
        Returns:
            int: 任务数量
        """
        return self.table_widget.rowCount()
    
    def get_selected_rows(self) -> list:
        """获取选中的行索引列表（从小到大排序）
        
        Returns:
            list: 选中的行索引列表
        """
        selected = set()
        for item in self.table_widget.selectedItems():
            selected.add(item.row())
        return sorted(selected)
        
    def _set_status_color(self, item: QTableWidgetItem, status: str):
        """设置状态颜色
        
        Args:
            item: 表格项
            status: 状态字符串
        """
        if status == "completed":
            item.setForeground(QColor("#4CAF50"))  # 绿色
            item.setFont(QFont("Microsoft YaHei", 10, QFont.Bold))
        elif status == "failed":
            item.setForeground(QColor("#f44336"))  # 红色
            item.setFont(QFont("Microsoft YaHei", 10, QFont.Bold))
        elif status == "processing":
            item.setForeground(QColor("#2196F3"))  # 蓝色
            item.setFont(QFont("Microsoft YaHei", 10, QFont.Bold))
        else:
            item.setForeground(QColor("#000000"))  # 黑色
            
    def _on_cell_double_clicked(self, row: int, column: int):
        """单元格双击事件
        
        Args:
            row: 行索引
            column: 列索引
        """
        # 双击打开文件所在目录
        if column == 0:  # 文件名列
            import os
            import subprocess
            
            # 获取文件路径（需要通过 parent 的 viewmodel 获取）
            main_window = self._find_main_window()
            if main_window and hasattr(main_window, 'viewmodel'):
                tasks = main_window.viewmodel.task_list.tasks
                if 0 <= row < len(tasks):
                    task = tasks[row]
                    file_path = task.file_path
                    
                    # 打开文件所在目录
                    try:
                        subprocess.run(['explorer', '/select,', file_path])
                    except Exception as e:
                        QMessageBox.warning(self, "警告", f"无法打开文件目录: {e}")
    
    def _find_main_window(self):
        """向上查找主窗口"""
        parent = self.parent()
        while parent:
            if hasattr(parent, 'viewmodel'):
                return parent
            parent = parent.parent()
        return None
    
    def _on_context_menu(self, position):
        """右键菜单
        
        Args:
            position: 菜单位置
        """
        selected_rows = self.get_selected_rows()
        if not selected_rows:
            return
        
        menu = QMenu(self)
        
        remove_action = menu.addAction(f"取消打印 ({len(selected_rows)} 项)")
        remove_action.triggered.connect(lambda: self.tasks_remove_requested.emit(selected_rows))
        
        menu.exec_(self.table_widget.mapToGlobal(position))
