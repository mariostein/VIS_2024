import sys  # Importiert das Modul sys
from PySide6.QtWidgets import (  # Importiert verschiedene Widgets aus dem Modul PySide6.QtWidgets
    QApplication,  # Importiert QApplication
    QMainWindow,  # Importiert QMainWindow
    QVBoxLayout,  # Importiert QVBoxLayout
    QWidget,  # Importiert QWidget
    QStatusBar,  # Importiert QStatusBar
    QFileDialog,  # Importiert QFileDialog
    QMessageBox,  # Importiert QMessageBox
    QToolBar,  # Importiert QToolBar
    QMenu,  # Importiert QMenu
    QToolButton  # Importiert QToolButton
)
from PySide6.QtGui import QAction  # Importiert QAction aus dem Modul PySide6.QtGui
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor  # Importiert QVTKRenderWindowInteractor aus vtkmodules.qt
import vtk  # Importiert das Modul vtk
import mbsModel  # Importiert das Modul mbsModel

class MainWindow(QMainWindow):  # Definiert die Klasse MainWindow, die von QMainWindow erbt
    def __init__(self):  # Initialisiert eine Instanz der Klasse MainWindow
        super().__init__()  # Ruft den Initialisierer der Elternklasse auf

        self.setWindowTitle("3D-Viewer mit VTK")  # Setzt den Fenstertitel
        self.resize(800, 600)  # Setzt die Fenstergröße

        # Modell initialisieren
        self.model = None  # Initialisiert das Modell als None

        # Hauptlayout erstellen
        self.central_widget = QWidget(self)  # Erstellt ein zentrales Widget
        self.setCentralWidget(self.central_widget)  # Setzt das zentrale Widget

        self.layout = QVBoxLayout(self.central_widget)  # Erstellt ein vertikales Layout

        # VTK-Render-Fenster hinzufügen
        self.vtk_widget = QVTKRenderWindowInteractor(self.central_widget)  # Erstellt ein VTK-Render-Fenster
        self.layout.addWidget(self.vtk_widget)  # Fügt das VTK-Render-Fenster zum Layout hinzu

        # VTK-Renderer erstellen
        self.renderer = vtk.vtkRenderer()  # Erstellt einen VTK-Renderer
        self.vtk_widget.GetRenderWindow().AddRenderer(self.renderer)  # Fügt den Renderer zum VTK-Render-Fenster hinzu

        # Standard-Hintergrundfarbe (schwarz) setzen
        self.renderer.SetBackground(0.0, 0.0, 0.0)  # Setzt die Hintergrundfarbe des Renderers auf schwarz

        # Menü und Toolbar einrichten
        self._create_menu()  # Ruft die Methode zum Erstellen des Menüs auf
        self._create_toolbar()  # Ruft die Methode zum Erstellen der Toolbar auf

        # Statusleiste einrichten
        self.status_bar = QStatusBar()  # Erstellt eine Statusleiste
        self.setStatusBar(self.status_bar)  # Setzt die Statusleiste

        # Sichtbarkeitsflag für CSYS initialisieren
        self.cs_visible = False  # Initialisiert das Sichtbarkeitsflag für das Koordinatensystem als False

        self.show()  # Zeigt das Hauptfenster an

    def _create_menu(self):  # Definiert die Methode zum Erstellen des Menüs
        # Menüleiste erstellen
        menu_bar = self.menuBar()  # Erstellt eine Menüleiste

        # Datei-Menü
        file_menu = menu_bar.addMenu("Datei")  # Fügt ein "Datei"-Menü zur Menüleiste hinzu

        load_action = QAction("Laden", self)  # Erstellt eine "Laden"-Aktion
        load_action.triggered.connect(self.load_model)  # Verbindet die "Laden"-Aktion mit der Methode load_model
        file_menu.addAction(load_action)  # Fügt die "Laden"-Aktion zum "Datei"-Menü hinzu

        save_action = QAction("Speichern", self)  # Erstellt eine "Speichern"-Aktion
        save_action.triggered.connect(self.save_model)  # Verbindet die "Speichern"-Aktion mit der Methode save_model
        file_menu.addAction(save_action)  # Fügt die "Speichern"-Aktion zum "Datei"-Menü hinzu

        import_action = QAction("FDD importieren", self)  # Erstellt eine "FDD importieren"-Aktion
        import_action.triggered.connect(self.import_fdd)  # Verbindet die "FDD importieren"-Aktion mit der Methode import_fdd
        file_menu.addAction(import_action)  # Fügt die "FDD importieren"-Aktion zum "Datei"-Menü hinzu

        exit_action = QAction("Beenden", self)  # Erstellt eine "Beenden"-Aktion
        exit_action.triggered.connect(self.close)  # Verbindet die "Beenden"-Aktion mit der Methode close
        file_menu.addAction(exit_action)  # Fügt die "Beenden"-Aktion zum "Datei"-Menü hinzu

        # Ansicht-Menü
        view_menu = menu_bar.addMenu("Ansicht")  # Fügt ein "Ansicht"-Menü zur Menüleiste hinzu

        # Aktionen zum Untermenü "Ansicht wählen" hinzufügen
        view_menu.addAction("Iso", lambda: self.change_view("Iso"))  # Fügt eine "Iso"-Aktion zum "Ansicht"-Menü hinzu
        view_menu.addAction("Rechts", lambda: self.change_view("Rechts"))  # Fügt eine "Rechts"-Aktion zum "Ansicht"-Menü hinzu
        view_menu.addAction("Vorne", lambda: self.change_view("Vorne"))  # Fügt eine "Vorne"-Aktion zum "Ansicht"-Menü hinzu
        view_menu.addAction("Oben", lambda: self.change_view("Oben"))  # Fügt eine "Oben"-Aktion zum "Ansicht"-Menü hinzu

        self.setMenuBar(menu_bar)  # Setzt die Menüleiste

    def _create_toolbar(self):  # Definiert die Methode zum Erstellen der Toolbar
        # Toolbar erstellen
        toolbar = QToolBar("Ansicht Toolbar", self)  # Erstellt eine Toolbar mit dem Titel "Ansicht Toolbar"
        self.addToolBar(toolbar)  # Fügt die Toolbar zum Hauptfenster hinzu

        # Hintergrund-Schaltfläche mit Dropdown-Menü erstellen
        background_button = QToolButton(self)  # Erstellt eine Schaltfläche für den Hintergrund
        background_button.setText("Hintergrund")  # Setzt den Text der Schaltfläche auf "Hintergrund"
        background_menu = QMenu(self)  # Erstellt ein Menü für die Hintergrund-Schaltfläche

        # Aktionen zum Menü hinzufügen
        black_action = QAction("Schwarz", self)  # Erstellt eine "Schwarz"-Aktion
        black_action.triggered.connect(lambda: self.set_background_color(0.0, 0.0, 0.0))  # Verbindet die "Schwarz"-Aktion mit der Methode set_background_color
        background_menu.addAction(black_action)  # Fügt die "Schwarz"-Aktion zum Hintergrund-Menü hinzu

        white_action = QAction("Weiß", self)  # Erstellt eine "Weiß"-Aktion
        white_action.triggered.connect(lambda: self.set_background_color(1.0, 1.0, 1.0))  # Verbindet die "Weiß"-Aktion mit der Methode set_background_color
        background_menu.addAction(white_action)  # Fügt die "Weiß"-Aktion zum Hintergrund-Menü hinzu

        yellow_action = QAction("Gelb", self)  # Erstellt eine "Gelb"-Aktion
        yellow_action.triggered.connect(lambda: self.set_background_color(1.0, 1.0, 0.0))  # Verbindet die "Gelb"-Aktion mit der Methode set_background_color
        background_menu.addAction(yellow_action)  # Fügt die "Gelb"-Aktion zum Hintergrund-Menü hinzu

        # Menü für die Schaltfläche setzen
        background_button.setMenu(background_menu)  # Setzt das Menü für die Hintergrund-Schaltfläche
        background_button.setPopupMode(QToolButton.InstantPopup)  # Setzt den Popup-Modus der Schaltfläche auf InstantPopup

        # Schaltfläche zur Toolbar hinzufügen
        toolbar.addWidget(background_button)  # Fügt die Hintergrund-Schaltfläche zur Toolbar hinzu

        # CSYS-Umschalt-Schaltfläche erstellen
        csys_button = QToolButton(self)  # Erstellt eine Schaltfläche für das Koordinatensystem
        csys_button.setText("CSYS")  # Setzt den Text der Schaltfläche auf "CSYS"
        csys_button.clicked.connect(self.toggle_csys)  # Verbindet die Schaltfläche mit der Methode toggle_csys

        # CSYS-Schaltfläche zur Toolbar hinzufügen
        toolbar.addWidget(csys_button)  # Fügt die CSYS-Schaltfläche zur Toolbar hinzu

        # Fit-Schaltfläche erstellen
        fit_button = QToolButton(self)  # Erstellt eine Schaltfläche zum Anpassen
        fit_button.setText("Anpassen")  # Setzt den Text der Schaltfläche auf "Anpassen"
        fit_button.clicked.connect(self.fit_model)  # Verbindet die Schaltfläche mit der Methode fit_model

        # Fit-Schaltfläche zur Toolbar hinzufügen
        toolbar.addWidget(fit_button)  # Fügt die Fit-Schaltfläche zur Toolbar hinzu

    def toggle_csys(self):  # Definiert die Methode zum Umschalten der Sichtbarkeit des Koordinatensystems
        """Sichtbarkeit des CSYS umschalten."""
        if self.cs_visible:  # Überprüft, ob das Koordinatensystem sichtbar ist
            self.renderer.RemoveActor(self.coordinate_system_actor)  # Entfernt den Koordinatensystem-Akteur vom Renderer
            self.cs_visible = False  # Setzt das Sichtbarkeitsflag auf False
        else:
            self.create_csys()  # Erstellt das Koordinatensystem
            self.renderer.AddActor(self.coordinate_system_actor)  # Fügt den Koordinatensystem-Akteur zum Renderer hinzu
            self.cs_visible = True  # Setzt das Sichtbarkeitsflag auf True

        self.vtk_widget.GetRenderWindow().Render()  # Aktualisiert das Render-Fenster

    def create_csys(self):  # Definiert die Methode zum Erstellen des Koordinatensystems
        """Koordinatensystem (CSYS) mit vtkAxesActor erstellen."""
        # Koordinatensystem (Achsen) erstellen
        self.coordinate_system_actor = vtk.vtkAxesActor()  # Erstellt einen vtkAxesActor für das Koordinatensystem

        # Koordinatensystem vergrößern
        self.coordinate_system_actor.SetTotalLength(0.5, 0.5, 0.5)  # X-, Y-, Z-Achsen skalieren

        # Koordinatensystem in der unteren linken Ecke des VTK-Fensters positionieren
        self.coordinate_system_actor.SetPosition(0.1, 0.1, 0.0)  # Setzt die Position des Koordinatensystems

        # Eigenschaften des Koordinatensystems einrichten (optional)
        self.coordinate_system_actor.GetXAxisCaptionActor2D().GetTextActor().SetTextScaleModeToNone()  # Setzt den Textskalierungsmodus der X-Achse
        self.coordinate_system_actor.GetXAxisCaptionActor2D().GetTextActor().GetTextProperty().SetFontSize(24)  # Setzt die Schriftgröße der X-Achse
        self.coordinate_system_actor.GetXAxisCaptionActor2D().GetTextActor().GetTextProperty().SetSpacing(5)  # Buchstabenabstand vergrößern

        self.coordinate_system_actor.GetYAxisCaptionActor2D().GetTextActor().SetTextScaleModeToNone()  # Setzt den Textskalierungsmodus der Y-Achse
        self.coordinate_system_actor.GetYAxisCaptionActor2D().GetTextActor().GetTextProperty().SetFontSize(24)  # Setzt die Schriftgröße der Y-Achse
        self.coordinate_system_actor.GetYAxisCaptionActor2D().GetTextActor().GetTextProperty().SetSpacing(5)  # Buchstabenabstand vergrößern

        self.coordinate_system_actor.GetZAxisCaptionActor2D().GetTextActor().SetTextScaleModeToNone()  # Setzt den Textskalierungsmodus der Z-Achse
        self.coordinate_system_actor.GetZAxisCaptionActor2D().GetTextActor().GetTextProperty().SetFontSize(24)  # Setzt die Schriftgröße der Z-Achse
        self.coordinate_system_actor.GetZAxisCaptionActor2D().GetTextActor().GetTextProperty().SetSpacing(5)  # Buchstabenabstand vergrößern

        # CSYS-Akteur zum Renderer hinzufügen
        self.renderer.AddActor(self.coordinate_system_actor)  # Fügt den Koordinatensystem-Akteur zum Renderer hinzu

    def change_view(self, view):  # Definiert die Methode zum Ändern der Kameraperspektive
        """Kameraperspektive basierend auf der ausgewählten Option ändern."""
        if not self.renderer:  # Überprüft, ob der Renderer vorhanden ist
            return

        # Kamera an die ausgewählte Ansicht anpassen
        camera = self.renderer.GetActiveCamera()  # Holt die aktive Kamera des Renderers

        # Kamera auf die Standardposition für jede Ansicht zurücksetzen
        if view == "Iso":  # Überprüft, ob die Ansicht "Iso" ist
            camera.SetPosition(1, 1, 1)  # Setzt die Kameraposition
            camera.SetFocalPoint(0, 0, 0)  # Setzt den Fokuspunkt der Kamera
            camera.SetViewUp(0, 1, 0)  # Setzt die ViewUp-Richtung der Kamera
        elif view == "Vorne":  # Überprüft, ob die Ansicht "Vorne" ist
            # Vorderansicht um 90° um die Z-Achse drehen
            camera.SetPosition(0, 0, 1)  # Angepasste Position
            camera.SetFocalPoint(0, 0, 0)  # Setzt den Fokuspunkt der Kamera
            camera.SetViewUp(0, 1, 0)  # Angepasste ViewUp-Richtung
        elif view == "Rechts":  # Überprüft, ob die Ansicht "Rechts" ist
            # Rechtsansicht um 90° um die Z-Achse drehen
            camera.SetPosition(1, 0, 0)  # Angepasste Position
            camera.SetFocalPoint(0, 0, 0)  # Setzt den Fokuspunkt der Kamera
            camera.SetViewUp(0, 1, 0)  # Angepasste ViewUp-Richtung
        elif view == "Oben":  # Überprüft, ob die Ansicht "Oben" ist
            camera.SetPosition(0, 1, 0)  # Setzt die Kameraposition
            camera.SetFocalPoint(0, 0, 0)  # Setzt den Fokuspunkt der Kamera
            camera.SetViewUp(0, 0, 1)  # Setzt die ViewUp-Richtung der Kamera

        # Kamera immer zurücksetzen und die neue Ansicht anwenden
        self.renderer.ResetCamera()  # Setzt die Kamera zurück
        self.vtk_widget.GetRenderWindow().Render()  # Aktualisiert das Render-Fenster

    def set_background_color(self, r, g, b):  # Definiert die Methode zum Setzen der Hintergrundfarbe
        """Hintergrundfarbe des VTK-Render-Fensters setzen."""
        self.renderer.SetBackground(r, g, b)  # Setzt die Hintergrundfarbe des Renderers
        self.vtk_widget.GetRenderWindow().Render()  # Aktualisiert das Render-Fenster

    def load_model(self):  # Definiert die Methode zum Laden eines Modells
        """Modell aus einer JSON-Datei laden."""
        file_name, _ = QFileDialog.getOpenFileName(self, "Modell laden", "", "JSON-Dateien (*.json)")  # Öffnet einen Dateidialog zum Laden einer JSON-Datei
        if file_name:  # Überprüft, ob eine Datei ausgewählt wurde
            try:
                self.model = mbsModel.mbsModel()  # Modell initialisieren
                self.model.loadDatabase(file_name)  # Modell aus JSON laden
                self.status_bar.showMessage(f"Modell geladen: {file_name}")  # Zeigt eine Statusmeldung an
                self.render_model()  # Rendert das Modell
            except Exception as e:  # Fängt Ausnahmen ab
                QMessageBox.critical(self, "Fehler", f"Modell konnte nicht geladen werden: {e}")  # Zeigt eine Fehlermeldung an

    def save_model(self):  # Definiert die Methode zum Speichern eines Modells
        """Aktuelles Modell in einer JSON-Datei speichern."""
        if not self.model:  # Überprüft, ob ein Modell vorhanden ist
            QMessageBox.warning(self, "Warnung", "Kein Modell zum Speichern vorhanden.")  # Zeigt eine Warnung an
            return

        file_name, _ = QFileDialog.getSaveFileName(self, "Modell speichern", "", "JSON-Dateien (*.json)")  # Öffnet einen Dateidialog zum Speichern einer JSON-Datei
        if file_name:  # Überprüft, ob eine Datei ausgewählt wurde
            try:
                self.model.saveDatabase(file_name)  # Modell als JSON speichern
                self.status_bar.showMessage(f"Modell gespeichert: {file_name}")  # Zeigt eine Statusmeldung an
            except Exception as e:  # Fängt Ausnahmen ab
                QMessageBox.critical(self, "Fehler", f"Modell konnte nicht gespeichert werden: {e}")  # Zeigt eine Fehlermeldung an

    def import_fdd(self):  # Definiert die Methode zum Importieren einer .fdd-Datei
        """Modell aus einer .fdd-Datei importieren."""
        file_name, _ = QFileDialog.getOpenFileName(self, "FDD-Datei importieren", "", "FDD-Dateien (*.fdd)")  # Öffnet einen Dateidialog zum Importieren einer .fdd-Datei
        if file_name:  # Überprüft, ob eine Datei ausgewählt wurde
            try:
                self.model = mbsModel.mbsModel()  # Modell initialisieren
                if self.model.importFddFile(file_name):  # Modell aus FDD importieren
                    self.status_bar.showMessage(f"FDD-Datei importiert: {file_name}")  # Zeigt eine Statusmeldung an
                    self.render_model()  # Rendert das Modell
                else:
                    QMessageBox.critical(self, "Fehler", "FDD-Datei konnte nicht importiert werden.")  # Zeigt eine Fehlermeldung an
            except Exception as e:  # Fängt Ausnahmen ab
                QMessageBox.critical(self, "Fehler", f"FDD-Datei konnte nicht importiert werden: {e}")  # Zeigt eine Fehlermeldung an

    def render_model(self):  # Definiert die Methode zum Rendern des Modells
        """Modell im VTK-Fenster rendern."""
        if not self.model:  # Überprüft, ob ein Modell vorhanden ist
            return

        self.renderer.RemoveAllViewProps()  # Renderer leeren

        # mbsObjects zum Renderer hinzufügen
        self.model.showModel(self.renderer)  # Methode showModel des Modells verwenden

        self.renderer.ResetCamera()  # Kamera zurücksetzen
        self.vtk_widget.GetRenderWindow().Render()  # Render-Fenster aktualisieren

    def fit_model(self):  # Definiert die Methode zum Anpassen des Modells an das Fenster
        """Modell an das Fenster anpassen."""
        self.renderer.ResetCamera()  # Kamera zurücksetzen
        self.vtk_widget.GetRenderWindow().Render()  # Render-Fenster aktualisieren

def main():  # Definiert die Hauptfunktion
    # Anwendung und Fenster initialisieren
    app = QApplication(sys.argv)  # Erstellt eine QApplication
    window = MainWindow()  # Erstellt ein Hauptfenster

    # Anfangsansicht auf "Iso" setzen
    window.change_view("Iso")  # Setzt die Anfangsansicht auf "Iso"

    # Wenn ein Kommandozeilenargument für die .fdd-Datei vorhanden ist, importieren
    if len(sys.argv) > 1:  # Überprüft, ob ein Kommandozeilenargument vorhanden ist
        fdd_file_path = sys.argv[1]  # Holt den Pfad der .fdd-Datei aus den Kommandozeilenargumenten
        
        if window.model is None:  # Überprüft, ob das Modell None ist
            window.model = mbsModel.mbsModel()  # Erstellt ein neues Modell
        window.model.importFddFile(fdd_file_path)  # Importiert die .fdd-Datei
        window.render_model()  # Rendert das Modell

    # Andernfalls die reguläre GUI-Anwendung starten
    sys.exit(app.exec())  # Startet die Anwendung und wartet auf das Beenden

if __name__ == "__main__":  # Überprüft, ob das Skript direkt ausgeführt wird
    main()  # Ruft die Hauptfunktion auf
