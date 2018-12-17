##r = read only
##w = write (deletes the current file contents)
##a = appending mode, can only add data
##r+ = read and write mode

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import copy
import math

fig, ax = plt.subplots()

n = 100
l = 15.0
xmin = -1
ymin = -1
xmax = 1
ymax = 1
bufferr = 0
noColorBar = True

def getField(x, y,charges):
    u,v = 0,0

    for i in range(0,len(charges[0])):

        kqr2 = (9*10**9)*charges[2][i]/((charges[1][i]-y)**2+(charges[0][i]-x)**2)
        theta = np.arctan((charges[1][i]-y)/(charges[0][i]-x))
        end = (charges[0][i]-x)/abs(charges[0][i]-x)

        u+= kqr2 * np.cos(theta) * end
        v+= kqr2 * np.sin(theta) * end


    return (u),(v)


def changeTooClose(x1,bufferr,ys):
    i = 0
    xx2 = list(x1)
    while i<len(xx2):
        for j in ys:
            if abs(xx2[i]-j)<=bufferr:

                xx2[i]+=0.01
        i+=1
    return np.array(xx2)

def adjustNdArray(U):
    a = 4
    L = list(U)
    a = sum(list(L[0])) / float(len(list(L[0])))
    a*=3
    i = 0
    while (i<len(L)):
        L[i] = list(L[i])
        j = 0
        while j<len(L[i]):

            if abs(L[i][j])>a:
                L[i][j] = a*L[i][j]/abs(L[i][j])
            j+=1
        L[i] = np.array(L[i])
        i+=1
    return np.array(L)
def logNdArray(U,a):

    L = list(U)
    avg = sum(L) / float(len(L))
    i = 0
    while (i<len(L)):
        L[i] = list(L[i])
        j = 0
        while j<len(L[i]):

            L[i][j] = math.log(L[i][j],a)
            j+=1
        L[i] = np.array(L[i])
        i+=1
    return np.array(L)


def animate(i):
    global noColorBar

    ax.clear()

    data = open('Data.txt', 'r').read()
    WindowVsPoints = data.split('\n_____\n')
    windows = WindowVsPoints[0].split('\n')
    points = WindowVsPoints[2].split('\n')
    printValFor = WindowVsPoints[3]
    printx, printy = printValFor.split(',')
    dims = []
    for window in windows:
        nothing, value = window.split('= ')
        dims.append(float(value))
    #USE THESE FOR THE CHARGES, NOT THE POINTS TO TEST
    xs = []
    ys = []
    qs = []
    for point in points:
        if len(point) > 1:
            x, y, q= point.split(',')
            xs.append(float(x))
            ys.append(float(y))
            qs.append(-float(q)*10**-9)

    x1 = np.linspace(dims[0],dims[1],n)
    x2 = np.linspace(dims[2],dims[3],n)

    X11,X22 = np.meshgrid(changeTooClose(x1,bufferr,xs),changeTooClose(x2,bufferr,ys))
    U2,V2 = getField(X11,X22,[xs,ys,qs])

    vells = np.hypot(U2,V2)
    S=adjustNdArray(vells)

    x1 = changeTooClose(x1,bufferr,xs)
    x2 = changeTooClose(x2,bufferr,ys)
    X1, X2 = np.meshgrid(x1, x2)
    U,V = getField(X1,X2,[xs,ys,qs])
    vels = np.hypot(U,V)


    strm = ax.streamplot(X1, X2, U, V, color = S, linewidth=1, cmap='cool')

    logS= logNdArray(S,100)
    con = ax.contour(X1,X2,logS,10,cmap = 'magma')

    if noColorBar:
        fig.colorbar(strm.lines)
        fig.colorbar(con)
        noColorBar = False


    for item in range(len(xs)):
        if (qs[item]<0):
            plt.plot(xs[item], ys[item], 'ro', color = 'r')
        elif (qs[item]>0):
            plt.plot(xs[item], ys[item], 'ro', color = 'b')



ani = animation.FuncAnimation(fig, animate, interval = 1000)
plt.show()

