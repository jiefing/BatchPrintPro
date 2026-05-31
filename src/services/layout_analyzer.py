"""
版式分析引擎
自动判断文件朝向（横纵向）

加入超时机制，防止OneDrive云端文件下载时卡死UI线程
"""

import os
import concurrent.futures
from typing import Optional

# 尝试导入图片处理库
try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    
# 尝试导入PDF处理库
try:
    import fitz
    PYMUPDF_AVAILABLE = True
except ImportError:
    PYMUPDF_AVAILABLE = False

# 文件读取超时（秒）
READ_TIMEOUT = 3

def _run_with_timeout(func, *args, timeout=READ_TIMEOUT):
    """带超时的函数执行，防止文件读取卡死"""
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(func, *args)
            return future.result(timeout=timeout)
    except concurrent.futures.TimeoutError:
        print(f"警告: 文件读取超时（{timeout}秒），可能是OneDrive云端文件正在下载")
        return None
    except Exception as e:
        print(f"文件读取失败: {e}")
        return None


class LayoutAnalysisEngine:
    """版式分析引擎 - 自动判断横纵向"""
    
    def __init__(self):
        """初始化版式分析引擎"""
        self.pil_available = PIL_AVAILABLE
        self.pymupdf_available = PYMUPDF_AVAILABLE
        
    def detect_orientation(self, file_path: str) -> str:
        """检测文件朝向
        
        Args:
            file_path: 文件路径
            
        Returns:
            str: 'portrait'（纵向）或 'landscape'（横向）
        """
        file_type = self._detect_file_type(file_path)
        
        if file_type == "image":
            return self._detect_image_orientation(file_path)
        elif file_type == "pdf":
            return self._detect_pdf_orientation(file_path)
        elif file_type == "word":
            return self._detect_word_orientation(file_path)
        else:
            return "portrait"  # 默认纵向
            
    def _detect_image_orientation(self, file_path: str) -> str:
        """检测图片朝向（带超时，防止OneDrive文件卡死）
        
        Args:
            file_path: 图片文件路径
            
        Returns:
            str: 'portrait' 或 'landscape'
        """
        if not self.pil_available:
            return "portrait"
            
        # 先用超时机制读取图片尺寸
        def _read_image_size(path):
            with Image.open(path) as img:
                return img.size  # (width, height)
        
        result = _run_with_timeout(_read_image_size, file_path, timeout=READ_TIMEOUT)
        
        if result is None:
            # 超时或失败，返回默认纵向
            print(f"图片朝向检测超时，使用默认纵向: {os.path.basename(file_path)}")
            return "portrait"
        
        width, height = result
        return "landscape" if width > height else "portrait"
            
    def _detect_pdf_orientation(self, file_path: str) -> str:
        """检测PDF朝向（带超时，防止OneDrive文件卡死）
        
        Args:
            file_path: PDF文件路径
            
        Returns:
            str: 'portrait' 或 'landscape'
        """
        if not self.pymupdf_available:
            return "portrait"
            
        # 用超时机制打开PDF
        def _read_pdf_size(path):
            doc = fitz.open(path)
            try:
                if len(doc) > 0:
                    page = doc[0]
                    rect = page.rect
                    return (rect.width, rect.height)
                return None
            finally:
                doc.close()
        
        result = _run_with_timeout(_read_pdf_size, file_path, timeout=READ_TIMEOUT)
        
        if result is None:
            print(f"PDF朝向检测超时，使用默认纵向: {os.path.basename(file_path)}")
            return "portrait"
        
        width, height = result
        return "landscape" if width > height else "portrait"
            
    def _detect_word_orientation(self, file_path: str) -> str:
        """检测Word文档朝向
        
        Args:
            file_path: Word文件路径
            
        Returns:
            str: 'portrait' 或 'landscape'
        """
        # 简化实现：尝试读取Word文档的页面设置
        # 完整实现需要用到win32com.client
        try:
            # 这里需要调用Word COM接口
            # 暂时返回默认值
            # TODO: 实现完整的Word朝向检测
            return "portrait"
        except Exception as e:
            print(f"检测Word朝向失败: {e}")
            return "portrait"
            
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
            
    def is_available(self) -> bool:
        """检查引擎是否可用
        
        Returns:
            bool: 是否可用
        """
        # 至少有一个库可用才认为引擎可用
        return self.pil_available or self.pymupdf_available
