import os
from backend import Backend
import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QFileDialog, QFrame
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QMovie
from backend import Backend
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QSlider

class VaaniApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Vaani App")
        self.setGeometry(100, 100, 720, 720)

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.layout = QVBoxLayout(central_widget)

        # Title "Vaani"
        title_label = QLabel("Vaani", self)
        title_label.setStyleSheet("font-size: 70px; font-weight: bold; color: #FFA500;")  # Orange color
        self.layout.addWidget(title_label, alignment=Qt.AlignCenter)

        # Underline Separator
        underline = QFrame(self)
        underline.setFrameShape(QFrame.HLine)
        underline.setFrameShadow(QFrame.Sunken)
        self.layout.addWidget(underline)

        # Create and place widgets
        self.label = QLabel("Enter prompt:", self)
        self.label.setStyleSheet("font-size: 20px; font-weight: bold; color: #32CD32;")  # Green color
        self.layout.addWidget(self.label, alignment=Qt.AlignCenter)

        self.entry = QLineEdit(self)
        self.entry.setFixedWidth(500)

        self.entry.setStyleSheet("font-size: 16px; padding: 8px;")
        self.layout.addWidget(self.entry, alignment=Qt.AlignCenter)

        # Submit Button
        self.button_submit = QPushButton("Submit", self)
        self.button_submit.setStyleSheet(
            "QPushButton {"
            "   background-color: #4169E1; /* Royal Blue color */"
            "   color: white;"
            "   font-weight: bold;"
            "   border-radius: 15px; /* Adjust the value to change the roundness */"
            "   border: none;"  # Remove default border
            "   padding: 10px 20px;"  # Adjust padding as needed
            "   box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.5); /* Add shadow */"
            "}"
            "QPushButton:hover {"  # Style on hover (optional)
            "   background-color: #32509A; /* Darker shade of blue */"
            "}"
        )
        self.button_submit.setFixedHeight(30)
        self.button_submit.setFixedWidth(150)  # Fixed width
        self.button_submit.clicked.connect(self.submit_data)
        self.layout.addWidget(self.button_submit, alignment=Qt.AlignCenter)

        # Browse Button
        self.button_browse = QPushButton("Browse GIF", self)
        self.button_browse.setStyleSheet(
            "QPushButton {"
            "   background-color: #FF6347; /* Tomato color */"
            "   color: white;"
            "   font-weight: bold;"
            "   border-radius: 15px; /* Adjust the value to change the roundness */"
            "   border: none;"  # Remove default border
            "   padding: 10px 20px;"  # Adjust padding as needed
            "   box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.5); /* Add shadow */"
            "}"
            "QPushButton:hover {"  # Style on hover (optional)
            "   background-color: #CC4F39; /* Darker shade of red */"
            "}"
        )
        self.button_browse.setFixedWidth(140)  # Fixed width
        self.button_browse.clicked.connect(self.browse_gif)
        self.layout.addWidget(self.button_browse, alignment=Qt.AlignCenter)

        # Label for GIF display
        self.label_gif = QLabel(self)
        self.label_gif.setFixedSize(256,256)
        self.layout.addWidget(self.label_gif, alignment=Qt.AlignCenter)  # Align the label containing GIF

        # Initialize variables
        self.movie = QMovie()
        self.original_image = None
        self.gif_path = None

        # GIF speed
        self.label = QLabel("GIF speed", self)
        self.label.setStyleSheet("font-size: 20px; font-weight: bold; color: #FF0000;")  # red color
        self.layout.addWidget(self.label, alignment=Qt.AlignCenter)

        # Slider for controlling GIF speed
        self.speed_slider = QSlider(Qt.Horizontal, self)
        self.speed_slider.setMinimum(1)
        self.speed_slider.setMaximum(100)
        self.speed_slider.setValue(50)  # Initial speed value
        self.speed_slider.setTickInterval(10)
        self.speed_slider.setSingleStep(1)
        self.layout.addWidget(self.speed_slider, alignment=Qt.AlignCenter)
        self.speed_slider.valueChanged.connect(self.change_speed)

        # Play/Pause Button
        self.button_play_pause = QPushButton("Play/Pause", self)
        self.button_play_pause.setStyleSheet(
            "QPushButton {"
            "   background-color: #FFD700; /* Gold color */"
            "   color: black;"
            "   font-weight: bold;"
            "   border-radius: 20px; /* Adjust the value to change the roundness */"
            "   border: none;"  # Remove default border
            "   padding: 10px 20px;"  # Adjust padding as needed
            "   box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.5); /* Add shadow */"
            "}"
            "QPushButton:hover {"  # Style on hover (optional)
            "   background-color: #CCA300; /* Darker shade of gold */"
            "}"
        )
        self.button_play_pause.setFixedHeight(40)
        self.button_play_pause.setFixedWidth(160)  # Fixed width
        self.button_play_pause.clicked.connect(self.toggle_animation)
        self.layout.addWidget(self.button_play_pause, alignment=Qt.AlignCenter)


        # alert 
        self.alert_timer = QTimer(self)
        self.alert_label = QLabel("", self)
        self.alert_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #FF0000;")  # Red color for alert
        self.layout.addWidget(self.alert_label, alignment=Qt.AlignCenter)
        self.alert_timer.timeout.connect(self.hide_alert)

        

    # alert slider logic
    def change_speed(self):
        speed = self.speed_slider.value()
        if speed != 0:
            # Calculate duration based on the speed value (higher speed = lower duration)
            duration = 1000 // speed
            self.movie.setSpeed(duration)

    def process_input(self, input_value):
        Backend(input_value)
    
        self.show_gif('Vanni_script/Gifoutput/output.gif')
        

    def toggle_animation(self):
        if self.movie.state() == QMovie.NotRunning:
            self.movie.start()
        else:
            if self.movie.state() == QMovie.Paused:
                self.movie.setPaused(False)
            else:
                self.movie.setPaused(True)

    def show_gif(self, path):
        self.gif_path = path
        if self.gif_path and os.path.exists(self.gif_path):
            self.original_image = QPixmap(self.gif_path)
            self.original_image = self.original_image.scaled(QSize(300, 225), Qt.KeepAspectRatio)
            self.movie.setFileName(self.gif_path)
            self.label_gif.setMovie(self.movie)
            self.movie.start()
        else:
            self.show_no_gif_message()

    def browse_gif(self):
        gif_path, _ = QFileDialog.getOpenFileName(self, "Browse GIF", "", "GIF files (*.gif)")
        if gif_path and os.path.exists(gif_path):
            self.show_gif(gif_path)
        else:
            self.show_no_gif_message()

    def show_no_gif_message(self):
        label_no_gif = QLabel("No valid GIF selected!", self)
        label_no_gif.setStyleSheet("font-size: 14px; font-weight: bold;")
        self.layout.addWidget(label_no_gif)

    def submit_data(self):
        input_value = self.entry.text().strip()  # Retrieve text and remove leading/trailing spaces
        if input_value:
            self.process_input(input_value)
        else:
            self.show_prompt_alert()

    def show_prompt_alert(self):
        self.alert_label.setText("Please enter the prompt before submitting.")
        self.alert_timer.start(10000)  # Show the alert for 10 seconds (10000 milliseconds)

    def hide_alert(self):
        self.alert_label.setText("")
        self.alert_timer.stop()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    vaani_app = VaaniApp()
    vaani_app.show()
    sys.exit(app.exec_())













