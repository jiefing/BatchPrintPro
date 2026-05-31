"""
图片打印适配器
使用 PIL + Windows GDI (win32ui) 直接打印图片
避免 rundll32 shimgvw.dll 在 Windows 10 上已废弃且不可靠的问题
"""

import os
import time

from PIL import Image, ImageWin

try:
    import win32print
    import win32ui
    import win32con
    WIN32_OK = True
except ImportError:
    WIN32_OK = False


class ImagePrintAdapter:
    """图片打印适配器 - 使用 PIL + Windows GDI 直接打印"""

    def __init__(self):
        self.name = "ImagePrintAdapter"

    def is_available(self):
        return WIN32_OK

    def print_file(self, file_path, printer_name, copies=1,
                   color_mode="color", orientation="portrait", scale_mode="fit"):
        if not os.path.exists(file_path):
            print("[ImageAdapter] 文件不存在: " + file_path)
            return False
        if not WIN32_OK:
            print("[ImageAdapter] win32 不可用")
            return False

        printer_name = str(printer_name).strip().rstrip("\x00")
        print("[ImageAdapter] 打印: " + os.path.basename(file_path) +
              " -> [" + printer_name + "]")

        try:
            image = Image.open(file_path)
            if image.mode not in ("RGB", "L"):
                image = image.convert("RGB")

            img_width, img_height = image.size

            # 根据朝向旋转
            if orientation == "landscape" and img_width < img_height:
                image = image.rotate(90, expand=True)
                img_width, img_height = image.size
            elif orientation == "portrait" and img_width > img_height:
                image = image.rotate(90, expand=True)
                img_width, img_height = image.size

            hdc = win32ui.CreateDC()
            hdc.CreatePrinterDC(printer_name)

            # 获取可打印区域 (HORZRES, VERTRES)
            page_w = hdc.GetDeviceCaps(win32con.HORZRES)
            page_h = hdc.GetDeviceCaps(win32con.VERTRES)

            # 计算缩放
            if scale_mode == "fit":
                ratio = min(page_w / img_width, page_h / img_height)
            else:
                ratio = 1.0

            scaled_w = int(img_width * ratio)
            scaled_h = int(img_height * ratio)

            # 居中
            x_offset = max(0, (page_w - scaled_w) // 2)
            y_offset = max(0, (page_h - scaled_h) // 2)

            for i in range(copies):
                hdc.StartDoc(file_path)
                hdc.StartPage()

                dib = ImageWin.Dib(image)
                dib.draw(
                    hdc.GetHandleOutput(),
                    (x_offset, y_offset, x_offset + scaled_w, y_offset + scaled_h)
                )

                hdc.EndPage()
                hdc.EndDoc()
                print("  ✓ 打印完成 (" + str(i + 1) + "/" + str(copies) + ")")
                if i < copies - 1:
                    time.sleep(0.5)

            print("[ImageAdapter] ✓ 图片打印完成")
            return True

        except Exception as e:
            print("[ImageAdapter] ✗ 直接打印失败: " + str(e))
            import traceback
            traceback.print_exc()
            return self._fallback_shellexecute(file_path, copies)

    def _fallback_shellexecute(self, file_path, copies):
        """降级：用 ShellExecute print 动词"""
        try:
            import win32api
            for i in range(copies):
                win32api.ShellExecute(
                    0, "print", file_path, None, None, win32con.SW_HIDE
                )
                time.sleep(2)
            print("[ImageAdapter] ✓ ShellExecute 降级打印已发送")
            return True
        except Exception as e:
            print("[ImageAdapter] ✗ ShellExecute 也失败: " + str(e))
            return False

    def get_name(self):
        return self.name
