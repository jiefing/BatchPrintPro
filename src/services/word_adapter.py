"""
Word 打印适配器
优先使用 win32com 调用 Word 打印；降级用 ShellExecute
"""

import os
import time

try:
    import win32com.client
    WIN32COM_AVAILABLE = True
except ImportError:
    WIN32COM_AVAILABLE = False

try:
    import win32api
    import win32con
    import win32print
    WIN32_AVAILABLE = True
except ImportError:
    WIN32_AVAILABLE = False


class WordPrintAdapter:
    """Word 打印适配器"""

    def __init__(self):
        self.name = "WordPrintAdapter"
        self._word_available = self._check_word()

    def _check_word(self):
        """检查 Word 是否可用"""
        if not WIN32COM_AVAILABLE:
            return False
        try:
            word = win32com.client.Dispatch("Word.Application")
            word.Quit(SaveChanges=False)
            return True
        except Exception:
            return False

    def is_available(self):
        """检查是否可用"""
        return True  # 始终有降级方案

    def print_file(self, file_path, printer_name, copies=1, color_mode="color",
                   orientation="portrait", scale_mode="fit"):
        """
        打印 Word 文件
        """
        if not os.path.exists(file_path):
            print(f"[WordAdapter] 文件不存在: {file_path}")
            return False

        file_path = os.path.abspath(file_path)
        printer_name = str(printer_name).strip()
        print(f"[WordAdapter] 打印: {os.path.basename(file_path)} -> [{printer_name}]")

        # 方法1: win32com 调用 Word（最可靠）
        if self._word_available:
            if self._print_via_com(file_path, printer_name, copies):
                return True
            print(f"[WordAdapter] COM 方法失败，尝试降级方案...")

        # 方法2: ShellExecute print 动词
        print(f"[WordAdapter] 使用系统默认程序打印（可能弹窗）")
        return self._print_via_shellexecute(file_path, copies)

    def _print_via_com(self, file_path, printer_name, copies):
        """通过 Word COM 对象打印"""
        word = None
        doc = None
        try:
            import win32com.client

            print(f"[WordAdapter] 启动 Word COM...")

            # 设置默认打印机
            try:
                win32print.SetDefaultPrinter(printer_name)
            except Exception as e:
                print(f"[WordAdapter] 设置默认打印机警告: {e}")

            # 启动 Word（不显示界面）
            word = win32com.client.Dispatch("Word.Application")
            word.Visible = False

            # 打开文档
            doc = word.Documents.Open(file_path)

            # 设置打印机（通过 ActivePrinter 属性）
            word.ActivePrinter = printer_name

            print(f"[WordAdapter] 发送打印命令 ({copies} 份)...")
            for i in range(copies):
                # Background=False 等待打印完成
                doc.PrintOut(
                    Background=False,
                    Copies=1
                )
                print(f"  ✓ 已发送 ({i+1}/{copies})")
                time.sleep(1)

            print(f"[WordAdapter] ✓ Word COM 打印命令已发送")
            return True

        except Exception as e:
            print(f"[WordAdapter] ✗ Word COM 打印失败: {e}")
            return False
        finally:
            try:
                if doc:
                    doc.Close(SaveChanges=False)
            except Exception:
                pass
            try:
                if word:
                    word.Quit(SaveChanges=False)
            except Exception:
                pass

    def _print_via_shellexecute(self, file_path, copies):
        """通过 ShellExecute 调用系统默认程序打印"""
        try:
            if not WIN32_AVAILABLE:
                print(f"[WordAdapter] ✗ win32api 不可用")
                return False

            for i in range(copies):
                win32api.ShellExecute(
                    0,
                    'print',
                    file_path,
                    None,
                    None,
                    win32con.SW_HIDE
                )
                print(f"  ✓ ShellExecute 已调用默认程序打印 ({i+1}/{copies})")
                time.sleep(2)

            print(f"[WordAdapter] ✓ 系统默认程序打印命令已发送")
            return True

        except Exception as e:
            print(f"[WordAdapter] ✗ ShellExecute 打印失败: {e}")
            return False

    def get_name(self):
        """获取适配器名称"""
        return self.name
