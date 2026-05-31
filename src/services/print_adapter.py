"""
打印适配器基类
定义统一的打印接口，所有具体适配器都继承此类
"""

from abc import ABC, abstractmethod
from typing import Optional


class PrintAdapter(ABC):
    """打印适配器基类"""
    
    @abstractmethod
    def print_file(self, file_path: str, printer_name: str, 
                  copies: int = 1, color_mode: str = "color",
                  orientation: str = "portrait", scale_mode: str = "fit") -> bool:
        """打印文件
        
        Args:
            file_path: 文件路径
            printer_name: 打印机名称
            copies: 打印份数，默认为1
            color_mode: 色彩模式，"color" 或 "monochrome"
            orientation: 朝向，"portrait" 或 "landscape"
            scale_mode: 缩放模式，"fit" 或 "original"
            
        Returns:
            bool: 是否打印成功
        """
        pass
        
    @abstractmethod
    def is_available(self) -> bool:
        """检查适配器是否可用
        
        Returns:
            bool: 是否可用
        """
        pass
        
    @abstractmethod
    def get_name(self) -> str:
        """获取适配器名称
        
        Returns:
            str: 适配器名称
        """
        pass
        
    def _validate_file_exists(self, file_path: str) -> bool:
        """验证文件是否存在
        
        Args:
            file_path: 文件路径
            
        Returns:
            bool: 文件是否存在
        """
        import os
        return os.path.exists(file_path)
        
    def _build_print_settings(self, copies: int, color_mode: str, 
                            orientation: str, scale_mode: str) -> dict:
        """构建打印设置字典
        
        Args:
            copies: 打印份数
            color_mode: 色彩模式
            orientation: 朝向
            scale_mode: 缩放模式
            
        Returns:
            dict: 打印设置字典
        """
        return {
            'copies': copies,
            'color_mode': color_mode,
            'orientation': orientation,
            'scale_mode': scale_mode
        }
