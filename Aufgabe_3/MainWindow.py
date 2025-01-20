import sys
import json
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QMenuBar, QStatusBar, QFileDialog, QMessageBox
from PySide6.QtGui import QAction
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import vtk
import inputfilereader  # Make sure this is your FDD file reader
import mbsModel  # Make sure the mbsModel is correctly imported

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("3D Viewer with VTK")
        self.resize(800, 600)

        # Initialize model
        self.model = None

        # Create main layout
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        # Add VTK render window
        self.vtk_widget = QVTKRenderWindowInteractor(self.central_widget)
        self.layout.addWidget(self.vtk_widget)

        # Create VTK renderer
        self.renderer = vtk.vtkRenderer()
        self.vtk_widget.GetRenderWindow().AddRenderer(self.renderer)

        # Setup menu
        self._create_menu()

        # Setup status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        self.show()

    def _create_menu(self):
        menu_bar = QMenuBar(self)

        # File menu
        file_menu = menu_bar.addMenu("File")

        load_action = QAction("Load", self)
        load_action.triggered.connect(self.load_model)
        file_menu.addAction(load_action)

        save_action = QAction("Save", self)
        save_action.triggered.connect(self.save_model)
        file_menu.addAction(save_action)

        import_action = QAction("Import FDD", self)
        import_action.triggered.connect(self.import_fdd)
        file_menu.addAction(import_action)

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        self.setMenuBar(menu_bar)

    def load_model(self):
        """Load a model from a JSON file."""
        file_name, _ = QFileDialog.getOpenFileName(self, "Load Model", "", "JSON Files (*.json)")
        if file_name:
            try:
                with open(file_name, "r") as file:
                    data = json.load(file)
                    self.model = mbsModel.mbsModel()
                    self.model.loadDatabase(data)
                    self.status_bar.showMessage(f"Model loaded: {file_name}")
                    self.render_model()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load model: {e}")

    def save_model(self):
        """Save the current model to a JSON file."""
        if not self.model:
            QMessageBox.warning(self, "Warning", "No model to save.")
            return

        file_name, _ = QFileDialog.getSaveFileName(self, "Save Model", "", "JSON Files (*.json)")
        if file_name:
            try:
                self.model.saveDatabase(file_name)
                self.status_bar.showMessage(f"Model saved: {file_name}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save model: {e}")

    def import_fdd(self):
        """Import a model from an FDD file."""
        file_name, _ = QFileDialog.getOpenFileName(self, "Import FDD File", "", "FDD Files (*.fdd)")
        if file_name:
            try:
                self.model = mbsModel.mbsModel()
                self.model.importFddFile(file_name)
                self.status_bar.showMessage(f"FDD file imported: {file_name}")
                self.render_model()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to import FDD file: {e}")

    def render_model(self):
        """Render the model in the VTK window."""
        if not self.model:
            QMessageBox.warning(self, "Warning", "No model loaded!")
            return

        self.renderer.RemoveAllViewProps()
        self.model.showModel(self.renderer)  # Show the model in the renderer
        self.renderer.ResetCamera()
        self.vtk_widget.GetRenderWindow().Render()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
