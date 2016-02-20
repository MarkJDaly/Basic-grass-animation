from Tkinter import *
from ttk import Frame, Button, Style
from ttk import Entry
import random
import time
import math

class Example(Frame):

#initilise Frame then initialise this Example class using initUI() 
    def __init__(self, parent,grassd):
        self.grassdict=grassd
        self.keys=self.grassdict.keys()
        self.keys.sort()
        start_time=time.time()
        Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()
        

        
    def initUI(self):

      
        self.parent.title("Grass")
#Configure parent for column layout       
        Style().configure("TButton", padding=(0, 5, 0, 5), 
            font='serif 10')
        
        self.columnconfigure(0, pad=3)
        self.columnconfigure(1, pad=3)
        self.columnconfigure(2, pad=3)
        self.columnconfigure(3, pad=3)
        
        self.rowconfigure(0, pad=3)
        self.rowconfigure(1, pad=3)
        self.rowconfigure(2, pad=3)
        self.rowconfigure(3, pad=3)
        self.rowconfigure(4, pad=3)
        self.rowconfigure(5, pad=3)
        self.rowconfigure(6, pad=3)

        self.w=self.winfo_screenwidth()//3
        self.h=self.winfo_screenheight()
        print self.w,self.h

        self.w = Canvas(self, width=self.w, height=self.h)
        self.w.grid(row=1, columnspan=4)
        self.after(70,self.draw)
        self.pack() 

    def draw(self):
        self.w.delete("all")
        self.w.create_polygon(50,100,405,100,405,668,50,668,fill='#A74A2A')
        for n in self.keys:
            self.grassdict[n].draw(self.w)
  
        self.after(70,self.draw)

class Grass(object):

#initilise Frame then initialise this Example class using initUI() 
    def __init__(self,pt1, pt2, pt3,freq,phs,starttime):
        self.phase=phs
        self.f=freq
        self.ctrlpt1=pt1
        self.ctrlpt2=pt2
        self.ctrlpt3=pt3
        self.ctrlpt1x=self.ctrlpt1[0]
        self.ctrlpt1y=self.ctrlpt1[1]
        self.div_num = 8
        self.start_time=starttime
        

    

#Main function that draws the grass then reinitialises the after method on the Frame

    def draw(self,canvas):  
            newx=self.ctrlpt1x+50*math.sin(self.phase+3.14*(0.1+self.f)*(self.start_time-time.time()))
            self.ctrlpt1=[newx,self.ctrlpt1y]  
            self.grass_polygon(canvas)


#Draws the positions of each division

    def draw_divide(self,canvas):
        cnv=canvas
        list1=self.divide_line(self.ctrlpt1,self.ctrlpt2)
        for n in range(len(list1)):  
            cnv.create_oval(
                           list1[n][0] - 2, list1[n][1] - 2, 
                           list1[n][0] + 2,list1[n][1] + 2,fill="black"
                           )
        list2=self.divide_line(self.ctrlpt2,self.ctrlpt3)  
        for n in range(len(list2)):  
            cnv.create_oval(
                           list2[n][0] - 2, list2[n][1] - 2, 
                           list2[n][0] + 2,list2[n][1] + 2,fill="black"
                           )  
#Draws the polygons for each section of the grass (Clean up function)
 
    def grass_polygon(self,canvas):
        cnv = canvas
        lst=self.intersect_list()
        pluslst2=[0]*(2*(len(lst)-1)-1)
        minuslst2=[0]*(2*(len(lst)-1)-1)
        pluslst2[0:1]=lst[0][1],lst[0][0]
        minuslst2[0:1]=lst[0]
        try:
            for n in range(1,len(lst)-1):
                width=2+10*(1-abs(1-2*(n+2)/float(len(lst))))
                m1 = self.slope(lst[n],lst[n+1]) 
                m = -1/m1
                dx = math.sqrt(width**2/(1+m**2))
                dy = math.sqrt(width**2/(1+1/m**2))
                minuslst2[2*n]=math.ceil(lst[n][0]-dx)
                minuslst2[2*n+1]=math.ceil(lst[n][1]-dy)
                pluslst2[2*n+1]=math.ceil(lst[n][0]+dx)
                pluslst2[2*n]=math.ceil(lst[n][1]+dy)
            pluslst2.reverse()    
            cnv.create_polygon(minuslst2,pluslst2,fill='green',outline='black')
        except TypeError:
            print "Slope error"
            

#Standard slope function (Convert to matrix form maybe? also fix the perp line case)   
    
    def slope(self,point1,point2):
        x1,y1 = point1
        x2,y2 = point2
        if abs(x2-x1) > 0.00001:
            m1=(y2+y1)/float(x2-x1)
            return m1
        else:
            return 'slope_error'
#Gets all the intersection points needed for the parabola

    def intersect_list(self):
        list1 = self.divide_line(self.ctrlpt1,self.ctrlpt2)
        list2 = self.divide_line(self.ctrlpt2,self.ctrlpt3)
        zplst = zip(list1[0:len(list1)-1],list2[1:len(list1)])
        para_list=[0]*(len(zplst)+1)
        para_list[0]=self.ctrlpt1
        para_list[len(zplst)]=self.ctrlpt3
        for n in range(len(zplst)-1):
            para_list[n+1]=self.intersection(
                                        zplst[n][0],zplst[n][1],
                                        zplst[n+1][0],zplst[n+1][1]
                                        )
        return para_list
  
#Draws the parabola points
          
    def plot_para(self,canvas):
        cnv = canvas
        plotlist=self.intersect_list()
        for n in range(len(plotlist)):  
            cnv.create_oval(
                                plotlist[n][0]-2, plotlist[n][1]-2, 
                                plotlist[n][0]+2, plotlist[n][1]+2,fill="black"
                                )

#Draws the strings
                    
    def string_art(self,canvas):
        cnv = canvas
        list1 = self.divide_line(self.ctrlpt1,self.ctrlpt2)
        list2 = self.divide_line(self.ctrlpt2,self.ctrlpt3)
        zplst = zip(list1[0:len(list1)-1],list2[1:len(list1)])
        for n in range(len(zplst)):  
            cnv.create_line(
                                zplst[n][0][0], zplst[n][0][1], 
                                zplst[n][1][0], zplst[n][1][1],fill="black"
                                         )

#Given four points which define two lines it finds the intersection point of the two lines. (Use matrix form)

    def intersection(self,point1,point2,point3,point4):
        x1,y1 = point1
        x2,y2 = point2
        x3,y3 = point3
        x4,y4 = point4
        if abs(x2-x1) > 0.00001 and abs(x4-x3) > 0.00001:
            m1=(y2-y1)/float(x2-x1)
            c1=y1-float(m1)*x1
            m2=(y4-y3)/float(x4-x3)
            c2=y3-float(m2)*x3
            xint = (c2-c1)/float((m1-m2))
            yint = m1*((c2-c1)/float((m1-m2)))+c1
        else:
            if abs(x2-x1) < 0.00001:
                xint=x2
                yint=(y4-y3)*x2/float(x4-x3)+y3-float((y4-y3)/float(x4-x3))*x3
            elif abs(x4-x3) < 0.00001:
                xint=x3
                yint=(y2-y1)/float(x2-x1)*x3+y1-float((y2-y1)/float(x2-x1))*x1
            
        return [xint,yint]

#Finds the points which divide a line defined by two points in to div_num sections

    def divide_line(self,point1,point2):
        x1,y1 = point1
        x2,y2 = point2
        list = [0]*(self.div_num+1)
        for n in range(self.div_num+1):
            list[n]=[x1+(n)*(x2-x1)/float(self.div_num),
            y1+(n)*(y2-y1)/float(self.div_num)]
        return list     

def main():
    start_time=time.time()
    grassdict={}
    L=300
    Lmin=100
    try:
        numgrass=int(raw_input("How many blades of grass?"))
    except ValueError:
        print "Enter a valid integer"
    for n in range(numgrass):
        [x3,y3] = [70+math.ceil(random.random()*315),
                   L/2+math.ceil(random.random()*(668-L/float(2)))]
        [x2,y2] = [x3+math.ceil(random.uniform(-1,1)*50),
                   y3-Lmin/2-math.ceil(random.random()*(L-Lmin)/float(2))]
        [x1,y1] = [x3-20,y3-Lmin/2-math.ceil(random.random()*(L-Lmin)/float(2))]
        freq=random.random()*0.1
        phase=random.random()*3.14
        grassdict['{0:03}{1:03}grass'.format(y3,x3)]=Grass([x1,y1],[x2,y2],[x3,y3],freq,phase,start_time)
    print len(grassdict)
    root = Tk()
    app = Example(root,grassdict)
    w=root.winfo_screenwidth()
    h=root.winfo_screenheight()
    root.geometry("%rx%r+%r+%r" % (w//3,h,500,100))
    root.mainloop() 


#Start program!

if __name__ == '__main__':
    main()

