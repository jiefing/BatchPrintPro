#!/usr/bin/env python3
"""
BatchPrint Pro - 批量打印工具
主程序
"""

import sys
import os
import datetime
import traceback

# 日志文件（exe 同级目录）
if getattr(sys, 'frozen', False):
    _log_dir = os.path.dirname(sys.executable)
else:
    _log_dir = os.path.dirname(os.path.abspath(__file__))

_log_path = os.path.join(_log_dir, "debug_main.log")


def _log(msg):
    try:
        with open(_log_path, "a", encoding="utf-8") as f:
            f.write(f"[{datetime.datetime.now():%H:%M:%S}] {msg}\n")
    except Exception:
        pass
    print(msg)


_log("=" * 40)
_log("BatchPrint Pro 启动")
_log(f"Python {sys.version}")
_log(f"frozen={getattr(sys, 'frozen', False)}")

# 添加 src 目录到 Python 路径
try:
    if getattr(sys, 'frozen', False):
        _src_dir = sys._MEIPASS
    else:
        _src_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "src"
        )
    sys.path.insert(0, _src_dir)
    _log(f"src 目录: {_src_dir}")
except Exception as e:
    _log(f"设置路径失败: {e}")


def _load_splash_image():
    """加载启动画面图片，失败则返回纯色 QPixmap"""
    from PySide6.QtGui import QPixmap, QColor, QImage

    # 尝试加载 splash.png
    if getattr(sys, 'frozen', False):
        splash_path = os.path.join(sys._MEIPASS, "splash.png")
    else:
        splash_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "splash.png"
        )
    _log(f"splash 路径: {splash_path}")

    pix = QPixmap(splash_path)
    if not pix.isNull():
        _log("splash.png 加载成功")
        return pix

    # 失败则用纯色图片替代
    _log("splash.png 加载失败，使用纯色替代")
    img = QImage(500, 300, QImage.Format_RGB32)
    img.fill(QColor("#1a1a2e"))
    return QPixmap.fromImage(img)


def main():
    _log("进入 main()")
    splash = None
    try:
        from PySide6.QtWidgets import QApplication, QSplashScreen, QMessageBox
        from PySide6.QtCore import Qt, QTimer

        _log("QApplication 创建前")
        app = QApplication(sys.argv)
        app.setApplicationName("BatchPrint Pro")
        _log("QApplication 创建成功")

        # ── 启动画面 ──
        _log("创建 QSplashScreen")
        splash_pix = _load_splash_image()
        splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
        splash.show()
        splash.showMessage(
            "正在启动...",
            Qt.AlignBottom | Qt.AlignHCenter,
            Qt.white,
        )
        app.processEvents()
        _log("启动画面显示成功")

        # ── 第1步：获取打印机列表 ──
        splash.showMessage(
            "正在检测打印机...",
            Qt.AlignBottom | Qt.AlignHCenter,
            Qt.white,
        )
        app.processEvents()
        _log("导入 printer_manager")
        from services.printer_manager import get_printers
        printer_list, default_printer, err_msg = get_printers()
        _log(f"打印机数量: {len(printer_list) if printer_list else 0}")

        # ── 第2步：创建视图模型 ──
        splash.showMessage(
            "正在初始化...",
            Qt.AlignBottom | Qt.AlignHCenter,
            Qt.white,
        )
        app.processEvents()
        _log("导入 PrintViewModel")
        from viewmodels.print_viewmodel import PrintViewModel
        viewmodel = PrintViewModel()
        _log("PrintViewModel 创建成功")

        # ── 第3步：创建主窗口 ──
        splash.showMessage(
            "正在加载界面...",
            Qt.AlignBottom | Qt.AlignHCenter,
            Qt.white,
        )
        app.processEvents()
        _log("导入 MainWindow")
        from views.main_window import MainWindow
        main_window = MainWindow(
            viewmodel,
            printer_list=printer_list,
            default_printer=default_printer,
        )
        _log("MainWindow 创建成功")

        # ── 完成 ──
        splash.showMessage(
            "启动完成！",
            Qt.AlignBottom | Qt.AlignHCenter,
            Qt.white,
        )
        app.processEvents()
        import time
        time.sleep(0.3)
        splash.finish(main_window)
        main_window.show()
        _log("主窗口显示成功，进入事件循环")

        sys.exit(app.exec())

    except Exception as e:
        _log(f"!!! 启动失败: {type(e).__name__}: {e}")
        _log(traceback.format_exc())
        # 尝试弹窗告知用户
        try:
            from PySide6.QtWidgets import QApplication, QMessageBox
            app = QApplication.instance()
            if app is None:
                app = QApplication(sys.argv)
            QMessageBox.critical(
                None,
                "启动失败",
                f"程序启动失败：\n\n{type(e).__name__}: {e}\n\n"
                f"详见：\n{_log_path}",
            )
        except Exception:
            pass
        sys.exit(1)


if __name__ == "__main__":
    main()
