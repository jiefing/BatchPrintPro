"""
打印机管理模块 - 纯函数式接口，无信号依赖
返回同步结果，由调用方自行更新 UI
"""

import os
import traceback


def get_printers():
    """获取系统中所有打印机列表（同步，立即返回）
    
    Returns:
        tuple: (printer_list, default_printer, error_msg)
            printer_list: [{'name': str, 'is_default': bool}, ...]
            default_printer: str 或 ''
            error_msg: str 或 None
    """
    try:
        import win32print
    except ImportError:
        return [], "", "win32print 不可用，请安装 pywin32 (pip install pywin32)"

    try:
        default_printer = win32print.GetDefaultPrinter()
    except Exception:
        default_printer = ""

    try:
        printers_raw = win32print.EnumPrinters(
            win32print.PRINTER_ENUM_LOCAL |
            win32print.PRINTER_ENUM_CONNECTIONS
        )
    except Exception as e:
        return [], default_printer, f"EnumPrinters 失败: {e}"

    printer_list = []
    for p in printers_raw:
        name = p[2]  # 打印机名称
        printer_list.append({
            'name': name,
            'is_default': (name == default_printer)
        })

    return printer_list, default_printer, None
