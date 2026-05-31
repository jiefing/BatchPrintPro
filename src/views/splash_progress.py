"""
启动进度窗口 - 带进度条动画的启动画面
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QProgressBar, QApplication
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt, QTimer, Signal


class SplashProgress(QWidget):
    """带进度条的启动画面"""

    closed = Signal()

    def __init__(self):
        super().__init__()
        self._progress = 0
        self._target_progress = 0
        self._init_ui()
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._update_progress)
        self._timer.start(30)

    def _init_ui(self):
        self.setWindowFlags(
            Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool
        )
        self.setFixedSize(500, 320)
        self.setStyleSheet("""
            QWidget {
                background-color: #1a1a2e;
                border-radius: 12px;
                border: 1px solid #333355;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(12)

        self.title = QLabel("BatchPrint Pro")
        self.title.setAlignment(Qt.AlignHCenter)
        self.title.setStyleSheet(
            "QLabel{color:#00d2ff;font-size:32px;"
            "font-weight:bold;font-family:'Microsoft YaHei';}"
        )
        layout.addWidget(self.title)

        self.subtitle = QLabel("批量打印工具")
        self.subtitle.setAlignment(Qt.AlignHCenter)
        self.subtitle.setStyleSheet(
            "QLabel{color:#aaaaaa;font-size:14px;"
            "font-family:'Microsoft YaHei';}"
        )
        layout.addWidget(self.subtitle)
        layout.addStretch()

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedHeight(8)
        self.progress_bar.setStyleSheet("""
            QProgressBar{background-color:#333355;border-radius:4px;border:none;}
            QProgressBar::chunk{background-color:#00d2ff;border-radius:4px;}
        """)
        layout.addWidget(self.progress_bar)

        self.status_label = QLabel("正在启动...")
        self.status_label.setAlignment(Qt.AlignHCenter)
        self.status_label.setStyleSheet(
            "QLabel{color:#888888;font-size:13px;"
            "font-family:'Microsoft YaHei';padding-top:8px;}"
        )
        layout.addWidget(self.status_label)
        self._center_on_screen()

    def _center_on_screen(self):
        screen = QApplication.primaryScreen().geometry()
        self.move(
            (screen.width() - self.width()) // 2,
            (screen.height() - self.height()) // 2,
        )

    def _update_progress(self):
        if self._progress < self._target_progress:
            self._progress = min(self._progress + 2, self._target_progress)
            self.progress_bar.setValue(int(self._progress))

    def set_progress(self, value: int, status: str = None):
        self._target_progress = max(0, min(100, value))
        if status:
            self.status_label.setText(status)
            _app = QApplication.instance()
            if _app:
                _app.processEvents()

    def finish(self, main_window):
        self._timer.stop()
        self.close()
        self.closed.emit()
