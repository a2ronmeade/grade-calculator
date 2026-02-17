import sys
import os
import json
from PyQt5.QtWidgets import *
from themes import LIGHT_THEME, DARK_THEME

class GradeCategory(QWidget):
    def __init__(self, name):
        super().__init__()
        self.name = name # store the category name (hw, quiz, etc.)
        self.layout = QVBoxLayout()
        
        top_row = QHBoxLayout()
        top_row.addWidget(QLabel(f"{name} Count:")) # select # of assignments for category name
        
        self.count_spin = QSpinBox()
        self.count_spin.setRange(0, 16)
        self.count_spin.valueChanged.connect(self.update_fields)
        top_row.addWidget(self.count_spin)

        top_row.addWidget(QLabel("Weight (%):")) # weight of the assigmnent
        self.weight_input = QLineEdit()
        self.weight_input.setPlaceholderText("e.g. 20")
        top_row.addWidget(self.weight_input)

        self.layout.addLayout(top_row)

        # input grades
        self.grade_layout = QVBoxLayout()
        self.grade_inputs = []
        self.layout.addLayout(self.grade_layout)

        self.setLayout(self.layout)

    def update_fields(self): #dynamically updates the input boxes
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

    def get_average(self): # calculates average
        grades = []
        for field in self.grade_inputs:
            try:
                grades.append(float(field.text()))
            except:
                pass

        if len(grades) == 0:
            return 0
        
        return sum(grades) / len(grades)

    def get_weight(self): #returns weight
        try:
            return float(self.weight_input.text())
        except:
            return 0


class GradeCalculator(QWidget): #controls app window (theme, categories, final grade)
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Grade Calculator")
        self.resize(600, 800)

        layout = QVBoxLayout()

        self.setStyleSheet(DARK_THEME)
        self.dark_mode = True  #dark mode is my preferred default

        self.theme_switch = QCheckBox("Dark Mode")
        self.theme_switch.setChecked(True)  
        self.theme_switch.stateChanged.connect(self.toggle_theme) 

        layout.addWidget(self.theme_switch)

        self.save_button = QPushButton("Save Grades")
        self.save_button.clicked.connect(self.save_grades)
        layout.addWidget(self.save_button)

        self.load_button = QPushButton("Load Grades")
        self.load_button.clicked.connect(self.load_grades)
        layout.addWidget(self.load_button)


        # scroll area for if there are many assignments
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(scroll_widget)

        # create categories (change as required but these are what i use)
        self.categories = [
            GradeCategory("Homework"),
            GradeCategory("Quizzes"),
            GradeCategory("Midterms"),
            GradeCategory("Final")
        ]

        for cat in self.categories:
            self.scroll_layout.addWidget(cat)

        scroll.setWidget(scroll_widget)
        layout.addWidget(scroll)

        # calculate final grade button
        self.calc_button = QPushButton("Calculate Final Grade")
        self.calc_button.clicked.connect(self.calculate_grade)
        layout.addWidget(self.calc_button)

        # result
        self.result_label = QLabel("Final Grade: ")
        layout.addWidget(self.result_label)

        self.setLayout(layout)

        self.save_folder = "saves"
        os.makedirs(self.save_folder, exist_ok=True)

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode

        if self.dark_mode:
            self.setStyleSheet(DARK_THEME)
        else:
            self.setStyleSheet(LIGHT_THEME)

    def save_grades(self):

        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Save Grades As",
            os.path.join(self.save_folder, "grades.json"),
            "JSON Files (*.json)"
        )

        if not filename:
            return
        
        self.current_file = filename

        data = {}

        for cat in self.categories:
            grades = []

            for field in cat.grade_inputs:
                try:
                    grades.append(float(field.text()))
                except:
                    pass

            data[cat.name] = {
                "weight": cat.get_weight(),
                "grades": grades
            }

        with open(filename, "w") as f:
            json.dump(data, f, indent=4)

    def load_grades(self):

        filename, _ = QFileDialog.getOpenFileName(
            self, "Load Grades", self.save_folder, "JSON Files (*.json)"
        )

        if not filename:
            return

        with open(filename, "r") as f:
            data = json.load(f)

        for cat in self.categories:

            if cat.name not in data:
                continue

            cat_data = data[cat.name]

            cat.weight_input.setText(str(cat_data["weight"]))

            grades = cat_data["grades"]

            cat.count_spin.setValue(len(grades))

            for field, grade in zip(cat.grade_inputs, grades):
                field.setText(str(grade))


    def calculate_grade(self): #calculates the final grade
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


if __name__ == "__main__": # creates the app and launches window
    app = QApplication(sys.argv)
    window = GradeCalculator()
    window.show()
    sys.exit(app.exec_())
