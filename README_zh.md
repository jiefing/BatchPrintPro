# BatchPrint Pro - 批量打印软件

一款原生、高性能的批量打印桌面应用，支持拖拽操作、多格式文件打印、自动化横纵向适配。

## 功能特性

- ✅ **拖拽操作**：支持拖拽文件或文件夹到主窗口
- ✅ **多格式支持**：图片 (.jpg, .jpeg, .png, .bmp, .tiff) 和文档 (.pdf, .doc, .docx)
- ✅ **自动横纵向适配**：根据文件内容自动判断打印朝向
- ✅ **打印参数微调**：支持修改打印份数、色彩模式、缩放模式等
- ✅ **全局统一设置**：支持一键设置所有任务为双面打印或统一黑白
- ✅ **异步打印**：后台执行打印任务，界面不卡顿
- ✅ **异常处理**：单个文件打印失败不影响整个队列

## 技术栈

- **开发语言**：Python 3
- **GUI 框架**：PySide6 (Qt for Python)
- **图片处理**：Pillow (PIL)
- **PDF 处理**：PyMuPDF (fitz)
- **Windows API**：pywin32 (win32print, win32com)

## 安装依赖

1. 创建虚拟环境（可选）：
   ```bash
   python -m venv venv
   ```

2. 激活虚拟环境：
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - Linux/Mac:
     ```bash
     source venv/bin/activate
     ```

3. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

## 运行程序

```bash
python main.py
```

## 使用说明

1. **选择打印机**：在顶部控制区选择要使用的打印机
2. **添加文件**：
   - 方法一：拖拽文件或文件夹到中间区域的拖拽区
   - 方法二：TODO（添加文件选择对话框）
3. **调整设置**：
   - 全局设置：勾选"双面打印"或"统一黑白"应用到所有任务
   - 单个任务设置：点击任务行末的"⚙️"按钮，调整该任务的打印参数
4. **开始打印**：点击底部"开始批量打印"按钮

## 注意事项

1. **PDF 打印**：需要安装 SumatraPDF 或 Ghostscript
   - SumatraPDF 下载：https://www.sumatrapdfreader.org/download-free-pdf-viewer.html
   - Ghostscript 下载：https://www.ghostscript.com/releases/gsdnld.html

2. **Word 打印**：需要安装 Microsoft Office Word

3. **图片打印**：使用 Windows 系统命令打印，确保系统关联了图片查看器

## 项目结构

```
BatchPrintPro/
├── main.py                 # 应用程序入口
├── requirements.txt        # 依赖清单
├── README.md              # 项目说明
├── src/
│   ├── models/           # Model层 - 数据模型
│   │   ├── print_task.py # PrintTask数据模型
│   │   └── task_list.py # PrintTaskList管理类
│   ├── views/            # View层 - UI界面
│   │   ├── main_window.py    # 主窗口
│   │   ├── drop_zone.py      # 拖拽区域组件
│   │   ├── task_list_widget.py # 任务列表组件
│   │   └── print_settings_dialog.py # 打印设置对话框
│   ├── viewmodels/       # ViewModel层 - 业务逻辑
│   │   └── print_viewmodel.py # 打印视图模型
│   └── services/        # Service层 - 核心服务
│       ├── file_scanner.py      # 文件扫描服务
│       ├── layout_analyzer.py   # 版式分析引擎
│       ├── print_adapter.py     # 打印适配器基类
│       ├── image_adapter.py     # 图片打印适配器
│       ├── pdf_adapter.py      # PDF打印适配器
│       ├── word_adapter.py     # Word打印适配器
│       └── printer_manager.py  # 打印机管理
└── venv/                    # 虚拟环境（创建后）
```

## 打包为可执行文件

### 使用 PyInstaller

```bash
# 安装 PyInstaller
pip install pyinstaller

# 打包命令
pyinstaller --name BatchPrintPro \
            --windowed \
            --onefile \
            --icon=resources/icons/app_icon.ico \
            --add-data "resources;resources" \
            main.py
```

### 使用 Nuitka

```bash
# 安装 Nuitka
pip install nuitka

# 打包命令
python -m nuitka --standalone \
                 --windows-disable-console \
                 --windows-icon-from-ico=resources/icons/app_icon.ico \
                 --output-filename=BatchPrintPro.exe \
                 main.py
```

## 常见问题

1. **程序无法启动，提示"导入错误"**：
   - 请确保已安装所有依赖：`pip install -r requirements.txt`

2. **无法打印 PDF 文件**：
   - 请确保已安装 SumatraPDF 或 Ghostscript，并且它们在系统 PATH 中

3. **无法打印 Word 文件**：
   - 请确保已安装 Microsoft Office Word

4. **拖拽文件没有反应**：
   - 请确保拖拽的是支持的文件格式

## 许可证

TODO（添加许可证）

## 贡献

TODO（添加贡献指南）

## 更新日志

- **v1.0.0** (2026-05-24): 初始版本
  - 实现基本功能：文件拖拽、打印队列管理、打印参数设置
  - 支持图片、PDF、Word 文件打印
  - 实现自动横纵向适配
  - 实现异步打印，界面不卡顿
