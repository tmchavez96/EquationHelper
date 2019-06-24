import re

class Digit:
    def __init__(self,name,text,size,posX,posY,id,selected):
        self.name = name
        self.text = text
        self.size = size
        self.posX = posX
        self.posY = posY
        self.id = id
        self.cur = selected
        self.sub = None

    def view(self):
        print("name = " + self.name)
        print("text = " + self.text)
        print("size = " + str(self.size))
        print("posX = " + str(self.posX))
        print("posY = " + str(self.posY))
        print("id = " + str(self.id))
        print("cur = " + str(self.cur))

    def quickView(self):
        print("text = " + self.text + "size = " + str(self.size))


    def lessThanX(other):
        if(self.posX < other.posX):
            return True
        else:
            return False

    #assume format [int]*[char]
    #example 12x
    def getCoef(self):
        term = self.text
        coef = ""
        end = len(term)-1
        index = 0
        filt = re.compile('[0-9]')
        while(index <= end):
            hit = filt.match(self.text[index])
            if(hit):
                #print("coef hit")
                coef = coef + self.text[index]
            else:
                break
            index = index + 1
        if(len(coef) >= 1):
            return int(coef)
        else:
            return None

    #assumes same format as getCoef
    def getVar(self):
        term = self.text
        var = ""
        end = len(term)-1
        index = 0
        filt = re.compile('[a-zA-z]')
        start = -1
        #edge case
        while(index <= end):
            #print("on "+str(self.text[index]))
            hit = filt.match(self.text[index])
            if(hit):
                #print("hit")
                start = index
                break
            index = index+1
        filt2 = re.compile('[/+%*-]')
        if(filt2.match(self.text)):
            return None
        if start < 0:
            return "int"
        #print("start = "+ str(start))
        while(start <= end):
            var = var + self.text[start]
            start = start + 1
        if(self.sub != None):
            self.sub.quickView()
            var = var + self.sub.text
        return var
