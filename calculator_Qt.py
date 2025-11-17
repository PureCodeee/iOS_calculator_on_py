import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, 
                              QGridLayout, QWidget, QPushButton, QLabel)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

class iOSButton(QPushButton):
    """Кастомная кнопка"""
    def __init__(self, text, color, text_color="white", font_size=35):
        super().__init__(text)
        
        self.setFixedSize(80, 80)
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                border-radius: 40px;
                color: {text_color};
                font-size: {font_size}px;
                font-weight: bold;
                border: none;
            }}
            QPushButton:hover {{
                background-color: {self._lighten_color(color)};
            }}
            QPushButton:pressed {{
                background-color: {self._darken_color(color)};
            }}
        """)
    
    def _lighten_color(self, color):
        if color == "#333333": return "#4d4d4d"
        elif color == "#747474": return "#c5c5c5"
        elif color == "#ff9500": return "#ffb143"
        return color
    
    def _darken_color(self, color):
        if color == "#333333": return "#737373"
        elif color == "#747474": return "#5a5a5a"
        elif color == "#ff9500": return "#cc7a00"
        return color

class Calculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("iOS Calculator")
        self.setFixedSize(350, 600)
        self.setStyleSheet("background-color: black;")
        
        self.current_input = "0"
        self.previous_input = ""
        self.operator = ""
        self.waiting_new_input = True
        
        self.init_ui()
    
    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 80, 10, 0)
        
        # Дисплей
        self.display = QLabel("0")
        self.display.setAlignment(Qt.AlignRight)
        self.display.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 70px;
                font-weight: light;
                background-color: black;
                border: none;
                padding: 0px 0px 0px 0px;
                margin: 0px;
            }
        """)
        self.display.setMinimumHeight(80)  # Минимальная высота
        layout.addWidget(self.display)
        
        # Сетка кнопок
        grid_layout = QGridLayout()
        grid_layout.setSpacing(5)  # Расстояние между кнопками
        grid_layout.setContentsMargins(0, 0, 0, 0)
        
        buttons = [
            ("AC", 0, 0, "#747474", "white"),
            ("+/-", 0, 1, "#747474", "white"), 
            ("%", 0, 2, "#747474", "white"),
            ("÷", 0, 3, "#ff9500", "white"),
            
            ("7", 1, 0, "#333333", "white"),
            ("8", 1, 1, "#333333", "white"),
            ("9", 1, 2, "#333333", "white"), 
            ("×", 1, 3, "#ff9500", "white"),
            
            ("4", 2, 0, "#333333", "white"),
            ("5", 2, 1, "#333333", "white"),
            ("6", 2, 2, "#333333", "white"),
            ("-", 2, 3, "#ff9500", "white"),
            
            ("1", 3, 0, "#333333", "white"),
            ("2", 3, 1, "#333333", "white"),
            ("3", 3, 2, "#333333", "white"),
            ("+", 3, 3, "#ff9500", "white"),
            
            ("0", 4, 0, "#333333", "white", 2),
            (".", 4, 2, "#333333", "white"),
            ("=", 4, 3, "#ff9500", "white"),
        ]
        
        for btn_info in buttons:
            if len(btn_info) == 5:
                text, row, col, color, text_color = btn_info
                colspan = 1
            else:
                text, row, col, color, text_color, colspan = btn_info
            
            if color == "#ff9500":
                font_size = 40
            else:
                font_size = 35
            
            button = iOSButton(text, color, text_color, font_size)
            
            if text == "0":
                button.setFixedSize(172, 80)
                button.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {color};
                        border-radius: 40px;
                        color: {text_color};
                        font-size: 35px;
                        font-weight: bold;
                        border: none;
                        text-align: left;
                        padding-left: 30px;
                    }}
                    QPushButton:hover {{
                        background-color: {button._lighten_color(color)};
                    }}
                    QPushButton:pressed {{
                        background-color: {button._darken_color(color)};
                    }}
                """)
            
            button.clicked.connect(lambda checked, t=text: self.button_clicked(t))
            grid_layout.addWidget(button, row, col, 1, colspan)
        
        layout.addLayout(grid_layout)
        central_widget.setLayout(layout)
    
    def button_clicked(self, text):
        if text in "0123456789":
            self.input_number(text)
        elif text in ["÷", "×", "-", "+"]:
            self.input_operator(text)
        elif text == "=":
            self.calculate()
        elif text == "AC":
            self.clear()
        elif text == "+/-":
            self.toggle_sign()
        elif text == "%":
            self.percentage()
        elif text == ".":
            self.input_decimal()
        
        self.update_display()
    
    def input_number(self, number):
        if self.waiting_new_input:
            self.current_input = number
            self.waiting_new_input = False
        else:
            if self.current_input == "0":
                self.current_input = number
            else:
                self.current_input += number
    
    def input_operator(self, operator):
        if not self.waiting_new_input:
            self.calculate()
        
        self.operator = operator
        self.previous_input = self.current_input
        self.waiting_new_input = True
    
    def calculate(self):
        if not self.operator or not self.previous_input:
            return
        
        try:
            prev = float(self.previous_input)
            curr = float(self.current_input)
            
            operations = {
                '+': lambda x, y: x + y,
                '-': lambda x, y: x - y,
                '×': lambda x, y: x * y,
                '÷': lambda x, y: x / y if y != 0 else "Error"
            }
            
            if self.operator in operations:
                result = operations[self.operator](prev, curr)
                
                if result == "Error":
                    self.current_input = "Error"
                elif result.is_integer():
                    self.current_input = str(int(result))
                else:
                    self.current_input = f"{result:.6g}".rstrip('0').rstrip('.')
                
                self.operator = ""
                self.previous_input = ""
                self.waiting_new_input = True
                
        except (ValueError, ZeroDivisionError):
            self.current_input = "Error"
            self.waiting_new_input = True
    
    def clear(self):
        self.current_input = "0"
        self.previous_input = ""
        self.operator = ""
        self.waiting_new_input = True
    
    def toggle_sign(self):
        if self.current_input and self.current_input != "0":
            if self.current_input[0] == '-':
                self.current_input = self.current_input[1:]
            else:
                self.current_input = '-' + self.current_input
    
    def percentage(self):
        try:
            value = float(self.current_input)
            self.current_input = str(value / 100)
            self.waiting_new_input = True
        except ValueError:
            self.current_input = "Error"
    
    def input_decimal(self):
        if self.waiting_new_input:
            self.current_input = "0."
            self.waiting_new_input = False
        elif '.' not in self.current_input:
            self.current_input += '.'
    
    def update_display(self):
        display_text = self.current_input
        if len(display_text) > 10:
            try:
                num = float(display_text)
                display_text = f"{num:.2e}"
            except:
                display_text = "Error"
        
        self.display.setText(display_text)

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    calculator = Calculator()
    calculator.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()