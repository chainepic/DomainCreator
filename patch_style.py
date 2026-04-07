import re

with open('domain_generator_gui.py', 'r', encoding='utf-8') as f:
    content = f.read()

style = """
        app.setStyle("Fusion")
        self.setStyleSheet(\"\"\"
            QMainWindow {
                background-color: #f5f6fa;
            }
            QGroupBox {
                font-weight: bold;
                border: 1px solid #dcdde1;
                border-radius: 6px;
                margin-top: 10px;
                padding-top: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
            QPushButton {
                background-color: #00a8ff;
                color: white;
                border-radius: 4px;
                padding: 6px 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0097e6;
            }
            QPushButton:pressed {
                background-color: #0086d3;
            }
            QLineEdit, QSpinBox {
                border: 1px solid #dcdde1;
                border-radius: 4px;
                padding: 4px;
                background-color: white;
            }
            QTabWidget::pane {
                border: 1px solid #dcdde1;
                border-radius: 4px;
                background-color: white;
            }
            QTabBar::tab {
                background-color: #f5f6fa;
                border: 1px solid #dcdde1;
                padding: 8px 16px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background-color: white;
                border-bottom-color: white;
                font-weight: bold;
            }
        \"\"\")
"""

# inject style after self.resize(750, 650)
content = content.replace("self.resize(750, 650)", "self.resize(750, 650)\n" + style)

with open('domain_generator_gui.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Style added.")
