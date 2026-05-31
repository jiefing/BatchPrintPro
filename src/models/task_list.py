"""
PrintTaskList 管理类
管理打印任务列表，提供任务的添加、删除、更新等功能
"""

from PySide6.QtCore import QObject, Signal, Slot
from typing import List, Optional

from .print_task import PrintTask


class PrintTaskList(QObject):
    """打印任务列表管理类"""
    
    # 信号定义
    task_added = Signal(PrintTask)           # 任务添加信号
    task_removed = Signal(int, str)           # 任务移除信号 (index, file_path)
    task_updated = Signal(PrintTask)           # 任务更新信号
    progress_updated = Signal(int, int)       # 进度更新信号 (current, total)
    list_cleared = Signal()                    # 列表清空信号
    
    def __init__(self, parent=None):
        """初始化任务列表
        
        Args:
            parent: 父对象
        """
        super().__init__(parent)
        self.tasks = []  # type: List[PrintTask]
        self.current_index = 0
        
    def add_task(self, task: PrintTask):
        """添加打印任务
        
        Args:
            task: 打印任务对象
        """
        self.tasks.append(task)
        self.task_added.emit(task)
        self._update_progress()
        
    def remove_task(self, index: int) -> bool:
        """移除打印任务
        
        Args:
            index: 任务索引
            
        Returns:
            bool: 是否成功移除
        """
        if 0 <= index < len(self.tasks):
            task = self.tasks.pop(index)
            self.task_removed.emit(index, task.file_path)
            self._update_progress()
            return True
        return False
            
    def clear_all(self):
        """清空所有任务"""
        self.tasks.clear()
        self.current_index = 0
        self.list_cleared.emit()
        self._update_progress()
        
    def get_task(self, index: int) -> Optional[PrintTask]:
        """获取指定索引的任务
        
        Args:
            index: 任务索引
            
        Returns:
            Optional[PrintTask]: 打印任务对象，如果索引无效则返回None
        """
        if 0 <= index < len(self.tasks):
            return self.tasks[index]
        return None
        
    def get_all_tasks(self) -> List[PrintTask]:
        """获取所有任务
        
        Returns:
            List[PrintTask]: 所有打印任务
        """
        return self.tasks.copy()
        
    def get_task_count(self) -> int:
        """获取任务数量
        
        Returns:
            int: 任务数量
        """
        return len(self.tasks)
        
    def get_pending_count(self) -> int:
        """获取待处理任务数量
        
        Returns:
            int: 待处理任务数量
        """
        return sum(1 for task in self.tasks if task.status == "pending")
        
    def get_completed_count(self) -> int:
        """获取已完成任务数量
        
        Returns:
            int: 已完成任务数量
        """
        return sum(1 for task in self.tasks if task.status == "completed")
        
    def get_failed_count(self) -> int:
        """获取失败任务数量
        
        Returns:
            int: 失败任务数量
        """
        return sum(1 for task in self.tasks if task.status == "failed")
        
    def update_task_status(self, index: int, status: str, error_msg: str = ""):
        """更新任务状态
        
        Args:
            index: 任务索引
            status: 新状态
            error_msg: 错误信息
        """
        if 0 <= index < len(self.tasks):
            task = self.tasks[index]
            task.update_status(status, error_msg)
            self.task_updated.emit(task)
            self._update_progress()
            
    def update_task_settings(self, index: int, **kwargs):
        """更新任务设置
        
        Args:
            index: 任务索引
            **kwargs: 设置参数
        """
        if 0 <= index < len(self.tasks):
            task = self.tasks[index]
            task.update_settings(**kwargs)
            self.task_updated.emit(task)
            
    def get_current_task(self) -> Optional[PrintTask]:
        """获取当前任务
        
        Returns:
            Optional[PrintTask]: 当前任务，如果没有则返回None
        """
        if 0 <= self.current_index < len(self.tasks):
            return self.tasks[self.current_index]
        return None
        
    def move_to_next_task(self) -> bool:
        """移动到下一个任务
        
        Returns:
            bool: 是否成功移动
        """
        if self.current_index < len(self.tasks) - 1:
            self.current_index += 1
            return True
        return False
        
    def reset_current_index(self):
        """重置当前索引"""
        self.current_index = 0
        
    def _update_progress(self):
        """更新进度"""
        total = len(self.tasks)
        completed = self.get_completed_count()
        self.progress_updated.emit(completed, total)
        
    def __len__(self) -> int:
        """获取任务数量"""
        return len(self.tasks)
        
    def __getitem__(self, index: int) -> PrintTask:
        """获取指定索引的任务"""
        return self.tasks[index]
        
    def __iter__(self):
        """迭代器"""
        return iter(self.tasks)
        
    def __str__(self) -> str:
        """字符串表示"""
        return f"PrintTaskList(tasks={len(self.tasks)}, completed={self.get_completed_count()})"
        
    def __repr__(self) -> str:
        """详细信息"""
        return self.__str__()
