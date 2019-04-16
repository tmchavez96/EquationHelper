class Digit:
    def __init__(self,name,text,size,posX,posY,id,selected):
        self.name = name
        self.text = text
        self.size = size
        self.posX = posX
        self.posY = posY
        self.id = id
        self.cur = selected

    def view(self):
        print("name = " + self.name)
        print("text = " + self.text)
        print("size = " + str(self.size))
        print("posX = " + str(self.posX))
        print("posY = " + str(self.posY))
        print("id = " + str(self.id))
        print("cur = " + str(self.cur))
