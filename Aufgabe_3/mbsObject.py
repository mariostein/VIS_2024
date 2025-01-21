import os  # Importiert das Modul os
import sys  # Importiert das Modul sys

class mbsObject:  # Definiert die Klasse mbsObject
    def __init__(self, type, subtype, **kwargs):  # Initialisiert ein mbsObject mit Typ, Subtyp und optionalen Parametern
        self.__type = type  # Setzt den Typ des Objekts
        self._subtype = subtype  # Setzt den Subtyp des Objekts
        self._symbolsScale = 10.0  # Setzt die Skalierung der Symbole
        if "parameter" in kwargs:  # Überprüft, ob Parameter bereitgestellt wurden
            self.parameter = kwargs["parameter"]  # Setzt die Parameter
        else:
            sys.exit("parameter not provided, cannot create mbsObject!")  # Beendet das Programm, wenn keine Parameter bereitgestellt werden

        self.actors = []  # Initialisiert eine leere Liste von Akteuren

        if "text" in kwargs:  # Überprüft, ob Text bereitgestellt wurde
            for line in kwargs["text"]:  # Iteriert über jede Zeile im Text
                splitted = line.split(":")  # Teilt die Zeile bei jedem Doppelpunkt
                for key in self.parameter.keys():  # Iteriert über jeden Schlüssel in den Parametern
                    keyString = splitted[0].strip()  # Entfernt Leerzeichen vom Schlüssel
                    valueString = line[len(key) + 1:].strip()  # Entfernt Leerzeichen vom Wert
                    if keyString == key:  # Überprüft, ob der Schlüssel übereinstimmt
                        if self.parameter[key]["type"] == "float":  # Überprüft, ob der Typ ein Float ist
                            self.parameter[key]["value"] = self.str2float(valueString)  # Konvertiert den Wert in einen Float
                        elif self.parameter[key]["type"] == "vector":  # Überprüft, ob der Typ ein Vektor ist
                            self.parameter[key]["value"] = self.str2vector(valueString)  # Konvertiert den Wert in einen Vektor
                        elif self.parameter[key]["type"] == "colorvector":  # Überprüft, ob der Typ ein Farbvektor ist
                            self.parameter[key]["value"] = self.str2colorvector(valueString)  # Konvertiert den Wert in einen Farbvektor
                        elif self.parameter[key]["type"] == "string":  # Überprüft, ob der Typ ein String ist
                            self.parameter[key]["value"] = valueString  # Setzt den Wert als String
                        elif self.parameter[key]["type"] == "filepath":  # Überprüft, ob der Typ ein Dateipfad ist
                            self.parameter[key]["value"] = os.path.normpath(valueString)  # Normalisiert den Dateipfad
                        elif self.parameter[key]["type"] == "bool":  # Überprüft, ob der Typ ein Bool ist
                            self.parameter[key]["value"] = self.str2bool(valueString)  # Konvertiert den Wert in einen Bool

    def getType(self):  # Gibt den Typ des Objekts zurück
        return self.__type  # Rückgabe des Typs

    def getSubType(self):  # Gibt den Subtyp des Objekts zurück
        return self._subtype  # Rückgabe des Subtyps

    def setModelContext(self, modelContext):  # Setzt den Modellkontext (derzeit keine Implementierung)
        return  # Rückgabe ohne Aktion

    def writeSolverInput(self, file):  # Schreibt die Eingabedaten für den Solver in eine Datei
        text = []  # Initialisiert eine leere Liste für den Text
        text.append(self.__type + " " + self._subtype + "\n")  # Fügt den Typ und Subtyp zum Text hinzu
        for key in self.parameter.keys():  # Iteriert über jeden Schlüssel in den Parametern
            value = self.parameter[key]["value"]  # Holt den Wert des Schlüssels
            if self.parameter[key]["type"] == "float":  # Überprüft, ob der Typ ein Float ist
                text.append("\t" + key + " = " + self.float2str(value) + "\n")  # Fügt den Schlüssel und Wert als Float zum Text hinzu
            elif self.parameter[key]["type"] == "vector":  # Überprüft, ob der Typ ein Vektor ist
                text.append("\t" + key + " = " + self.vector2str(value) + "\n")  # Fügt den Schlüssel und Wert als Vektor zum Text hinzu
            elif self.parameter[key]["type"] == "string":  # Überprüft, ob der Typ ein String ist
                text.append("\t" + key + " = " + value + "\n")  # Fügt den Schlüssel und Wert als String zum Text hinzu
            elif self.parameter[key]["type"] == "filepath":  # Überprüft, ob der Typ ein Dateipfad ist
                text.append("\t" + key + " = " + value + "\n")  # Fügt den Schlüssel und Wert als Dateipfad zum Text hinzu
            elif self.parameter[key]["type"] == "bool":  # Überprüft, ob der Typ ein Bool ist
                text.append("\t" + key + " = " + self.bool2str(value) + "\n")  # Fügt den Schlüssel und Wert als Bool zum Text hinzu
        text.append("End" + self.__type + "\n%\n")  # Fügt das Ende des Typs zum Text hinzu

        file.writelines(text)  # Schreibt den Text in die Datei

    @staticmethod
    def str2float(inString):  # Konvertiert einen String in einen Float
        return float(inString)  # Rückgabe des konvertierten Floats

    @staticmethod
    def float2str(inFloat):  # Konvertiert einen Float in einen String
        return str(inFloat)  # Rückgabe des konvertierten Strings

    @staticmethod
    def str2vector(inString):  # Konvertiert einen String in einen Vektor (Liste von Floats)
        return [float(inString.split(",")[0]), float(inString.split(",")[1]), float(inString.split(",")[2])]  # Rückgabe des konvertierten Vektors

    @staticmethod
    def vector2str(inVector):  # Konvertiert einen Vektor (Liste von Floats) in einen String
        return str(inVector[0]) + "," + str(inVector[1]) + "," + str(inVector[2])  # Rückgabe des konvertierten Strings

    @staticmethod
    def str2colorvector(inString):  # Konvertiert einen String in einen Farbvektor (Liste von Integers)
        splitted = inString.split(" ")  # Teilt den String bei jedem Leerzeichen
        return [int(splitted[0]), int(splitted[1]), int(splitted[2]), int(splitted[1])]  # Rückgabe des konvertierten Farbvektors

    @staticmethod
    def str2bool(inString):  # Konvertiert einen String in einen Bool
        return bool(int(inString))  # Rückgabe des konvertierten Bools

    @staticmethod
    def bool2str(inBool):  # Konvertiert einen Bool in einen String
        if inBool:  # Überprüft, ob der Bool True ist
            return "yes"  # Rückgabe "yes"
        else:
            return "no"  # Rückgabe "no"

    def show(self, renderer):  # Zeigt die Akteure im Renderer an
        for actor in self.actors:  # Iteriert über jeden Akteur
            renderer.AddActor(actor)  # Fügt den Akteur zum Renderer hinzu

    def hide(self, renderer):  # Verbirgt die Akteure im Renderer
        for actor in self.actors:  # Iteriert über jeden Akteur
            renderer.RemoveActor(actor)  # Entfernt den Akteur vom Renderer