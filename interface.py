from tkinter import *
import time
from digit import Digit

root = Tk()

theFrame = Frame(root)
theFrame.pack()

#global vars
curwidth = 1200
curheight = 900

digitList = []
curDigit = None

#event functions that need that need to be declared before canvas
def get_text():
    s = entry.get()
    inputlen = len(s)
    #print("input length = " + str(inputlen))
    xcount = 0
    i = 0
    while(i < inputlen):
        if(s[i] != ' '):
            draw_text(s[i],s[i],300+xcount,100,100)
            xcount = xcount + 100

        i = i +1

    #draw_text(s,s,300,100,100)

#def key(event):
    #w.focus_set()
    #print ("pressed")
    #print(repr(event.char))
    #curElm = id_to_object(id)
    #if(curElm == None):
        #print("no element selected")

def callback(event):
    frame.focus_set()
    #print ("clicked at")
    sumstr = str(event.x) + "," + str(event.y)
    #print (sumstr)
    curDigit = findCur()
    #print("curdigit = ")
    #print(curDigit)
    if curDigit == None:
        bindDigit(event.x,event.y)
    else:
        update_text(curDigit,event.x,event.y)

def findCur():
    #print("**in findCur")
    for elm in digitList:
        if elm.cur == True:
            #print("**findCur succses")
            #entry2.delete(0,1)
            entry2.insert(0,elm.name)
            print("inserted elm name")
            return elm.id

    return None


def changeColor(id,color):
    #print("in change color id and color: " +str(id)+ ","+color)
    w.itemconfigure(id,fill=color)
    w.update_idletasks()
    w.update()

def bindDigit(eventX,eventY):
    for elm in digitList:
        #print("checking bind for " + elm.name)
        eX = str(elm.posX)
        eY = str(elm.posY)
        eS = str(elm.size)
        #print("eml stats: " + eX+" " +eY+" "+eS)
        flag = check_coords(eventX,eventY,elm.posX,elm.posY,elm.size)
        if (flag):
            #print("check passed")
            curDigit = elm.id
            #print("curdigit = ")
            #print(curDigit)
            elm.cur = True
            return True
        else:
            print("check failed")

    return False

def delItem():
    id = findCur()
    if (id != None):
        w.delete(id)
        for elm in digitList:
            if elm.id == id:
                digitList.remove(elm)
    else:
        print("no item selected")

def copyBotLine():
    posY = getBotY()
    for elm in digitList:
        #if (elm.posY >= (posY-elm.size) and eml.posY <= posY):
        if (elm.posY == posY):
            draw_text(elm.name+"*",elm.text,elm.posX,elm.posY+100,elm.size)


def getBotY():
    temp = 0
    for elm in digitList:
        if (elm.posY > temp):
            temp = elm.posY

    return temp

def plusSize():
    id = findCur()
    if(id == None):
        return
    elm = id_to_object(id)
    tempname = elm.name + "~"
    tempinfo = elm.text
    tempX = elm.posX
    tempY = elm.posY
    tempsize = elm.size * 2
    w.delete(id)
    #time.sleep(.1)
    draw_text(tempname,tempinfo,tempX,tempY,tempsize)
    return

def plusSize2():
    id = findCur()
    if(id == None):
        return
    elm = id_to_object(id)
    size = elm.size * 2
    fontstr = "Times "+str(size)+" italic bold"
    w.itemconfig(id,font =fontstr)
    elm.size = size

def minusSize2():
    id = findCur()
    if(id == None):
        return
    elm = id_to_object(id)
    size = elm.size / 2
    fontstr = "Times "+str(size)+" italic bold"
    w.itemconfig(id,font =fontstr)
    elm.size = size

def minusSize():
    id = findCur()
    if(id == None):
        return
    elm = id_to_object(id)
    tempname = elm.name + "~"
    tempinfo = elm.text
    tempX = elm.posX
    tempY = elm.posY
    tempsize = int(elm.size / 2)
    w.delete(id)
    #time.sleep(.1)
    draw_text(tempname,tempinfo,tempX,tempY,tempsize)
    return



def sortDigitList():
    tupleList = []
    for elm in digitList:
        curTuple = (elm.id,elm.posX,elm.posY)
        tupleList.append(curTuple)
    #digitList = sorted(digitList, key = lambda x: (x[1], x[2]))
    print("the tuple list was")
    #print(tupleList)
    return tupleList


def useX(e):
    return e[1]

#returns all elements at height, sorted by x values
def getRowTuple(tupleList,height):
    rowTuple = []
    for tup in tupleList:
        if(tup[2] <= height and tup[2] > (height-100)):
            rowTuple.append(tup)

    #print("row tuple")
    #print(rowTuple)
    rowTuple.sort(key = useX)
    #print("sorted")
    #print(rowTuple)
    return rowTuple

#hardwired around size 100
def stringForLine(tupleList,height):
    retstring = ' '
    rowTuple = getRowTuple(tupleList,height)
    for tup in rowTuple:
        #if(tup[2] <= height and tup[2] > (height-100)):
        elm = id_to_object(tup[0])
        retstring = retstring + elm.text



    retstring = retstring + '\n'
    #print("str for height: " + str(height))
    #print(retstring)
    return retstring

#random string structure?
#
def saveToText2():
    filename = entry4.get()
    fd = open(filename,"w")
    #dat = digitsAsTuples
    dat = sortDigitList()
    count = 200
    while count < curheight:
        #print("int while loop")
        wstring = stringForLine(dat,count)
        #print("str after return: ")
        #print(wstring)
        if(wstring != None):
            fd.write(wstring)
        count = count + 100
    fd.close()


w = Canvas(root, width = curwidth, height = curheight)
w.pack()

w.focus_set()
w.bind("<1>", lambda event: w.focus_set())
#w.bind("<Key>", key)
w.pack()
w.bind("<Button-1>", callback)
w.pack()

frame = Frame(root,bg = "grey")
frame.place(relwidth = 0.175,relheight = 1.0)

exitbutton = Button(frame, text="Quit", bg="red",command=root.destroy)
exitbutton.grid(row=0,column=0)

label = Label(frame,text="Enter a text to add:",bg="green")
label.grid(row=1,column=0)

label = Label(frame,bg="grey")
label.grid(row=2,column=0)

entry = Entry(frame,bg="white")
entry.grid(row=3,column=0)

button = Button(frame,text="Enter",bg="green",state="normal",command=get_text)
button.grid(row=4,column=0)

label = Label(frame,bg="grey")
label.grid(row=5,column=0)

label3 = Label(frame,text="Currently selected:",bg="green")
label3.grid(row=6,column=0)

entry2 = Entry(frame,bg="white")
entry2.grid(row=7,column=0)

label = Label(frame,bg="grey")
label.grid(row=8,column=0)

button = Button(frame,text="Delete seleted item",bg="green",state="normal",command=delItem)
button.grid(row=9,column=0)

label4 = Label(frame,bg="grey")
label4.grid(row=10,column=0)

label4 = Label(frame,text="ChangeSize:",bg="green")
label4.grid(row=11,column=0)

buttona = Button(frame,text="+",bg="green",state="normal",command=plusSize2)
buttona.grid(row=12,column=0)

buttonb = Button(frame,text="-",bg="green",state="normal",command=minusSize2)
buttonb.grid(row=13,column=0)

label4 = Label(frame,bg="grey")
label4.grid(row=14,column=0)

button3 = Button(frame,text="Copy Bottom Line",bg="green",state="normal",command=copyBotLine)
button3.grid(row=15,column=0)

label5 = Label(frame,bg="grey")
label5.grid(row=16,column=0)

label6 = Label(frame,text="Save to file:",bg="green")
label6.grid(row=17,column=0)

entry4 = Entry(frame,bg="white")
entry4.grid(row=18,column=0)

button4 = Button(frame,text="save",bg="green",state="normal",command=saveToText2)
button4.grid(row=19,column=0)

def draw_grid(ch,cw,lineSize,space):
    a = int((cw/100)*2)
    b = int((ch/100)*2)


    counter = 1
    for x in range(a):
        if (counter%2) != 0 :
            w.create_line(counter*space,0,counter*space,ch,fill="blue",width=lineSize/2)
        else:
            w.create_line(counter*space,0,counter*space,ch,fill="blue",width=lineSize)
        counter += 1

    counter = 1
    for x in range(b):
        if (counter%2) != 0 :
            w.create_line(0, counter*space,cw, counter*space,fill="blue",width=lineSize/2)
        else:
            w.create_line(0, counter*space,cw, counter*space,fill="blue",width=lineSize)
        counter += 1
    #draw insert rect
    points = (0,0,
              cw,100
              )
    w.create_rectangle(points,fill="green")


def draw_text(name,info,posX,posY,size):
    name = Digit(name,info,size,posX,posY,-1,False)
    fontstr = "Times "+str(size)+" italic bold"
    name.id = w.create_text(posX,posY,text=info,anchor="se",font=fontstr)
    #name.view()
    digitList.append(name)
    listsize = len(digitList)
    ls = str(listsize)
    return name
    #print("list size: " + ls)
    #for elm in digitList:
        #print(elm.name)

def check_coords(cX,cY,dX,dY,size):
    if(cX > dX):
        #print("### check 1")
        return False
    elif(cY > dY):
        #print("### check 2")
        return False
    elif(cX < dX-size):
        #print("### check 3")
        return False
    elif(cY < dY-size):
        #print("### check 4")
        return False
    else:
        #print("### else")
        return True

def id_to_object(id):
    for elm in digitList:
        if(elm.id == id):
            return elm

    return None

def mod_math(pos,size):
    tempOffset = pos % size
    realOffset = size - tempOffset
    newPos = pos + realOffset
    return newPos
#pos = 200, next = 300;
def update_text(id,eventX,eventY):
    #tupvar = w.find_all()
    #print(tupvar)
    elm = id_to_object(id)
    newX = mod_math(eventX,elm.size)
    newY = mod_math(eventY,elm.size)
    #print("newX and newY = " + str(newX) + "," + str(newY))
    distX = newX - elm.posX
    distY = newY - elm.posY
    #print("distX and distY = " + str(distX) + "," + str(distY))
    #w.itemconfig(id,font = "Times 50 italic bold")
    w.move(id,distX,distY)
    elm.posX = newX
    elm.posY = newY
    curDigit = None
    elm.cur = False

    #elm.view()

#given an elems current coords, and mouseclick coords
#use elems size to to get proper lower right bound (modulus to subtraction)


draw_grid(curheight,curwidth,4.0,50)
#draw_text(name1,"X",600,200,100)

count = 0

#while True:
#    w.update_idletasks()
#    w.update()

root.mainloop()
