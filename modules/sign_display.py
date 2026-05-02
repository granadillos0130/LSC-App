import os
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class SignDisplay:
    def __init__(self, signs_path='assets/signs'):
        self.signs_path = signs_path
        self.signs = {}
        self.load_signs()

    def load_signs(self):
        if not os.path.exists(self.signs_path):
            print("No existe la carpeta de señas")
            return

        for file in os.listdir(self.signs_path):
            if file.endswith('.png') or file.endswith('.jpg'):
                letter = file.split('.')[0].upper()
                full_path = os.path.join(self.signs_path, file)
                self.signs[letter] = full_path
                
        print(f"Señas cargadas: {len(self.signs)}")

    def get_sign_pixmap(self, letter, size=150):
        letter = letter.upper()
        if letter not in self.signs:
            print(f"No hay imagen para la letra: {letter}")
            return None

        pixmap = QPixmap(self.signs[letter])
        pixmap = pixmap.scaled(
            size, size,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        return pixmap

    def get_sentence_signs(self, sentence):
        signs = []
        for char in sentence.upper():
            if char == ' ':
                signs.append(('SPACE', None))
            elif char in self.signs:
                signs.append((char, self.get_sign_pixmap(char)))
        return signs
