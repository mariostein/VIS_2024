import mbsObject
f = open("inputfilereader/test.fdd","r")

fileContent = f.read().splitlines()
f.close()


currentTextType = ""
currentTextBlock =[]
search4Objects = []
listOfMbsObjects = []

for line in fileContent:
    if(line.find("$")>=0): #neuer Block wurde gefunden
        if(currentTextType != ""):
            if(currentTextType == "RIGID_BODY"):
                listOfMbsObjects.append(mbsObject.mbsObject("body",currentTextBlock))
            currentTextType = ""


    for type_i in search4Objects:
        if(line.find(type_i,1,len(type_i)+1)>=0):
            currentTextType = type_i
            currentTextBlock.clear()
            break

    currentTextBlock.append(line)

print("numberOfRigidBodys =",listOfMbsObjects)