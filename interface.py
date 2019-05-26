from tkinter import *
import time
from digit import Digit
import re

root = Tk()

theFrame = Frame(root)
theFrame.pack()

#global vars
curwidth = 1200
curheight = 900

centerLine = int(((curwidth-200)/2)+200)

digitList = []
curDigit = None

#--event functions that need that need to be declared before canvas--
#function used to add text to the green bar on the canvas
def get_text():
    #clear the first row to avoid overlapping text
    clearRow(100)
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
    center()

def clearBottomRow():
    posY = getBotY()
    clearRow(posY)

#function to clear row on Y value
#this is gross code but removing list elements
#in one iteration was hurting me
def clearRow(posY):
    index = 0
    count = 0
    for elm in digitList:
        if(elm.posY <= posY) and (elm.posY > posY-100):
            count = count + 1
        index = index + 1
    while(count > 0):
        index = 0
        for elm in digitList:
            if(elm.posY <= posY) and (elm.posY > posY-100):
                w.delete(elm.id)
                digitList.pop(index)
                break
            index = index + 1
        count = count - 1


#adds input from user as step,
# to both sides of the equation
def add_step():
    s = entry.get()
    filt = re.compile('[+*%/-]\s*\d*\s*')
    test = filt.match(s)
    filt2 = re.compile('\d*\s*[+*%/-]\s*')
    test2 = filt2.match(s)
    posY = getBotY()
    rowList = []
    for elm in digitList:
        if (elm.posY <= posY) and (elm.posY > posY-100):
            rowList.append(elm)
    low, high = getLowHighX(rowList)
    if test:
        write_step(s,low,high,posY)
    elif test2:
        write_step(s[::-1],low,high,posY)
    else:
        print("not a properly formated step")

#add_step helper function
#actually adds text to Canvas
#assumes default text size of 100 required
def write_step(step,low,high,posY):
    lineLength = high - low
    tempLen = int(lineLength/2)
    stepSize = len(step)
    #sp = startpoint, isp = inverted start point
    sp = centerLine - tempLen
    sp = sp - (stepSize*100)
    isp = centerLine + tempLen + 100
    for char in step:
        draw_text(char+"a",char,isp,posY,100)
        isp = isp+100
    istep = step[::-1]
    for char in istep:
        draw_text(char+"b",char,sp,posY,100)
        sp = sp + 100



#callback handles the mouseclick events
#allows moving items on the canvas
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

#helper function
#finds the currently selected element
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

#change the color of an element
#never managed to work
#sad reacts only
def changeColor(id,color):
    w.itemconfigure(id,fill=color)
    w.update_idletasks()
    w.update()

#uses mouse event to see if a digit was selected
#if so, mark that digit as current
def bindDigit(eventX,eventY):
    for elm in digitList:
        eX = str(elm.posX)
        eY = str(elm.posY)
        eS = str(elm.size)
        flag = check_coords(eventX,eventY,elm.posX,elm.posY,elm.size)
        if (flag):
            curDigit = elm.id
            elm.cur = True
            return True
        else:
            print("check failed")

    return False

#delets current item, pretty self explanitory
def delItem():
    id = findCur()
    if (id != None):
        w.delete(id)
        for elm in digitList:
            if elm.id == id:
                digitList.remove(elm)
    else:
        print("no item selected")

#copies the lowest elemnts on the canavas
def copyBotLine():
    posY = getBotY()
    for elm in digitList:
        #if (elm.posY > (posY-elm.size) and eml.posY <= posY):
        if (elm.posY == posY):
            draw_text(elm.name+"*",elm.text,elm.posX,elm.posY+100,elm.size)

#helper
def getBotY():
    temp = 0
    for elm in digitList:
        if (elm.posY > temp):
            temp = elm.posY

    return temp

#doubles the size of the selected element
def plusSize2():
    id = findCur()
    if(id == None):
        return
    elm = id_to_object(id)
    size = elm.size * 2
    fontstr = "Times "+str(size)+" italic bold"
    w.itemconfig(id,font =fontstr)
    elm.size = size
    print("attempting plus")
    print(elm.view())

#opposite of plusSize
def minusSize2():
    id = findCur()
    if(id == None):
        return
    elm = id_to_object(id)
    size = elm.size / 2
    size = int(size)
    fontstr = "Times "+str(size)+" italic bold"
    w.itemconfig(id,font =fontstr)
    elm.size = size
    print("attempting minus")
    print(elm.view())

#combine wrapper, to call all lines
#for now, operate only on bot line
def compact():
    posY = getBotY()
    #rowCounter = 100
    #while(rowCounter <= curheight):
    compactRow(posY)
        #rowCounter = rowCounter + 100

def compactRow(posY):
    rowList = []
    sortedList = []
    eqx = 0
    for elm in digitList:
        if (elm.posY <= posY) and (elm.posY > posY-100):
            rowList.append(elm)
    if len(rowList) > 0:
        sortedList = isrl(rowList)
    else:
        return
    midIndex = -1
    curIndex = 0
    for elm in sortedList:
        if elm.text == '=':
            midIndex = curIndex
            eqx = elm.posX
            break
        curIndex = curIndex + 1
    if midIndex < 0:
        return None
    side1 = []
    side2 = []
    curIndex = 0
    for elm in sortedList:
        if curIndex < midIndex:
            side1.append(elm)
        if curIndex > midIndex:
            side2.append(elm)
        curIndex = curIndex + 1
    compactSide(side1)
    compactSide(side2)
    #draw the compacted line on the next line, current line will bug

    for elm in side1:
        draw_text(elm.name+":",elm.text,elm.posX,elm.posY+100,elm.size)
    draw_text("=*","=",eqx,posY+100,100)
    for elm in side2:
        draw_text(elm.name+":",elm.text,elm.posX,elm.posY+100,elm.size)

def compactSide(inList):
    filt = re.compile('\d*\w*')
    filt2 = re.compile('[0-9]+[0-9a-zA-Z]+')
    if len(inList) < 2:
        return None
    endpoint = len(inList)-1
    index = 0
    while(index < endpoint):
        elm1 = inList[index]
        elm2 = inList[index+1]
        compstr = elm1.text + elm2.text
        #print(compstr)
        reHit = filt2.match(compstr)
        if reHit:
            #print("reHIT on ")
            elm1.text = elm1.text + elm2.text
            inList.pop(index + 1)
            endpoint = endpoint - 1
            index = index-1
        index = index + 1
    retstr = ""
    for elm in inList:
        retstr = retstr + elm.text
    #print("did we have tegridy?: " + retstr)


#wrapper function for center
def center():
    rowCounter = 100
    while(rowCounter <= curheight):
        centerRow(rowCounter)
        rowCounter = rowCounter + 100

#finds all the elemnts that belong in a "row"
#calculate the line length
#uses linelength to shift to center
def centerRow(posY):
    #second thought, does using a new list to put elms in,
    #then shifting them not mess up the digitList dataStructure?
    #seems to work fine
    rowList = []
    low = 0
    high = 0
    for elm in digitList:
        if (elm.posY <= posY) and (elm.posY > posY-100):
            rowList.append(elm)
    if len(rowList) > 0:
        low, high = getLowHighX(rowList)
        lineLength = high - low
        tempLen = int(lineLength/2)
        startPoint = centerLine - tempLen
        shiftToStart(rowList,startPoint)

#helper function, moves the elements accordingly
def shiftToStart(rowList,startPos):
    sortedList = isrl(rowList)
    for elm in sortedList:
        w.move(elm.id,startPos-elm.posX,0)
        elm.posX = startPos
        startPos = startPos + elm.size

#insertionSortRowList
#ended up making my own sorting method
#empties original list and returns a sorted one
def isrl(rowList):
    retList = []

    while(len(rowList) > 0):
        #magic number, max width for first comparison
        lowestX = 1200
        for elm in rowList:
            if(elm.posX < lowestX):
                lowestX = elm.posX

        for elm in rowList:
            if(elm.posX == lowestX):
                retList.append(elm)
                rowList.remove(elm)
    return retList

#helper function
#returns the low,high poisitons of a row
def getLowHighX(rowList):
    tempElm = rowList[0]
    leftmost = tempElm.posX
    rightmost = tempElm.posX
    for elm in rowList:
        if(elm.posX < leftmost):
            leftmost = elm.posX
        if(elm.posX > rightmost):
            rightmost = elm.posX
    return leftmost, rightmost

#turns list of digits into a tupl containing id,posX,posY
def sortDigitList():
    tupleList = []
    for elm in digitList:
        curTuple = (elm.id,elm.posX,elm.posY)
        tupleList.append(curTuple)
    print("the tuple list was")
    return tupleList

#used for pythons sort
def useX(e):
    return e[1]

#returns all elements at height, sorted by x values
def getRowTuple(tupleList,height):
    rowTuple = []
    for tup in tupleList:
        if(tup[2] <= height and tup[2] > (height-100)):
            rowTuple.append(tup)


    rowTuple.sort(key = useX)
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


#wrapped function for saving to text
#recieves string interpretation of each line
#writes to file specified in interface
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

#~~~~~~~TOOL BAR FORMATTING ~~~~~~~~~~~
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

buttonw = Button(frame,text="add step",bg="green",state="normal",command=add_step)
buttonw.grid(row=5,column=0)

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

buttonc = Button(frame,text="Clear Bottom Line",bg="green",state="normal",command=clearBottomRow)
buttonc.grid(row=14,column=0)

button3 = Button(frame,text="Copy Bottom Line",bg="green",state="normal",command=copyBotLine)
button3.grid(row=15,column=0)

button3b = Button(frame,text="center",bg="green",state="normal",command=center)
button3b.grid(row=16,column=0)


label6 = Label(frame,text="Save to file:",bg="green")
label6.grid(row=17,column=0)

entry4 = Entry(frame,bg="white")
entry4.grid(row=18,column=0)

button4 = Button(frame,text="save",bg="green",state="normal",command=saveToText2)
button4.grid(row=19,column=0)

label = Label(frame,bg="grey")
label.grid(row=20,column=0)

button5 = Button(frame,text="compact",bg="green",state="normal",command=compact)
button5.grid(row=21,column=0)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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



#given an elems current coords, and mouseclick coords
#use elems size to to get proper lower right bound (modulus to subtraction)


draw_grid(curheight,curwidth,4.0,50)
#draw_text(name1,"X",600,200,100)

count = 0

#while True:
#    w.update_idletasks()
#    w.update()

root.mainloop()
