
import sys
import os

from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QProgressBar,
    QSizePolicy,
)

# Allow imports from the project root
PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

sys.path.insert(0, PROJECT_ROOT)

from core.diskScanner import get_disks, scan_disk
from core.folderScanner import get_subfolders, get_folder_size
from core.fileScanner import get_large_files


# ============================================================
# SCAN WORKER
# ============================================================

class ScanWorker(QThread):

    status = Signal(str)
    progress = Signal(int)
    results_ready = Signal(dict)
    finished_scan = Signal()
    cancelled = Signal()

    def __init__(self, drive, scan_type):
        super().__init__()

        self.drive = drive
        self.scan_type = scan_type
        self._stop_requested = False

    def stop(self):
        self._stop_requested = True

    # ========================================================
    # QUICK FINDINGS
    # ========================================================

    def find_quick_findings(self):

        findings = {
            "node_modules": 0,
            "venv": 0,
            ".venv": 0,
            "__pycache__": 0,
            "Temp": 0,
            "Cache": 0,
        }

        # Directory names that we want to detect
        target_names = {
            "node_modules",
            "venv",
            ".venv",
            "__pycache__",
            "temp",
            "cache",
        }

        try:

            for root, dirs, files in os.walk(
                self.drive,
                topdown=True,
                onerror=lambda error: None
            ):

                if self._stop_requested:
                    return None

                directories_to_scan = []

                remaining_dirs = []

                for directory in dirs:

                    directory_lower = directory.lower()

                    if directory_lower in target_names:

                        directories_to_scan.append(
                            directory
                        )

                    else:

                        remaining_dirs.append(
                            directory
                        )

                # Do not walk into target directories again.
                # Their size will be calculated separately.
                dirs[:] = remaining_dirs

                for directory in directories_to_scan:

                    if self._stop_requested:
                        return None

                    full_path = os.path.join(
                        root,
                        directory
                    )

                    try:

                        size = get_folder_size(
                            full_path
                        )

                        directory_lower = (
                            directory.lower()
                        )

                        if directory_lower == "node_modules":

                            findings["node_modules"] += size

                        elif directory_lower == "venv":

                            findings["venv"] += size

                        elif directory_lower == ".venv":

                            findings[".venv"] += size

                        elif directory_lower == "__pycache__":

                            findings["__pycache__"] += size

                        elif directory_lower == "temp":

                            findings["Temp"] += size

                        elif directory_lower == "cache":

                            findings["Cache"] += size

                    except (
                        PermissionError,
                        OSError
                    ):

                        continue

        except (
            PermissionError,
            OSError
        ):

            pass

        return findings

    # ========================================================
    # WORKER
    # ========================================================

    def run(self):

        if self.scan_type != "Quick Scan":

            self.status.emit(
                "Deep Scan is not implemented yet."
            )

            self.finished_scan.emit()

            return

        try:

            # ------------------------------------------------
            # STEP 1 - FOLDERS
            # ------------------------------------------------

            self.status.emit(
                "Analyzing folders..."
            )

            self.progress.emit(10)

            folders = get_subfolders(
                self.drive
            )

            folder_sizes = []

            for folder in folders:

                if self._stop_requested:

                    self.cancelled.emit()

                    return

                try:

                    size = get_folder_size(
                        folder
                    )

                    folder_sizes.append(
                        (
                            folder.name,
                            size
                        )
                    )

                except (
                    PermissionError,
                    OSError
                ):

                    continue

            folder_sizes.sort(
                key=lambda item: item[1],
                reverse=True
            )

            largest_folders = (
                folder_sizes[:3]
            )

            self.progress.emit(35)

            # ------------------------------------------------
            # STEP 2 - LARGE FILES
            # ------------------------------------------------

            if self._stop_requested:

                self.cancelled.emit()

                return

            self.status.emit(
                "Finding large files..."
            )

            self.progress.emit(40)

            large_files = get_large_files(
                self.drive,
                limit=3
            )

            self.progress.emit(65)

            # ------------------------------------------------
            # STEP 3 - QUICK FINDINGS
            # ------------------------------------------------

            if self._stop_requested:

                self.cancelled.emit()

                return

            self.status.emit(
                "Checking storage consumers..."
            )

            self.progress.emit(70)

            findings = self.find_quick_findings()

            if findings is None:

                self.cancelled.emit()

                return

            self.progress.emit(90)

            # ------------------------------------------------
            # STEP 4 - RESULTS
            # ------------------------------------------------

            if self._stop_requested:

                self.cancelled.emit()

                return

            self.status.emit(
                "Preparing results..."
            )

            self.progress.emit(100)

            results = {
                "largest_folders": largest_folders,
                "largest_files": large_files,
                "findings": findings,
            }

            self.results_ready.emit(
                results
            )

            self.finished_scan.emit()

        except Exception as error:

            self.status.emit(
                f"Scan error: {error}"
            )

            self.results_ready.emit({
                "largest_folders": [],
                "largest_files": [],
                "findings": {},
            })

            self.finished_scan.emit()


# ============================================================
# MAIN WINDOW
# ============================================================

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle(
            "Disk Space Detective"
        )

        self.resize(
            1100,
            750
        )

        # ----------------------------------------------------
        # DATA
        # ----------------------------------------------------

        self.selected_drive = "C:\\"

        self.worker = None

        self.drive_data = {}

        self.drive_cards = {}

        self.drive_labels = {}

        self.quick_scan_results = {
            "largest_folders": [],
            "largest_files": [],
            "findings": {},
        }

        # ----------------------------------------------------
        # MAIN WIDGET
        # ----------------------------------------------------

        central_widget = QWidget()

        self.setCentralWidget(
            central_widget
        )

        self.main_layout = QVBoxLayout(
            central_widget
        )

        self.main_layout.setContentsMargins(
            35,
            25,
            35,
            20
        )

        self.main_layout.setSpacing(
            20
        )

        # ----------------------------------------------------
        # BACKGROUND
        # ----------------------------------------------------

        self.setStyleSheet("""
            QMainWindow {
                background-color: #0f172a;
            }

            QWidget {
                color: #f8fafc;
                font-family: Arial;
            }

            QLabel {
                color: #f8fafc;
            }

            QPushButton {
                border: none;
            }
        """)

        # ----------------------------------------------------
        # BUILD UI
        # ----------------------------------------------------

        self.create_navbar()

        self.create_status()

        self.create_hero()

        self.create_disk_section()

        self.create_scan_buttons()

        self.create_results_card()

        self.create_footer()

        # ----------------------------------------------------
        # LOAD REAL DISKS
        # ----------------------------------------------------

        self.load_drive_data()


    # ========================================================
    # NAVBAR
    # ========================================================

    def create_navbar(self):

        navbar = QHBoxLayout()

        navbar.setSpacing(
            25
        )

        # Logo
        logo = QLabel(
            "Disk Space Detective"
        )

        logo.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
        """)

        navbar.addWidget(
            logo
        )

        navbar.addStretch()

        # Main
        main_button = QPushButton(
            "Main"
        )

        main_button.setStyleSheet("""
            QPushButton {
                color: #f8fafc;
                font-size: 14px;
                padding: 8px 12px;
            }

            QPushButton:hover {
                color: #60a5fa;
            }
        """)

        navbar.addWidget(
            main_button
        )

        # Help
        help_button = QPushButton(
            "Help"
        )

        help_button.setStyleSheet("""
            QPushButton {
                color: #94a3b8;
                font-size: 14px;
                padding: 8px 12px;
            }

            QPushButton:hover {
                color: #f8fafc;
            }
        """)

        navbar.addWidget(
            help_button
        )

        # Contact
        contact_button = QPushButton(
            "Contact"
        )

        contact_button.setStyleSheet("""
            QPushButton {
                color: #94a3b8;
                font-size: 14px;
                padding: 8px 12px;
            }

            QPushButton:hover {
                color: #f8fafc;
            }
        """)

        navbar.addWidget(
            contact_button
        )

        # Refresh
        refresh_button = QPushButton(
            "↻"
        )

        refresh_button.setFixedSize(
            40,
            40
        )

        refresh_button.setStyleSheet("""
            QPushButton {
                background-color: #1e293b;
                border: 1px solid #334155;
                border-radius: 8px;
                color: #f8fafc;
                font-size: 22px;
            }

            QPushButton:hover {
                background-color: #334155;
            }
        """)

        refresh_button.clicked.connect(
            self.refresh_data
        )

        navbar.addWidget(
            refresh_button
        )

        self.main_layout.addLayout(
            navbar
        )


    # ========================================================
    # STATUS
    # ========================================================

    def create_status(self):

        self.status_label = QLabel(
            "Ready"
        )

        self.status_label.setStyleSheet("""
            color: #94a3b8;
            font-size: 13px;
        """)

        self.main_layout.addWidget(
            self.status_label
        )


    # ========================================================
    # HERO
    # ========================================================

    def create_hero(self):

        hero_layout = QVBoxLayout()

        hero_layout.setSpacing(
            8
        )

        hero_layout.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        title = QLabel(
            "Understand what's using your storage"
        )

        title.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        title.setStyleSheet("""
            font-size: 30px;
            font-weight: bold;
            margin-top: 5px;
        """)

        subtitle = QLabel(
            "Select a drive and start a scan to discover "
            "where your storage space is being used."
        )

        subtitle.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        subtitle.setStyleSheet("""
            color: #94a3b8;
            font-size: 15px;
        """)

        hero_layout.addWidget(
            title
        )

        hero_layout.addWidget(
            subtitle
        )

        self.main_layout.addLayout(
            hero_layout
        )


    # ========================================================
    # DISK SECTION
    # ========================================================

    def create_disk_section(self):

        title = QLabel(
            "Disk Usage"
        )

        title.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
        """)

        self.main_layout.addWidget(
            title
        )

        self.drive_layout = QHBoxLayout()

        self.drive_layout.setSpacing(
            15
        )

        self.main_layout.addLayout(
            self.drive_layout
        )


    # ========================================================
    # LOAD DISK DATA
    # ========================================================

    def load_drive_data(self):

        while self.drive_layout.count():

            item = self.drive_layout.takeAt(0)

            widget = item.widget()

            if widget:

                widget.deleteLater()

        self.drive_cards.clear()

        self.drive_labels.clear()

        self.drive_data.clear()

        try:

            partitions = get_disks()

            if not partitions:

                self.status_label.setText(
                    "No drives found."
                )

                return

            for index, partition in enumerate(
                partitions
            ):

                try:

                    data = scan_disk(
                        index
                    )

                    drive = data["drive"]

                    self.drive_data[
                        drive
                    ] = data

                    self.create_drive_card(
                        drive,
                        data
                    )

                except (
                    PermissionError,
                    OSError
                ):

                    continue

            if self.drive_data:

                if (
                    self.selected_drive
                    not in self.drive_data
                ):

                    self.selected_drive = (
                        next(
                            iter(
                                self.drive_data
                            )
                        )
                    )

                self.update_drive_selection()

                self.status_label.setText(
                    "Ready"
                )

        except Exception as error:

            self.status_label.setText(
                f"Unable to load drives: {error}"
            )


    # ========================================================
    # DRIVE CARD
    # ========================================================

    def create_drive_card(
        self,
        drive,
        data
    ):

        card = QFrame()

        card.setFixedHeight(
            120
        )

        card.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed
        )

        card.setStyleSheet("""
            QFrame {
                background-color: #1e293b;
                border: 1px solid #334155;
                border-radius: 12px;
            }
        """)

        layout = QVBoxLayout(
            card
        )

        layout.setContentsMargins(
            18,
            15,
            18,
            15
        )

        layout.setSpacing(
            5
        )

        drive_label = QLabel(
            drive
        )

        drive_label.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
        """)

        usage_label = QLabel(
            f"{data['used_percent']}% used"
        )

        usage_label.setStyleSheet("""
            color: #94a3b8;
            font-size: 13px;
        """)

        space_label = QLabel(
            f"{self.format_size(data['free'])} free"
        )

        space_label.setStyleSheet("""
            color: #94a3b8;
            font-size: 13px;
        """)

        layout.addWidget(
            drive_label
        )

        layout.addWidget(
            usage_label
        )

        layout.addWidget(
            space_label
        )

        self.drive_layout.addWidget(
            card
        )

        self.drive_cards[
            drive
        ] = card

        self.drive_labels[
            drive
        ] = (
            usage_label,
            space_label
        )

        card.mousePressEvent = (
            lambda event, d=drive:
            self.select_drive(d)
        )


    # ========================================================
    # SELECT DRIVE
    # ========================================================

    def select_drive(
        self,
        drive
    ):

        if (
            self.worker
            and self.worker.isRunning()
        ):

            return

        self.selected_drive = drive

        self.update_drive_selection()

        self.status_label.setText(
            f"{drive} selected"
        )


    # ========================================================
    # UPDATE DRIVE SELECTION
    # ========================================================

    def update_drive_selection(self):

        for drive, card in (
            self.drive_cards.items()
        ):

            if drive == self.selected_drive:

                card.setStyleSheet("""
                    QFrame {
                        background-color: #1e293b;
                        border: 2px solid #2563eb;
                        border-radius: 12px;
                    }
                """)

            else:

                card.setStyleSheet("""
                    QFrame {
                        background-color: #1e293b;
                        border: 1px solid #334155;
                        border-radius: 12px;
                    }
                """)


    # ========================================================
    # SCAN BUTTONS
    # ========================================================

    def create_scan_buttons(self):

        button_layout = QHBoxLayout()

        button_layout.setSpacing(
            15
        )

        # ----------------------------------------------------
        # QUICK SCAN
        # ----------------------------------------------------

        quick_button_frame = QFrame()

        quick_button_frame.setStyleSheet("""
            QFrame {
                background-color: #1e293b;
                border: 1px solid #334155;
                border-radius: 12px;
            }
        """)

        quick_layout = QVBoxLayout(
            quick_button_frame
        )

        quick_layout.setContentsMargins(
            18,
            15,
            18,
            15
        )

        quick_button = QPushButton(
            "Quick Scan"
        )

        quick_button.setFixedHeight(
            42
        )

        quick_button.setStyleSheet("""
            QPushButton {
                background-color: #2563eb;
                color: white;
                border-radius: 8px;
                font-size: 15px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #1d4ed8;
            }

            QPushButton:disabled {
                background-color: #475569;
            }
        """)

        quick_button.clicked.connect(
            lambda: self.start_scan(
                "Quick Scan"
            )
        )

        quick_description = QLabel(
            "Fast overview of your storage"
        )

        quick_description.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        quick_description.setStyleSheet("""
            color: #94a3b8;
            font-size: 13px;
        """)

        quick_layout.addWidget(
            quick_button
        )

        quick_layout.addWidget(
            quick_description
        )

        # ----------------------------------------------------
        # DEEP SCAN
        # ----------------------------------------------------

        deep_button_frame = QFrame()

        deep_button_frame.setStyleSheet("""
            QFrame {
                background-color: #1e293b;
                border: 1px solid #334155;
                border-radius: 12px;
            }
        """)

        deep_layout = QVBoxLayout(
            deep_button_frame
        )

        deep_layout.setContentsMargins(
            18,
            15,
            18,
            15
        )

        deep_button = QPushButton(
            "Deep Scan"
        )

        deep_button.setFixedHeight(
            42
        )

        deep_button.setStyleSheet("""
            QPushButton {
                background-color: #334155;
                color: #f8fafc;
                border-radius: 8px;
                font-size: 15px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #475569;
            }

            QPushButton:disabled {
                background-color: #1e293b;
            }
        """)

        deep_button.clicked.connect(
            lambda: self.start_scan(
                "Deep Scan"
            )
        )

        deep_description = QLabel(
            "Detailed analysis of files & folders"
        )

        deep_description.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        deep_description.setStyleSheet("""
            color: #94a3b8;
            font-size: 13px;
        """)

        deep_layout.addWidget(
            deep_button
        )

        deep_layout.addWidget(
            deep_description
        )

        button_layout.addWidget(
            quick_button_frame
        )

        button_layout.addWidget(
            deep_button_frame
        )

        self.main_layout.addLayout(
            button_layout
        )

        self.quick_button = quick_button

        self.deep_button = deep_button


    # ========================================================
    # RESULTS CARD
    # ========================================================

    def create_results_card(self):

        self.results_card = QFrame()

        self.results_card.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )

        self.results_card.setStyleSheet("""
            QFrame {
                background-color: #1e293b;
                border: 1px solid #334155;
                border-radius: 12px;
            }
        """)

        self.results_layout = QVBoxLayout(
            self.results_card
        )

        self.results_layout.setContentsMargins(
            25,
            20,
            25,
            20
        )

        self.results_layout.setSpacing(
            15
        )

        self.main_layout.addWidget(
            self.results_card
        )

        self.show_welcome_results()


    # ========================================================
    # WELCOME RESULTS
    # ========================================================

    def show_welcome_results(self):

        self.clear_results()

        title = QLabel(
            "Scan Results"
        )

        title.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
        """)

        message = QLabel(
            "Select a drive and start a Quick Scan "
            "to see where your storage is being used."
        )

        message.setWordWrap(
            True
        )

        message.setStyleSheet("""
            color: #94a3b8;
            font-size: 14px;
        """)

        self.results_layout.addWidget(
            title
        )

        self.results_layout.addWidget(
            message
        )

        self.results_layout.addStretch()


    # ========================================================
    # START SCAN
    # ========================================================

    def start_scan(
        self,
        scan_type
    ):

        if (
            self.worker
            and self.worker.isRunning()
        ):

            return

        if not self.selected_drive:

            self.status_label.setText(
                "Please select a drive first."
            )

            return

        self.quick_scan_results = {
            "largest_folders": [],
            "largest_files": [],
            "findings": {},
        }

        self.worker = ScanWorker(
            self.selected_drive,
            scan_type
        )

        self.worker.status.connect(
            self.update_scan_status
        )

        self.worker.progress.connect(
            self.update_scan_progress
        )

        self.worker.results_ready.connect(
            self.store_scan_results
        )

        self.worker.finished_scan.connect(
            self.scan_finished
        )

        self.worker.cancelled.connect(
            self.scan_cancelled
        )

        self.quick_button.setEnabled(
            False
        )

        self.deep_button.setEnabled(
            False
        )

        self.show_scanning_results(
            scan_type
        )

        self.worker.start()


    # ========================================================
    # SCAN STATUS
    # ========================================================

    def update_scan_status(
        self,
        message
    ):

        self.status_label.setText(
            message
        )

        self.scan_status_label.setText(
            message
        )


    # ========================================================
    # SCAN PROGRESS
    # ========================================================

    def update_scan_progress(
        self,
        value
    ):

        self.progress_bar.setValue(
            value
        )


    # ========================================================
    # STORE RESULTS
    # ========================================================

    def store_scan_results(
        self,
        results
    ):

        self.quick_scan_results = results


    # ========================================================
    # SCAN FINISHED
    # ========================================================

    def scan_finished(self):

        self.quick_button.setEnabled(
            True
        )

        self.deep_button.setEnabled(
            True
        )

        self.status_label.setText(
            "Scan completed"
        )

        self.show_quick_results()

        self.worker = None


    # ========================================================
    # SCAN CANCELLED
    # ========================================================

    def scan_cancelled(self):

        self.quick_button.setEnabled(
            True
        )

        self.deep_button.setEnabled(
            True
        )

        self.status_label.setText(
            "Scan stopped"
        )

        self.worker = None

        self.show_welcome_results()


    # ========================================================
    # SCANNING SCREEN
    # ========================================================

    def show_scanning_results(
        self,
        scan_type
    ):

        self.clear_results()

        title = QLabel(
            scan_type
        )

        title.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
        """)

        self.scan_status_label = QLabel(
            "Starting scan..."
        )

        self.scan_status_label.setStyleSheet("""
            color: #94a3b8;
            font-size: 14px;
        """)

        self.progress_bar = QProgressBar()

        self.progress_bar.setValue(
            0
        )

        self.progress_bar.setTextVisible(
            True
        )

        self.progress_bar.setStyleSheet("""
            QProgressBar {
                background-color: #0f172a;
                border: 1px solid #334155;
                border-radius: 7px;
                height: 14px;
                text-align: center;
                color: #f8fafc;
            }

            QProgressBar::chunk {
                background-color: #2563eb;
                border-radius: 6px;
            }
        """)

        stop_button = QPushButton(
            "Stop Scan"
        )

        stop_button.setFixedHeight(
            40
        )

        stop_button.setStyleSheet("""
            QPushButton {
                background-color: #334155;
                color: #f8fafc;
                border-radius: 8px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #475569;
            }
        """)

        stop_button.clicked.connect(
            self.stop_scan
        )

        self.results_layout.addWidget(
            title
        )

        self.results_layout.addWidget(
            self.scan_status_label
        )

        self.results_layout.addWidget(
            self.progress_bar
        )

        self.results_layout.addStretch()

        self.results_layout.addWidget(
            stop_button
        )


    # ========================================================
    # STOP SCAN
    # ========================================================

    def stop_scan(self):

        if (
            self.worker
            and self.worker.isRunning()
        ):

            self.worker.stop()

            self.status_label.setText(
                "Stopping scan..."
            )


    # ========================================================
    # QUICK RESULTS
    # ========================================================

    def show_quick_results(self):

        self.clear_results()

        # ----------------------------------------------------
        # TITLE
        # ----------------------------------------------------

        title = QLabel(
            f"Quick Scan Results — "
            f"{self.selected_drive}"
        )

        title.setStyleSheet("""
            font-size: 19px;
            font-weight: bold;
        """)

        self.results_layout.addWidget(
            title
        )

        # ----------------------------------------------------
        # DISK USAGE
        # ----------------------------------------------------

        disk_title = QLabel(
            "Disk Usage"
        )

        disk_title.setStyleSheet("""
            font-size: 15px;
            font-weight: bold;
        """)

        self.results_layout.addWidget(
            disk_title
        )

        disk = self.drive_data.get(
            self.selected_drive
        )

        if disk:

            disk_info = QLabel(
                f"Total: {self.format_size(disk['total'])}    "
                f"Used: {self.format_size(disk['used'])}    "
                f"Free: {self.format_size(disk['free'])}    "
                f"({disk['used_percent']}% used)"
            )

            disk_info.setStyleSheet("""
                color: #94a3b8;
                font-size: 14px;
            """)

            self.results_layout.addWidget(
                disk_info
            )

        # ----------------------------------------------------
        # TOP 3 FOLDERS
        # ----------------------------------------------------

        folder_title = QLabel(
            "Top 3 Largest Folders"
        )

        folder_title.setStyleSheet("""
            font-size: 15px;
            font-weight: bold;
            margin-top: 8px;
        """)

        self.results_layout.addWidget(
            folder_title
        )

        largest_folders = (
            self.quick_scan_results.get(
                "largest_folders",
                []
            )
        )

        if largest_folders:

            for folder_name, size in (
                largest_folders
            ):

                self.add_result_row(
                    folder_name,
                    self.format_size(size)
                )

        else:

            empty_label = QLabel(
                "No folder information found."
            )

            empty_label.setStyleSheet("""
                color: #94a3b8;
            """)

            self.results_layout.addWidget(
                empty_label
            )

        # ----------------------------------------------------
        # TOP 3 FILES
        # ----------------------------------------------------

        file_title = QLabel(
            "Top 3 Largest Files"
        )

        file_title.setStyleSheet("""
            font-size: 15px;
            font-weight: bold;
            margin-top: 8px;
        """)

        self.results_layout.addWidget(
            file_title
        )

        largest_files = (
            self.quick_scan_results.get(
                "largest_files",
                []
            )
        )

        if largest_files:

            for file_path, size in (
                largest_files
            ):

                file_name = os.path.basename(
                    str(file_path)
                )

                self.add_result_row(
                    file_name,
                    self.format_size(size)
                )

        else:

            empty_label = QLabel(
                "No large files found."
            )

            empty_label.setStyleSheet("""
                color: #94a3b8;
            """)

            self.results_layout.addWidget(
                empty_label
            )

        # ----------------------------------------------------
        # QUICK FINDINGS
        # ----------------------------------------------------

        findings_title = QLabel(
            "Quick Findings"
        )

        findings_title.setStyleSheet("""
            font-size: 15px;
            font-weight: bold;
            margin-top: 8px;
        """)

        self.results_layout.addWidget(
            findings_title
        )

        findings = (
            self.quick_scan_results.get(
                "findings",
                {}
            )
        )

        found_anything = False

        if isinstance(
            findings,
            dict
        ):

            finding_order = [
                (
                    "node_modules",
                    "node_modules"
                ),
                (
                    "venv",
                    "venv"
                ),
                (
                    ".venv",
                    ".venv"
                ),
                (
                    "__pycache__",
                    "__pycache__"
                ),
                (
                    "Temp",
                    "Temp"
                ),
                (
                    "Cache",
                    "Cache"
                ),
            ]

            for key, display_name in (
                finding_order
            ):

                size = findings.get(
                    key,
                    0
                )

                if size > 0:

                    found_anything = True

                    self.add_result_row(
                        f"{display_name} found",
                        self.format_size(size)
                    )

        if not found_anything:

            finding_label = QLabel(
                "No common storage consumers found."
            )

            finding_label.setStyleSheet("""
                color: #94a3b8;
                font-size: 13px;
            """)

            self.results_layout.addWidget(
                finding_label
            )

        self.results_layout.addStretch()


    # ========================================================
    # RESULT ROW
    # ========================================================

    def add_result_row(
        self,
        name,
        size
    ):

        row = QFrame()

        row.setStyleSheet("""
            QFrame {
                background-color: #0f172a;
                border: 1px solid #334155;
                border-radius: 8px;
            }
        """)

        layout = QHBoxLayout(
            row
        )

        layout.setContentsMargins(
            12,
            8,
            12,
            8
        )

        name_label = QLabel(
            str(name)
        )

        name_label.setStyleSheet("""
            color: #f8fafc;
            font-size: 13px;
        """)

        size_label = QLabel(
            str(size)
        )

        size_label.setAlignment(
            Qt.AlignmentFlag.AlignRight
        )

        size_label.setStyleSheet("""
            color: #60a5fa;
            font-size: 13px;
            font-weight: bold;
        """)

        layout.addWidget(
            name_label
        )

        layout.addStretch()

        layout.addWidget(
            size_label
        )

        self.results_layout.addWidget(
            row
        )


    # ========================================================
    # CLEAR RESULTS
    # ========================================================

    def clear_results(self):

        while self.results_layout.count():

            item = self.results_layout.takeAt(
                0
            )

            widget = item.widget()

            if widget:

                widget.deleteLater()


    # ========================================================
    # REFRESH
    # ========================================================

    def refresh_data(self):

        if (
            self.worker
            and self.worker.isRunning()
        ):

            return

        self.status_label.setText(
            "Refreshing disk information..."
        )

        self.load_drive_data()

        self.show_welcome_results()


    # ========================================================
    # FORMAT SIZE
    # ========================================================

    def format_size(
        self,
        size
    ):

        units = [
            "B",
            "KB",
            "MB",
            "GB",
            "TB",
            "PB"
        ]

        size = float(size)

        for unit in units:

            if size < 1024:

                return f"{size:.2f} {unit}"

            size /= 1024

        return f"{size:.2f} PB"


    # ========================================================
    # FOOTER
    # ========================================================

    def create_footer(self):

        footer = QLabel(
            "Disk Space Detective • Version 1.0.0"
        )

        footer.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        footer.setStyleSheet("""
            color: #64748b;
            font-size: 12px;
            padding-top: 5px;
        """)

        self.main_layout.addWidget(
            footer
        )


# ============================================================
# APPLICATION
# ============================================================

if __name__ == "__main__":

    app = QApplication(
        sys.argv
    )

    window = MainWindow()

    window.show()

    sys.exit(
        app.exec()
    )
