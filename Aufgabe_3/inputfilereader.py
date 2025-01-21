import body  # Importiert das Modul body
import constraint  # Importiert das Modul constraint
import force  # Importiert das Modul force
import measure  # Importiert das Modul measure
import dataobject  # Importiert das Modul dataobject
import json  # Importiert das Modul json

def readInput(path2File):  # Definiert die Funktion readInput, die den Inhalt einer Datei liest und mbsObjects erstellt
    f = open(path2File, "r")  # Öffnet die Datei zum Lesen

    fileContent = f.read().splitlines()  # Liest den Inhalt der Datei und teilt ihn in Zeilen auf
    f.close()  # Schließt die Datei

    currentBlockType = ""  # Initialisiert den aktuellen Blocktyp als leeren String
    currentTextBlock = []  # Initialisiert den aktuellen Textblock als leere Liste
    listOfMbsObjects = []  # Initialisiert die Liste der mbsObjects als leere Liste
    search4Objects = ["RIGID_BODY", "CONSTRAINT", "FORCE_GenericForce", "FORCE_GenericTorque", "MEASURE", "DATAOBJECT_PARAMETER"]  # Definiert die zu suchenden Objekttypen
    for line in fileContent:  # Iteriert über jede Zeile im Dateiinhalte
        if line.find("$") >= 0:  # Überprüft, ob die Zeile ein Dollarzeichen enthält (neuer Block)
            if currentBlockType != "":  # Überprüft, ob ein aktueller Blocktyp vorhanden ist
                if currentBlockType == "RIGID_BODY":  # Überprüft, ob der Blocktyp ein starrer Körper ist
                    listOfMbsObjects.append(body.rigidBody(text=currentTextBlock))  # Fügt einen starren Körper zur Liste hinzu
                elif currentBlockType == "CONSTRAINT":  # Überprüft, ob der Blocktyp eine Einschränkung ist
                    listOfMbsObjects.append(constraint.genericConstraint(text=currentTextBlock))  # Fügt eine generische Einschränkung zur Liste hinzu
                elif currentBlockType == "FORCE_GenericForce":  # Überprüft, ob der Blocktyp eine generische Kraft ist
                    listOfMbsObjects.append(force.genericForce(text=currentTextBlock))  # Fügt eine generische Kraft zur Liste hinzu
                elif currentBlockType == "FORCE_GenericTorque":  # Überprüft, ob der Blocktyp ein generisches Drehmoment ist
                    listOfMbsObjects.append(force.genericTorque(text=currentTextBlock))  # Fügt ein generisches Drehmoment zur Liste hinzu
                elif currentBlockType == "MEASURE":  # Überprüft, ob der Blocktyp eine Messung ist
                    listOfMbsObjects.append(measure.measure(text=currentTextBlock))  # Fügt eine Messung zur Liste hinzu
                elif currentBlockType == "DATAOBJECT_PARAMETER":  # Überprüft, ob der Blocktyp ein Parameter-Datenobjekt ist
                    listOfMbsObjects.append(dataobject.parameter(text=currentTextBlock))  # Fügt ein Parameter-Datenobjekt zur Liste hinzu
                currentBlockType = ""  # Setzt den aktuellen Blocktyp zurück

        for type_i in search4Objects:  # Iteriert über jeden zu suchenden Objekttyp
            if line.find(type_i, 1, len(type_i) + 1) >= 0:  # Überprüft, ob die Zeile den Objekttyp enthält
                currentBlockType = type_i  # Setzt den aktuellen Blocktyp
                currentTextBlock.clear()  # Löscht den aktuellen Textblock
                break  # Bricht die Schleife ab
        
        currentTextBlock.append(line)  # Fügt die Zeile zum aktuellen Textblock hinzu
    
    return listOfMbsObjects  # Rückgabe der Liste der mbsObjects