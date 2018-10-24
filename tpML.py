import matplotlib.pyplot as plt
import numpy as np
import csv,os,math,pickle

user = {'bedtime':[],'fruitNum':[],'mileTime':[],'heartRate':[]}

# https://docs.python.org/2/library/csv.html
# used csv docs to read/write csv file
with open('userBedtime.csv', 'r') as csvfile:
     reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
     for row in reader:
         for dataPoint in row:
            print(dataPoint)
            user['bedtime'] += [float(dataPoint)]

# https://wiki.python.org/moin/UsingPickle
# userData = pickle.load(open('save.p','rb'))

general = pickle.load(open('save2.p','rb'))

# calculate stats from userData and use that to compare to ideal
# overlay graphs of user and model

# Sleep
# bedtime + wake up time to suggest whether it matches natural sleep cycles
# http://time.com/3183183/best-time-to-sleep/

def roundHalfUp(n):
    if '.' not in str(n): return int(n)
    decimal = str(n).split('.')[1]
    if float(decimal) < 0.5: return n
    else: return n + 1

# http://www.statisticshowto.com/how-to-find-a-linear-regression-equation/
# used formula from website but manually implemented it in my code in a way
    # that is meaningful
def linearRegression(x,y):
    xSq,XY = [],[]
    n = len(x)
    if n==1: return(y[0],0)
    for i in range(1,len(x)+1):
        xSq += [x[i-1]**2]
        XY += [x[i-1]*y[i-1]]
    sumX,sumY,sumXSq,sumXY = sum(x),sum(y),sum(xSq),sum(XY)
    a = ((sumY*sumXSq) - (sumX*sumXY))/((n*sumXSq) - (sumX*sumX))
    b = ((n*sumXY) - (sumX*sumY))/((n*sumXSq) - (sumX*sumX))
    # a = y-int, b = slope in form y = a + bx
    return (a,b)

def sleepUser(user):
    if general['age'] < 25: idealBedtime = 12
    elif general['age'] < 30: idealBedtime = 11
    else: idealBedtime = 10
    # converts list to an array so numpy can implement it
    avgBedtime = np.mean(np.asarray(user['bedtime']))
    if avgBedtime == idealBedtime: 
        sleepImprovement = 0
    else: 
        sleepImprovement = idealBedtime - avgBedtime
    weeks = list(range(1,len(user['bedtime'])+1))
    x = np.arange(0.5,len(user['bedtime'])+1,0.5)
    line = linearRegression(weeks,user['bedtime'])
    (a,b) = line
    plt.scatter(weeks,user['bedtime'])
    plt.plot(x, a+b*x)
    if len(user['bedtime']) %7 == 0:
        plt.xlabel('Day')
    else:
        plt.xlabel('Week')
    plt.ylabel('Average Bedtime Each Week')
    plt.title('Sleep')
    # creates suitable axes for the graph
    if idealBedtime < min(user['bedtime']):
        plt.axis([0,len(weeks)+2,idealBedtime-1,max(user['bedtime'])+1])
    elif idealBedtime > max(user['bedtime']):
        plt.axis([0,len(weeks)+2,min(user['bedtime'])-1,idealBedtime+1])
    else:
        plt.axis([0,len(weeks)+2,min(user['bedtime'])-1,max(user['bedtime'])+1])
    goal = idealBedtime
    plt.plot(x,goal+0*x)
    predictedBedtime(user,line,idealBedtime)
    wakeUpTime(avgBedtime)
    plt.show()

def predictedBedtime(user, line,idealBedtime):
    (a,b) = line
    nextDay = len(user['bedtime'])+1
    lastPoint = a + b*(len(user['bedtime']))
    if idealBedtime > lastPoint:
        # http://stackoverflow.com/questions/27779845/how-to-plot-one-single-data-point
        # plotted a single point as a marker using a user answer
        plt.plot([nextDay],[idealBedtime],marker='o',markersize=7,color='red')
        plt.text(nextDay, idealBedtime,r'BEDTIME')
        hourMin = str(idealBedtime).split('.')
        if idealBedtime != 12:
            print('Try to go to sleep at %d:%dpm.'%(hourMin[0],hourMin[1]))
        else:
            print('Try to go to sleep at 12am.')
    else:
        if b < 0:
            bedtime = a + b*(nextDay)
        else:
            bedtime = lastPoint + (-0.5*b)*nextDay
        # see citation in lines 86-87
        plt.plot([nextDay],[bedtime],marker='o',markersize=7,color='red')
        plt.text(nextDay, bedtime,r'BEDTIME')
        # manipulation of times from graph to standard time
        hourMin = str(bedtime).split('.')
        hourMin[1] = float('0.%s'% hourMin[1])*60
        hourMin[1] = int(roundHalfUp(hourMin[1]))
        if len(str(hourMin[1])) == 1: 
            hourMin[1] = '0%s' % hourMin[1]
        if bedtime > 12:
            hourMin[0] = str(int(hourMin[0]) - 12)
            print('Try to go to sleep at %s:%sam tonight.'%(hourMin[0],hourMin[1]))
        elif hourMin[0] == 12:
            print('Try to go to sleep at 12:%sam tonight.'%(hourMin[1]))
        else:
            print('Try to go to sleep at %s:%spm tonight.'%(hourMin[0],hourMin[1]))

def wakeUpTime(actualBedtime):
    wakeUp = []
    for i in range(4,7):
        wakeUp += actualBedtime + i*1.5
    print(wakeUp)

# Fruit
def fruitUser(fruitNum,goal):
    weeks = range(len(fruitNum))
    plt.bar(weeks,fruitNum,facecolor='#9999ff',edgecolor='white')
    plt.xlabel('Day')
    plt.ylabel('Number of Fruits Eaten Per Day')
    plt.title('Fruit')
    goal = [goal]*(len(fruitNum))
    plt.plot(weeks,goal)
    plt.show()

# Running
# chart progress of distance run 
# different color dots
def runningUser(distance,weeksRun,goal):
    weeks = range(len(distance))
    for i in range(len(weeksRun)):
        if weeksRun[i] >= goal:
            plt.plot(weeks,distance,'rs')
        else:
            plt.plot(weeks,distance,'g^')
    plt.xlabel('Day')
    plt.ylabel('Rate (in mph)')
    plt.title('Running')
    plt.show()

# Meditation
def meditationUser(time,heartRate):
    plt.plot(time,heartRate)
    plt.xlabel('Time')
    plt.ylabel('HeartRate')
    plt.title('Meditation')
    plt.show()

# other habits in progress
sleepUser(user)