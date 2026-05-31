# BatchPrint Pro / BatchPrint Pro - 批量打印软件

一款基于 MVVM 架构的桌面批量打印应用，支持 PDF、Word 及图片格式，适用于高效的文档处理工作流。

A desktop application for batch printing documents with a Model-View-ViewModel (MVVM) architecture, designed for efficient document processing workflows.

---

## 功能特性 | Features

### 核心功能 | Core Functionality

- ✅ **拖拽操作** | **Drag-and-Drop**: 支持拖拽文件或文件夹到主窗口 / Support drag-and-drop of files or folders to the main window
- ✅ **多格式支持** | **Multi-format Support**: 处理 PDF、Word 和图片文档（`.pdf`, `.docx`, `.jpg`, `.jpeg`, `.png`, `.bmp`, `.tiff`)/ Process PDF, Word, and image documents through a unified interface
- ✅ **批量处理** | **Batch Processing**: 将多个文档加入队列依次打印 / Queue multiple documents for sequential printing
- ✅ **打印预览** | **Print Preview**: 打印前可视化确认文档 / Visual confirmation of documents before printing
- ✅ **打印机选择** | **Printer Selection**: 动态枚举和选择可用打印机 / Dynamic enumeration and selection of available printers
- ✅ **打印设置** | **Print Settings**: 可配置页面方向（纵向/横向）和页面范围选择 / Configurable page orientation (portrait/landscape) and page range selection
- ✅ **任务管理** | **Task Management**: 添加、删除和重新排序打印队列中的任务 / Add, remove, and reorder print tasks in the queue
- ✅ **进度跟踪** | **Progress Tracking**: 打印操作期间实时状态更新 / Real-time status updates during printing operations
- ✅ **异步打印** | **Asynchronous Processing**: 后台执行打印任务，界面保持响应 / Print operations execute in a separate thread to maintain UI responsiveness

### 用户界面 | User Interface

- **拖拽区** | **Drag-and-Drop Zone**: 通过拖拽或文件对话框添加文件到打印队列 / Add files to the print queue via drag-and-drop or file dialog
- **任务列表** | **Task List**: 表格化显示队列中的文档及状态指示器 / Tabular display of queued documents with status indicators
- **设置对话框** | **Settings Dialog**: 打印参数模态配置界面 / Modal configuration interface for print parameters
- **启动画面** | **Splash Screen**: 应用程序启动进度指示 / Application startup progress indication

---

## 架构 | Architecture

本应用采用 MVVM（Model-View-ViewModel）设计模式，实现数据模型、业务逻辑和用户界面组件之间的关注点分离。

The application follows the MVVM (Model-View-ViewModel) design pattern to separate concerns between data models, business logic, and user interface components.

### 目录结构 | Directory Structure

```
BatchPrintPro/
├── main.py                    # 应用程序入口 | Application entry point
├── requirements.txt           # Python 依赖清单 | Python dependencies
├── src/
│   ├── models/              # 数据模型 | Data models
│   │   ├── print_task.py    # 打印任务数据结构 | Print task data structure
│   │   └── task_list.py     # 任务列表管理 | Task list management
│   ├── services/            # 业务逻辑层 | Business logic layer
│   │   ├── file_scanner.py  # 文件系统操作 | File system operations
│   │   ├── image_adapter.py # 图片打印适配器 | Image printing adapter
│   │   ├── layout_analyzer.py # 文档布局分析 | Document layout analysis
│   │   ├── pdf_adapter.py   # PDF 打印适配器 | PDF printing adapter
│   │   ├── print_adapter.py # 抽象打印接口 | Abstract print interface
│   │   ├── printer_manager.py # 打印机枚举与控制 | Printer enumeration and control
│   │   └── word_adapter.py  # Word 文档打印适配器 | Word document printing adapter
│   ├── viewmodels/          # 表现层逻辑 | Presentation logic
│   │   └── print_viewmodel.py # 协调模型与视图的 ViewModel | ViewModel coordinating models and views
│   └── views/              # 用户界面组件 | User interface components
│       ├── drop_zone.py      # 拖拽文件接收区 | Drag-and-drop file acceptance
│       ├── main_window.py    # 主应用窗口 | Primary application window
│       ├── print_settings_dialog.py # 打印配置对话框 | Print configuration dialog
│       ├── splash_progress.py # 启动进度指示器 | Startup progress indicator
│       └── task_list_widget.py # 任务队列显示组件 | Task queue display widget
└── resources/              # 静态资源 | Static assets
    ├── icon.ico             # 应用图标 | Application icon
    └── splash.png           # 启动画面图片 | Splash screen image
```

### 组件职责 | Component Responsibilities

**模型层 | Models** (`src/models/`):

- `PrintTask`: 封装单个打印任务元数据（文件路径、状态、设置）/ Encapsulates individual print job metadata (file path, status, settings)
- `TaskList`: 管理打印任务集合，支持添加/删除/重新排序操作 / Manages the collection of print tasks with add/remove/reorder operations

**服务层 | Services** (`src/services/`):

- `FileScanner`: 验证文件类型并扫描可打印文档的目录 / Validates file types and scans directories for printable documents
- `PrinterManager`: 枚举系统打印机并管理打印机句柄生命周期 / Enumerates system printers and manages printer handle lifecycle
- `PrintAdapter`（抽象类 | abstract）: 定义格式特定打印实现的接口 / Defines the interface for format-specific printing implementations
- `PDFAdapter`: 通过 PyMuPDF 实现 PDF 渲染和打印 / Implements PDF rendering and printing via PyMuPDF
- `WordAdapter`: 通过 python-docx 实现 Word 文档打印 / Implements Word document printing via python-docx
- `ImageAdapter`: 通过 Pillow 和 win32ui GDI 实现图片打印 / Implements image printing via Pillow and win32ui GDI
- `LayoutAnalyzer`: 分析文档结构以优化打印布局 / Analyzes document structure for optimal print layout

**视图模型层 | ViewModels** (`src/viewmodels/`):

- `PrintViewModel`: 协调模型与视图，处理用户操作和状态转换 / Mediates between Models and Views, handling user actions and state transitions

**视图层 | Views** (`src/views/`):

- `MainWindow`: 带菜单栏和中央部件的主应用窗口 / Primary application window with menu bar and central widget
- `TaskListWidget`: 显示打印队列的 QTableWidget 子类 / QTableWidget subclass displaying the print queue
- `DropZone`: 接受拖拽文件添加的自定义组件 / Custom widget accepting drag-and-drop file additions
- `PrintSettingsDialog`: 配置打印参数的 QDialog / QDialog for configuring print parameters
- `SplashProgress`: 启动进度指示的 QSplashScreen 子类 / QSplashScreen subclass for startup progress indication

---

## 安装 | Installation

### 前置要求 | Prerequisites

- Python 3.13 或更高版本 / Python 3.13 or higher
- Windows 操作系统（打印功能依赖 `pywin32`，为 Windows 专用）/ Windows operating system (printing functionality is Windows-specific due to `pywin32` dependency)

### 快速开始 | Quick Start

**1. 克隆仓库 | Clone the repository:**

```bash
git clone https://github.com/jiefing/BatchPrintPro.git
cd BatchPrintPro
```

**2. 创建虚拟环境 | Create a virtual environment:**

```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

**3. 安装依赖 | Install dependencies:**

```bash
pip install -r requirements.txt
```

**4. 运行应用 | Run the application:**

```bash
python main.py
```

---

## 使用方法 | Usage

### 添加文档 | Adding Documents

- 点击"添加文件"（Add Files）打开文件对话框 / Click "添加文件" (Add Files) to open a file dialog
- 或者，直接拖拽文件到应用窗口 / Alternatively, drag and drop files directly onto the application window
- 支持格式 | Supported formats: `.pdf`, `.docx`, `.jpg`, `.jpeg`, `.png`, `.bmp`, `.tiff`

### 管理打印队列 | Managing the Print Queue

- 在队列中选择一个或多个任务 / Select one or more tasks in the queue
- 右键点击删除选中的任务 / Right-click to remove selected tasks
- 使用"取消打印"（Cancel Print）按钮删除任务 / Use the "取消打印" (Cancel Print) button to remove tasks
- 任务可通过左键点击选择；支持多选 / Tasks can be selected with left-click; multiple selection is supported

### 配置打印设置 | Configuring Print Settings

- 选择一个任务并点击"打印设置"（Print Settings）/ Select a task and click "打印设置" (Print Settings)
- 从可用系统打印机中选择目标打印机 / Choose target printer from available system printers
- 选择页面方向（纵向或横向）/ Select page orientation (Portrait or Landscape)
- 指定页面范围（所有页面或自定义范围）/ Specify page range (All pages or custom range)

### 执行打印任务 | Executing Print Jobs

- 点击"开始打印"（Start Printing）开始批量打印 / Click "开始打印" (Start Printing) to begin batch printing
- 通过状态栏和任务列表指示器监控进度 / Monitor progress via the status bar and task list indicators
- 应用按顺序处理任务 / The application processes tasks sequentially

---

## 技术规格 | Technical Specifications

### 打印适配器 | Print Adapters

每种文档格式由实现 `PrintAdapter` 接口的专用适配器处理：

Each document format is handled by a dedicated adapter implementing the `PrintAdapter` interface:

| 格式 / Format | 适配器类 / Adapter Class | 后端库 / Backend Library | 打印方法 / Printing Method |
|--------|--------------|------------------|-----------------|
| PDF    | `PDFAdapter` | PyMuPDF (fitz)  | `fitz.Rect` + `fitz.Pixmap` 渲染到打印机 DC / rendering to printer DC |
| Word   | `WordAdapter` | python-docx      | 通过中间 PDF 转换渲染 / Renders via intermediate PDF conversion |
| Image  | `ImageAdapter` | Pillow + pywin32 | `win32ui` GDI `CreateDC` + `ImageWin.Dib` |

### 打印机管理 | Printer Management

`PrinterManager` 服务通过 `pywin32` 封装 Windows GDI 打印 API：

The `PrinterManager` service wraps the Windows GDI print API via `pywin32`:

- `win32print.EnumPrinters()`: 枚举可用打印机 / Enumerates available printers
- `win32print.OpenPrinter()`: 获取打印机句柄 / Obtains printer handle
- `win32print.GetPrinter()`: 检索打印机功能 / Retrieves printer capabilities
- `win32ui.CreateDC()`: 创建用于渲染的设备上下文 / Creates device context for rendering

### 异步处理 | Asynchronous Processing

打印操作在独立线程中执行以保持 UI 响应：

Print operations execute in a separate thread to maintain UI responsiveness:

- `QThread` 子类用于打印任务执行 / `QThread` subclass for print job execution
- 用于进度更新的信号-槽连接 / Signal-slot connections for progress updates
- 通过 `QMutex` 实现线程安全的任务队列访问 / Thread-safe task queue access via `QMutex`

---

## 依赖项 | Dependencies

| 包名 / Package | 版本 / Version | 用途 / Purpose |
|---------|---------|---------|
| `PySide6` | 6.11.1 | GUI 框架（Qt 6 绑定）/ GUI framework (Qt 6 bindings) |
| `Pillow` | ≥10.0.0 | 图像处理 / Image processing |
| `PyMuPDF` (fitz) | ≥1.23.0 | PDF 渲染 / PDF rendering |
| `python-docx` | ≥0.8.11 | Word 文档解析 / Word document parsing |
| `pywin32` | ≥306 | Windows GDI/打印 API / Windows GDI/printing API |
| `watchdog` | ≥4.0.0 | （可选）文件系统监控 / (Optional) File system monitoring |

---

## 从源码构建 | Building from Source

### 创建独立可执行文件 | Creating a Standalone Executable

应用可使用 PyInstaller 打包为独立的 Windows 可执行文件：

The application can be packaged as a standalone Windows executable using PyInstaller:

**1. 安装 PyInstaller | Install PyInstaller:**

```bash
pip install pyinstaller
```

**2. 运行构建脚本 | Run the build script:**

```bash
python -m PyInstaller BatchPrintPro.spec
```

**3. 可执行文件将生成在 `dist/BatchPrintPro/` 目录中。**

The executable will be generated in `dist/BatchPrintPro/`.

### Spec 文件配置 | Spec File Configuration

`BatchPrintPro.spec` 文件包含 PyInstaller 配置：

The `BatchPrintPro.spec` file contains the PyInstaller configuration:

```python
datas=[('splash.png', '.'), ('icon.ico', '.')],
hiddenimports=[
    'PySide6.QtCore', 'PySide6.QtGui', 'PySide6.QtWidgets',
    'PIL._imaging', 'fitz', 'win32print', 'win32api', 'docx'
],
icon='icon.ico'
```

---

## 贡献 | Contributing

欢迎贡献代码。提交拉取请求前，请先查阅[架构文档](ARCHITECTURE.md)。

Contributions are welcome. Please review the [architecture documentation](ARCHITECTURE.md) before submitting pull requests.

### 开发指南 | Development Guidelines

1. 遵循 PEP 8 代码风格指南 / Follow PEP 8 style guidelines
2. 保持 MVVM 关注点分离 / Maintain MVVM separation of concerns
3. 为新功能添加单元测试 / Add unit tests for new functionality
4. 更新 API 变更的文档 / Update documentation for API changes

### 报告问题 | Reporting Issues

报告 Bug 时，请包含以下信息：

When reporting bugs, please include:

- 操作系统版本 / Operating system version
- Python 版本 / Python version
- 已安装包版本（`pip freeze`）/ Installed package versions (`pip freeze`)
- 复现问题的步骤 / Steps to reproduce the issue
- 预期行为与实际行为 / Expected vs. actual behavior

更多指南请参阅 [CONTRIBUTING.md](CONTRIBUTING.md)。

See [CONTRIBUTING.md](CONTRIBUTING.md) for more guidelines.

---

## 许可证 | License

本项目采用 MIT 许可证 - 详情请参阅 [LICENSE](LICENSE) 文件。

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 致谢 | Acknowledgments

- Qt framework by The Qt Company
- PySide6 bindings by Qt for Python team
- PyMuPDF for PDF rendering capabilities
- Pillow development team for image processing library

---

**版本 | Version**: 1.0.0  
**最后更新 | Last Updated**: May 2026  
**维护者 | Maintainer**: BatchPrint Pro Contributors
