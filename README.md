# BatchPrint Pro

A desktop application for batch printing documents with a Model-View-ViewModel (MVVM) architecture, designed for efficient document processing workflows.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Usage](#usage)
- [Technical Specifications](#technical-specifications)
- [Dependencies](#dependencies)
- [Building from Source](#building-from-source)
- [Contributing](#contributing)
- [License](#license)

## Overview

BatchPrint Pro is a cross-format document printing utility that enables users to process multiple documents sequentially through a graphical interface. The application supports common office document formats including PDF, Microsoft Word (`.docx`), and image files (`.jpg`, `.png`, `.bmp`, `.tiff`).

The software implements an MVVM architectural pattern to separate concerns between data models, business logic, and user interface components. This design facilitates maintainability and extensibility for future development.

## Features

### Core Functionality

- **Multi-format Support**: Process PDF, Word, and image documents through a unified interface
- **Batch Processing**: Queue multiple documents for sequential printing
- **Print Preview**: Visual confirmation of documents before printing
- **Printer Selection**: Dynamic enumeration and selection of available printers
- **Print Settings**: Configurable page orientation (portrait/landscape) and page range selection
- **Task Management**: Add, remove, and reorder print tasks in the queue
- **Progress Tracking**: Real-time status updates during printing operations

### User Interface

- **Drag-and-Drop**: Add files to the print queue via drag-and-drop or file dialog
- **Task List**: Tabular display of queued documents with status indicators
- **Settings Dialog**: Modal configuration interface for print parameters
- **Splash Screen**: Application startup progress indication

## Architecture

The application follows the MVVM (Model-View-ViewModel) design pattern:

### Directory Structure

```
BatchPrintPro/
├── main.py                    # Application entry point
├── requirements.txt           # Python dependencies
├── src/
│   ├── models/              # Data models
│   │   ├── print_task.py    # Print task data structure
│   │   └── task_list.py     # Task list management
│   ├── services/            # Business logic layer
│   │   ├── file_scanner.py  # File system operations
│   │   ├── image_adapter.py # Image printing adapter
│   │   ├── layout_analyzer.py # Document layout analysis
│   │   ├── pdf_adapter.py   # PDF printing adapter
│   │   ├── print_adapter.py # Abstract print interface
│   │   ├── printer_manager.py # Printer enumeration and control
│   │   └── word_adapter.py  # Word document printing adapter
│   ├── viewmodels/          # Presentation logic
│   │   └── print_viewmodel.py # ViewModel coordinating models and views
│   └── views/              # User interface components
│       ├── drop_zone.py      # Drag-and-drop file acceptance
│       ├── main_window.py    # Primary application window
│       ├── print_settings_dialog.py # Print configuration dialog
│       ├── splash_progress.py # Startup progress indicator
│       └── task_list_widget.py # Task queue display widget
└── resources/              # Static assets
    ├── icon.ico             # Application icon
    └── splash.png           # Splash screen image
```

### Component Responsibilities

**Models** (`src/models/`):
- `PrintTask`: Encapsulates individual print job metadata (file path, status, settings)
- `TaskList`: Manages the collection of print tasks with add/remove/reorder operations

**Services** (`src/services/`):
- `FileScanner`: Validates file types and scans directories for printable documents
- `PrinterManager`: Enumerates system printers and manages printer handle lifecycle
- `PrintAdapter` (abstract): Defines the interface for format-specific printing implementations
- `PDFAdapter`: Implements PDF rendering and printing via PyMuPDF
- `WordAdapter`: Implements Word document printing via python-docx
- `ImageAdapter`: Implements image printing via Pillow and win32ui GDI
- `LayoutAnalyzer`: Analyzes document structure for optimal print layout

**ViewModels** (`src/viewmodels/`):
- `PrintViewModel`: Mediates between Models and Views, handling user actions and state transitions

**Views** (`src/views/`):
- `MainWindow`: Primary application window with menu bar and central widget
- `TaskListWidget`: QTableWidget subclass displaying the print queue
- `DropZone`: Custom widget accepting drag-and-drop file additions
- `PrintSettingsDialog`: QDialog for configuring print parameters
- `SplashProgress`: QSplashScreen subclass for startup progress indication

## Installation

### Prerequisites

- Python 3.13 or higher
- Windows operating system (printing functionality is Windows-specific due to `pywin32` dependency)

### Quick Start

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/BatchPrintPro.git
   cd BatchPrintPro
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   python main.py
   ```

## Usage

### Adding Documents

- Click "添加文件" (Add Files) to open a file dialog
- Alternatively, drag and drop files directly onto the application window
- Supported formats: `.pdf`, `.docx`, `.jpg`, `.jpeg`, `.png`, `.bmp`, `.tiff`

### Managing the Print Queue

- Select one or more tasks in the queue
- Right-click to remove selected tasks
- Use the "取消打印" (Cancel Print) button to remove tasks
- Tasks can be selected with left-click; multiple selection is supported

### Configuring Print Settings

- Select a task and click "打印设置" (Print Settings)
- Choose target printer from available system printers
- Select page orientation (Portrait or Landscape)
- Specify page range (All pages or custom range)

### Executing Print Jobs

- Click "开始打印" (Start Printing) to begin batch printing
- Monitor progress via the status bar and task list indicators
- The application processes tasks sequentially

## Technical Specifications

### Print Adapters

Each document format is handled by a dedicated adapter implementing the `PrintAdapter` interface:

| Format | Adapter Class | Backend Library | Printing Method |
|--------|--------------|------------------|-----------------|
| PDF    | `PDFAdapter` | PyMuPDF (fitz)  | `fitz.Rect` + `fitz.Pixmap` rendering to printer DC |
| Word   | `WordAdapter` | python-docx      | Renders via intermediate PDF conversion |
| Image  | `ImageAdapter` | Pillow + pywin32 | `win32ui` GDI `CreateDC` + `ImageWin.Dib` |

### Printer Management

The `PrinterManager` service wraps the Windows GDI print API via `pywin32`:

- `win32print.EnumPrinters()`: Enumerates available printers
- `win32print.OpenPrinter()`: Obtains printer handle
- `win32print.GetPrinter()`: Retrieves printer capabilities
- `win32ui.CreateDC()`: Creates device context for rendering

### Asynchronous Processing

Print operations execute in a separate thread to maintain UI responsiveness:

- `QThread` subclass for print job execution
- Signal-slot connections for progress updates
- Thread-safe task queue access via `QMutex`

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `PySide6` | 6.11.1 | GUI framework (Qt 6 bindings) |
| `Pillow` | ≥10.0.0 | Image processing |
| `PyMuPDF` (fitz) | ≥1.23.0 | PDF rendering |
| `python-docx` | ≥0.8.11 | Word document parsing |
| `pywin32` | ≥306 | Windows GDI/printing API |
| `watchdog` | ≥4.0.0 | (Optional) File system monitoring |

## Building from Source

### Creating a Standalone Executable

The application can be packaged as a standalone Windows executable using PyInstaller:

1. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```

2. Run the build script:
   ```bash
   python -m PyInstaller BatchPrintPro.spec
   ```

3. The executable will be generated in `dist/BatchPrintPro/`.

### Spec File Configuration

The `BatchPrintPro.spec` file contains the PyInstaller configuration:

```python
datas=[('splash.png', '.'), ('icon.ico', '.')],
hiddenimports=[
    'PySide6.QtCore', 'PySide6.QtGui', 'PySide6.QtWidgets',
    'PIL._imaging', 'fitz', 'win32print', 'win32api', 'docx'
],
icon='icon.ico'
```

## Contributing

Contributions are welcome. Please review the [architecture documentation](ARCHITECTURE.md) before submitting pull requests.

### Development Guidelines

1. Follow PEP 8 style guidelines
2. Maintain MVVM separation of concerns
3. Add unit tests for new functionality
4. Update documentation for API changes

### Reporting Issues

When reporting bugs, please include:
- Operating system version
- Python version
- Installed package versions (`pip freeze`)
- Steps to reproduce the issue
- Expected vs. actual behavior

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Qt framework by The Qt Company
- PySide6 bindings by Qt for Python team
- PyMuPDF for PDF rendering capabilities
- Pillow development team for image processing library

---

**Version**: 1.0.0  
**Last Updated**: May 2026  
**Maintainer**: BatchPrint Pro Contributors
