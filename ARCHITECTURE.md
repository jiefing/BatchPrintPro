# BatchPrint Pro - 软件架构文档
# 版本：v0.9（调试中）
# 日期：2026-05-28

---

## 一、项目概述

| 项目 | 内容 |
|---|---|
| 软件名称 | BatchPrint Pro |
| 用途 | Windows 批量打印工具，支持拖拽添加图片/PDF/Word，精细化控制打印参数 |
| 技术栈 | Python 3.13 + PySide6 6.11.1 + pywin32 |
| 架构模式 | MVVM（Model - View - ViewModel）|
| 目标系统 | Windows 10/11 |
| 项目路径（推荐运行）| `F:\work2\BatchPrintPro\`（纯英文路径，中文路径有兼容问题）|
| 项目路径（原始）| `F:\work2\打印软件\BatchPrintPro\` |

---

## 二、目录结构

```
F:\work2\BatchPrintPro\
├── main.py                      # 程序入口
├── run.bat                     # 启动脚本（自动检测/创建 venv）
├── run_debug.bat              # 调试启动脚本
├── requirements.txt            # Python 依赖清单
├── venv\                      # Python 虚拟环境（自动创建）
├── error.log                  # 运行时错误日志
├── debug_main.log             # 启动过程调试日志
├── debug_print.log            # 打印过程调试日志
└── src\
    ├── models\
    │   ├── __init__.py
    │   ├── print_task.py      # PrintTask 数据模型（QObject子类）
    │   └── task_list.py      # PrintTaskList 任务列表管理（QObject子类）
    ├── views\
    │   ├── __init__.py
    │   ├── main_window.py     # MainWindow 主窗口（QMainWindow子类）
    │   ├── drop_zone.py      # DropZoneWidget 拖拽区域（QWidget子类）
    │   ├── task_list_widget.py# TaskListWidget 任务表格（QWidget子类）
    │   └── print_settings_dialog.py  # PrintSettingsDialog 设置弹窗（QDialog子类）
    ├── viewmodels\
    │   ├── __init__.py
    │   └── print_viewmodel.py # PrintViewModel + PrintThread（QObject/QThread子类）
    └── services\
        ├── __init__.py
        ├── print_adapter.py   # PrintAdapter 抽象基类（ABC）
        ├── image_adapter.py   # ImagePrintAdapter 图片打印
        ├── pdf_adapter.py     # PdfPrintAdapter PDF打印
        ├── word_adapter.py    # WordPrintAdapter Word打印
        ├── printer_manager.py  # get_printers() 打印机列表获取（纯函数）
        ├── file_scanner.py    # FileScannerService 文件扫描服务
        └── layout_analyzer.py# LayoutAnalysisEngine 版式分析（朝向检测）
```

---

## 三、架构设计（MVVM）

```
┌─────────────────────────────────────────────────────┐
│                   main.py（入口）                    │
│  1. 同步调用 get_printers() 获取打印机列表        │
│  2. 创建 PrintViewModel（传入打印机列表）          │
│  3. 创建 MainWindow（传入 ViewModel + 打印机列表） │
│  4. 启动 QApplication 事件循环                    │
└──────────────────────┬──────────────────────────┘
                           │
          ┌──────────────┴──────────────┐
          │       ViewModel 层              │
          │  PrintViewModel（QObject）     │
          │  - task_list: PrintTaskList   │
          │  - print_adapters: dict       │
          │  - print_thread: PrintThread  │
          │  - 信号：task_added/removed/  │
          │    updated/progress_updated/    │
          │    print_started/finished/     │
          │    print_error                 │
          └──────────────┬──────────────┘
                         │ 信号绑定
    ┌────────────────────┴────────────────────┐
    │              View 层（PySide6 GUI）       │
    │  MainWindow                               │
    │  ├── DropZoneWidget（拖拽区）           │
    │  ├── TaskListWidget（任务表格）           │
    │  ├── QComboBox（打印机选择）             │
    │  ├── QCheckBox（双面/黑白）             │
    │  ├── QPushButton（开始/清空）            │
    │  └── QProgressBar（进度条）             │
    └────────────────────┬────────────────────┘
                         │ 调用
          ┌──────────────┴──────────────┐
          │              Model 层               │
          │  PrintTask（QObject，单任务）    │
          │  PrintTaskList（QObject，列表）  │
          │  - tasks: List[PrintTask]      │
          │  - 信号：task_added/removed/   │
          │    updated/progress_updated/     │
          │    list_cleared                 │
          └──────────────┬──────────────┘
                         │ 调用
    ┌────────────────────┴────────────────────┐
    │           Services 层（业务逻辑）          │
    │  PrintAdapter（抽象基类）                │
    │  ├── ImagePrintAdapter                   │
    │  ├── PdfPrintAdapter（SumatraPDF优先）  │
    │  └── WordPrintAdapter                   │
    │  PrinterManager（get_printers()）        │
    │  FileScannerService（文件扫描）          │
    │  LayoutAnalysisEngine（朝向检测）        │
    └─────────────────────────────────────────┘
```

---

## 四、核心模块详解

### 4.1 main.py（入口）

**职责：** 程序启动引导，同步获取打印机列表后初始化 GUI。

**启动流程：**
1. 调用 `printer_manager.get_printers()` 同步获取打印机列表
2. 创建 `PrintViewModel()` 实例
3. 创建 `MainWindow(viewmodel, printer_list, default_printer)` 实例
4. 调用 `main_window.show()` 显示主窗口
5. 进入 `app.exec()` Qt 事件循环

**调试日志：** 写入 `debug_main.log`，每行带 `[HH:MM:SS]` 时间戳。

---

### 4.2 PrintTask（数据模型）

**文件：** `src/models/print_task.py`

**属性：**

| 属性 | 类型 | 说明 |
|---|---|---|
| `file_path` | str | 文件绝对路径 |
| `file_name` | str | `os.path.basename(file_path)` |
| `file_type` | str | `"image"` / `"pdf"` / `"word"` / `"unknown"` |
| `page_count` | int | 页数（当前未实现，恒为0）|
| `orientation` | str | `"auto"` / `"portrait"` / `"landscape"` |
| `copies` | int | 打印份数，默认1 |
| `color_mode` | str | `"color"` / `"monochrome"` |
| `scale_mode` | str | `"fit"` / `"original"` |
| `status` | str | `"pending"` / `"processing"` / `"completed"` / `"failed"` |
| `error_message` | str | 失败时的错误信息 |

**信号：**
- `status_changed(str)` — 状态改变时发射
- `settings_changed()` — 设置改变时发射

**已知问题：**
- `page_count` 始终为 0，未实现 PDF/Word 页数检测
- `_detect_file_type()` 中 `.tiff` 拼写为 `.tiff`（多了一个 `f`），`.tif` 正确

---

### 4.3 PrintTaskList（任务列表管理）

**文件：** `src/models/task_list.py`

**职责：** 管理任务列表，发射列表变化信号。

**主要方法：**

| 方法 | 说明 |
|---|---|
| `add_task(task)` | 追加任务，发射 `task_added` |
| `remove_task(index)` | 按索引移除，发射 `task_removed` |
| `clear_all()` | 清空列表，发射 `list_cleared` |
| `get_task(index)` | 按索引获取任务 |
| `update_task_status(index, status)` | 更新任务状态，发射 `task_updated` |
| `update_task_settings(index, **kwargs)` | 更新任务设置，发射 `task_updated` |

**信号：**
- `task_added(PrintTask)`
- `task_removed(int, str)` — `(index, file_path)`
- `task_updated(PrintTask)`
- `progress_updated(int, int)` — `(completed, total)`

---

### 4.4 PrintViewModel（视图模型）

**文件：** `src/viewmodels/print_viewmodel.py`

**职责：** 连接 View 和 Model，处理所有业务逻辑。

**主要方法：**

| 方法 | 说明 |
|---|---|
| `add_files(file_paths)` | 添加文件/文件夹到队列 |
| `_add_single_file(file_path)` | 添加单个文件（含格式检查、朝向检测）|
| `remove_task(index)` | 移除任务 |
| `clear_all_tasks()` | 清空所有任务 |
| `update_task_settings(index, **kwargs)` | 更新任务设置 |
| `start_printing(printer_name)` | 启动打印线程 |
| `cancel_printing()` | 取消打印线程 |
| `set_global_duplex(enabled)` | 设置全局双面打印 |
| `set_global_monochrome(enabled)` | 设置全局黑白打印 |

**信号：**
- `task_added(PrintTask)`
- `task_removed(int, str)`
- `task_updated(PrintTask)`
- `progress_updated(int, int)`
- `print_started()`
- `print_finished()`
- `print_error(str)`

**打印适配器字典：**
```python
self.print_adapters = {
    'image': ImagePrintAdapter(),
    'pdf': PdfPrintAdapter(),
    'word': WordPrintAdapter()
}
```

---

### 4.5 PrintThread（打印线程）

**文件：** `src/viewmodels/print_viewmodel.py`（与 ViewModel 同文件）

**职责：** 后台 QThread，逐任务调用对应适配器执行打印。

**信号：**
- `progress_updated(int, int)` — `(current, total)`
- `task_completed(int, bool)` — `(index, success)`
- `all_completed()`
- `error_occurred(str)`

**取消机制：** `_is_cancelled` 标志 + `QMutex` 保护，调用 `cancel()` 设置标志。

**已知问题：**
- `task_completed` 信号在 ViewModel 中连接到了 `_on_task_completed`，但该方法体为 `pass`，未实现任何逻辑
- `all_completed` 信号发射后，`print_finished` 信号正确连接到 MainWindow 的 `_on_print_finished`

---

### 4.6 打印适配器

#### 4.6.1 PrintAdapter（抽象基类）

**文件：** `src/services/print_adapter.py`

**接口方法：**
- `print_file(file_path, printer_name, copies, color_mode, orientation, scale_mode) -> bool`
- `is_available() -> bool`
- `get_name() -> str`

#### 4.6.2 ImagePrintAdapter

**文件：** `src/services/image_adapter.py`

**当前实现：** 使用 `os.startfile(file_path, "print")` 调用系统默认程序打印。

**流程：**
1. 调用 `win32print.SetDefaultPrinter(printer_name)` 设置默认打印机
2. 循环 `copies` 次，每次调用 `os.startfile(file_path, "print")`
3. 每次调用后 `time.sleep(3)` 等待打印作业入队

**已知问题：**
- `os.startfile(file_path, "print")` 依赖系统默认程序（照片查看器/画图）的打印功能，行为不可控
- 打印完成后无回调确认，仅表示"打印命令已发送"
- 中文字符路径下可能失败（已在纯英文路径测试通过）

#### 4.6.3 PdfPrintAdapter

**文件：** `src/services/pdf_adapter.py`

**当前实现：** 优先使用 SumatraPDF 命令行打印，降级使用 `os.startfile(..., "print")`。

**SumatraPDF 打印命令：**
```python
cmd = [sumatra_path, '-print-to', printer_name, '-silent', file_path]
```

**降级方案：** `os.startfile(file_path, "print")` 使用系统默认 PDF 阅读器打印。

**已知问题：**
- SumatraPDF 未随软件分发，需用户自行安装
- `get_sumatra_download_info()` 方法已定义但未在 UI 中调用

#### 4.6.4 WordPrintAdapter

**文件：** `src/services/word_adapter.py`

**当前实现：** 使用 `os.startfile(file_path, "print")` 调用 Word 打印。

**已知问题：**
- 依赖 Microsoft Word 已安装
- 打印后 Word 进程可能残留（不自动关闭）
- 无静默打印选项

---

### 4.7 PrinterManager

**文件：** `src/services/printer_manager.py`

**接口：** 纯函数 `get_printers() -> (printer_list, default_printer, error_msg)`

**实现：** 使用 `win32print.EnumPrinters()` 获取系统中所有打印机。

**返回格式：**
```python
printer_list = [
    {'name': 'Printer Name', 'is_default': True},
    ...
]
default_printer = 'Printer Name'  # 或 ''
error_msg = None  # 或错误信息字符串
```

**调用时机：** 仅在 `main.py` 启动时同步调用一次，结果传入 `MainWindow`。

---

### 4.8 FileScannerService

**文件：** `src/services/file_scanner.py`

**职责：** 扫描文件/文件夹，过滤支持的文件格式。

**支持格式：**
- 图片：`.jpg`, `.jpeg`, `.png`, `.bmp`, `.tiff`, `.tif`
- PDF：`.pdf`
- Word：`.doc`, `.docx`

**扫描深度：** 默认最大 2 级目录深度。

**文件有效性检查（`_is_valid_file`）：**
- 检查文件大小 > 1KB（跳过 OneDrive 占位文件）
- 尝试以二进制模式读取第 1 个字节（检查文件是否锁定或可访问）

---

### 4.9 LayoutAnalysisEngine

**文件：** `src/services/layout_analyzer.py`

**职责：** 自动检测文件朝向（横向/纵向）。

**检测方法：**
- 图片：用 Pillow (`Image.open`) 读取尺寸，宽 > 高则为横向
- PDF：用 PyMuPDF (`fitz.open`) 读取第一页尺寸
- Word：当前未实现，返回默认 `"portrait"`

**超时机制：** 文件读取通过 `concurrent.futures.ThreadPoolExecutor` 执行，超时 3 秒，防止 OneDrive 云端文件卡死。

**已知问题：**
- `_detect_image_orientation` 和 `_detect_pdf_orientation` 方法签名中 `self` 参数缩进错误（语法上仍正确，因为 Python 不检查缩进对齐）
- Word 朝向检测未实现（TODO 注释存在）

---

## 五、信号流转

### 5.1 添加文件流程

```
用户拖拽文件
    ↓
DropZoneWidget.files_dropped.emit(file_paths)
    ↓
PrintViewModel.add_files(file_paths)
    ↓
PrintViewModel._add_single_file(file_path)
    ↓
FileScannerService.is_supported_file(file_path)  # 格式检查
FileScannerService._is_valid_file(file_path)      # 有效性检查
LayoutAnalysisEngine.detect_orientation(file_path) # 朝向检测
    ↓
PrintTask(file_path)  # 创建任务对象
    ↓
PrintTaskList.add_task(task)
    ↓
PrintTaskList.task_added.emit(task)
    ↓
MainWindow._on_task_added(task)
    ↓
TaskListWidget.add_task(task)  # 更新 UI 表格
```

### 5.2 打印流程

```
用户点击"开始批量打印"
    ↓
MainWindow._on_start_clicked()
    ↓
PrintViewModel.start_printing(printer_name)
    ↓
创建 PrintThread(task_list, printer_name, adapters)
    ↓
PrintThread.start()  # 启动线程
    ↓
PrintViewModel.print_started.emit()
    ↓
MainWindow._on_print_started()  # 禁用 UI 控件
    ↓
PrintThread.run()  # 逐任务执行
    ↓
adapter.print_file(...)  # 调用对应适配器
    ↓
PrintThread.progress_updated.emit(current, total)
    ↓
PrintViewModel.progress_updated.emit(current, total)
    ↓
MainWindow._on_progress_updated(current, total)  # 更新进度条
    ↓
PrintThread.all_completed.emit()
    ↓
PrintViewModel._on_all_completed()
    ↓
PrintViewModel.print_finished.emit()
    ↓
MainWindow._on_print_finished()  # 弹窗提示，恢复 UI
```

---

## 六、已知问题汇总

| # | 问题 | 严重程度 | 所在文件 |
|---|---|---|---|
| 1 | 中文路径下 `os.startfile("print")` 可能弹出"系统找不到指定的路径" | 高 | `image_adapter.py`, `pdf_adapter.py`, `word_adapter.py` |
| 2 | `PrintThread._on_task_completed` 方法体为 `pass`，未处理单任务完成逻辑 | 中 | `print_viewmodel.py` |
| 3 | `page_count` 始终为 0，未实现 PDF/Word 页数检测 | 中 | `print_task.py` |
| 4 | Word 朝向检测未实现，始终返回 `"portrait"` | 低 | `layout_analyzer.py` |
| 5 | SumatraPDF 未随软件分发，需用户自行安装 | 中 | `pdf_adapter.py` |
| 6 | Word 打印后进程可能残留 | 中 | `word_adapter.py` |
| 7 | `file_scanner.py` 中 `.tiff` 扩展名拼写多了一个 `f` | 低 | `file_scanner.py` |
| 8 | `layout_analyzer.py` 中 `_detect_image_orientation` 方法 `self` 缩进不一致（语法无错误但代码不规范）| 低 | `layout_analyzer.py` |

---

## 七、依赖清单

```
PySide6>=6.5.0          # Qt 绑定（GUI 框架）
Pillow>=10.0.0           # 图片处理（朝向检测）
PyMuPDF>=1.23.0          # PDF 处理（页数检测、朝向检测）
pywin32>=306              # Windows API（打印机管理、打印）
python-docx>=0.8.11      # Word 文档处理（页数检测）
```

---

## 八、运行方式

### 推荐方式（纯英文路径，无中文）：

```bat
cd F:\work2\BatchPrintPro
run.bat
```

`run.bat` 会自动检测 venv 是否存在，若不存在则自动创建并安装依赖。

### 调试方式：

```bat
cd F:\work2\BatchPrintPro
run_debug.bat
```

调试模式下，标准错误输出写入 `debug_main.log`。

---

## 九、供专家评估的重点问题

1. **打印可靠性**：当前使用 `os.startfile("print")` 是最简单的方式，但无法确认打印是否真正成功，也无法控制打印参数（纸张大小、质量等）。是否有更可靠的方案？

2. **中文路径兼容**：用户在 `F:\work2\打印软件\` 路径下运行时，系统弹出"系统找不到指定的路径"。已建议用户改用 `F:\work2\BatchPrintPro\` 纯英文路径。根本原因是 Windows 老版本 `ShellExecute` / `rundll32` 对 Unicode 路径支持不好。是否有必要在代码层面进一步处理？

3. **打印线程设计**：当前 `PrintThread` 逐任务打印，每个任务用 `time.sleep(3)` 等待打印作业入队。这是否合理？是否需要用 `QTimer` 或回调机制替代？

4. **Word 打印方案**：当前用 `os.startfile("print")` 调用 Word 打印，Word 进程会残留。是否有办法静默打印并自动关闭 Word？

5. **安装包分发**：当前需要用户自行安装 Python + 依赖。是否需要打包为独立的 `.exe`（用 PyInstaller 或 Nuitka）？

---

*文档生成时间：2026-05-28*
*软件版本：v0.9（开发调试中）*
