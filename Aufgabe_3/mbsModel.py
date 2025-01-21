import inputfilereader  # Importiert das Modul inputfilereader
import body  # Importiert das Modul body
import constraint  # Importiert das Modul constraint
import force  # Importiert das Modul force
import measure  # Importiert das Modul measure
import dataobject  # Importiert das Modul dataobject
import json  # Importiert das Modul json
import os  # Importiert das Modul os

class mbsModel:  # Definiert die Klasse mbsModel
    def __init__(self):  # Initialisiert eine Instanz der Klasse mbsModel
        self.__mbsObjectList = []  # Initialisiert eine leere Liste von mbsObjects

    def importFddFile(self, filepath):  # Importiert eine .fdd-Datei und liest die mbsObjects ein
        file_name, file_extension = os.path.splitext(filepath)  # Teilt den Dateipfad in Name und Erweiterung
        if file_extension == ".fdd":  # Überprüft, ob die Datei eine .fdd-Datei ist
            self.__mbsObjectList = inputfilereader.readInput(filepath)  # Liest die mbsObjects aus der Datei
        else:
            print("Wrong file type: " + file_extension)  # Gibt eine Fehlermeldung aus, wenn der Dateityp falsch ist
            return False  # Rückgabe False
        
        for object in self.__mbsObjectList:  # Iteriert über jedes mbsObject
            object.setModelContext(self)  # Setzt den Modellkontext für das Objekt
        return True  # Rückgabe True
        
    def exportFdsFile(self, filepath):  # Exportiert die mbsObjects in eine .fds-Datei
        f = open(filepath, "w")  # Öffnet die Datei zum Schreiben
        for object in self.__mbsObjectList:  # Iteriert über jedes mbsObject
            object.writeSolverInput(f)  # Schreibt die Eingabedaten des Objekts in die Datei
        f.close()  # Schließt die Datei
        
    def loadDatabase(self, database2Load):  # Lädt eine Datenbank (JSON-Datei) und erstellt die entsprechenden mbsObjects
        f = open(database2Load)  # Öffnet die Datenbankdatei
        data = json.load(f)  # Lädt die Daten aus der Datei
        f.close()  # Schließt die Datei
        for modelObject in data["modelObjects"]:  # Iteriert über jedes Modellobjekt in den Daten
            if modelObject["type"] == "Body" and modelObject["subtype"] == "Rigid_EulerParameter_PAI":  # Überprüft, ob das Objekt ein starrer Körper ist
                self.__mbsObjectList.append(body.rigidBody(parameter=modelObject["parameter"]))  # Fügt einen starren Körper zur Liste hinzu
            elif modelObject["type"] == "Constraint" and modelObject["subtype"] == "Generic":  # Überprüft, ob das Objekt eine generische Einschränkung ist
                self.__mbsObjectList.append(constraint.genericConstraint(parameter=modelObject["parameter"]))  # Fügt eine generische Einschränkung zur Liste hinzu
            elif modelObject["type"] == "Force":  # Überprüft, ob das Objekt eine Kraft ist
                if modelObject["subtype"] == "GenericForce":  # Überprüft, ob die Kraft generisch ist
                    self.__mbsObjectList.append(force.genericForce(parameter=modelObject["parameter"]))  # Fügt eine generische Kraft zur Liste hinzu
                elif modelObject["subtype"] == "GenericTorque":  # Überprüft, ob das Drehmoment generisch ist
                    self.__mbsObjectList.append(force.genericTorque(parameter=modelObject["parameter"]))  # Fügt ein generisches Drehmoment zur Liste hinzu
            elif modelObject["type"] == "Measure":  # Überprüft, ob das Objekt eine Messung ist
                self.__mbsObjectList.append(measure.measure(parameter=modelObject["parameter"]))  # Fügt eine Messung zur Liste hinzu
            elif modelObject["type"] == "DataObject" and modelObject["subtype"] == "Parameter":  # Überprüft, ob das Objekt ein Parameter-Datenobjekt ist
                self.__mbsObjectList.append(dataobject.parameter(parameter=modelObject["parameter"]))  # Fügt ein Parameter-Datenobjekt zur Liste hinzu

        return True  # Rückgabe True

    def saveDatabase(self, dataBasePath):  # Speichert die mbsObjects in einer Datenbank (JSON-Datei)
        modelObjects = []  # Initialisiert eine leere Liste von Modellobjekten
        for object in self.__mbsObjectList:  # Iteriert über jedes mbsObject
            modelObject = {  # Erstellt ein Modellobjekt-Dictionary
                "type": object.getType(),  # Setzt den Typ des Objekts
                "subtype": object.getSubType(),  # Setzt den Subtyp des Objekts
                "parameter": object.parameter  # Setzt die Parameter des Objekts
            }
            modelObjects.append(modelObject)  # Fügt das Modellobjekt zur Liste hinzu

        jDataBase = json.dumps({"modelObjects": modelObjects})  # Konvertiert die Liste der Modellobjekte in einen JSON-String

        with open(dataBasePath, "w") as outfile:  # Öffnet die Datenbankdatei zum Schreiben
            outfile.write(jDataBase)  # Schreibt den JSON-String in die Datei

    def showModel(self, renderer):  # Zeigt das Modell im Renderer an
        for object in self.__mbsObjectList:  # Iteriert über jedes mbsObject
            object.show(renderer)  # Zeigt das Objekt im Renderer an
