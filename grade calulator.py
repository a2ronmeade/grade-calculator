import sys
from PyQt5.QtWidgets import *

class GradeCategory(QWidget):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.layout = QVBoxLayout()
        
        # Number of assignments selector
        top_row = QHBoxLayout()
        top_row.addWidget(QLabel(f"{name} Count:"))
        
        self.count_spin = QSpinBox()
        self.count_spin.setRange(0, 50)
        self.count_spin.valueChanged.connect(self.update_fields)
        top_row.addWidget(self.count_spin)

        # Weight input
        top_row.addWidget(QLabel("Weight (%):"))
        self.weight_input = QLineEdit()
        self.weight_input.setPlaceholderText("e.g. 25")
        top_row.addWidget(self.weight_input)

        self.layout.addLayout(top_row)

        # Area for grade inputs
        self.grade_layout = QVBoxLayout()
        self.grade_inputs = []
        self.layout.addLayout(self.grade_layout)

        self.setLayout(self.layout)

    def update_fields(self):
        # Clear old fields
        for field in self.grade_inputs:
            field.deleteLater()
        self.grade_inputs.clear()

        # Create new fields
        for i in range(self.count_spin.value()):
            grade_input = QLineEdit()
            grade_input.setPlaceholderText(f"{self.name} {i+1} Grade")
            self.grade_layout.addWidget(grade_input)
            self.grade_inputs.append(grade_input)

    def get_average(self):
        grades = []
        for field in self.grade_inputs:
            try:
                grades.append(float(field.text()))
            except:
                pass

        if len(grades) == 0:
            return 0
        
        return sum(grades) / len(grades)

    def get_weight(self):
        try:
            return float(self.weight_input.text())
        except:
            return 0


class GradeCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Grade Calculator")
        self.resize(400, 600)

        layout = QVBoxLayout()

        # Scroll area (useful if many assignments)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(scroll_widget)

        # Create categories
        self.categories = [
            GradeCategory("Homework"),
            GradeCategory("Quizzes"),
            GradeCategory("Midterms"),
            GradeCategory("Finals")
        ]

        for cat in self.categories:
            self.scroll_layout.addWidget(cat)

        scroll.setWidget(scroll_widget)
        layout.addWidget(scroll)

        # Calculate button
        self.calc_button = QPushButton("Calculate Final Grade")
        self.calc_button.clicked.connect(self.calculate_grade)
        layout.addWidget(self.calc_button)

        # Result label
        self.result_label = QLabel("Final Grade: ")
        layout.addWidget(self.result_label)

        self.setLayout(layout)

    def calculate_grade(self):
        total = 0
        total_weight = 0

        for cat in self.categories:
            avg = cat.get_average()
            weight = cat.get_weight()

            total += avg * weight
            total_weight += weight

        if total_weight == 0:
            self.result_label.setText("Final Grade: N/A")
        else:
            final_grade = total / total_weight
            self.result_label.setText(f"Final Grade: {final_grade:.2f}%")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GradeCalculator()
    window.show()
    sys.exit(app.exec_())
