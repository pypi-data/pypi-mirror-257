from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QVBoxLayout, QTextEdit, QLineEdit, QCheckBox, QComboBox, QRadioButton, QProgressBar, QSlider
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWebEngineWidgets import QWebEngineView
import sys

class App:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.windows = []

    def newWindow(self, name, width, height):
        num_of_windows = len(self.windows)
        window = Window()
        self.windows.append(window)
        self.windows[num_of_windows].window.setWindowTitle(name)
        self.windows[num_of_windows].window.setGeometry(100, 100, width, height)
        self.windows[num_of_windows].window.show()
        return window
    
    def run(self):
        self.app.exec()

class Window:
    def __init__(self):
        self.window = QWidget()
        self.layout = QVBoxLayout()
        self.window.setLayout(self.layout)

    def setWindowTitle(self, name):
        self.window.setWindowTitle(name)
    
    def setIcon(self, icon):
        self.window.setWindowIcon(icon)

    def setGeometry(self, width, height):
        self.window.setGeometry(width, height)

    def setCoordinates(self, x, y):
        self.window.move(x, y)

    def addAttribute(self, attribute, stylesheet=""):
        self.window.setAttribute(attribute)
        self.window.setStyleSheet(stylesheet)

    def showElement(self, element):
        element.show(self)


class Elements:
    class Text:
        def __init__(self, text, font=QFont("Arial")):
            self.text = text
            self.qElement = QLabel(self.text)
            self.qElement.setFont(font)

        def __str__(self):
            return self.text

        def __repr__(self):
            return self.text

        def setGeometry(self, x, y, width, height):
            self.qElement.setGeometry(x,y,width, height)
            
        def move(self, x, y):
            self.qElement.move(x, y)

        def show(self, parent):
            parent.layout.addWidget(self.qElement)
        
        def changeText(self, text):
            self.qElement.setText(text)
        def destruct(self):
            self.qElement.deleteLater()

    class Button:
        def __init__(self, text, onPressed, font=QFont("Arial")):
            self.text = text
            self.qElement = QPushButton()
            self.qElement.setText(text)
            self.qElement.setFont(QFont(font))
            self.qElement.clicked.connect(onPressed)

        def __str__(self):
            return self.text

        def __repr__(self):
            return self.text

        def move(self, x, y):
            self.qElement.move(x, y)

        def setGeometry(self, x, y, width, height):
            self.qElement.setGeometry(x,y,width, height)

        def show(self, parent):
            parent.layout.addWidget(self.qElement)

        def destruct(self):
            self.qElement.deleteLater()

        def onPress(self, onPressed):
            self.qElement.clicked.connect(onPressed)

    class TextArea:
        def __init__(self, text, font=QFont("Arial"), richText=False):
            self.qElement = QTextEdit()
            self.qElement.setText(text)
            self.qElement.setFont(QFont(font))
            if richText:
                self.qElement.acceptRichText()

        def getText(self):
            return self.qElement.toPlainText()

        def setText(self, text):
            self.qElement.setText(text)

        def move(self, x, y):
            self.qElement.move(x, y)

        def show(self, parent):
            parent.layout.addWidget(self.qElement)

        def destruct(self):
            self.qElement.deleteLater()

        def setGeometry(self, x, y, width, height):
            self.qElement.setGeometry(x,y,width, height)
            
    class TextInput:
        def __init__(self, text, font=QFont("Arial")):
            self.qElement = QLineEdit()
            self.qElement.setText(text)
            self.qElement.setFont(QFont(font))

        def getText(self):
            return str(self.qElement.text())

        def setText(self, text):
            self.qElement.setText(text)

        def move(self, x, y):
            self.qElement.move(x, y)

        def show(self, parent):
            parent.layout.addWidget(self.qElement)

        def destruct(self):
            self.qElement.deleteLater()

        def setGeometry(self, x, y, width, height):
            self.qElement.setGeometry(x,y,width, height)
    
    class WebView:
        def __init__(self):
            self.qElement = QWebEngineView()

        def setHTML(self, html):
            self.qElement.setHtml(html)

        def move(self, x, y):
            self.qElement.move(x, y)

        def show(self, parent):
            parent.layout.addWidget(self.qElement)

        def destruct(self):
            self.qElement.deleteLater()

        def getHTML(self):
            return self.qElement.page().toHtml()

        def setURL(self, url):
            self.qElement.setUrl(QUrl(url))

        def setGeometry(self, x,y,width, height):
            self.qElement.setGeometry(x, y, width, height)

    class Image:
        def __init__(self, image):
            self.qElement = QLabel()
            self.qElement.setPixmap(QPixmap(image))

        def setGeometry(self, width, height):
            self.qElement.setGeometry(width, height)

        def move(self, x, y):
            self.qElement.move(x, y)

        def show(self, parent):
            parent.layout.addWidget(self.qElement)

        def destruct(self):
            self.qElement.deleteLater()
        def setGeometry(self, x, y, width, height):
            self.qElement.setGeometry(x, y, width, height)
        def changeImage(self, image):
            self.qElement.setPixmap(QPixmap(image))
    class Checkbox:
            def __init__(self, text, checked=False):
                self.qElement = QCheckBox(text)
                self.qElement.setChecked(checked)

            def move(self, x, y):
                self.qElement.move(x, y)

            def show(self, parent):
                parent.layout.addWidget(self.qElement)
            
            def destruct(self):
                self.qElement.deleteLater()
            def setGeometry(self, x, y, width, height):
                self.qElement.setGeometry(x, y, width, height)
            def isChecked(self):
                return self.qElement.isChecked()

    class RadioButton:
        def __init__(self, text, group=None, checked=False):
            self.qElement = QRadioButton(text)
            if group:
                group.addButton(self.qElement)
            self.qElement.setChecked(checked)

        def move(self, x, y):
            self.qElement.move(x, y)

        def show(self, parent):
            parent.layout.addWidget(self.qElement)
        def setGeometry(self, x, y, width, height):
            self.qElement.setGeometry(x, y, width, height)
        def isChecked(self):
            return self.qElement.isChecked()

    class ComboBox:
        def __init__(self, items):
            self.qElement = QComboBox()
            self.qElement.addItems(items)

        def move(self, x, y):
            self.qElement.move(x, y)

        def show(self, parent):
            parent.layout.addWidget(self.qElement)

        def currentIndex(self):
            return self.qElement.currentIndex()

        def currentText(self):
            return self.qElement.currentText()
        def setGeometry(self, x, y, width, height):
            self.qElement.setGeometry(x, y, width, height)
        def setCurrentIndex(self, index):
            self.qElement.setCurrentIndex(index)

    class Progressbar:
        def __init__(self, min_value=0, max_value=100):
            self.qElement = QProgressBar()
            self.qElement.setRange(min_value, max_value)

        def move(self, x, y):
            self.qElement.move(x, y)

        def show(self, parent):
            parent.layout.addWidget(self.qElement)
        def setGeometry(self, x, y, width, height):
            self.qElement.setGeometry(x, y, width, height)

        def setValue(self, value):
            self.qElement.setValue(value)

    class Slider:
        def __init__(self, min_value=0, max_value=100):
            self.qElement = QSlider(Qt.Horizontal)
            self.qElement.setRange(min_value, max_value)

        def move(self, x, y):
            self.qElement.move(x, y)

        def show(self, parent):
            parent.layout.addWidget(self.qElement)

        def value(self):
            return self.qElement.value()
        
        def setGeometry(self, x, y, width, height):
            self.qElement.setGeometry(x, y, width, height)

        def setValue(self, value):
            self.qElement.setValue(value)