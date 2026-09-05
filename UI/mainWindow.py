from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame
)
from PySide6.QtCore import Qt
import sys


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Disk Space Detective")
        self.setMinimumSize(1000, 650)

        # ==========================================
        # CENTRAL WIDGET
        # ==========================================

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main vertical layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 25, 30, 25)
        main_layout.setSpacing(20)

        central_widget.setLayout(main_layout)

        # ==========================================
        # HEADER
        # ==========================================

        title = QLabel("Disk Space Detective")
        title.setAlignment(Qt.AlignCenter)
        title.setObjectName("title")

        subtitle = QLabel(
            "Quickly find out what is using your disk space"
        )
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setObjectName("subtitle")

        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)

        # ==========================================
        # SCAN BUTTON
        # ==========================================

        scan_button = QPushButton("Start Quick Scan")
        scan_button.setFixedSize(220, 50)
        scan_button.setObjectName("scanButton")

        main_layout.addWidget(
            scan_button,
            alignment=Qt.AlignCenter
        )

        # ==========================================
        # DISK USAGE
        # ==========================================

        disk_title = QLabel("Disk Usage")
        disk_title.setObjectName("sectionTitle")

        main_layout.addWidget(disk_title)

        disk_layout = QHBoxLayout()
        disk_layout.setSpacing(15)

        # Temporary values for UI testing
        c_card = self.create_card(
            "C:\\",
            "59.6% Used"
        )

        d_card = self.create_card(
            "D:\\",
            "12.3% Used"
        )

        e_card = self.create_card(
            "E:\\",
            "80.3% Used"
        )

        disk_layout.addWidget(c_card)
        disk_layout.addWidget(d_card)
        disk_layout.addWidget(e_card)

        main_layout.addLayout(disk_layout)

        # ==========================================
        # LARGEST FOLDERS + FILES
        # ==========================================

        results_layout = QHBoxLayout()
        results_layout.setSpacing(15)

        folders_card = self.create_card(
            "Largest Folders",
            "Results will appear here"
        )

        files_card = self.create_card(
            "Largest Files",
            "Results will appear here"
        )

        results_layout.addWidget(folders_card)
        results_layout.addWidget(files_card)

        main_layout.addLayout(results_layout)

        # ==========================================
        # QUICK FINDINGS
        # ==========================================

        findings_card = QFrame()
        findings_card.setObjectName("findingsCard")

        findings_layout = QVBoxLayout()
        findings_layout.setContentsMargins(20, 15, 20, 15)
        findings_layout.setSpacing(8)

        findings_title = QLabel("Quick Findings")
        findings_title.setObjectName("cardTitle")

        findings_subtitle = QLabel(
            "Potential storage consumers found on your disk"
        )
        findings_subtitle.setObjectName("cardText")

        findings_layout.addWidget(findings_title)
        findings_layout.addWidget(findings_subtitle)

        # Finding items
        findings = [
            ("📁", "node_modules", "1.7 GB"),
            ("🐍", "Python environments", "1.2 GB"),
            ("🗑", "Temporary / cache files", "650 MB"),
            ("⚙", "__pycache__", "450 MB")
        ]

        for icon, name, size in findings:

            row = QHBoxLayout()

            icon_label = QLabel(icon)
            icon_label.setObjectName("findingIcon")

            name_label = QLabel(name)
            name_label.setObjectName("findingName")

            size_label = QLabel(size)
            size_label.setObjectName("findingSize")
            size_label.setAlignment(Qt.AlignRight)

            row.addWidget(icon_label)
            row.addWidget(name_label)
            row.addStretch()
            row.addWidget(size_label)

            findings_layout.addLayout(row)

        # Set layout AFTER adding all finding rows
        findings_card.setLayout(findings_layout)

        # Add card to main layout
        main_layout.addWidget(findings_card)

    # ==========================================
    # CREATE CARD
    # ==========================================

    def create_card(self, title, text):

        card = QFrame()
        card.setObjectName("card")

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(10)

        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setObjectName("cardTitle")

        text_label = QLabel(text)
        text_label.setAlignment(Qt.AlignCenter)
        text_label.setObjectName("cardText")

        layout.addWidget(title_label)
        layout.addWidget(text_label)

        card.setLayout(layout)

        return card


# ==============================================
# APPLICATION STYLE
# ==============================================

STYLE = """

QMainWindow {
    background-color: #0f172a;
}

QWidget {
    color: #e2e8f0;
    font-family: Arial;
}


/* ==========================================
   Main Title
   ========================================== */

#title {
    font-size: 30px;
    font-weight: bold;
    color: #f8fafc;
}


/* ==========================================
   Subtitle
   ========================================== */

#subtitle {
    font-size: 15px;
    color: #94a3b8;
}


/* ==========================================
   Section Titles
   ========================================== */

#sectionTitle {
    font-size: 20px;
    font-weight: bold;
    color: #f8fafc;
}


/* ==========================================
   Scan Button
   ========================================== */

#scanButton {
    background-color: #2563eb;
    color: white;
    border: none;
    border-radius: 10px;
    font-size: 16px;
    font-weight: bold;
}

#scanButton:hover {
    background-color: #1d4ed8;
}

#scanButton:pressed {
    background-color: #1e40af;
}


/* ==========================================
   Cards
   ========================================== */

#card {
    background-color: #1e293b;
    border: 1px solid #334155;
    border-radius: 12px;
}


/* ==========================================
   Card Title
   ========================================== */

#cardTitle {
    font-size: 18px;
    font-weight: bold;
    color: #f8fafc;
}


/* ==========================================
   Card Text
   ========================================== */

#cardText {
    font-size: 15px;
    color: #94a3b8;
}


/* ==========================================
   Quick Findings
   ========================================== */

#findingsCard {
    background-color: #1e293b;
    border: 1px solid #334155;
    border-radius: 12px;
}


/* Finding Icons */

#findingIcon {
    font-size: 18px;
    min-width: 30px;
}


/* Finding Names */

#findingName {
    font-size: 14px;
    color: #cbd5e1;
}


/* Finding Sizes */

#findingSize {
    font-size: 14px;
    font-weight: bold;
    color: #f8fafc;
}

"""


# ==============================================
# RUN APPLICATION
# ==============================================

if __name__ == "__main__":

    app = QApplication(sys.argv)

    # Apply stylesheet
    app.setStyleSheet(STYLE)

    # Create window
    window = MainWindow()

    # Show window
    window.show()

    # Start application
    sys.exit(app.exec())