# from PyQt5.QtWidgets import (QApplication, QMainWindow, QTextEdit, QVBoxLayout, QStackedWidget, QHBoxLayout, QWidget, QFrame, QLabel, QLineEdit , QPushButton, QGridLayout, QSizePolicy)
# from PyQt5.QtGui import QIcon, QPainter, QMovie, QColor, QFont, QTextCharFormat, QTextBlockFormat, QPixmap
# from PyQt5.QtCore import Qt , QSize , QTimer
# from dotenv import dotenv_values
# import sys
# import os

# def get_scaled_size(screen_width, fraction, min_size=24, max_size=120):
#     return max(min_size, min(int(screen_width * fraction), max_size))
# # def safe_load_icon(path, width=60, height=60):
# #     if os.path.exists(path):
# #         pixmap = QPixmap(path)
# #         new_pixmap = pixmap.scaled(width, height)
# #         return new_pixmap
# #     else:
# #         print(f"Image missing: {path}")
# #         return QPixmap()
# def safe_load_icon(path, width=60, height=60):
#     print("Trying to load image:", path)
#     if os.path.exists(path):
#         pixmap = QPixmap(path)
#         if pixmap.isNull():
#             print(f"Loaded pixmap is null for {path}. Using blank pixmap instead.")
#             pixmap = QPixmap(width, height)
#             pixmap.fill(Qt.transparent)
#         else:
#             pixmap = pixmap.scaled(width, height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
#         return pixmap
#     else:
#         print(f"Image missing: {path}")
#         blank_pixmap = QPixmap(width, height)
#         blank_pixmap.fill(Qt.transparent)
#         return blank_pixmap



# env_vars = dotenv_values(".env")
# Assistantname = env_vars.get("Assistantname")
# current_dir = os.getcwd()
# old_chat_message = ""
# TempDirPath = rf"{current_dir}\Fronted\Files"
# GraphicsDirPath = rf"{current_dir}\Fronted\Graphics"


# def ensure_folder_exists(folder_path):
#     if not os.path.exists(folder_path):
#         os.makedirs(folder_path, exist_ok=True)

# def ensure_file_exists(filepath, default_text=""):
#     os.makedirs(os.path.dirname(filepath), exist_ok=True)
#     if not os.path.exists(filepath):
#         with open(filepath, "w", encoding="utf-8") as f:
#             f.write(default_text)

# os.makedirs(TempDirPath, exist_ok=True)
# os.makedirs(GraphicsDirPath, exist_ok=True)
# def AnswerModifier(Answer):
#     lines = Answer.split('\n')
#     non_empty_lines = [line for line in lines if line.strip()]
#     modified_answer = '\n'.join(non_empty_lines)
#     return modified_answer

# def QueryModifier(Query):
#     new_query = Query.lower().strip()
#     query_words = new_query.split()
#     question_words = ["how", "what", "who", "where", "when", "why", "which", "whose", "whom", "can you", "what's", "where's", "how's"]

#     if any(word + " " in new_query for word in question_words):
#         if query_words[-1][-1] in ['.', '?', '!']:
#             new_query = new_query[:-1] + "?"
#         else:
#             new_query += "?"
#     else:
#         if query_words[-1][-1] in ['.', '?', '!']:
#             new_query = new_query[:-1] + "."
#         else:
#             new_query += "."

#     return new_query.capitalize()

# def SetMicrophoneStatus(Command):
#     ensure_file_exists(TempDirectoryPath('Mic.data'))
#     with open(rf'{TempDirPath}\Mic.data', "w", encoding='utf-8') as file:
#         file.write(Command)

# def GetMicrophoneStatus():
#     ensure_file_exists(TempDirectoryPath('Mic.data'))
#     with open(rf'{TempDirPath}\Mic.data', "r", encoding='utf-8') as file:
#         Status = file.read()
#         return Status
    
# def SetAssistantStatus(Status):
#     ensure_file_exists(TempDirectoryPath('Status.data'))
#     with open(rf'{TempDirPath}\Status.data', "w", encoding='utf-8') as file:
#         file.write(Status)

# def GetAssistantStatus():
#     ensure_file_exists(TempDirectoryPath('Status.data'))

#     with open(rf'{TempDirPath}\Status.data', "r" , encoding= 'utf-8') as file:
#       Status = file.read()
#     return Status

# def MicButtonInitialed():
#     SetMicrophoneStatus("False")

# def MicButtonClosed():
#     SetMicrophoneStatus("True")

# def GraphicsDirectoryPath(Filename):
#     Path = rf'{GraphicsDirPath}\{Filename}'
#     return Path

# def TempDirectoryPath(Filename):
#     Path = rf'{TempDirPath}\{Filename}'
#     return Path

# def ShowTextToScreen(Text):
#     ensure_file_exists(TempDirectoryPath('Responses.data'))
#     with open(rf'{TempDirPath}\Responses.data', "w", encoding='utf-8') as file:
#         file.write(Text)

# class ChatSection(QWidget):
#     def loadMessages(self):

#         global old_chat_message
#         ensure_file_exists(TempDirectoryPath('Responses.data'))

#         with open(TempDirectoryPath('Responses.data'), "r", encoding='utf-8') as file:
#             messages = file.read()

#         if None == messages:
#             pass

#         elif len(messages) <= 1:
#             pass

#         elif str(old_chat_message) == str(messages):
#             pass

#         else:
#             self.addMessage(message=messages, color='white')
#             old_chat_message = messages

#     def SpeechRecogText(self):
#         ensure_file_exists(TempDirectoryPath('Status.data'))

#         with open(TempDirectoryPath('Status.data'), "r", encoding='utf-8') as file:
#             messages = file.read()
#             self.label.setText(messages)
    
#     def load_icon(self, path, width=60, height=60):
#         # pixmap = QPixmap(path)
#         # new_pixmap = pixmap.scaled(width, height)
#         # self.icon_label.setPixmap(new_pixmap)
#         new_pixmap = safe_load_icon(path, width, height)
#         self.icon_label.setPixmap(new_pixmap)

    
#     def toggle_icon(self, event=None):
#         if self.toggled:
#             self.load_icon(GraphicsDirectoryPath('voice.jpg'), 60, 60)
#             MicButtonInitialed()
    
#         else:
#             self.load_icon(GraphicsDirectoryPath('Mic.jpg'), 60, 60)
#             MicButtonClosed()
    
#         self.toggled = not self.toggled

#     def addMessage(self, message, color):
#         cursor = self.chat_text_edit.textCursor()
#         format = QTextCharFormat()
#         formatm = QTextBlockFormat()
#         formatm.setTopMargin(10)
#         formatm.setLeftMargin(10)
#         format.setForeground(QColor(color))
#         cursor.setCharFormat(format)
#         cursor.setBlockFormat(formatm)
#         cursor.insertText(message + "\n")
#         self.chat_text_edit.setTextCursor(cursor)
        
#     def __init__(self):
#         super(ChatSection, self).__init__()
#         layout = QVBoxLayout(self)
#         # layout.setContentsMargins(-10, 40, 40, 100)
#         # layout.setSpacing(-100)
#         desktop = QApplication.desktop()                     # <<< Yeh add karo start mein
#         screen_width = desktop.screenGeometry().width()      # <<< Yeh add karo start mein
#         screen_height = desktop.screenGeometry().height()   
#         layout.setContentsMargins(0, 0, 0, get_scaled_size(screen_height, 0.07, 30, 120))
#         layout.setSpacing(get_scaled_size(screen_height, 0.02, 8, 24))
#         self.chat_text_edit = QTextEdit()
#         self.chat_text_edit.setReadOnly(True)
#         self.chat_text_edit.setTextInteractionFlags(Qt.NoTextInteraction)  # No text interaction
#         self.chat_text_edit.setFrameStyle(QFrame.NoFrame)
#         layout.addWidget(self.chat_text_edit)
#         self.setStyleSheet("background-color: black;")
#         layout.setSizeConstraint(QVBoxLayout.SetDefaultConstraint)
#         layout.setStretch(1, 1)
#         self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
#         text_color = QColor(Qt.blue)
#         text_color_text = QTextCharFormat()
#         text_color_text.setForeground(text_color)
#         self.chat_text_edit.setCurrentCharFormat(text_color_text)
#         self.gif_label = QLabel()
#         self.gif_label.setStyleSheet("border: none;")
#         movie = QMovie(GraphicsDirectoryPath('Jarvis.gif'))
#         max_gif_size_W = 550
#         max_gif_size_H = 360   #  yaha change karna 
#         movie.setScaledSize(QSize(max_gif_size_W, max_gif_size_H))
#         self.gif_label.setAlignment(Qt.AlignRight | Qt.AlignBottom)
#         self.gif_label.setMovie(movie)
#         movie.start()
#         layout.addWidget(self.gif_label)
#         self.label = QLabel("")
#         self.label.setStyleSheet("""color: cyan; font-size:22px;margin-right: 195px; border: none; margin-top: -30px;""")   # yaha bhi dekhna 
#         self.label.setAlignment(Qt.AlignRight)
#         layout.addWidget(self.label)
#         # layout.setSpacing(1)
#         layout.setSpacing(-10)
#         layout.addWidget(self.gif_label)

#         # font = QFont()
#         # font.setPointSize(13)
#         # self.chat_text_edit.setFont(font)
#         font = QFont()
#         font.setPointSize(get_scaled_size(screen_height, 0.022, 10, 22))
#         self.chat_text_edit.setFont(font)

#         font_size = get_scaled_size(screen_height, 0.025, 12, 28)
#         self.label.setStyleSheet(f"color: cyan; font-size:{font_size}px ; margin-bottom:0;")


#         self.timer = QTimer(self)
#         self.timer.timeout.connect(self.loadMessages)
#         self.timer.timeout.connect(self.SpeechRecogText)
#         self.timer.start(5)
#         self.chat_text_edit.viewport().installEventFilter(self)
#         self.setStyleSheet("""
#                 QScrollBar:vertical {
#                     border: none;
#                     background: black;
#                     width: 10px;
#                     margin: 0px 0px 0px 0px;
#                 }
                
#                 QScrollBar::handle:vertical {
#                     background: white;
#                     min-height: 20px;
#                 }
                
#                 QScrollBar::add-line:vertical {
#                     background: black;
#                      subcontrol-position: bottom;
#                      subcontrol-origin: margin;
#                      height: 10px;
#                  }
                           
#                  QScrollBar::sub-line:vertical {
#                     background: black;
#                      subcontrol-position: top;
#                      subcontrol-origin: margin;
#                      height: 10px;
#                  }
                 
                 
#                  QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
#                      border: none;
#                      background: none;
#                      color: none;
#                  }
                 
#                  QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
#                      background: none;  
#                  }
#             """)


# class InitialScreen(QWidget):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         desktop = QApplication.desktop()
#         screen_width = desktop.screenGeometry().width()
#         screen_height = desktop.screenGeometry().height()
#         content_layout = QVBoxLayout()
#         # content_layout.setContentsMargins(0, 0, 0, 0)
#         # content_layout.setSpacing(20)
#         content_layout.setContentsMargins(0, 0, 0, get_scaled_size(screen_height, 0.07, 30, 120))
#         content_layout.setSpacing(get_scaled_size(screen_height, 0.015, 8, 24))
#         gif_label = QLabel()
#         movie = QMovie(GraphicsDirectoryPath('Jarvis.gif'))
#         gif_label.setMovie(movie)
#         #max_gif_size_H = int(screen_width / 16*9 )
#         # gif_width = 1000
#         # gif_height = 700
#         # Example: InitialScreen __init__ mein (GIF size)
#         gif_width = get_scaled_size(screen_width, 0.45, 300, 650)
#         gif_height = get_scaled_size(screen_height, 0.4, 200, 450)
#         movie.setScaledSize(QSize(gif_width,gif_height))
#         gif_label.setAlignment(Qt.AlignCenter)
#         movie.start()
#         self.icon_label = QLabel()
#         # pixmap = QPixmap(GraphicsDirectoryPath('Mic_on.jpg'))
#         # new_pixmap = pixmap.scaled(60, 60)
#         # self.icon_label.setPixmap(new_pixmap)
#         # self.icon_label.setFixedSize(150,150)
#         mic_icon_size = get_scaled_size(screen_width, 0.08, 60, 120)
#         pixmap = QPixmap(GraphicsDirectoryPath('Mic_on.jpg'))
#         new_pixmap = pixmap.scaled(mic_icon_size, mic_icon_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
#         self.icon_label.setPixmap(new_pixmap)
#         self.icon_label.setFixedSize(mic_icon_size, mic_icon_size)
#         self.icon_label.setAlignment(Qt.AlignCenter)
#         self.toggled = True
#         self.toggle_icon()
#         self.icon_label.mousePressEvent = self.toggle_icon
#         self.label = QLabel("")
#         self.label.setStyleSheet("color: cyan; font-size:22px ; margin-bottom:0;")
#         #content_layout.addWidget(gif_label, alignment=Qt.AlignCenter)
#         #content_layout.addWidget(self.label, alignment=Qt.AlignCenter)
#         #content_layout.addWidget(self.icon_label, alignment=Qt.AlignCenter)
#         #content_layout.setContentsMargins(0, 0, 0, 150)
#         content_layout.addStretch(1)                      # Push down from top
#         content_layout.addWidget(gif_label, 0, Qt.AlignCenter)
#         content_layout.addSpacing(5)
#         content_layout.addWidget(self.label, 0, Qt.AlignCenter)
#         content_layout.addSpacing(5)
#         content_layout.addWidget(self.icon_label, 0, Qt.AlignCenter)
#         content_layout.addStretch(1)
#         self.setLayout(content_layout)
#         self.setFixedHeight(screen_height)
#         self.setFixedWidth(screen_width)
#         self.setStyleSheet("background-color: black;")
#         self.timer = QTimer(self)
#         self.timer.timeout.connect(self.SpeechRecogText)
#         self.timer.start(5)

#     def SpeechRecogText(self):
#         with open(TempDirectoryPath('Status.data'), "r", encoding='utf-8') as file:
#             messages = file.read()
#             self.label.setText(messages)
    
#     # def load_icon(self, path, width=60, height=60):
#     #     pixmap = QPixmap(path)
#     #     new_pixmap = pixmap.scaled(width, height)
#     #     self.icon_label.setPixmap(new_pixmap)
#     def load_icon(self, path, width=60, height=60):
#         new_pixmap = safe_load_icon(path, width, height)
#         self.icon_label.setPixmap(new_pixmap)

    
#     def toggle_icon(self, event=None):
             
#         if self.toggled:
#              self.load_icon(GraphicsDirectoryPath('Mic_on.jpg'), 60, 60)
#              MicButtonInitialed()    
#         else:
#             self.load_icon(GraphicsDirectoryPath('Mic_off.jpg'), 60, 60)
#             MicButtonClosed()    

#         self.toggled = not self.toggled

# class MessageScreen(QWidget):

#     def __init__(self, parent=None):
#         super().__init__(parent)
#         desktop = QApplication.desktop()
#         screen_width = desktop.screenGeometry().width()
#         screen_height = desktop.screenGeometry().height()
#         layout = QVBoxLayout()
#         label = QLabel("")
#         layout.addWidget(label)
#         chat_section = ChatSection()
#         layout.addWidget(chat_section)
#         self.setLayout(layout)
#         self.setStyleSheet("background-color: black;")
#         self.setFixedHeight(screen_height)
#         self.setFixedWidth(screen_width)


# class CustomTopBar(QWidget):

#     def __init__(self, parent, stacked_widget):
#         super().__init__(parent)
#         self.initUI()
#         self.current_screen = None
#         self.stacked_widget = stacked_widget

#     def initUI(self):
#         desktop = QApplication.desktop()                     # <<< Yeh add karo start mein
#         screen_width = desktop.screenGeometry().width()      # <<< Yeh add karo start mein
#         screen_height = desktop.screenGeometry().height()

#         topbar_icon_size = get_scaled_size(screen_width, 0.03, 28, 40)  # place after screen_width initialization


#         self.setFixedHeight(50)  
#         layout = QHBoxLayout(self)
#         layout.setAlignment(Qt.AlignRight)
#         home_button = QPushButton()
#         home_icon = QIcon(GraphicsDirectoryPath("Home.jpg"))
#         home_button.setIcon(home_icon)
#         home_button.setIconSize(QSize(topbar_icon_size, topbar_icon_size))
#         home_button.setText("  Home")
#         home_button.setStyleSheet("height:40px; line-height:40px ; background-color:white ; color: black")

#         message_button = QPushButton()
#         message_icon = QIcon(GraphicsDirectoryPath("Chats.jpg"))
#         message_button.setIcon(message_icon)
#         message_button.setIconSize(QSize(topbar_icon_size, topbar_icon_size))
#         message_button.setText("  Chat")
#         message_button.setStyleSheet("height:40px; line-height:40px; background-color:white ; color: black")

#         minimize_button = QPushButton()
#         minimize_icon = QIcon(GraphicsDirectoryPath("Minimize2.jpg"))
#         minimize_button.setIcon(minimize_icon)
#         minimize_button.setIconSize(QSize(topbar_icon_size, topbar_icon_size))
#         minimize_button.setStyleSheet("background-color:white")
#         minimize_button.clicked.connect(self.minimizeWindow)

#         self.maximize_button = QPushButton()
#         self.maximize_icon = QIcon(GraphicsDirectoryPath('Maximize.jpg'))
#         self.restore_icon = QIcon(GraphicsDirectoryPath('Minimize.jpg'))
#         self.maximize_button.setIcon(self.maximize_icon)
#         self.maximize_button.setIconSize(QSize(topbar_icon_size, topbar_icon_size))
#         self.maximize_button.setFlat(True)
#         self.maximize_button.setStyleSheet("background-color:white")
#         self.maximize_button.clicked.connect(self.maximizeWindow)

#         close_button = QPushButton()
#         close_icon = QIcon(GraphicsDirectoryPath('Close.jpg'))
#         close_button.setIcon(close_icon)
#         close_button.setIconSize(QSize(topbar_icon_size, topbar_icon_size))
#         close_button.setStyleSheet("background-color:white")
#         close_button.clicked.connect(self.closeWindow)

#         line_frame = QFrame()
#         line_frame.setFixedHeight(1)
#         line_frame.setFrameShape(QFrame.HLine)
#         line_frame.setFrameShadow(QFrame.Sunken)
#         line_frame.setStyleSheet("border-color: black;")
#         #title_label = QLabel(f"{str(Assistantname).capitalize()} AI  ")
#         title_label = QLabel("Assistant AI  ")
#         title_label.setStyleSheet("color: black; font-size: 18px ; background-color:white")
#         home_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
#         message_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
#         layout.addWidget(title_label)
#         layout.addStretch(1)
#         layout.addWidget(home_button)
#         layout.addWidget(message_button)
#         layout.addStretch(1)
#         layout.addWidget(minimize_button)
#         layout.addWidget(self.maximize_button)
#         layout.addWidget(close_button)
#         layout.addWidget(line_frame)
#         self.draggable = True
#         self.offset = None

#     def paintEvent(self, event):
#         painter = QPainter(self)
#         painter.fillRect(self.rect(), Qt.white)
#         super().paintEvent(event)

#     def minimizeWindow(self):
#         self.parent().showMinimized()

#     def maximizeWindow(self):
#         if self.parent().isMaximized():
#             self.parent().showNormal()
#             self.maximize_button.setIcon(self.maximize_icon)
#         else:
#             self.parent().showMaximized()
#             self.maximize_button.setIcon(self.restore_icon)

#     def closeWindow(self):
#         self.parent().close()

#     def mousePressEvent(self, event):
#         if self.draggable:
#             self.offset = event.pos()

#     def mouseMoveEvent(self, event):
#         if self.draggable and self.offset:
#             new_pos = event.globalPos() - self.offset
#             self.parent().move(new_pos)


#     def showMessageScreen(self):
#         if self.current_screen is not None:
#             self.current_screen.hide()

#         message_screen = MessageScreen(self)
#         layout = self.parent().layout()
#         if layout is not None:
#             layout.addWidget(message_screen)
#         self.current_screen = message_screen

#     def showInitialScreen(self):
#         if self.current_screen is not None:
#             self.current_screen.hide()

#         initial_screen = InitialScreen(self)
#         layout = self.parent().layout()
#         if layout is not None:
#             layout.addWidget(initial_screen)
#         self.current_screen = initial_screen


# class MainWindow(QMainWindow):

#     def __init__(self):
#         super().__init__()
#         self.setWindowFlags(Qt.FramelessWindowHint)
#         self.initUI()

#     def initUI(self):
#         desktop = QApplication.desktop()
#         screen_width = desktop.screenGeometry().width()
#         screen_height = desktop.screenGeometry().height()


    
#         stacked_widget = QStackedWidget(self)
#         initial_screen = InitialScreen()
#         message_screen = MessageScreen()
#         stacked_widget.addWidget(initial_screen)
#         stacked_widget.addWidget(message_screen)
#         self.setGeometry(0, 0, screen_width, screen_height)
#         self.setStyleSheet("background-color: black;")
#         top_bar = CustomTopBar(self, stacked_widget)
#         self.setMenuWidget(top_bar)
#         self.setCentralWidget(stacked_widget)


# def GraphicalUserInterface():
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec_())


# if __name__ == "__main__":
    
  


#     ensure_folder_exists(TempDirPath)
#     ensure_file_exists(TempDirectoryPath('Status.data'))
#     ensure_file_exists(TempDirectoryPath('Mic.data'))
#     ensure_file_exists(TempDirectoryPath('Responses.data'))

#     GraphicalUserInterface()

from PyQt5.QtWidgets import (QApplication, QMainWindow, QTextEdit, QVBoxLayout, QStackedWidget, QHBoxLayout,
                             QWidget, QFrame, QLabel, QPushButton, QSizePolicy)
from PyQt5.QtGui import QIcon, QPainter, QMovie, QColor, QFont, QTextCharFormat, QTextBlockFormat, QPixmap
from PyQt5.QtCore import Qt, QSize, QTimer
from dotenv import dotenv_values
import sys
import os

# ------------------- High DPI + Utility Scaling -------------------
# (ye attributes QApplication banne se pehle lagte hain)
QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

def _get_screen_metrics():
    # safer than deprecated QApplication.desktop()
    app = QApplication.instance()
    screen = app.primaryScreen()
    size = screen.size()
    w, h = size.width(), size.height()
    # 14-inch laptops commonly 1366x768 or 1920x1080
    # base ko 1920x1080 maana, scale = min(w/1920, h/1080)
    scale = min(w / 1920.0, h / 1080.0)
    # clamp taaki bahut chhote/bohot bade screens par bhi theek lage
    scale = max(0.75, min(1.25, scale))
    return w, h, scale

def dp(px):
    # device independent pixels
    _, _, s = _get_screen_metrics()
    return max(1, int(px * s))

def get_scaled_size(screen_width, fraction, min_size=24, max_size=120):
    # tumhara original helper; min/max ko dp se pass karo
    return max(dp(min_size), min(int(screen_width * fraction), dp(max_size)))

# ------------------- Safe Image Loader -------------------
def safe_load_icon(path, width=60, height=60):
    print("Trying to load image:", path)
    if os.path.exists(path):
        pixmap = QPixmap(path)
        if pixmap.isNull():
            print(f"Loaded pixmap is null for {path}. Using blank pixmap instead.")
            pixmap = QPixmap(width, height)
            pixmap.fill(Qt.transparent)
        else:
            pixmap = pixmap.scaled(width, height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        return pixmap
    else:
        print(f"Image missing: {path}")
        blank_pixmap = QPixmap(width, height)
        blank_pixmap.fill(Qt.transparent)
        return blank_pixmap

# ------------------- Paths / Env -------------------
env_vars = dotenv_values(".env")
Assistantname = env_vars.get("Assistantname")
current_dir = os.getcwd()
old_chat_message = ""
# TempDirPath = rf"{current_dir}\Fronted\Files"
# GraphicsDirPath = rf"{current_dir}\Fronted\Graphics"
TempDirPath = r"C:\Users\hites\OneDrive\Desktop\Voice Assistent\Frontend\Fronted\Files"
GraphicsDirPath = r"C:\Users\hites\OneDrive\Desktop\Voice Assistent\Frontend\Fronted\Graphics"


def ensure_folder_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path, exist_ok=True)

def ensure_file_exists(filepath, default_text=""):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    if not os.path.exists(filepath):
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(default_text)

os.makedirs(TempDirPath, exist_ok=True)
os.makedirs(GraphicsDirPath, exist_ok=True)

def AnswerModifier(Answer):
    lines = Answer.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    modified_answer = '\n'.join(non_empty_lines)
    return modified_answer

def QueryModifier(Query):
    new_query = Query.lower().strip()
    query_words = new_query.split()
    question_words = ["how", "what", "who", "where", "when", "why", "which", "whose", "whom", "can you",
                      "what's", "where's", "how's"]

    if any(word + " " in new_query for word in question_words):
        if query_words[-1][-1] in ['.', '?', '!']:
            new_query = new_query[:-1] + "?"
        else:
            new_query += "?"
    else:
        if query_words[-1][-1] in ['.', '?', '!']:
            new_query = new_query[:-1] + "."
        else:
            new_query += "."

    return new_query.capitalize()

def GraphicsDirectoryPath(Filename):
    Path = rf'{GraphicsDirPath}\{Filename}'
    return Path

def TempDirectoryPath(Filename):
    Path = rf'{TempDirPath}\{Filename}'
    return Path

def SetMicrophoneStatus(Command):
    ensure_file_exists(TempDirectoryPath('Mic.data'))
    with open(rf'{TempDirPath}\Mic.data', "w", encoding='utf-8') as file:
        file.write(Command)

def GetMicrophoneStatus():
    ensure_file_exists(TempDirectoryPath('Mic.data'))
    with open(rf'{TempDirPath}\Mic.data', "r", encoding='utf-8') as file:
        Status = file.read()
        return Status

def SetAssistantStatus(Status):
    ensure_file_exists(TempDirectoryPath('Status.data'))
    with open(rf'{TempDirPath}\Status.data', "w", encoding='utf-8') as file:
        file.write(Status)

def GetAssistantStatus():
    ensure_file_exists(TempDirectoryPath('Status.data'))
    with open(rf'{TempDirPath}\Status.data', "r", encoding='utf-8') as file:
        Status = file.read()
    return Status

def MicButtonInitialed():
    SetMicrophoneStatus("False")

def MicButtonClosed():
    SetMicrophoneStatus("True")

def ShowTextToScreen(Text):
    ensure_file_exists(TempDirectoryPath('Responses.data'))
    with open(rf'{TempDirPath}\Responses.data', "w", encoding='utf-8') as file:
        file.write(Text)

# ------------------- Widgets -------------------
class ChatSection(QWidget):
    def loadMessages(self):
        global old_chat_message
        ensure_file_exists(TempDirectoryPath('Responses.data'))
        with open(TempDirectoryPath('Responses.data'), "r", encoding='utf-8') as file:
            messages = file.read()

        if not messages:
            return
        if len(messages) <= 1:
            return
        if str(old_chat_message) == str(messages):
            return

        self.addMessage(message=messages, color='white')
        old_chat_message = messages

    def SpeechRecogText(self):
        ensure_file_exists(TempDirectoryPath('Status.data'))
        with open(TempDirectoryPath('Status.data'), "r", encoding='utf-8') as file:
            messages = file.read()
            self.label.setText(messages)

    def load_icon(self, path, width=60, height=60):
        new_pixmap = safe_load_icon(path, width, height)
        self.icon_label.setPixmap(new_pixmap)

    def toggle_icon(self, event=None):
        if self.toggled:
            self.load_icon(GraphicsDirectoryPath('voice.png'), dp(60), dp(60))
            MicButtonInitialed()
        else:
            self.load_icon(GraphicsDirectoryPath('Mic.png'), dp(60), dp(60))
            MicButtonClosed()
        self.toggled = not self.toggled

    def addMessage(self, message, color):
        cursor = self.chat_text_edit.textCursor()
        format = QTextCharFormat()
        formatm = QTextBlockFormat()
        formatm.setTopMargin(dp(10))
        formatm.setLeftMargin(dp(10))
        format.setForeground(QColor(color))
        cursor.setCharFormat(format)
        cursor.setBlockFormat(formatm)
        cursor.insertText(message + "\n")
        self.chat_text_edit.setTextCursor(cursor)

    def __init__(self):
        super(ChatSection, self).__init__()
        layout = QVBoxLayout(self)
        w, h, _ = _get_screen_metrics()

        # margins & spacing responsive
        layout.setContentsMargins(dp(0), dp(0), dp(0), get_scaled_size(h, 0.07, 30, 120))
        layout.setSpacing(get_scaled_size(h, 0.02, 8, 24))

        self.chat_text_edit = QTextEdit()
        self.chat_text_edit.setReadOnly(True)
        self.chat_text_edit.setTextInteractionFlags(Qt.NoTextInteraction)
        self.chat_text_edit.setFrameStyle(QFrame.NoFrame)
        self.chat_text_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # font responsive
        font = QFont()
        font.setPointSize(max(10, dp(12)))
        self.chat_text_edit.setFont(font)

        layout.addWidget(self.chat_text_edit, 1)

        # # GIF (no fixed sizes; scaled)
        # self.gif_label = QLabel()
        # self.gif_label.setStyleSheet("border: none;")
        # movie = QMovie(GraphicsDirectoryPath('Jarvis.gif'))
        # max_gif_size_W = dp(550)
        # max_gif_size_H = dp(360)
        # movie.setScaledSize(QSize(max_gif_size_W, max_gif_size_H))
        # self.gif_label.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        # self.gif_label.setMovie(movie)
        # movie.start()
        # layout.addWidget(self.gif_label, 0, Qt.AlignRight | Qt.AlignBottom)

        # self.label = QLabel("")
       

  

        # 1) GIF
        self.gif_label = QLabel()
        movie = QMovie(GraphicsDirectoryPath('Jarvis.gif'))
        movie.setScaledSize(QSize(550, 375))   # tumhara GIF size
        self.gif_label.setMovie(movie)
        movie.start()

        gif_w = movie.scaledSize().width()     # GIF width
        self.gif_label.setFixedWidth(gif_w)
        self.gif_label.setAlignment(Qt.AlignCenter)

        # 2) LISTENING label (GIF ke exactly neeche center)
        self.label = QLabel("")
        self.label.setText("")                 # runtime me update hota h
        self.label.setStyleSheet("color: cyan; font-size:18px;")
        self.label.setAlignment(Qt.AlignCenter)

        # same width as GIF so always center exactly below it
        self.label.setFixedWidth(gif_w)

        # 3) Vertical container (GIF upar, Listening neeche)
        self.media_container = QWidget()
        v = QVBoxLayout(self.media_container)
        v.setContentsMargins(0, 0, 0, 0)
        v.setSpacing(5)

        v.addWidget(self.gif_label, 0, Qt.AlignCenter)
        v.addWidget(self.label, 0, Qt.AlignCenter)

        # 4) Ye container ko ChatSection ke bottom-right me laga do
        layout.addWidget(self.media_container, 0, Qt.AlignBottom | Qt.AlignRight)


        # Event filter + Scrollbar style
        self.chat_text_edit.viewport().installEventFilter(self)
        self.setStyleSheet("""
            QWidget { background-color: black; }
            QScrollBar:vertical { border: none; background: black; width: 10px; margin: 0; }
            QScrollBar::handle:vertical { background: white; min-height: 20px; }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { background: black; height: 10px; }
            QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical { border: none; background: none; color: none; }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: none; }
        """)

        # Icon (optional use)
        self.icon_label = QLabel()
        self.toggled = True

        # Timer throttled (100ms instead of 5ms)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.loadMessages)
        self.timer.timeout.connect(self.SpeechRecogText)
        self.timer.start(100)

class InitialScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        w, h, _ = _get_screen_metrics()
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(dp(0), dp(0), dp(0), get_scaled_size(h, 0.07, 30, 120))
        content_layout.setSpacing(get_scaled_size(h, 0.015, 8, 24))

        gif_label = QLabel()
        movie = QMovie(GraphicsDirectoryPath('Jarvis.gif'))
        gif_width = int(w * 0.60)     
        gif_height = int(h * 0.65)   
        movie.setScaledSize(QSize(gif_width, gif_height))


        
       
        gif_label.setMovie(movie)
        gif_label.setAlignment(Qt.AlignCenter)
        movie.start()

        self.icon_label = QLabel()
        mic_icon_size = get_scaled_size(w, 0.08, 60, 120)




        pixmap = safe_load_icon(GraphicsDirectoryPath('Mic_on.png'), mic_icon_size, mic_icon_size)
        self.icon_label.setPixmap(pixmap)
        self.icon_label.setFixedSize(mic_icon_size, mic_icon_size)  # icon clickable area
        self.icon_label.setAlignment(Qt.AlignCenter)
        self.toggled = True
        self.toggle_icon()
        self.icon_label.mousePressEvent = self.toggle_icon

        # self.label = QLabel("")
        # self.label.setStyleSheet(f"color: cyan; font-size:{max(14, dp(18))}px; margin-bottom:0;")
        self.label = QLabel("")
        self.label.setStyleSheet("""
            color: cyan;
            font-size: 20px;      /* size badha diya */
            font-weight: bold;    /* bold kar diya */
            margin-bottom: 0;
        """)
        self.label.setAlignment(Qt.AlignCenter)



        content_layout.addStretch(1)
        content_layout.addWidget(gif_label, 0, Qt.AlignCenter)
        content_layout.addSpacing(dp(5))
        content_layout.addWidget(self.label, 0, Qt.AlignCenter)
        content_layout.addSpacing(dp(5))
        content_layout.addWidget(self.icon_label, 0, Qt.AlignCenter)
        content_layout.addStretch(1)

        self.setLayout(content_layout)
        # ❌ Fixed size hataya; responsive banane ke liye policies:
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setStyleSheet("background-color: black;")

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.SpeechRecogText)
        self.timer.start(100)  # throttled

    def SpeechRecogText(self):
        ensure_file_exists(TempDirectoryPath('Status.data'))
        with open(TempDirectoryPath('Status.data'), "r", encoding='utf-8') as file:
            messages = file.read()
            self.label.setText(messages)

    def load_icon(self, path, width=60, height=60):
        new_pixmap = safe_load_icon(path, width, height)
        self.icon_label.setPixmap(new_pixmap)

    def toggle_icon(self, event=None):
        if self.toggled:
            self.load_icon(GraphicsDirectoryPath('Mic_on.png'), dp(60), dp(60))
            MicButtonInitialed()
        else:
            self.load_icon(GraphicsDirectoryPath('Mic_off.png'), dp(60), dp(60))
            MicButtonClosed()
        self.toggled = not self.toggled

class MessageScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        label = QLabel("")
        layout.addWidget(label)
        chat_section = ChatSection()
        layout.addWidget(chat_section)
        self.setLayout(layout)
        self.setStyleSheet("background-color: black;")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

class CustomTopBar(QWidget):
    def __init__(self, parent, stacked_widget):
        super().__init__(parent)
        self.stacked_widget = stacked_widget
        self.initUI()
        self.current_screen = None

    def initUI(self):
        w, h, _ = _get_screen_metrics()
        topbar_icon_size = get_scaled_size(w, 0.03, 24, 40)

        self.setFixedHeight(dp(50))
        layout = QHBoxLayout(self)
        layout.setContentsMargins(dp(8), dp(4), dp(8), dp(4))
        layout.setAlignment(Qt.AlignRight)

        def mk_btn(icon_name, text=None):
            btn = QPushButton()
            icon = QIcon(GraphicsDirectoryPath(icon_name))
            btn.setIcon(icon)
            btn.setIconSize(QSize(topbar_icon_size, topbar_icon_size))
            if text:
                btn.setText(f"  {text}")
            btn.setStyleSheet("height:40px; line-height:40px; background-color:white;font-weight: bold ; color:black;")
            btn.setCursor(Qt.PointingHandCursor)
            return btn

        home_button = mk_btn("Home.png", "Home")
        message_button = mk_btn("Chats.png", "Chat")

        minimize_button = mk_btn("Minimize2.png")
        minimize_button.clicked.connect(self.minimizeWindow)

        self.maximize_button = mk_btn("Maximize.png")
        self.maximize_icon = QIcon(GraphicsDirectoryPath('Maximize.png'))
        self.restore_icon = QIcon(GraphicsDirectoryPath('Minimize.png'))
        self.maximize_button.clicked.connect(self.maximizeWindow)

        close_button = mk_btn("Close.png")
        close_button.clicked.connect(self.closeWindow)

        line_frame = QFrame()
        line_frame.setFixedHeight(1)
        line_frame.setFrameShape(QFrame.HLine)
        line_frame.setFrameShadow(QFrame.Sunken)
        line_frame.setStyleSheet("border-color: black;")

        title_label = QLabel(f"{(Assistantname or 'Assistant').capitalize()} AI  ")
        title_label.setStyleSheet(f"color: black;font-weight: bold ; font-size:{max(18, dp(20))}px; background-color:white")
        title_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        home_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        message_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))

        layout.addWidget(title_label)
        layout.addStretch(1)
        layout.addWidget(home_button)
        layout.addWidget(message_button)
        layout.addStretch(1)
        layout.addWidget(minimize_button)
        layout.addWidget(self.maximize_button)
        layout.addWidget(close_button)
        layout.addWidget(line_frame)
        self.draggable = True
        self.offset = None

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), Qt.white)
        super().paintEvent(event)

    def minimizeWindow(self):
        self.parent().showMinimized()

    def maximizeWindow(self):
        if self.parent().isMaximized():
            self.parent().showNormal()
            self.maximize_button.setIcon(self.maximize_icon)
        else:
            self.parent().showMaximized()
            self.maximize_button.setIcon(self.restore_icon)

    def closeWindow(self):
        self.parent().close()

    def mousePressEvent(self, event):
        if self.draggable and event.button() == Qt.LeftButton:
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.draggable and self.offset and not self.parent().isMaximized():
            new_pos = event.globalPos() - self.offset
            self.parent().move(new_pos)

    def showMessageScreen(self):
        if self.current_screen is not None:
            self.current_screen.hide()
        message_screen = MessageScreen(self)
        layout = self.parent().layout()
        if layout is not None:
            layout.addWidget(message_screen)
        self.current_screen = message_screen

    def showInitialScreen(self):
        if self.current_screen is not None:
            self.current_screen.hide()
        initial_screen = InitialScreen(self)
        layout = self.parent().layout()
        if layout is not None:
            layout.addWidget(initial_screen)
        self.current_screen = initial_screen

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.initUI()

    def initUI(self):
        w, h, _ = _get_screen_metrics()

        stacked_widget = QStackedWidget(self)
        initial_screen = InitialScreen()
        message_screen = MessageScreen()
        stacked_widget.addWidget(initial_screen)
        stacked_widget.addWidget(message_screen)

        # start maximized for 14-inch laptops; avoids fixed geometry
        self.resize(int(w * 0.9), int(h * 0.9))
        self.setStyleSheet("background-color: black;")

        top_bar = CustomTopBar(self, stacked_widget)
        self.setMenuWidget(top_bar)
        self.setCentralWidget(stacked_widget)

def GraphicalUserInterface():
    app = QApplication(sys.argv)
    # optionally set app-wide default font scaling
    _, _, s = _get_screen_metrics()
    base_font = QFont()
    base_font.setPointSizeF(9 * s + 2)  # thoda sa bump for readability
    app.setFont(base_font)

    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec_())

if __name__ == "__main__":
    ensure_folder_exists(TempDirPath)
    ensure_file_exists(TempDirectoryPath('Status.data'))
    ensure_file_exists(TempDirectoryPath('Mic.data'))
    ensure_file_exists(TempDirectoryPath('Responses.data'))
    GraphicalUserInterface()
