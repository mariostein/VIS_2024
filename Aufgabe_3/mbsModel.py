import inputfilereader
import body
import constraint
import force
import measure
import dataobject
import json
import os

class mbsModel:
    def __init__(self):
        # Initialisiert eine leere Liste von mbsObjects
        self.__mbsObjectList = []

    def importFddFile(self, filepath):
        # Importiert eine .fdd-Datei und liest die mbsObjects ein
        file_name, file_extension = os.path.splitext(filepath)
        if file_extension == ".fdd":
            self.__mbsObjectList = inputfilereader.readInput(filepath)
        else:
            print("Wrong file type: " + file_extension)
            return False
        
        for object in self.__mbsObjectList:
            object.setModelContext(self)
        return True
        
    def exportFdsFile(self, filepath):
        # Exportiert die mbsObjects in eine .fds-Datei
        f = open(filepath, "w")
        for object in self.__mbsObjectList:
            object.writeSolverInput(f)
        f.close()
        
    def loadDatabase(self, database2Load):
        # Lädt eine Datenbank (JSON-Datei) und erstellt die entsprechenden mbsObjects
        f = open(database2Load)
        data = json.load(f)
        f.close()
        for modelObject in data["modelObjects"]:
            if modelObject["type"] == "Body" and modelObject["subtype"] == "Rigid_EulerParameter_PAI":
                self.__mbsObjectList.append(body.rigidBody(parameter=modelObject["parameter"]))
            elif modelObject["type"] == "Constraint" and modelObject["subtype"] == "Generic":
                self.__mbsObjectList.append(constraint.genericConstraint(parameter=modelObject["parameter"]))
            elif modelObject["type"] == "Force":
                if modelObject["subtype"] == "GenericForce":
                    self.__mbsObjectList.append(force.genericForce(parameter=modelObject["parameter"]))
                elif modelObject["subtype"] == "GenericTorque":
                    self.__mbsObjectList.append(force.genericTorque(parameter=modelObject["parameter"]))
            elif modelObject["type"] == "Measure":
                self.__mbsObjectList.append(measure.measure(parameter=modelObject["parameter"]))
            elif modelObject["type"] == "DataObject" and modelObject["subtype"] == "Parameter":
                self.__mbsObjectList.append(dataobject.parameter(parameter=modelObject["parameter"]))

        return True

    def saveDatabase(self, dataBasePath):
        # Speichert die mbsObjects in einer Datenbank (JSON-Datei)
        modelObjects = []
        for object in self.__mbsObjectList:
            modelObject = {
                "type": object.getType(),
                "subtype": object.getSubType(),
                "parameter": object.parameter
            }
            modelObjects.append(modelObject)

        jDataBase = json.dumps({"modelObjects": modelObjects})

        with open(dataBasePath, "w") as outfile:
            outfile.write(jDataBase)

    def showModel(self, renderer):
        # Zeigt das Modell im Renderer an
        for object in self.__mbsObjectList:
            object.show(renderer)
