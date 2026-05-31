"""
PDF 打印适配器
优先级：SumatraPDF > Adobe Acrobat > ShellExecute 降级
所有方法均使用安全（ASCII）临时路径，避免中文路径问题
"""

import os
import subprocess
import shutil
import tempfile
import time

try:
    import win32api
    import win32con
    import win32print
    WIN32_OK = True
except ImportError:
    WIN32_OK = False


def _safe_temp_copy(src_path):
    """将文件复制到安全 ASCII 路径，返回 (safe_path, is_temp)"""
    ext = os.path.splitext(src_path)[1] or ".tmp"
    win_temp = r"C:\Windows\Temp"
    if not os.path.isdir(win_temp):
        win_temp = tempfile.gettempdir()
    stamp = int(time.time() * 1000)
    dest = os.path.join(win_temp, f"bp_pdf_{stamp}{ext}")
    try:
        shutil.copy2(src_path, dest)
        print(f"[PdfAdapter] 临时副本: {dest}")
        return dest, True
    except Exception as e:
        print(f"[PdfAdapter] 复制失败，用原路径: {e}")
        return os.path.abspath(src_path), False


class PdfPrintAdapter:
    """PDF 打印适配器"""

    def __init__(self):
        self.name = "PdfPrintAdapter"
        self._sumatra_path = self._find_sumatra()
        self._acrobat_path = self._find_acrobat()

    def _find_sumatra(self):
        possible = [
            r"C:\Program Files\SumatraPDF\SumatraPDF.exe",
            r"C:\Program Files (x86)\SumatraPDF\SumatraPDF.exe",
        ]
        for p in possible:
            if os.path.exists(p):
                return p
        return shutil.which("SumatraPDF.exe")

    def _find_acrobat(self):
        possible = [
            r"C:\Program Files\Adobe\Acrobat DC\Acrobat\Acrobat.exe",
            r"C:\Program Files (x86)\Adobe\Acrobat DC\Acrobat\Acrobat.exe",
            r"C:\Program Files\Adobe\Acrobat Reader DC\Reader\AcroRd32.exe",
            r"C:\Program Files (x86)\Adobe\Acrobat Reader DC\Reader\AcroRd32.exe",
        ]
        for p in possible:
            if os.path.exists(p):
                return p
        return shutil.which("AcroRd32.exe")

    def is_available(self):
        return True  # 始终有降级方案

    def print_file(self, file_path, printer_name, copies=1,
                   color_mode="color", orientation="portrait", scale_mode="fit"):
        if not os.path.exists(file_path):
            print(f"[PdfAdapter] 文件不存在: {file_path}")
            return False

        printer_name = str(printer_name).strip().rstrip("\x00")
        print(f"[PdfAdapter] 打印: {os.path.basename(file_path)} -> [{printer_name}]")

        # 复制到安全路径
        safe_path, is_temp = _safe_temp_copy(file_path)

        try:
            if self._sumatra_path:
                if self._print_via_sumatra(safe_path, printer_name, copies):
                    return True
                print("[PdfAdapter] SumatraPDF 失败，降级...")

            if self._acrobat_path:
                if self._print_via_acrobat(safe_path, printer_name, copies):
                    return True
                print("[PdfAdapter] Acrobat 失败，降级...")

            print("[PdfAdapter] 使用 ShellExecute 降级方案...")
            return self._print_via_shellexecute(safe_path, copies)
        finally:
            if is_temp:
                def _delay_delete():
                    time.sleep(10)
                    try:
                        if os.path.exists(safe_path):
                            os.remove(safe_path)
                            print(f"[PdfAdapter] 已清理临时文件")
                    except Exception:
                        pass
                import threading
                threading.Thread(target=_delay_delete, daemon=True).start()

    def _print_via_sumatra(self, file_path, printer_name, copies):
        try:
            for i in range(copies):
                cmd = [
                    self._sumatra_path,
                    '-print-to', printer_name,
                    '-silent',
                    file_path
                ]
                print(f"  [SumatraPDF] 打印中 ({i+1}/{copies})...")
                result = subprocess.run(
                    cmd, capture_output=True, text=True, timeout=30, shell=False
                )
                if result.returncode != 0:
                    err = (result.stderr or result.stdout or "").strip()
                    print(f"  ✗ SumatraPDF 失败: {err}")
                    return False
                print(f"  ✓ SumatraPDF 已发送 ({i+1}/{copies})")
            print("[PdfAdapter] ✓ SumatraPDF 完成")
            return True
        except subprocess.TimeoutExpired:
            print("  ✗ SumatraPDF 超时")
            return False
        except Exception as e:
            print(f"  ✗ SumatraPDF 异常: {e}")
            return False

    def _print_via_acrobat(self, file_path, printer_name, copies):
        try:
            try:
                win32print.SetDefaultPrinter(printer_name)
            except Exception:
                pass
            for i in range(copies):
                cmd = [self._acrobat_path, '/p', '/h', file_path]
                print(f"  [Acrobat] 打印中 ({i+1}/{copies})...")
                subprocess.run(cmd, capture_output=True, timeout=30, shell=False)
                print(f"  ✓ Acrobat 已发送 ({i+1}/{copies})")
                time.sleep(2)
            print("[PdfAdapter] ✓ Acrobat 完成")
            return True
        except Exception as e:
            print(f"  ✗ Acrobat 异常: {e}")
            return False

    def _print_via_shellexecute(self, file_path, copies):
        try:
            if not WIN32_OK:
                print("  ✗ win32 不可用")
                return False
            for i in range(copies):
                win32api.ShellExecute(
                    0, "print", file_path, None, None, win32con.SW_HIDE
                )
                print(f"  ✓ ShellExecute ({i+1}/{copies})")
                time.sleep(2)
            print("[PdfAdapter] ✓ ShellExecute 完成")
            return True
        except Exception as e:
            print(f"  ✗ ShellExecute 失败: {e}")
            return False

    def get_name(self):
        return self.name

    def get_sumatra_download_info(self):
        return {
            'name': 'SumatraPDF',
            'url': 'https://www.sumatrapdfreader.org/download-free-pdf-reader.html',
            'description': '轻量级 PDF 阅读器，支持静默打印（推荐安装）'
        }
