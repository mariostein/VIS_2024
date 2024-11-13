class mbsObject:
    def __init__(self,type,text):
        self.__type = type

        for line in text:
            splitted = line.split(":")
            if(splitted[0].strip() == "mass"):  #0 ist die variable
                self.mass = float(splitted[1])  #1 ist der wert