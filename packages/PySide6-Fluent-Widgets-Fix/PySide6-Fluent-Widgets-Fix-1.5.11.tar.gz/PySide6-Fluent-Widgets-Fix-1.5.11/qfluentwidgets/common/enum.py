from PySide6.QtCore import Qt, QEvent, QPropertyAnimation, QFile
from PySide6.QtGui import QPainter, QPalette


# Fix memory leak
class QtEnum:
    class Qt:
        NoPen = Qt.NoPen
        white = Qt.white
        black = Qt.black
        AlignCenter = Qt.AlignCenter
        ForegroundRole = Qt.ForegroundRole
        CheckStateRole = Qt.CheckStateRole

    class QPalette:
        Text = QPalette.Text
        HighlightedText = QPalette.HighlightedText

    class QPropertyAnimation:
        Running = QPropertyAnimation.Running

    class QPainter:
        Antialiasing = QPainter.Antialiasing
        TextAntialiasing = QPainter.TextAntialiasing
        SmoothPixmapTransform = QPainter.SmoothPixmapTransform

    class QFile:
        ReadOnly = QFile.ReadOnly

    class QEvent:
        WindowStateChange = QEvent.WindowStateChange
        Resize = QEvent.Resize
        MouseButtonPress = QEvent.MouseButtonPress
        MouseButtonRelease = QEvent.MouseButtonRelease
        Enter = QEvent.Enter
        Leave = QEvent.Leave
        Wheel = QEvent.Wheel

        class Type:
            EnabledChange = QEvent.Type.EnabledChange
            Enter = QEvent.Type.Enter
            Leave = QEvent.Type.Leave
            MouseButtonPress = QEvent.Type.MouseButtonPress
