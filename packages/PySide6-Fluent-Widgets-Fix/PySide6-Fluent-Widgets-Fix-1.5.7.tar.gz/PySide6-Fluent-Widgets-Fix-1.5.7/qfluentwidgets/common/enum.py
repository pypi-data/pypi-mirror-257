from PySide6.QtCore import Qt, QEvent
from PySide6.QtGui import QPainter


# Fix memory leak
class QtEnum:
    class Qt:
        NoPen = Qt.NoPen
        white = Qt.white
        AlignCenter = Qt.AlignCenter

    class QPainter:
        Antialiasing = QPainter.Antialiasing
        TextAntialiasing = QPainter.TextAntialiasing
        SmoothPixmapTransform = QPainter.SmoothPixmapTransform

    class QEvent:
        WindowStateChange = QEvent.WindowStateChange
        Resize = QEvent.Resize

