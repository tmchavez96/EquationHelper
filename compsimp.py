import digit
from digit import Digit
import re

#alter list so elements intended to be together
#are combines into one element
#ex. 2 x -> 2x
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
        e1t = elm1.text
        lelm1 = len(e1t)
        compstr = e1t[lelm1-1] + elm2.text
        reHit = filt2.match(compstr)
        if reHit:
            print("reHIT on " + compstr)
            elm1.text = elm1.text + elm2.text
            inList.pop(index + 1)
            endpoint = endpoint - 1
            index = index-1
        index = index + 1
    retstr = ""
    for elm in inList:
        retstr = retstr + elm.text
    #print("did we have tegridy?: " + retstr)

#check coef for - sign
def checkCoef(coef):
    if(coef < 0):
        return True


#check if previos element was '-'
def signCheck(index,inList):
    if(index == 0):
        return False
    prev = inList[index-1]
    print("signCheck: comparing " + prev.text + " index: " + str(index))
    if(prev.text == '-'):
        print("signCheck wokred")
        return True
    else:
        return False



#use elm sizes to allocate elm "sub" field
def setSub(inList):
    index = 0
    end = len(inList)-1
    for elm in inList:
        next = elm
        if(index < end):
            next = inList[index+1]
        else:
            break
        if(next.size < elm.size):
            elm.sub = next
        else:
            elm.sub = None
        index = index + 1

    return
