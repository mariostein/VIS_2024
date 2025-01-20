import sys
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QStatusBar,
    QFileDialog,
    QMessageBox,
    QToolBar,
    QMenu,
    QToolButton
)
from PySide6.QtGui import QAction
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import vtk
import mbsModel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("3D-Viewer mit VTK")
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

        # Set default background color (black)
        self.renderer.SetBackground(0.0, 0.0, 0.0)

        # Setup menu and toolbar
        self._create_menu()
        self._create_toolbar()

        # Setup status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        self.show()

    def _create_menu(self):
        menu_bar = self.menuBar()

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

        # View menu
        view_menu = menu_bar.addMenu("View")

        # Add actions to the "Choose View" submenu
        view_menu.addAction("Iso", lambda: self.change_view("Iso"))
        view_menu.addAction("Right", lambda: self.change_view("Right"))
        view_menu.addAction("Front", lambda: self.change_view("Front"))
        view_menu.addAction("Top", lambda: self.change_view("Top"))

        self.setMenuBar(menu_bar)

    def _create_toolbar(self):
        # Create toolbar
        toolbar = QToolBar("View Toolbar", self)
        self.addToolBar(toolbar)

        # Create the background button with dropdown menu
        background_button = QToolButton(self)
        background_button.setText("Background")
        background_menu = QMenu(self)

        # Add actions to the menu
        black_action = QAction("Black", self)
        black_action.triggered.connect(lambda: self.set_background_color(0.0, 0.0, 0.0))
        background_menu.addAction(black_action)

        white_action = QAction("White", self)
        white_action.triggered.connect(lambda: self.set_background_color(1.0, 1.0, 1.0))
        background_menu.addAction(white_action)

        yellow_action = QAction("Yellow", self)
        yellow_action.triggered.connect(lambda: self.set_background_color(1.0, 1.0, 0.0))
        background_menu.addAction(yellow_action)

        # Set the menu for the button
        background_button.setMenu(background_menu)
        background_button.setPopupMode(QToolButton.InstantPopup)

        # Add the button to the toolbar
        toolbar.addWidget(background_button)

    def change_view(self, view):
        """Change the camera view based on the selected option."""
        if not self.renderer:
            return

        # Adjust the camera to the selected view
        camera = self.renderer.GetActiveCamera()

        # Reset the camera to the default position for each view
        if view == "Iso":
            camera.SetPosition(1, 1, 1)
            camera.SetFocalPoint(0, 0, 0)
            camera.SetViewUp(0, 1, 0)
        elif view == "Front":
            # Rotate Front view 90° about the Z-axis
            camera.SetPosition(0, 0, 1)  # Adjusted position
            camera.SetFocalPoint(0, 0, 0)
            camera.SetViewUp(0, -1, 0)  # Adjusted ViewUp direction
        elif view == "Right":
            # Rotate Right view 90° about the Z-axis
            camera.SetPosition(1, 0, 0)  # Adjusted position
            camera.SetFocalPoint(0, 0, 0)
            camera.SetViewUp(0, 1, 0)  # Adjusted ViewUp direction
        elif view == "Top":
            camera.SetPosition(0, 1, 0)
            camera.SetFocalPoint(0, 0, 0)
            camera.SetViewUp(0, 0, 1)

        # Always reset the camera and apply the new view
        self.renderer.ResetCamera()
        self.vtk_widget.GetRenderWindow().Render()

    def set_background_color(self, r, g, b):
        """Set the background color of the VTK render window."""
        self.renderer.SetBackground(r, g, b)
        self.vtk_widget.GetRenderWindow().Render()

    def load_model(self):
        """Load a model from a JSON file."""
        file_name, _ = QFileDialog.getOpenFileName(self, "Load Model", "", "JSON Files (*.json)")
        if file_name:
            try:
                self.model = mbsModel.mbsModel()  # Initialize the model
                self.model.loadDatabase(file_name)  # Load the model from JSON
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
                self.model.saveDatabase(file_name)  # Save the model as JSON
                self.status_bar.showMessage(f"Model saved: {file_name}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save model: {e}")

    def import_fdd(self):
        """Import a model from a .fdd file."""
        file_name, _ = QFileDialog.getOpenFileName(self, "Import FDD File", "", "FDD Files (*.fdd)")
        if file_name:
            try:
                self.model = mbsModel.mbsModel()  # Initialize the model
                if self.model.importFddFile(file_name):  # Import the model from FDD
                    self.status_bar.showMessage(f"FDD file imported: {file_name}")
                    self.render_model()
                else:
                    QMessageBox.critical(self, "Error", "Failed to import FDD file.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to import FDD file: {e}")

    def render_model(self):
        """Render the model in the VTK window."""
        if not self.model:
            return

        self.renderer.RemoveAllViewProps()  # Clear the renderer

        # Add mbsObjects to the renderer
        self.model.showModel(self.renderer)  # Use model's showModel method

        self.renderer.ResetCamera()
        self.vtk_widget.GetRenderWindow().Render()

def main():
    # Initialize the application and window
    app = QApplication(sys.argv)
    window = MainWindow()

    # Set the initial camera view to "Iso"
    window.change_view("Iso")

    # If there's a command-line argument for the .fdd file, import it
    if len(sys.argv) > 1:
        fdd_file_path = sys.argv[1]
        
        if window.model is None:
            window.model = mbsModel.mbsModel()
        window.model.importFddFile(fdd_file_path)
        window.render_model()

    # Otherwise, just start the regular GUI application
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
