"""
文件扫描服务
实现2级目录遍历，过滤支持的文件格式
跳过 OneDrive 云端占位文件，防止卡死
"""

import os
import time
from typing import List, Set


class FileScannerService:
    """文件扫描服务 - 2级目录遍历"""
    
    # 支持的文件扩展名
    SUPPORTED_EXTENSIONS = {
        'image': ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif'],
        'pdf': ['.pdf'],
        'word': ['.doc', '.docx']
    }
    
    # 最小文件大小（字节），小于此大小的文件视为占位文件
    MIN_FILE_SIZE = 1024  # 1KB
    
    def __init__(self, max_depth: int = 2):
        """初始化文件扫描服务
        
        Args:
            max_depth: 最大扫描深度，默认为2
        """
        self.max_depth = max_depth
        
        # 合并所有支持的扩展名
        self._all_extensions = set()  # type: Set[str]
        for extensions in self.SUPPORTED_EXTENSIONS.values():
            self._all_extensions.update(extensions)
        
    def scan_files(self, path: str) -> List[str]:
        """扫描文件，返回支持的文件列表
        
        Args:
            path: 文件路径或目录路径
            
        Returns:
            List[str]: 支持的文件路径列表
        """
        if os.path.isfile(path):
            # 如果是文件，检查是否支持
            return [path] if self._is_supported_file(path) else []
        
        # 如果是目录，执行扫描
        result = []
        self._scan_directory(path, 0, result)
        return result
        
    def _scan_directory(self, dir_path: str, current_depth: int, result: List[str]):
        """递归扫描目录
        
        Args:
            dir_path: 目录路径
            current_depth: 当前扫描深度
            result: 结果列表
        """
        # 检查是否超过最大深度
        if current_depth >= self.max_depth:
            return
            
        try:
            with os.scandir(dir_path) as entries:
                for entry in entries:
                    # 检查是否支持的文件
                    if entry.is_file() and self._is_supported_file(entry.path):
                        # 检查文件是否有效（非占位、可读）
                        if self._is_valid_file(entry.path):
                            result.append(entry.path)
                        # 无效文件已在上一步打印了跳过信息
                    elif entry.is_dir():
                        # 递归扫描子目录
                        self._scan_directory(entry.path, current_depth + 1, result)
        except (PermissionError, OSError) as e:
            # 跳过无权限访问的目录
            print(f"跳过目录 {dir_path}: {e}")
            pass
            
    def _is_supported_file(self, file_path: str) -> bool:
        """检查文件是否支持
        
        Args:
            file_path: 文件路径
            
        Returns:
            bool: 是否支持
        """
        ext = os.path.splitext(file_path)[1].lower()
        return ext in self._all_extensions
    
    def _is_valid_file(self, file_path: str) -> bool:
        """检查文件是否有效（非占位文件、可读）
        
        Args:
            file_path: 文件路径
            
        Returns:
            bool: 文件是否有效
        """
        try:
            # 检查文件大小（跳过 0 字节或太小的占位文件）
            file_size = os.path.getsize(file_path)
            if file_size < self.MIN_FILE_SIZE:
                print(f"跳过占位文件（大小={file_size}字节）: {os.path.basename(file_path)}")
                return False
            
            # 尝试以只读方式打开文件，检查是否被锁定
            with open(file_path, 'rb') as f:
                f.read(1)  # 尝试读取1个字节
            return True
        except (OSError, IOError) as e:
            print(f"跳过无法访问的文件: {os.path.basename(file_path)} - {e}")
            return False
        
    def get_supported_extensions(self) -> Set[str]:
        """获取所有支持的扩展名
        
        Returns:
            Set[str]: 支持的扩展名集合
        """
        return self._all_extensions.copy()
        
    def is_supported_file(self, file_path: str) -> bool:
        """公共方法：检查文件是否支持
        
        Args:
            file_path: 文件路径
            
        Returns:
            bool: 是否支持
        """
        return self._is_supported_file(file_path)
