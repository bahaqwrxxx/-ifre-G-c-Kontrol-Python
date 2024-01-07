import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from PyQt5.QtGui import QIcon, QPixmap
import random
import string
import pyperclip
import requests 

#__author__ = "bahaqwrx"
#__description__ = "Python Şifre Gücü Kontrol Etme Programı"


class PasswordStrengthChecker(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Password Gücü Denetleyici')
        self.setGeometry(300, 300, 400, 200)

        icon_url = "https://w7.pngwing.com/pngs/259/835/png-transparent-computer-icons-key-key-angle-desktop-wallpaper-black-and-white.png"
        icon_data = requests.get(icon_url).content
        icon_pixmap = QPixmap()
        icon_pixmap.loadFromData(icon_data)

        self.setWindowIcon(QIcon(icon_pixmap))

        self.password_label = QLabel('Şifre:', self)
        self.password_input = QLineEdit(self)
        self.check_button = QPushButton('Şifre Gücünü Kontrol Et', self)
        self.check_button.clicked.connect(self.check_password_strength)

        self.password_strength_label = QLabel('', self)
        self.new_password_button = QPushButton('Yeni Şifre Oluştur', self)
        self.new_password_button.clicked.connect(self.generate_new_password)

        self.copy_to_clipboard_button = QPushButton('Panoya Kopyala', self)
        self.copy_to_clipboard_button.clicked.connect(self.copy_to_clipboard)

        layout = QVBoxLayout(self)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.check_button)
        layout.addWidget(self.password_strength_label)
        layout.addWidget(self.new_password_button)
        layout.addWidget(self.copy_to_clipboard_button)

        self.setStyleSheet("""
            QWidget {
                font-family: Arial;
                font-size: 12pt;
            }

            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 8px;
                text-align: center;
                text-decoration: none;
                font-size: 16px;
                margin: 4px 2px;
            }

            QPushButton:hover {
                background-color: #45a049;
            }
        """)

        self.show()

    def check_password_strength(self):
        user_password = self.password_input.text()
        strength_percentage = self.password_strength(user_password)
        self.password_strength_label.setText(f'Şifre Gücü: {strength_percentage}%')

        if strength_percentage < 40:
            response = QMessageBox.question(self, 'Zayıf Şifre', 'Şifre zayıf. Yeni bir şifre oluşturmak ister misiniz?',
                                            QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)

            if response == QMessageBox.Yes:
                self.generate_new_password()

    def password_strength(self, password):
        length = len(password)
        if length >= 12:
            return 100
        elif length >= 8:
            return int((length / 12) * 100)
        else:
            return int((length / 8) * 100)

    def generate_new_password(self):
        new_password = ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(12))
        self.password_input.setText(new_password)
        self.password_strength_label.clear()

    def copy_to_clipboard(self):
        new_password = self.password_input.text()
        try:
            pyperclip.copy(new_password)
            QMessageBox.information(self, 'Kopyalandı', 'Şifre panoya kopyalandı.')
        except Exception as e:
            print(f'Hata: {e}')
            QMessageBox.warning(self, 'Hata', 'Panoya kopyalama yapılamadı.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PasswordStrengthChecker()
    sys.exit(app.exec_())
