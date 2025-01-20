import json
import os
import vtk

# Base class for all MBS objects
class MbsObject:
    def __init__(self, parameter):
        self.parameter = parameter

    def getType(self):
        raise NotImplementedError()

    def getSubType(self):
        raise NotImplementedError()

    def show(self, renderer):
        raise NotImplementedError()

    def setModelContext(self, model):
        self.model = model

# RigidBody object
class RigidBody(MbsObject):
    def __init__(self, parameter):
        super().__init__(parameter)

    def getType(self):
        return "Body"

    def getSubType(self):
        return "Rigid_EulerParameter_PAI"

    def show(self, renderer):
        # Create a simple sphere to represent the rigid body
        sphere = vtk.vtkSphereSource()
        sphere.SetRadius(self.parameter.get("radius", 1.0))
        sphere.Update()

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(sphere.GetOutputPort())

        actor = vtk.vtkActor()
        actor.SetMapper(mapper)

        renderer.AddActor(actor)

# Force object
class Force(MbsObject):
    def __init__(self, parameter):
        super().__init__(parameter)

    def getType(self):
        return "Force"

    def getSubType(self):
        return "GenericForce"

    def show(self, renderer):
        # Represent the force with a simple arrow
        arrow = vtk.vtkArrowSource()
        arrow.SetTipRadius(0.1)
        arrow.SetTipLength(2.0)
        arrow.Update()

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(arrow.GetOutputPort())

        actor = vtk.vtkActor()
        actor.SetMapper(mapper)

        renderer.AddActor(actor)

# Constraint object
class Constraint(MbsObject):
    def __init__(self, parameter):
        super().__init__(parameter)

    def getType(self):
        return "Constraint"

    def getSubType(self):
        return "Generic"

    def show(self, renderer):
        # Represent the constraint with a simple cylinder
        cylinder = vtk.vtkCylinderSource()
        cylinder.SetRadius(0.2)
        cylinder.SetHeight(3.0)
        cylinder.Update()

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(cylinder.GetOutputPort())

        actor = vtk.vtkActor()
        actor.SetMapper(mapper)

        renderer.AddActor(actor)

# mbsModel class
class mbsModel:
    def __init__(self):
        self.__mbsObjectList = []

    def importFddFile(self, filepath):
        file_name, file_extension = os.path.splitext(filepath)
        if file_extension == ".fdd":
            # Read FDD file and generate model objects
            self.__mbsObjectList = inputfilereader.readInput(filepath)
        else:
            print("Wrong file type: " + file_extension)
            return False

        for obj in self.__mbsObjectList:
            obj.setModelContext(self)

        return True

    def exportFdsFile(self, filepath):
        with open(filepath, "w") as f:
            for obj in self.__mbsObjectList:
                obj.writeSolverInput(f)

    def loadDatabase(self, database2Load):
        with open(database2Load) as f:
            data = json.load(f)

        for modelObject in data["modelObjects"]:
            if modelObject["type"] == "Body" and modelObject["subtype"] == "Rigid_EulerParameter_PAI":
                self.__mbsObjectList.append(RigidBody(parameter=modelObject["parameter"]))
            elif modelObject["type"] == "Constraint" and modelObject["subtype"] == "Generic":
                self.__mbsObjectList.append(Constraint(parameter=modelObject["parameter"]))
            elif modelObject["type"] == "Force" and modelObject["subtype"] == "GenericForce":
                self.__mbsObjectList.append(Force(parameter=modelObject["parameter"]))

        return True

    def saveDatabase(self, dataBasePath):
        modelObjects = []
        for obj in self.__mbsObjectList:
            modelObject = {
                "type": obj.getType(),
                "subtype": obj.getSubType(),
                "parameter": obj.parameter
            }
            modelObjects.append(modelObject)

        jDataBase = json.dumps({"modelObjects": modelObjects})

        with open(dataBasePath, "w") as outfile:
            outfile.write(jDataBase)

    def showModel(self, renderer):
        for obj in self.__mbsObjectList:
            obj.show(renderer)

