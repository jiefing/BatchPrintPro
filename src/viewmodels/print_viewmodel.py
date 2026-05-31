"""
打印视图模型
连接 View 和 Model，处理业务逻辑
"""

import os
from typing import List, Dict, Optional
from PySide6.QtCore import QObject, Signal, Slot, QThread, QMutex, QMutexLocker

from models.print_task import PrintTask
from models.task_list import PrintTaskList
from services.file_scanner import FileScannerService
from services.layout_analyzer import LayoutAnalysisEngine
from services.image_adapter import ImagePrintAdapter
from services.pdf_adapter import PdfPrintAdapter
from services.word_adapter import WordPrintAdapter


class PrintViewModel(QObject):
    """打印视图模型 - 连接View和Model"""

    # 信号定义
    task_added = Signal(PrintTask)
    task_removed = Signal(int, str)
    task_updated = Signal(PrintTask)
    progress_updated = Signal(int, int)
    print_started = Signal()
    print_finished = Signal()
    print_error = Signal(str)

    def __init__(self, parent=None):
        """初始化视图模型

        Args:
            parent: 父对象
        """
        super().__init__(parent)
        self.task_list = PrintTaskList()
        self.file_scanner = FileScannerService()
        self.layout_analyzer = LayoutAnalysisEngine()

        # 创建打印适配器字典
        self.print_adapters = {
            'image': ImagePrintAdapter(),
            'pdf': PdfPrintAdapter(),
            'word': WordPrintAdapter()
        }

        # 全局打印设置
        self.global_duplex = False
        self.global_monochrome = False
        # 打印线程
        self.print_thread = None

        # 连接信号
        self._connect_signals()

    # ── 信号连接 ─────────────────────────────────────────────
    def _connect_signals(self):
        """连接信号"""
        self.task_list.task_added.connect(self.task_added)
        self.task_list.task_removed.connect(self.task_removed)
        self.task_list.task_updated.connect(self.task_updated)
        self.task_list.progress_updated.connect(self.progress_updated)

    # ── 文件管理 ─────────────────────────────────────────────
    def add_files(self, file_paths: List[str]):
        """添加文件到打印队列

        Args:
            file_paths: 文件路径列表
        """
        for file_path in file_paths:
            if os.path.isdir(file_path):
                scanned_files = self.file_scanner.scan_files(file_path)
                for scanned_file in scanned_files:
                    self._add_single_file(scanned_file)
            else:
                self._add_single_file(file_path)

    def _add_single_file(self, file_path: str):
        """添加单个文件（带文件有效性检查）

        Args:
            file_path: 文件路径
        """
        if not self.file_scanner.is_supported_file(file_path):
            print(f"[ViewModel] 不支持的文件格式: {file_path}")
            return

        # 检查文件是否有效（非占位、可读）
        if hasattr(self.file_scanner, '_is_valid_file'):
            if not self.file_scanner._is_valid_file(file_path):
                print(f"[ViewModel] 跳过无效文件: {os.path.basename(file_path)}")
                return

        try:
            task = PrintTask(file_path)
        except Exception as e:
            print(f"[ViewModel] 创建打印任务失败: {file_path} - {e}")
            return

        # 检测朝向（带超时，不会卡死）
        try:
            task.orientation = self.layout_analyzer.detect_orientation(file_path)
        except Exception as e:
            print(f"[ViewModel] 检测朝向失败，使用默认纵向: {e}")
            task.orientation = "portrait"

        if self.global_monochrome:
            task.color_mode = "monochrome"

        self.task_list.add_task(task)

    def remove_task(self, index: int):
        """移除任务

        Args:
            index: 任务索引
        """
        self.task_list.remove_task(index)

    def remove_tasks(self, indices: list):
        """批量移除任务（从大到小删，避免索引漂移）

        Args:
            indices: 要移除的索引列表
        """
        for index in sorted(indices, reverse=True):
            self.task_list.remove_task(index)

    def clear_all_tasks(self):
        """清空所有任务"""
        self.task_list.clear_all()

    def update_task_settings(self, index: int, **kwargs):
        """更新任务设置

        Args:
            index: 任务索引
            **kwargs: 设置参数
        """
        task = self.task_list.get_task(index)
        if task:
            for key, value in kwargs.items():
                if hasattr(task, key):
                    setattr(task, key, value)
            self.task_list.update_task_settings(index, **kwargs)

    # ── 打印控制 ─────────────────────────────────────────────
    def start_printing(self, printer_name: str):
        """开始打印

        Args:
            printer_name: 打印机名称
        """
        if len(self.task_list) == 0:
            self.print_error.emit("没有要打印的任务")
            return

        if not printer_name:
            self.print_error.emit("请选择打印机")
            return

        # 如果旧线程还在跑，先结束
        if self.print_thread and self.print_thread.isRunning():
            print("[ViewModel] 旧打印线程仍在运行，先取消...")
            self.print_thread.cancel()
            self.print_thread.wait(3000)  # 等3秒

        self.print_thread = PrintThread(
            self.task_list, printer_name, self.print_adapters
        )
        self.print_thread.progress_updated.connect(self.progress_updated)
        self.print_thread.task_completed.connect(self._on_task_completed)
        self.print_thread.all_completed.connect(self._on_all_completed)
        self.print_thread.error_occurred.connect(self.print_error)
        self.print_thread.start()

        self.print_started.emit()

    def cancel_printing(self):
        """取消打印"""
        if self.print_thread and self.print_thread.isRunning():
            self.print_thread.cancel()

    # ── 回调 ───────────────────────────────────────────────
    def _on_task_completed(self, index: int, success: bool):
        """任务完成回调"""
        pass

    def _on_all_completed(self):
        """所有任务完成回调"""
        self.print_finished.emit()

    # ── 全局设置 ───────────────────────────────────────────
    def set_global_duplex(self, enabled: bool):
        """设置全局双面打印"""
        self.global_duplex = enabled

    def set_global_monochrome(self, enabled: bool):
        """设置全局黑白打印"""
        self.global_monochrome = enabled

        for i in range(len(self.task_list)):
            task = self.task_list.get_task(i)
            if task:
                task.color_mode = "monochrome" if enabled else "color"
                self.task_list.update_task_settings(i, color_mode=task.color_mode)

    # ── 状态查询 ───────────────────────────────────────────
    def get_task_count(self) -> int:
        """获取任务数量"""
        return len(self.task_list)

    def get_completed_count(self) -> int:
        """获取已完成任务数量"""
        return self.task_list.get_completed_count()

    def get_failed_count(self) -> int:
        """获取失败任务数量"""
        return self.task_list.get_failed_count()


class PrintThread(QThread):
    """打印线程 - 后台执行打印任务

    信号必须在类体中直接定义（PySide6 要求）
    """
    progress_updated = Signal(int, int)   # current, total
    task_completed = Signal(int, bool)     # index, success
    all_completed = Signal()
    error_occurred = Signal(str)

    def __init__(self, task_list, printer_name: str,
                 adapters: Dict[str, object], parent=None):
        """初始化打印线程

        Args:
            task_list: 打印任务列表
            printer_name: 打印机名称
            adapters: 打印适配器字典
            parent: 父对象
        """
        super().__init__(parent)
        self.task_list = task_list
        self.printer_name = printer_name
        self.adapters = adapters
        self._is_cancelled = False
        self._mutex = QMutex()

    def run(self):
        """执行打印"""
        total_tasks = len(self.task_list.tasks)

        for i, task in enumerate(self.task_list.tasks):
            # 检查取消
            with QMutexLocker(self._mutex):
                if self._is_cancelled:
                    break

            self.progress_updated.emit(i + 1, total_tasks)
            self.task_list.update_task_status(i, "processing")

            try:
                adapter = self.adapters.get(task.file_type)
                if adapter and adapter.is_available():
                    print(f"[PrintThread] 正在打印任务 {i+1}/{total_tasks}: {task.file_name}")
                    success = adapter.print_file(
                        task.file_path,
                        self.printer_name,
                        task.copies,
                        task.color_mode,
                        task.orientation,
                        task.scale_mode
                    )
                    if success:
                        self.task_list.update_task_status(i, "completed")
                        print(f"[PrintThread] ✓ 任务 {i+1} 打印成功")
                    else:
                        self.task_list.update_task_status(i, "failed", "打印返回失败")
                        print(f"[PrintThread] ✗ 任务 {i+1} 打印返回失败")
                else:
                    name = task.file_type
                    print(f"[PrintThread] ✗ 无可用适配器: {name}")
                    self.task_list.update_task_status(i, "failed", f"缺少适配器: {name}")

            except Exception as e:
                import traceback
                tb = traceback.format_exc()
                print(f"[PrintThread] ✗ 任务 {i+1} 异常: {e}")
                print(tb)
                self.task_list.update_task_status(i, "failed", str(e))
                self.error_occurred.emit(f"打印 {task.file_name} 失败: {str(e)}")

        print("[PrintThread] 所有任务处理完毕")
        self.all_completed.emit()

    def cancel(self):
        """取消打印"""
        with QMutexLocker(self._mutex):
            self._is_cancelled = True
