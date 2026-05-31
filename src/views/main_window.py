"""
主窗口组件
BatchPrint Pro 的主界面
"""
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QComboBox, QCheckBox, QPushButton,
    QProgressBar, QMessageBox, QDialog
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from .drop_zone import DropZoneWidget
from .task_list_widget import TaskListWidget
from .print_settings_dialog import PrintSettingsDialog


class MainWindow(QMainWindow):
    """主窗口"""

    def __init__(self, viewmodel, printer_list=None, default_printer="", parent=None):
        """初始化主窗口

        Args:
            viewmodel: 打印视图模型
            printer_list: 打印机列表（由 main.py 传入）
            default_printer: 默认打印机名称
            parent: 父窗口
        """
        super().__init__(parent)
        self.viewmodel = viewmodel
        self.printer_list = printer_list or []
        self.default_printer = default_printer
        self.printer_combo = None

        self.setWindowTitle("BatchPrint Pro - 正在加载...")
        self.setMinimumSize(900, 700)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        main_layout.addWidget(self._create_control_panel())
        main_layout.addWidget(self._create_interaction_panel(), 1)
        main_layout.addWidget(self._create_execution_panel())

        self._populate_printers()
        self._apply_styles()
        self._connect_signals()

    # ── UI 构建 ──────────────────────────────────────

    def _create_control_panel(self):
        panel = QWidget()
        layout = QHBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(QLabel("打印机:"))

        self.printer_combo = QComboBox()
        self.printer_combo.setMinimumWidth(300)
        layout.addWidget(self.printer_combo)

        layout.addStretch()

        self.duplex_checkbox = QCheckBox("双面打印")
        self.duplex_checkbox.setChecked(False)
        layout.addWidget(self.duplex_checkbox)

        self.monochrome_checkbox = QCheckBox("统一黑白")
        self.monochrome_checkbox.setChecked(False)
        layout.addWidget(self.monochrome_checkbox)

        return panel

    def _create_interaction_panel(self):
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        self.drop_zone = DropZoneWidget()
        layout.addWidget(self.drop_zone, 1)

        self.task_list_widget = TaskListWidget()
        layout.addWidget(self.task_list_widget, 2)

        return panel

    def _create_execution_panel(self):
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFormat("就绪")
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 0, 0, 0)

        self.start_button = QPushButton("开始批量打印")
        self.start_button.setMinimumHeight(50)
        self.start_button.setFont(QFont("Microsoft YaHei", 12, QFont.Bold))
        self.start_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 16px;
                font-weight: bold;
                border-radius: 8px;
            }
            QPushButton:hover { background-color: #45a049; }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """)
        button_layout.addWidget(self.start_button)

        self.cancel_button = QPushButton("取消打印")
        self.cancel_button.setMinimumHeight(50)
        self.cancel_button.setFont(QFont("Microsoft YaHei", 12, QFont.Bold))
        self.cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #FF9800;
                color: white;
                font-size: 16px;
                font-weight: bold;
                border-radius: 8px;
            }
            QPushButton:hover { background-color: #F57C00; }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """)
        self.cancel_button.setEnabled(False)
        button_layout.addWidget(self.cancel_button)

        self.clear_button = QPushButton("清空列表")
        self.clear_button.setMinimumHeight(50)
        self.clear_button.setFont(QFont("Microsoft YaHei", 10))
        self.clear_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                font-size: 14px;
                font-weight: bold;
                border-radius: 8px;
            }
            QPushButton:hover { background-color: #da190b; }
        """)
        button_layout.addWidget(self.clear_button)

        layout.addLayout(button_layout)
        return panel

    # ── 打印机下拉框填充 ──────────────────────────────────────

    def _populate_printers(self):
        """用传入的打印机列表填充下拉框"""
        self.printer_combo.clear()

        if not self.printer_list:
            self.printer_combo.addItem("⚠ 未检测到打印机")
            self.setWindowTitle("BatchPrint Pro - 未检测到打印机")
            QMessageBox.warning(
                self, "打印机",
                "未检测到任何打印机！\n\n"
                "请确认：\n"
                "  1. 系统已安装打印机\n"
                "  2. 打印机已开机并处于就绪状态\n\n"
                "程序将继续运行，但无法执行打印。"
            )
            return

        for item in self.printer_list:
            name = item.get("name", "未知打印机")
            self.printer_combo.addItem(name)

        # 选中默认打印机
        if self.default_printer:
            idx = self.printer_combo.findText(self.default_printer)
            if idx >= 0:
                self.printer_combo.setCurrentIndex(idx)

        count = self.printer_combo.count()
        self.setWindowTitle(f"BatchPrint Pro - {count} 台打印机已加载")

    # ── 信号连接 ──────────────────────────────────────

    def _connect_signals(self):
        """连接信号"""
        # ViewModel 信号
        self.viewmodel.task_added.connect(self._on_task_added)
        self.viewmodel.task_removed.connect(self._on_task_removed)
        self.viewmodel.progress_updated.connect(self._on_progress_updated)
        self.viewmodel.print_started.connect(self._on_print_started)
        self.viewmodel.print_finished.connect(self._on_print_finished)
        self.viewmodel.print_error.connect(self._on_print_error)

        # UI 控件信号
        self.start_button.clicked.connect(self._on_start_clicked)
        self.cancel_button.clicked.connect(self._on_cancel_clicked)
        self.clear_button.clicked.connect(self._on_clear_clicked)
        self.duplex_checkbox.toggled.connect(self._on_duplex_toggled)
        self.monochrome_checkbox.toggled.connect(self._on_monochrome_toggled)

        # DropZone 信号
        self.drop_zone.files_dropped.connect(self.viewmodel.add_files)

        # TaskListWidget 信号
        self.task_list_widget.settings_requested.connect(self._on_settings_requested)
        self.task_list_widget.tasks_remove_requested.connect(self._on_tasks_remove_requested)

    # ── 样式 ──────────────────────────────────────

    def _apply_styles(self):
        self.setStyleSheet("""
            QMainWindow { background-color: #f5f5f5; }
            QComboBox {
                padding: 8px 12px;
                border: 1px solid #ccc;
                border-radius: 6px;
                min-height: 32px;
                font-size: 14px;
            }
            QComboBox:hover { border-color: #4CAF50; }
            QCheckBox {
                spacing: 8px;
                font-size: 14px;
                padding: 5px;
            }
            QCheckBox::indicator { width: 18px; height: 18px; }
            QProgressBar {
                border: 1px solid #ccc;
                border-radius: 6px;
                text-align: center;
                height: 28px;
                font-size: 13px;
                font-weight: bold;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
                border-radius: 5px;
            }
        """)

    # ── 槽函数 ──────────────────────────────────────

    def _on_task_added(self, task):
        self.task_list_widget.add_task(task)
        total = self.viewmodel.get_task_count()
        self.progress_bar.setMaximum(total if total > 0 else 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setFormat(f"就绪 ({total} 个任务)")

    def _on_task_removed(self, index, file_path):
        self.task_list_widget.remove_task(index)
        total = self.viewmodel.get_task_count()
        self.progress_bar.setMaximum(total if total > 0 else 100)
        self.progress_bar.setValue(0)
        if total > 0:
            self.progress_bar.setFormat(f"就绪 ({total} 个任务)")
        else:
            self.progress_bar.setFormat("就绪")

    def _on_progress_updated(self, current, total):
        self.progress_bar.setMaximum(total)
        self.progress_bar.setValue(current)
        self.progress_bar.setFormat(f"处理中 {current}/{total}")

    def _on_print_started(self):
        self.start_button.setText("打印中...")
        self.start_button.setEnabled(False)
        self.cancel_button.setEnabled(True)
        self.clear_button.setEnabled(False)
        self.printer_combo.setEnabled(False)
        self.drop_zone.setEnabled(False)

    def _on_print_finished(self):
        self.start_button.setText("开始批量打印")
        self.start_button.setEnabled(True)
        self.cancel_button.setEnabled(False)
        self.clear_button.setEnabled(True)
        self.printer_combo.setEnabled(True)
        self.drop_zone.setEnabled(True)

        completed = self.viewmodel.get_completed_count()
        failed = self.viewmodel.get_failed_count()
        QMessageBox.information(
            self, "打印完成",
            f"打印任务已完成！\n\n成功: {completed}\n失败: {failed}"
        )

    def _on_print_error(self, error_msg):
        QMessageBox.warning(self, "打印错误", error_msg)

    def _on_start_clicked(self):
        printer_name = self.printer_combo.currentText()
        if not printer_name or printer_name.startswith("⚠"):
            QMessageBox.warning(self, "警告", "请先选择一台有效的打印机！")
            return
        if self.viewmodel.get_task_count() == 0:
            QMessageBox.warning(self, "警告", "没有要打印的任务！")
            return
        self.viewmodel.start_printing(printer_name)

    def _on_cancel_clicked(self):
        """取消打印按钮：停止当前打印线程，并移除所有未完成的任务"""
        reply = QMessageBox.question(
            self, "确认取消",
            "确定要取消打印吗？\n已打印完成的任务不会被移除。",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.viewmodel.cancel_printing()
            self.cancel_button.setEnabled(False)

    def _on_tasks_remove_requested(self, rows):
        """从表格和 ViewModel 中批量移除选中的任务（从大到小删，避免索引漂移）

        Args:
            rows: 要移除的行索引列表（已排序）
        """
        if not rows:
            return
        reply = QMessageBox.question(
            self, "确认移除",
            f"确定要移除选中的 {len(rows)} 个任务吗？",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply != QMessageBox.Yes:
            return

        # 从大到小删除，避免索引漂移
        for index in sorted(rows, reverse=True):
            self.viewmodel.remove_task(index)

    def _on_clear_clicked(self):
        reply = QMessageBox.question(
            self, "确认", "确定要清空所有任务吗？",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.viewmodel.clear_all_tasks()
            self.task_list_widget.clear_all()
            self.progress_bar.setMaximum(100)
            self.progress_bar.setValue(0)
            self.progress_bar.setFormat("就绪")

    def _on_duplex_toggled(self, checked):
        self.viewmodel.set_global_duplex(checked)

    def _on_monochrome_toggled(self, checked):
        self.viewmodel.set_global_monochrome(checked)

    def _on_settings_requested(self, index):
        task = self.viewmodel.task_list.get_task(index)
        if not task:
            return
        dialog = PrintSettingsDialog(task, self)
        if dialog.exec() == QDialog.Accepted:
            settings = dialog.get_settings()
            self.viewmodel.update_task_settings(index, **settings)
