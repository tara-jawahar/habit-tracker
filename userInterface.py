# Tara Jawahar
# 15-112 Term Project

import csv,pickle

user = {'bedtime':[],'fruitNum':[],'mileTime':[],'heartRate':[]}

general = {'age': 0, 'height':0,'weight':0}

class TextBox(object):
    def __init__(self,width,height,x,y):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        
    def createBox(self,canvas,text='',fill='white',outline='white'):
        canvas.create_rectangle(self.x,self.y,self.x+self.width,
            self.y+self.height,outline=outline)
        cx = self.x + self.width/2
        cy = self.y + self.height/2
        canvas.create_text(cx,cy,text=text,fill=fill,font="Avenir 14 bold")
    
    def insideBox(self,x,y):
        if (self.x < x and x < self.x+self.width and
            self.y < y and y < self.y + self.height): return True
        else: return False

from tkinter import *

# events-example0 Animation demo
# http://www.cs.cmu.edu/~112/notes/events-example0.py
def init(data):
    data.mode = "homeScreen"
    # Home Screen boxes
    data.new = TextBox(150,50,data.width/2-200,data.height*(2/3))
    data.cont = TextBox(150,50,data.width/2+50,data.height*(2/3))
    # http://www.cs.cmu.edu/~112/notes/notes-animations-examples.html#imagesDemo
    data.image = PhotoImage(file='nightSky.ppm')
    # New Habit boxes
    data.sleepButton = TextBox(150,50,data.width/2-75,data.height*(3/8))
    data.fruitButton = TextBox(150,50,data.width/2-75,data.height*(4/8))
    data.runningButton = TextBox(150,50,data.width/2-75,data.height*(5/8))
    data.meditationButton = TextBox(150,50,data.width/2-75,data.height*(6/8))
    # General Data boxes
    data.ageButton = TextBox(100,75,data.width/2-100,data.height*0.3)
    data.heightButton = TextBox(100,75,data.width/2-100,data.height*0.5)
    data.weightButton = TextBox(100,75,data.width/2-100,data.height*0.7)
    # General Data text
    data.ageTextLegal,data.weightTextLegal,data.heightTextLegal = False,False,False
    data.ageText,data.weightText,data.heightText = '','',''
    # Sleep Screen 1 Button
    data.sleepScreen2aButton = TextBox(100,75,data.width/2,data.height*0.4)
    data.sleepNumWeeks = ''
    data.sleepScreen2bButton = TextBox(100,75,data.width/2,data.height*0.4)
    data.sleepScreen2bText = ''
    # http://www.cs.cmu.edu/~112/notes/notes-2d-lists.html
    def make2dList(rows, cols):
        a=[]
        for row in range(rows): a += [[0]*cols]
        return a
    data.calContents = make2dList(5,7)
    fillCalendar(data)

def mousePressed(event,data):
    if data.mode == "homeScreen":
        if data.new.insideBox(event.x,event.y):
            data.mode = "newHabit"
        elif data.cont.insideBox(event.x,event.y):
            data.mode = "contHabit"
    if data.mode == "newHabit":
        if data.sleepButton.insideBox(event.x,event.y):
            data.mode = "new/sleep"
        if data.fruitButton.insideBox(event.x,event.y):
            data.mode = "new/fruit"
        if data.runningButton.insideBox(event.x,event.y):
            data.mode = "new/running"
        if data.meditationButton.insideBox(event.x,event.y):
            data.mode = "new/meditation"
    if data.mode == 'new/sleep':
        if data.ageButton.insideBox(event.x,event.y):
            data.ageTextLegal = True
        if data.weightButton.insideBox(event.x,event.y):
            data.weightTextLegal = True
        if data.heightButton.insideBox(event.x,event.y):
            data.heightTextLegal = True

def keyPressed(event, data):
    if event.keysym == 'h':
        data.mode = 'homeScreen'
    if event.keysym == 'n':
        data.mode = 'newHabit'
    if event.keysym == 'c':
        data.mode = 'contHabit'
    if data.mode == 'new/sleep':
        if event.keysym == 'e':
            data.ageText,data.heightText,data.weightText='','',''
        if data.ageTextLegal == True:
            if (data.heightTextLegal or data.weightTextLegal):
                data.ageTextLegal = False
            else: data.ageText+=event.keysym
        if data.heightTextLegal == True:
            if (data.ageTextLegal or data.weightTextLegal):
                data.heightTextLegal = False
            else: data.heightText+=event.keysym
        if data.weightTextLegal == True:
            if (data.heightTextLegal or data.ageTextLegal):
                data.weightTextLegal = False
            else: data.weightText+=event.keysym
        if event.keysym == 'Return':
            data.mode = 'sleep1'
    if data.mode == 'sleep1':
        if event.keysym == 'space':
            data.mode = 'sleep2'
    if data.mode == 'sleep2':
        if event.keysym != 'space':
            data.sleepNumWeeks += event.keysym

def timerFired(data):
    pass

def drawHomeScreen(canvas,data):
    canvas.create_text(data.width/2,data.height*0.35,
        text="Welcome to Patterns of Progress!",fill="white",font="Avenir 30")
    canvas.create_text(data.width/2,data.height*0.45,
        text='Press "h" at any point to return to this screen.',fill='white',
        font='Avenir 16')
    data.new.createBox(canvas,"New Habit",fill='white',outline='white')
    data.cont.createBox(canvas,"Continue Habit",fill='white',outline='white')

def drawCalendar(canvas,data):
    margin = 5
    canvas.create_text(data.width/2,data.height*0.1,
        text="This is your progress thus far.\n\tMay 2017",
        fill='white',font='Avenir 20')
    colWidth  = (data.width - 2*margin)/7
    rowWidth = (data.height - (2*margin+100))/5
    for row in range(5):
        for col in range(7):
            x0 = margin + colWidth * col
            x1 = margin + colWidth * (col+1)
            y0 = margin + 100 + rowWidth * row
            y1 = margin + 100 + rowWidth * (row+1)
            canvas.create_rectangle(x0, y0, x1, y1,fill="white",outline="black")
            canvas.create_text(x0+10,y0+10,text=data.calContents[row][col])

def fillCalendar(data):
    num = 1
    for row in range(5):
        for col in range(7):
            data.calContents[row][col] = num
            num += 1
            if num >= 32: data.calContents[row][col] = None
            
def newHabitScreen(canvas,data):
    canvas.create_text(data.width/2,data.height*(1/4),
        text="Which habit would you like to\n          work on today?",
        fill="white",font = "Avenir 25 bold")
    data.sleepButton.createBox(canvas,"Sleeping")
    data.fruitButton.createBox(canvas,"Eating More Fruit")
    data.runningButton.createBox(canvas,"Running")
    data.meditationButton.createBox(canvas,"Meditation Practice")

# Scrolling text?
def sleepScreen1(canvas,data):
    print('sleepScreen1 called')
    text = """
    In today's busy world, there is hardly any time to prioritize sleeping over
    work despite the countless studies and overwhelming amount of evidence that 
    prove otherwise. This Sleep Tracker is meant to help you be the most
    productive by building a habit of going to bed and waking up at a particular
    time such that you are as well-rested as you can be.
    """
    canvas.create_text(data.width/2,data.height*(1/2),text=text,
        fill='white',font='Avenir 16')
    canvas.create_text(data.width/2,data.height*(7/8),
        text="Press space to continue.",fill='white',font='Avenir 12')

def sleepScreen2a(canvas,data):
    text = """
    How many weeks of data would you like to input?
    """
    canvas.create_text(data.width/2,data.height*0.25,text=text,fill='white',
        font='Avenir 18')
    canvas.create_text(data.width/2,data.height*0.4,text=data.sleepNumWeeks,
        fill='white',font='Avenir 14')
    data.sleepNumWeeks = int(data.sleepNumWeeks)
    print('%d Weeks of Data'% data.sleepNumWeeks)
    daily = list()
    for week in range(int(data.sleepNumWeeks)):
        for day in range(7):
            # add try/except for input
            dayStr = input("Bedtime for Week %d, Day %d (ex.12:00am): " % (week,day))
            time = dayStr[:-2]
            hourMin = time.split(':')
            # avoids adding for 12am
            if 'am' in dayStr and hourMin[0] != '12':
                hourMin[0] = int(hourMin[0])+12
            time = int(hourMin[0]) + int(hourMin[1])/60
            daily += [float(time)]
        if data.sleepNumWeeks > 2:
            # weekly average if there are more than 2 weeks
            dataPoint = sum(daily)/7
            user['bedtime'] += [dataPoint]
            daily = []
            with open('userBedtime.csv','a') as csvfile:
                writer = csv.writer(csvfile, delimiter=' ',quotechar='|',
                    quoting=csv.QUOTE_MINIMAL)
                # print(dataPoint)
                writer.writerow([dataPoint])
        else:
            user['bedtime'] += [daily]
        # http://www.pythonforbeginners.com/systems-programming/
        #       using-the-csv-module-in-python/
        # https://docs.python.org/2/library/csv.html
            with open('userBedtime.csv','a') as csvfile:
                writer = csv.writer(csvfile, delimiter=' ',quotechar='|',
                    quoting=csv.QUOTE_MINIMAL)
                writer.writerow(daily)
            daily = []
    data.mode = 'graph'

def graph(canvas,data):
    import tpML

def generalData(canvas,data):
    text="""
    Let's begin by gathering some information
    about you. Click the box to enter data and 
    press ENTER when you're done.
    """
    canvas.create_text(data.width/2,data.height*(0.2),text=text,fill='white',
        font='Avenir 20')
    data.ageButton.createBox(canvas,'Age\n'+data.ageText)
    data.heightButton.createBox(canvas,'Height\n(inches)\n'+data.heightText)
    data.weightButton.createBox(canvas,'Weight (lbs)\n'+data.weightText)
    # prevent from throwing an error
    general['age']=int(data.ageText)
    general['height']=int(data.heightText)
    general['weight']=int(data.weightText)
    # https://wiki.python.org/moin/UsingPickle
    # Pickle module used to read/write dictionary
    pickle.dump(general,open('save2.p','wb'))

def comingSoon(canvas,data):
    canvas.create_text(data.width/2, data.height/2,text="Coming Soon!",fill='white',
        font='Avenir 30')

def redrawAll(canvas, data):
    # http://www.cs.cmu.edu/~112/notes/notes-animations-examples.html#imagesDemo
    canvas.create_image(0,0,image=data.image)
    if data.mode == "homeScreen":
        drawHomeScreen(canvas,data)
    if data.mode == "newHabit":
        newHabitScreen(canvas,data)
    if data.mode == 'new/sleep':
        generalData(canvas,data)
    if (data.mode=='new/fruit' or data.mode=='new/running' or
        data.mode=='new/meditation'):
        comingSoon(canvas,data)
    if data.mode == 'sleep1':
        sleepScreen1(canvas,data)
    if data.mode == 'sleep2':
        sleepScreen2a(canvas,data)
    if data.mode == 'graph':
        graph(canvas,data)
    if data.mode == "contHabit":
        drawCalendar(canvas,data)

# http://www.cs.cmu.edu/~112/notes/events-example0.py
####################################
def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    root = Tk()
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(600, 600)
