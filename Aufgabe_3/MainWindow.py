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

        # Modell initialisieren
        self.model = None

        # Hauptlayout erstellen
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        # VTK-Render-Fenster hinzufügen
        self.vtk_widget = QVTKRenderWindowInteractor(self.central_widget)
        self.layout.addWidget(self.vtk_widget)

        # VTK-Renderer erstellen
        self.renderer = vtk.vtkRenderer()
        self.vtk_widget.GetRenderWindow().AddRenderer(self.renderer)

        # Standard-Hintergrundfarbe (schwarz) setzen
        self.renderer.SetBackground(0.0, 0.0, 0.0)

        # Menü und Toolbar einrichten
        self._create_menu()
        self._create_toolbar()

        # Statusleiste einrichten
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        # Sichtbarkeitsflag für CSYS initialisieren
        self.cs_visible = False

        self.show()

    def _create_menu(self):
        # Menüleiste erstellen
        menu_bar = self.menuBar()

        # Datei-Menü
        file_menu = menu_bar.addMenu("Datei")

        load_action = QAction("Laden", self)
        load_action.triggered.connect(self.load_model)
        file_menu.addAction(load_action)

        save_action = QAction("Speichern", self)
        save_action.triggered.connect(self.save_model)
        file_menu.addAction(save_action)

        import_action = QAction("FDD importieren", self)
        import_action.triggered.connect(self.import_fdd)
        file_menu.addAction(import_action)

        exit_action = QAction("Beenden", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Ansicht-Menü
        view_menu = menu_bar.addMenu("Ansicht")

        # Aktionen zum Untermenü "Ansicht wählen" hinzufügen
        view_menu.addAction("Iso", lambda: self.change_view("Iso"))
        view_menu.addAction("Rechts", lambda: self.change_view("Rechts"))
        view_menu.addAction("Vorne", lambda: self.change_view("Vorne"))
        view_menu.addAction("Oben", lambda: self.change_view("Oben"))

        self.setMenuBar(menu_bar)

    def _create_toolbar(self):
        # Toolbar erstellen
        toolbar = QToolBar("Ansicht Toolbar", self)
        self.addToolBar(toolbar)

        # Hintergrund-Schaltfläche mit Dropdown-Menü erstellen
        background_button = QToolButton(self)
        background_button.setText("Hintergrund")
        background_menu = QMenu(self)

        # Aktionen zum Menü hinzufügen
        black_action = QAction("Schwarz", self)
        black_action.triggered.connect(lambda: self.set_background_color(0.0, 0.0, 0.0))
        background_menu.addAction(black_action)

        white_action = QAction("Weiß", self)
        white_action.triggered.connect(lambda: self.set_background_color(1.0, 1.0, 1.0))
        background_menu.addAction(white_action)

        yellow_action = QAction("Gelb", self)
        yellow_action.triggered.connect(lambda: self.set_background_color(1.0, 1.0, 0.0))
        background_menu.addAction(yellow_action)

        # Menü für die Schaltfläche setzen
        background_button.setMenu(background_menu)
        background_button.setPopupMode(QToolButton.InstantPopup)

        # Schaltfläche zur Toolbar hinzufügen
        toolbar.addWidget(background_button)

        # CSYS-Umschalt-Schaltfläche erstellen
        csys_button = QToolButton(self)
        csys_button.setText("CSYS")
        csys_button.clicked.connect(self.toggle_csys)

        # CSYS-Schaltfläche zur Toolbar hinzufügen
        toolbar.addWidget(csys_button)

        # Fit-Schaltfläche erstellen
        fit_button = QToolButton(self)
        fit_button.setText("Anpassen")
        fit_button.clicked.connect(self.fit_model)

        # Fit-Schaltfläche zur Toolbar hinzufügen
        toolbar.addWidget(fit_button)

    def toggle_csys(self):
        """Sichtbarkeit des CSYS umschalten."""
        if self.cs_visible:
            self.renderer.RemoveActor(self.coordinate_system_actor)
            self.cs_visible = False
        else:
            self.create_csys()
            self.renderer.AddActor(self.coordinate_system_actor)
            self.cs_visible = True

        self.vtk_widget.GetRenderWindow().Render()

    def create_csys(self):
        """Koordinatensystem (CSYS) mit vtkAxesActor erstellen."""
        # Koordinatensystem (Achsen) erstellen
        self.coordinate_system_actor = vtk.vtkAxesActor()

        # Koordinatensystem vergrößern
        self.coordinate_system_actor.SetTotalLength(0.5, 0.5, 0.5)  # X-, Y-, Z-Achsen skalieren

        # Koordinatensystem in der unteren linken Ecke des VTK-Fensters positionieren
        self.coordinate_system_actor.SetPosition(0.1, 0.1, 0.0)

        # Eigenschaften des Koordinatensystems einrichten (optional)
        self.coordinate_system_actor.GetXAxisCaptionActor2D().GetTextActor().SetTextScaleModeToNone()
        self.coordinate_system_actor.GetXAxisCaptionActor2D().GetTextActor().GetTextProperty().SetFontSize(24)
        self.coordinate_system_actor.GetXAxisCaptionActor2D().GetTextActor().GetTextProperty().SetSpacing(5)  # Buchstabenabstand vergrößern

        self.coordinate_system_actor.GetYAxisCaptionActor2D().GetTextActor().SetTextScaleModeToNone()
        self.coordinate_system_actor.GetYAxisCaptionActor2D().GetTextActor().GetTextProperty().SetFontSize(24)
        self.coordinate_system_actor.GetYAxisCaptionActor2D().GetTextActor().GetTextProperty().SetSpacing(5)  # Buchstabenabstand vergrößern

        self.coordinate_system_actor.GetZAxisCaptionActor2D().GetTextActor().SetTextScaleModeToNone()
        self.coordinate_system_actor.GetZAxisCaptionActor2D().GetTextActor().GetTextProperty().SetFontSize(24)
        self.coordinate_system_actor.GetZAxisCaptionActor2D().GetTextActor().GetTextProperty().SetSpacing(5)  # Buchstabenabstand vergrößern

        # CSYS-Akteur zum Renderer hinzufügen
        self.renderer.AddActor(self.coordinate_system_actor)

    def change_view(self, view):
        """Kameraperspektive basierend auf der ausgewählten Option ändern."""
        if not self.renderer:
            return

        # Kamera an die ausgewählte Ansicht anpassen
        camera = self.renderer.GetActiveCamera()

        # Kamera auf die Standardposition für jede Ansicht zurücksetzen
        if view == "Iso":
            camera.SetPosition(1, 1, 1)
            camera.SetFocalPoint(0, 0, 0)
            camera.SetViewUp(0, 1, 0)
        elif view == "Vorne":
            # Vorderansicht um 90° um die Z-Achse drehen
            camera.SetPosition(0, 0, 1)  # Angepasste Position
            camera.SetFocalPoint(0, 0, 0)
            camera.SetViewUp(0, -1, 0)  # Angepasste ViewUp-Richtung
        elif view == "Rechts":
            # Rechtsansicht um 90° um die Z-Achse drehen
            camera.SetPosition(1, 0, 0)  # Angepasste Position
            camera.SetFocalPoint(0, 0, 0)
            camera.SetViewUp(0, 1, 0)  # Angepasste ViewUp-Richtung
        elif view == "Oben":
            camera.SetPosition(0, 1, 0)
            camera.SetFocalPoint(0, 0, 0)
            camera.SetViewUp(0, 0, 1)

        # Kamera immer zurücksetzen und die neue Ansicht anwenden
        self.renderer.ResetCamera()
        self.vtk_widget.GetRenderWindow().Render()

    def set_background_color(self, r, g, b):
        """Hintergrundfarbe des VTK-Render-Fensters setzen."""
        self.renderer.SetBackground(r, g, b)
        self.vtk_widget.GetRenderWindow().Render()

    def load_model(self):
        """Modell aus einer JSON-Datei laden."""
        file_name, _ = QFileDialog.getOpenFileName(self, "Modell laden", "", "JSON-Dateien (*.json)")
        if file_name:
            try:
                self.model = mbsModel.mbsModel()  # Modell initialisieren
                self.model.loadDatabase(file_name)  # Modell aus JSON laden
                self.status_bar.showMessage(f"Modell geladen: {file_name}")
                self.render_model()
            except Exception as e:
                QMessageBox.critical(self, "Fehler", f"Modell konnte nicht geladen werden: {e}")

    def save_model(self):
        """Aktuelles Modell in einer JSON-Datei speichern."""
        if not self.model:
            QMessageBox.warning(self, "Warnung", "Kein Modell zum Speichern vorhanden.")
            return

        file_name, _ = QFileDialog.getSaveFileName(self, "Modell speichern", "", "JSON-Dateien (*.json)")
        if file_name:
            try:
                self.model.saveDatabase(file_name)  # Modell als JSON speichern
                self.status_bar.showMessage(f"Modell gespeichert: {file_name}")
            except Exception as e:
                QMessageBox.critical(self, "Fehler", f"Modell konnte nicht gespeichert werden: {e}")

    def import_fdd(self):
        """Modell aus einer .fdd-Datei importieren."""
        file_name, _ = QFileDialog.getOpenFileName(self, "FDD-Datei importieren", "", "FDD-Dateien (*.fdd)")
        if file_name:
            try:
                self.model = mbsModel.mbsModel()  # Modell initialisieren
                if self.model.importFddFile(file_name):  # Modell aus FDD importieren
                    self.status_bar.showMessage(f"FDD-Datei importiert: {file_name}")
                    self.render_model()
                else:
                    QMessageBox.critical(self, "Fehler", "FDD-Datei konnte nicht importiert werden.")
            except Exception as e:
                QMessageBox.critical(self, "Fehler", f"FDD-Datei konnte nicht importiert werden: {e}")

    def render_model(self):
        """Modell im VTK-Fenster rendern."""
        if not self.model:
            return

        self.renderer.RemoveAllViewProps()  # Renderer leeren

        # mbsObjects zum Renderer hinzufügen
        self.model.showModel(self.renderer)  # Methode showModel des Modells verwenden

        self.renderer.ResetCamera()
        self.vtk_widget.GetRenderWindow().Render()

    def fit_model(self):
        """Modell an das Fenster anpassen."""
        self.renderer.ResetCamera()
        self.vtk_widget.GetRenderWindow().Render()

def main():
    # Anwendung und Fenster initialisieren
    app = QApplication(sys.argv)
    window = MainWindow()

    # Anfangsansicht auf "Iso" setzen
    window.change_view("Iso")

    # Wenn ein Kommandozeilenargument für die .fdd-Datei vorhanden ist, importieren
    if len(sys.argv) > 1:
        fdd_file_path = sys.argv[1]
        
        if window.model is None:
            window.model = mbsModel.mbsModel()
        window.model.importFddFile(fdd_file_path)
        window.render_model()

    # Andernfalls die reguläre GUI-Anwendung starten
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
