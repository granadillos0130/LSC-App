import cv2
import numpy as np
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                              QHBoxLayout, QPushButton, QLabel, 
                              QTextEdit, QTabWidget, QScrollArea)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap

from modules.detector import HandDetector
from modules.classifier import SignClassifier
from modules.voice import VoiceModule
from modules.sentence_builder import SentenceBuilder
from modules.sign_display import SignDisplay

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LSC - Traductor de Lengua de Señas Colombiana")
        self.setMinimumSize(1000, 700)

        self.detector = HandDetector()
        self.classifier = SignClassifier()
        self.voice = VoiceModule()
        self.builder = SentenceBuilder()
        self.display = SignDisplay()

        self.cap = cv2.VideoCapture(0)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

        self.init_ui()

    def init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        tabs = QTabWidget()
        tabs.addTab(self.create_sign_to_text_tab(), "Seña → Texto")
        tabs.addTab(self.create_voice_to_sign_tab(), "Voz → Seña")
        tabs.addTab(self.create_training_tab(), "Entrenar Modelo")
        main_layout.addWidget(tabs)

    def create_sign_to_text_tab(self):
        widget = QWidget()
        layout = QHBoxLayout(widget)
        cam_layout = QVBoxLayout()
        self.camera_label = QLabel("Cámara")
        self.camera_label.setMinimumSize(640, 480)
        self.camera_label.setAlignment(Qt.AlignCenter)
        self.camera_label.setStyleSheet("background-color: black;")
        cam_layout.addWidget(self.camera_label)
        btn_layout = QHBoxLayout()
        self.btn_start = QPushButton("Iniciar Cámara")
        self.btn_start.clicked.connect(self.start_camera)
        self.btn_stop = QPushButton("Detener Cámara")
        self.btn_stop.clicked.connect(self.stop_camera)
        btn_layout.addWidget(self.btn_start)
        btn_layout.addWidget(self.btn_stop)
        cam_layout.addLayout(btn_layout)
        layout.addLayout(cam_layout)
        right_layout = QVBoxLayout()
        self.prediction_label = QLabel("Letra detectada: -")
        self.prediction_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        right_layout.addWidget(self.prediction_label)
        self.sentence_label = QLabel("Oración: ")
        self.sentence_label.setStyleSheet("font-size: 16px;")
        self.sentence_label.setWordWrap(True)
        right_layout.addWidget(self.sentence_label)
        btn_speak = QPushButton("Leer oración en voz alta")
        btn_speak.clicked.connect(self.speak_sentence)
        right_layout.addWidget(btn_speak)
        btn_clear = QPushButton("Limpiar oración")
        btn_clear.clicked.connect(self.clear_sentence)
        right_layout.addWidget(btn_clear)
        right_layout.addStretch()
        layout.addLayout(right_layout)
        return widget

    def create_voice_to_sign_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        btn_listen = QPushButton("🎤 Escuchar")
        btn_listen.setMinimumHeight(50)
        btn_listen.clicked.connect(self.listen_and_show)
        layout.addWidget(btn_listen)
        self.voice_text_label = QLabel("Texto escuchado: -")
        self.voice_text_label.setStyleSheet("font-size: 16px;")
        layout.addWidget(self.voice_text_label)

        # ScrollArea para las imágenes
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFixedHeight(350)
        scroll_widget = QWidget()
        self.signs_container = QHBoxLayout(scroll_widget)
        self.signs_container.setSpacing(15)
        self.signs_container.setContentsMargins(10, 10, 10, 10)
        self.signs_container.addStretch()
        scroll.setWidget(scroll_widget)
        layout.addWidget(scroll)
        layout.addStretch()
        return widget

    def create_training_tab(self):
        widget = QWidget()
        layout = QHBoxLayout(widget)
        cam_layout = QVBoxLayout()
        self.training_camera_label = QLabel("Cámara")
        self.training_camera_label.setMinimumSize(640, 480)
        self.training_camera_label.setAlignment(Qt.AlignCenter)
        self.training_camera_label.setStyleSheet("background-color: black;")
        cam_layout.addWidget(self.training_camera_label)
        btn_start_training = QPushButton("Iniciar Cámara")
        btn_start_training.clicked.connect(self.start_camera)
        cam_layout.addWidget(btn_start_training)
        layout.addLayout(cam_layout)
        right_layout = QVBoxLayout()
        self.training_label = QLabel("Letra a entrenar:")
        right_layout.addWidget(self.training_label)
        self.letter_input = QTextEdit()
        self.letter_input.setMaximumHeight(40)
        right_layout.addWidget(self.letter_input)
        btn_capture = QPushButton("Capturar ejemplo")
        btn_capture.clicked.connect(self.capture_training)
        right_layout.addWidget(btn_capture)
        btn_burst = QPushButton("⚡ Ráfaga (30 ejemplos)")
        btn_burst.clicked.connect(self.capture_burst)
        btn_burst.setStyleSheet("background-color: #e67e22; color: white; font-weight: bold;")
        right_layout.addWidget(btn_burst)
        self.training_status = QLabel("Ejemplos guardados: 0")
        right_layout.addWidget(self.training_status)
        right_layout.addStretch()
        layout.addLayout(right_layout)
        return widget

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return
        frame, landmarks = self.detector.detect(frame)
        if landmarks:
            normalized = self.detector.normalize(landmarks)
            if normalized:
                letter, confidence = self.classifier.predict(normalized)
                if letter and confidence >= 0.8:
                    self.builder.add_letter(letter, confidence)
                    self.prediction_label.setText(f"Letra detectada: {letter} ({confidence:.0%})")
                    self.sentence_label.setText(f"Oración: {self.builder.get_sentence()}")
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = frame_rgb.shape
        img = QImage(frame_rgb.data, w, h, ch * w, QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(img)
        self.camera_label.setPixmap(pixmap)
        self.training_camera_label.setPixmap(pixmap)

    def start_camera(self):
        self.timer.start(30)

    def stop_camera(self):
        self.timer.stop()

    def speak_sentence(self):
        sentence = self.builder.get_sentence()
        if sentence:
            self.voice.speak(sentence)

    def clear_sentence(self):
        self.builder.clear()
        self.sentence_label.setText("Oración: ")
        self.prediction_label.setText("Letra detectada: -")

    def listen_and_show(self):
        text = self.voice.listen()
        if text:
            self.voice_text_label.setText(f"Texto escuchado: {text}")
            signs = self.display.get_sentence_signs(text)

            # Limpiar señas anteriores
            while self.signs_container.count() > 1:
                item = self.signs_container.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()

            # Insertar antes del stretch
            for letter, pixmap in signs:
                lbl = QLabel()
                lbl.setContentsMargins(5, 5, 5, 5)
                if pixmap:
                    lbl.setPixmap(pixmap)
                else:
                    lbl.setText(letter)
                    lbl.setStyleSheet("font-size: 20px; font-weight: bold; padding: 10px;")
                self.signs_container.insertWidget(self.signs_container.count() - 1, lbl)

    def capture_training(self):
        letter = self.letter_input.toPlainText().strip().upper()
        if not letter:
            return
        ret, frame = self.cap.read()
        if not ret:
            return
        _, landmarks = self.detector.detect(frame)
        if landmarks:
            normalized = self.detector.normalize(landmarks)
            if normalized:
                self.classifier.save_example(normalized, letter)
                count = len(self.classifier.labels)
                self.training_status.setText(f"Ejemplos guardados: {count}")

    def capture_burst(self):
        letter = self.letter_input.toPlainText().strip().upper()
        if not letter:
            return
        count = 0
        for _ in range(30):
            ret, frame = self.cap.read()
            if not ret:
                continue
            _, landmarks = self.detector.detect(frame)
            if landmarks:
                normalized = self.detector.normalize(landmarks)
                if normalized:
                    self.classifier.save_example(normalized, letter)
                    count += 1
        total = len(self.classifier.labels)
        self.training_status.setText(f"Ejemplos guardados: {total} (+{count} de {letter})")

    def closeEvent(self, event):
        self.stop_camera()
        if self.cap.isOpened():
            self.cap.release()
        event.accept()