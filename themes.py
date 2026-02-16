LIGHT_THEME = """
QWidget {
    background-color: #f5f5f5;
    font-size: 22px;
}

QLabel {
    color: #222;
}

QLineEdit, QSpinBox {
    background-color: white;
    border: 1px solid #ccc;
    padding: 5px;
    border-radius: 6px;
}

QPushButton {
    background-color: #66ff99;
    color: black;
    padding: 6px;
    border-radius: 8px;
}

QPushButton:hover {
    background-color: #99ffcc;
}

QCheckBox::indicator {
            width: 30px;
            height: 30px;
}
QCheckBox::indicator:unchecked {
    background-color: #99ff99;
    border-radius: 6px;
}
"""


DARK_THEME = """
QWidget {
    background-color: #2b2b2b;
    color: #dddddd;
    font-size: 22px;
}

QLineEdit, QSpinBox {
    background-color: #3c3f41;
    border: 1px solid #555;
    padding: 5px;
    border-radius: 6px;
    color: white;
}

QPushButton {
    background-color: #00802b;
    color: white;
    padding: 6px;
    border-radius: 8px;
}

QPushButton:hover {
    background-color: #009933;
}

QCheckBox::indicator {
            width: 30px;
            height: 30px;
            border-radius: 6px;
}
QCheckBox::indicator:checked {
    background-color: #006622;
    image: url(icons/checkmark.png);
}
"""
