import os
import sys

class mbsObject:
    def __init__(self, type, subtype, **kwargs):
        # Initialisiert ein mbsObject mit Typ, Subtyp und optionalen Parametern
        self.__type = type
        self._subtype = subtype
        self._symbolsScale = 10.0
        if "parameter" in kwargs:
            self.parameter = kwargs["parameter"]
        else:
            sys.exit("parameter not provided, cannot create mbsObject!")  # Beendet das Programm, wenn keine Parameter bereitgestellt werden

        self.actors = []

        if "text" in kwargs:
            for line in kwargs["text"]:
                splitted = line.split(":")
                for key in self.parameter.keys():
                    keyString = splitted[0].strip()
                    valueString = line[len(key) + 1:].strip()
                    if keyString == key:
                        if self.parameter[key]["type"] == "float":
                            self.parameter[key]["value"] = self.str2float(valueString)
                        elif self.parameter[key]["type"] == "vector":
                            self.parameter[key]["value"] = self.str2vector(valueString)
                        elif self.parameter[key]["type"] == "colorvector":
                            self.parameter[key]["value"] = self.str2colorvector(valueString)
                        elif self.parameter[key]["type"] == "string":
                            self.parameter[key]["value"] = valueString
                        elif self.parameter[key]["type"] == "filepath":
                            self.parameter[key]["value"] = os.path.normpath(valueString)
                        elif self.parameter[key]["type"] == "bool":
                            self.parameter[key]["value"] = self.str2bool(valueString)

    def getType(self):
        # Gibt den Typ des Objekts zurück
        return self.__type

    def getSubType(self):
        # Gibt den Subtyp des Objekts zurück
        return self._subtype

    def setModelContext(self, modelContext):
        # Setzt den Modellkontext (derzeit keine Implementierung)
        return

    def writeSolverInput(self, file):
        # Schreibt die Eingabedaten für den Solver in eine Datei
        text = []
        text.append(self.__type + " " + self._subtype + "\n")
        for key in self.parameter.keys():
            value = self.parameter[key]["value"]
            if self.parameter[key]["type"] == "float":
                text.append("\t" + key + " = " + self.float2str(value) + "\n")
            elif self.parameter[key]["type"] == "vector":
                text.append("\t" + key + " = " + self.vector2str(value) + "\n")
            elif self.parameter[key]["type"] == "string":
                text.append("\t" + key + " = " + value + "\n")
            elif self.parameter[key]["type"] == "filepath":
                text.append("\t" + key + " = " + value + "\n")
            elif self.parameter[key]["type"] == "bool":
                text.append("\t" + key + " = " + self.bool2str(value) + "\n")
        text.append("End" + self.__type + "\n%\n")

        file.writelines(text)

    @staticmethod
    def str2float(inString):
        # Konvertiert einen String in einen Float
        return float(inString)

    @staticmethod
    def float2str(inFloat):
        # Konvertiert einen Float in einen String
        return str(inFloat)

    @staticmethod
    def str2vector(inString):
        # Konvertiert einen String in einen Vektor (Liste von Floats)
        return [float(inString.split(",")[0]), float(inString.split(",")[1]), float(inString.split(",")[2])]

    @staticmethod
    def vector2str(inVector):
        # Konvertiert einen Vektor (Liste von Floats) in einen String
        return str(inVector[0]) + "," + str(inVector[1]) + "," + str(inVector[2])

    @staticmethod
    def str2colorvector(inString):
        # Konvertiert einen String in einen Farbvektor (Liste von Integers)
        splitted = inString.split(" ")
        return [int(splitted[0]), int(splitted[1]), int(splitted[2]), int(splitted[1])]

    @staticmethod
    def str2bool(inString):
        # Konvertiert einen String in einen Bool
        return bool(int(inString))

    @staticmethod
    def bool2str(inBool):
        # Konvertiert einen Bool in einen String
        if inBool:
            return "yes"
        else:
            return "no"

    def show(self, renderer):
        # Zeigt die Akteure im Renderer an
        for actor in self.actors:
            renderer.AddActor(actor)

    def hide(self, renderer):
        # Verbirgt die Akteure im Renderer
        for actor in self.actors:
            renderer.RemoveActor(actor)