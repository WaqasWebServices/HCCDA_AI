import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QComboBox, QTabWidget, 
                             QGroupBox, QFormLayout, QDateEdit, QTableWidget, 
                             QTableWidgetItem, QHeaderView)
from PyQt5.QtChart import QChart, QChartView, QLineSeries, QValueAxis
from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont, QColor, QPainter
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class AdvancedBMICalculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Advanced BMI Calculator")
        self.setGeometry(100, 100, 900, 700)
        
        # Initialize data storage
        self.history_data = []
        
        # Create main widget and layout
        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout()
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)
        
        # Create tab widget
        self.tabs = QTabWidget()
        self.main_layout.addWidget(self.tabs)
        
        # Create tabs
        self.create_calculator_tab()
        self.create_history_tab()
        self.create_analysis_tab()
        self.create_about_tab()
        
        # Apply styles
        self.apply_styles()
        
    def apply_styles(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QTabWidget::pane {
                border: 1px solid #d4d4d4;
                background: white;
            }
            QTabBar::tab {
                background: #e0e0e0;
                border: 1px solid #d4d4d4;
                padding: 8px;
                font-size: 12px;
            }
            QTabBar::tab:selected {
                background: white;
                border-bottom: 2px solid #2a82da;
            }
            QGroupBox {
                border: 1px solid #d4d4d4;
                border-radius: 5px;
                margin-top: 10px;
                font-size: 14px;
                font-weight: bold;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px;
            }
            QPushButton {
                background-color: #2a82da;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #3a92ea;
            }
            QLabel {
                font-size: 14px;
            }
            QLineEdit, QComboBox, QDateEdit {
                padding: 6px;
                border: 1px solid #d4d4d4;
                border-radius: 4px;
                font-size: 14px;
            }
            QTableWidget {
                border: 1px solid #d4d4d4;
                font-size: 14px;
            }
        """)
        
    def create_calculator_tab(self):
        self.calculator_tab = QWidget()
        self.tabs.addTab(self.calculator_tab, "BMI Calculator")
        
        layout = QVBoxLayout()
        self.calculator_tab.setLayout(layout)
        
        # Unit selection
        unit_group = QGroupBox("Units")
        unit_layout = QHBoxLayout()
        self.unit_combo = QComboBox()
        self.unit_combo.addItems(["Metric (kg, cm)", "Imperial (lbs, inches)"])
        unit_layout.addWidget(QLabel("Measurement System:"))
        unit_layout.addWidget(self.unit_combo)
        unit_layout.addStretch()
        unit_group.setLayout(unit_layout)
        layout.addWidget(unit_group)
        
        # Input fields
        input_group = QGroupBox("Personal Information")
        input_layout = QFormLayout()
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter your name")
        
        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setCalendarPopup(True)
        
        self.age_input = QLineEdit()
        self.age_input.setPlaceholderText("Enter your age")
        self.age_input.setValidator(QtGui.QIntValidator(1, 120))
        
        self.gender_combo = QComboBox()
        self.gender_combo.addItems(["Male", "Female", "Other"])
        
        self.weight_input = QLineEdit()
        self.weight_input.setPlaceholderText("Enter weight")
        
        self.height_input = QLineEdit()
        self.height_input.setPlaceholderText("Enter height")
        
        input_layout.addRow("Name:", self.name_input)
        input_layout.addRow("Date:", self.date_input)
        input_layout.addRow("Age:", self.age_input)
        input_layout.addRow("Gender:", self.gender_combo)
        input_layout.addRow("Weight:", self.weight_input)
        input_layout.addRow("Height:", self.height_input)
        
        input_group.setLayout(input_layout)
        layout.addWidget(input_group)
        
        # Calculate button
        self.calculate_btn = QPushButton("Calculate BMI")
        self.calculate_btn.clicked.connect(self.calculate_bmi)
        layout.addWidget(self.calculate_btn)
        
        # Results display
        self.result_group = QGroupBox("Results")
        result_layout = QVBoxLayout()
        
        self.bmi_label = QLabel("BMI: ")
        self.bmi_label.setFont(QFont("Arial", 16, QFont.Bold))
        
        self.category_label = QLabel("Category: ")
        self.category_label.setFont(QFont("Arial", 14))
        
        self.ideal_weight_label = QLabel("Ideal Weight Range: ")
        self.ideal_weight_label.setFont(QFont("Arial", 12))
        
        self.recommendation_label = QLabel("Recommendation: ")
        self.recommendation_label.setFont(QFont("Arial", 12))
        self.recommendation_label.setWordWrap(True)
        
        result_layout.addWidget(self.bmi_label)
        result_layout.addWidget(self.category_label)
        result_layout.addWidget(self.ideal_weight_label)
        result_layout.addWidget(self.recommendation_label)
        
        self.result_group.setLayout(result_layout)
        layout.addWidget(self.result_group)
        
        # Initially hide results
        self.result_group.hide()
        
    def create_history_tab(self):
        self.history_tab = QWidget()
        self.tabs.addTab(self.history_tab, "History")
        
        layout = QVBoxLayout()
        self.history_tab.setLayout(layout)
        
        # History table
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(6)
        self.history_table.setHorizontalHeaderLabels(["Date", "Name", "Age", "Gender", "BMI", "Category"])
        self.history_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        layout.addWidget(self.history_table)
        
    def create_analysis_tab(self):
        self.analysis_tab = QWidget()
        self.tabs.addTab(self.analysis_tab, "Analysis")
        
        layout = QVBoxLayout()
        self.analysis_tab.setLayout(layout)
        
        # BMI Trend Chart
        chart_group = QGroupBox("BMI Trend Over Time")
        chart_layout = QVBoxLayout()
        
        self.chart_view = QChartView()
        self.chart_view.setRenderHint(QPainter.Antialiasing)
        
        chart_layout.addWidget(self.chart_view)
        chart_group.setLayout(chart_layout)
        layout.addWidget(chart_group)
        
        # BMI Distribution Chart (Matplotlib)
        dist_group = QGroupBox("BMI Distribution")
        dist_layout = QVBoxLayout()
        
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        
        dist_layout.addWidget(self.canvas)
        dist_group.setLayout(dist_layout)
        layout.addWidget(dist_group)
        
    def create_about_tab(self):
        self.about_tab = QWidget()
        self.tabs.addTab(self.about_tab, "About")
        
        layout = QVBoxLayout()
        self.about_tab.setLayout(layout)
        
        about_text = QLabel("""
            <h2>Advanced BMI Calculator</h2>
            <p>Version 1.0</p>
            <p>This application calculates your Body Mass Index (BMI) and provides detailed analysis of your weight status.</p>
            <p>BMI Categories:</p>
            <ul>
                <li>Underweight: BMI less than 18.5</li>
                <li>Normal weight: BMI 18.5 to 24.9</li>
                <li>Overweight: BMI 25 to 29.9</li>
                <li>Obesity Class I: BMI 30 to 34.9</li>
                <li>Obesity Class II: BMI 35 to 39.9</li>
                <li>Obesity Class III: BMI 40 or greater</li>
            </ul>
            <p>Note: BMI is a screening tool but not a diagnostic of body fatness or health.</p>
        """)
        about_text.setWordWrap(True)
        layout.addWidget(about_text)
        
    def calculate_bmi(self):
        # Get input values
        name = self.name_input.text().strip()
        date = self.date_input.date().toString("yyyy-MM-dd")
        age = self.age_input.text().strip()
        gender = self.gender_combo.currentText()
        weight = self.weight_input.text().strip()
        height = self.height_input.text().strip()
        
        # Validate inputs
        if not name or not age or not weight or not height:
            self.show_error("Please fill in all fields")
            return
            
        try:
            weight = float(weight)
            height = float(height)
            age = int(age)
            
            if weight <= 0 or height <= 0:
                raise ValueError
        except ValueError:
            self.show_error("Please enter valid numbers for weight and height")
            return
            
        # Calculate BMI based on selected units
        if self.unit_combo.currentText() == "Metric (kg, cm)":
            bmi = weight / ((height / 100) ** 2)
        else:  # Imperial
            bmi = (weight / (height ** 2)) * 703
            
        # Determine category
        category, color = self.get_bmi_category(bmi)
        
        # Calculate ideal weight range
        if self.unit_combo.currentText() == "Metric (kg, cm)":
            min_ideal = 18.5 * ((height / 100) ** 2)
            max_ideal = 24.9 * ((height / 100) ** 2)
            ideal_range = f"{min_ideal:.1f} - {max_ideal:.1f} kg"
        else:
            min_ideal = (18.5 * (height ** 2)) / 703
            max_ideal = (24.9 * (height ** 2)) / 703
            ideal_range = f"{min_ideal:.1f} - {max_ideal:.1f} lbs"
            
        # Get recommendation
        recommendation = self.get_recommendation(bmi, age, gender)
        
        # Display results
        self.bmi_label.setText(f"BMI: <span style='color:{color}; font-weight:bold;'>{bmi:.1f}</span>")
        self.category_label.setText(f"Category: <span style='color:{color};'>{category}</span>")
        self.ideal_weight_label.setText(f"Ideal Weight Range: {ideal_range}")
        self.recommendation_label.setText(f"Recommendation: {recommendation}")
        
        # Show results
        self.result_group.show()
        
        # Add to history
        self.add_to_history(date, name, age, gender, bmi, category)
        
        # Update charts
        self.update_charts()
        
    def get_bmi_category(self, bmi):
        if bmi < 16:
            return "Severe Thinness", "#3498db"
        elif bmi < 17:
            return "Moderate Thinness", "#5dade2"
        elif bmi < 18.5:
            return "Mild Thinness", "#85c1e9"
        elif bmi < 25:
            return "Normal range", "#2ecc71"
        elif bmi < 30:
            return "Overweight", "#f39c12"
        elif bmi < 35:
            return "Obese Class I", "#e67e22"
        elif bmi < 40:
            return "Obese Class II", "#d35400"
        else:
            return "Obese Class III", "#c0392b"
            
    def get_recommendation(self, bmi, age, gender):
        if bmi < 18.5:
            return "You are underweight. Consider consulting a nutritionist for a healthy weight gain plan."
        elif bmi < 25:
            return "Your weight is in the normal range. Maintain a balanced diet and regular exercise."
        elif bmi < 30:
            return "You are overweight. Consider increasing physical activity and reducing calorie intake."
        else:
            return "You are in the obesity range. Consult with a healthcare provider for a weight management plan."
            
    def add_to_history(self, date, name, age, gender, bmi, category):
        # Add to data storage
        self.history_data.append({
            "date": date,
            "name": name,
            "age": age,
            "gender": gender,
            "bmi": bmi,
            "category": category
        })
        
        # Update table
        self.history_table.setRowCount(len(self.history_data))
        for row, entry in enumerate(self.history_data):
            self.history_table.setItem(row, 0, QTableWidgetItem(entry["date"]))
            self.history_table.setItem(row, 1, QTableWidgetItem(entry["name"]))
            self.history_table.setItem(row, 2, QTableWidgetItem(str(entry["age"])))
            self.history_table.setItem(row, 3, QTableWidgetItem(entry["gender"]))
            self.history_table.setItem(row, 4, QTableWidgetItem(f"{entry['bmi']:.1f}"))
            self.history_table.setItem(row, 5, QTableWidgetItem(entry["category"]))
            
    def update_charts(self):
        if not self.history_data:
            return
            
        # Update BMI trend chart
        chart = QChart()
        chart.setTitle("BMI Trend Over Time")
        chart.setAnimationOptions(QChart.SeriesAnimations)
        
        series = QLineSeries()
        series.setName("BMI")
        
        # Sort data by date
        sorted_data = sorted(self.history_data, key=lambda x: x["date"])
        
        for i, entry in enumerate(sorted_data):
            series.append(i, entry["bmi"])
            
        chart.addSeries(series)
        
        # Create axes
        axis_x = QValueAxis()
        axis_x.setTitleText("Measurements")
        axis_x.setLabelFormat("%d")
        axis_x.setRange(0, len(sorted_data) - 1)
        
        axis_y = QValueAxis()
        axis_y.setTitleText("BMI")
        axis_y.setRange(10, 50 if max(entry["bmi"] for entry in sorted_data) < 40 else 60)
        
        chart.addAxis(axis_x, Qt.AlignBottom)
        chart.addAxis(axis_y, Qt.AlignLeft)
        series.attachAxis(axis_x)
        series.attachAxis(axis_y)
        
        self.chart_view.setChart(chart)
        
        # Update BMI distribution chart
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        bmis = [entry["bmi"] for entry in self.history_data]
        categories = [self.get_bmi_category(bmi)[0] for bmi in bmis]
        
        unique_categories = sorted(set(categories), key=lambda x: np.mean([bmi for bmi, cat in zip(bmis, categories) if cat == x]))
        category_counts = [categories.count(cat) for cat in unique_categories]
        
        colors = [self.get_bmi_category(np.mean([bmi for bmi, cat in zip(bmis, categories) if cat == c]))[1] for c in unique_categories]
        
        ax.bar(unique_categories, category_counts, color=colors)
        ax.set_title("BMI Category Distribution")
        ax.set_ylabel("Count")
        ax.tick_params(axis='x', rotation=45)
        self.figure.tight_layout()
        self.canvas.draw()
        
    def show_error(self, message):
        error_label = QLabel(f"<span style='color:red;'>{message}</span>")
        error_label.setAlignment(Qt.AlignCenter)
        
        # Add to layout temporarily
        if hasattr(self, 'error_label'):
            self.main_layout.removeWidget(self.error_label)
            self.error_label.deleteLater()
            
        self.error_label = error_label
        self.main_layout.insertWidget(0, self.error_label)
        
        # Hide after 3 seconds
        QTimer.singleShot(3000, self.hide_error)
        
    def hide_error(self):
        if hasattr(self, 'error_label'):
            self.main_layout.removeWidget(self.error_label)
            self.error_label.deleteLater()
            del self.error_label


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Set application font
    font = QFont()
    font.setFamily("Arial")
    font.setPointSize(10)
    app.setFont(font)
    
    calculator = AdvancedBMICalculator()
    calculator.show()
    sys.exit(app.exec_())