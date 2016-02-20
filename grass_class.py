from Tkinter import *
from ttk import Frame, Button, Style
from ttk import Entry
import time
import math


class Example(Frame):
#Initialise values

    start_time=time.time()
    para_toggle=0
    grass_toggle=1
    string_toggle=0
    divide_toggle=0
    ctrl_toggle=0
    ctrlpt1=[85,55]
    ctrlpt1x=ctrlpt1[0]
    ctrlpt2=[150,180]
    ctrlpt3=[105,255]
    div_num = 8

#initilise Frame then initialise this Example class using initUI() 
    def __init__(self, parent):
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

#Buttons and stuff

        frame1 = Frame(self)
        frame1.grid(row=0,columnspan=4)
        self.lbl1 = Label(frame1, text="")
        self.lbl1.pack(side=LEFT, padx=5, pady=5)

        frame2 = Frame(self)
        frame2.grid(row=1,columnspan=4)
        lbl2 = Label(frame2, text="Divisions", width=6)
        lbl2.pack(side=LEFT, padx=5, pady=5)
        self.entry1=Entry(frame2) 
        self.entry1.pack(fill=X, padx=5, expand=True)        
        
        frame3 = Frame(self)
        frame3.grid(row=2,columnspan=4)
        self.lbl3 = Label(frame3, text="Divisions =%r"%self.div_num)
        self.lbl3.pack(side=LEFT, expand=True)
    

        set_point = Button(self, text="Set divisions", command=self.get_div)
        set_point.grid(row=3, column=0)

        show_ctrl_points = Button(
                                  self, text="Control points",
                                  command=self.toggle_ctrl
                                  )
        show_ctrl_points.grid(row=3, column=2)
               
        div = Button(self, text="Divide", command=self.toggle_divide)
        div.grid(row = 5, column = 0,columnspan=2)

        strart = Button(self, text="Strings", command=self.toggle_string)
        strart.grid(row = 5, column = 2,columnspan=2)

        plotpar = Button(self, text="Parabola", command=self.toggle_para)
        plotpar.grid(row = 6, column = 0,columnspan=2)

        grass = Button(self, text="Grass", command=self.toggle_grass)
        grass.grid(row = 6, column = 2,columnspan=2)

        self.w = Canvas(self, width=200, height=900)
        self.w.grid(row=7, columnspan=4)
        self.after(70,self.draw)
        self.pack() 

#Draw initial control points for user


        

#Various toggles to show/remove parts of the model

    def toggle_ctrl(self):
        self.ctrl_toggle=(self.ctrl_toggle+1)%2
   
    def toggle_para(self):
        self.para_toggle=(self.para_toggle+1)%2

    def toggle_grass(self):
        self.grass_toggle=(self.grass_toggle+1)%2
    
    def toggle_string(self):
        self.string_toggle=(self.string_toggle+1)%2  
   
    def toggle_divide(self):
        self.divide_toggle=(self.divide_toggle+1)%2  

#Main function that draws the grass then reinitialises the after method on the Frame

    def draw(self):  
            newx=self.ctrlpt1x+50*math.sin(3.14*0.5*(self.start_time-time.time()))
            self.ctrlpt1=[newx,55]
            self.w.delete("all")
            if self.divide_toggle==1:
                self.draw_divide()
            if self.grass_toggle==1:       
                self.grass_polygon()
                self.w.create_polygon(0,235,400,235,400,400,0,400,fill='#A74A2A')
            if self.string_toggle==1:
                self.string_art()
            if self.para_toggle==1:
                self.plot_para()
            if self.ctrl_toggle==1:
                self.w.create_oval(
                                   self.ctrlpt1[0] - 2, self.ctrlpt1[1] - 2, 
                                   self.ctrlpt1[0] + 2, self.ctrlpt1[1] + 2,
                                   fill="black"
                                  )
                self.w.create_oval(
                                   self.ctrlpt2[0] - 2, self.ctrlpt2[1] - 2, 
                                   self.ctrlpt2[0] + 2, self.ctrlpt2[1] + 2,
                                   fill="black"
                                  )
                self.w.create_oval(
                                   self.ctrlpt3[0] - 2, self.ctrlpt3[1] - 2, 
                                   self.ctrlpt3[0] + 2, self.ctrlpt3[1] + 2,
                                   fill="black"
                                  )
            self.after(70,self.draw)
  
#Gets the number of divisions from the label and then sets it          
    
    def get_div(self):
        try:
            self.div_num=int(self.entry1.get())
            self.lbl1.config(text="Division number set")
            self.lbl3.config(text="Divisions =%r"%self.div_num)
        except ValueError:
            self.lbl1.config(text="Incorrect entry type")

#Draws the positions of each division

    def draw_divide(self):
        self.w.delete("all")
        list1=self.divide_line(self.ctrlpt1,self.ctrlpt2)
        for n in range(len(list1)):  
            self.w.create_oval(
                               list1[n][0] - 2, list1[n][1] - 2, 
                               list1[n][0] + 2,list1[n][1] + 2,fill="black"
                              )
        list2=self.divide_line(self.ctrlpt2,self.ctrlpt3)  
        for n in range(len(list2)):  
            self.w.create_oval(
                               list2[n][0] - 2, list2[n][1] - 2, 
                               list2[n][0] + 2,list2[n][1] + 2,fill="black"
                              )  
#Draws the polygons for each section of the grass (Clean up function)
 
    def grass_polygon(self):
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
            self.w.create_polygon(minuslst2,pluslst2,fill='green')
        except TypeError:
            self.lbl1.config(text="Slope error")
            

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
          
    def plot_para(self):
        plotlist=self.intersect_list()
        for n in range(len(plotlist)):  
            self.w.create_oval(
                                plotlist[n][0]-2, plotlist[n][1]-2, 
                                plotlist[n][0]+2, plotlist[n][1]+2,fill="black"
                                  )

#Draws the strings
                    
    def string_art(self):
        list1 = self.divide_line(self.ctrlpt1,self.ctrlpt2)
        list2 = self.divide_line(self.ctrlpt2,self.ctrlpt3)
        zplst = zip(list1[0:len(list1)-1],list2[1:len(list1)])
        for n in range(len(zplst)):  
            self.w.create_line(
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
            else:
                xint=x3
            
        return [xint,yint]

#Finds the points which divide a line defined by two points in to div_num sections

    def divide_line(self,point1,point2):
        x1,y1 = point1
        x2,y2 = point2
        list = [0]*(self.div_num+1)
        for n in range(self.div_num+1):
            list[n]=[x1+(n)*(x2-x1)/float(self.div_num),y1+(n)*(y2-y1)/float(self.div_num)]
        return list     
#Clears the canvas       

    def clear_canvas(self):
        self.w.delete("all") 


#Called to initialise the frame                      

def main():
  
    root = Tk()
    app = Example(root)
    w=root.winfo_screenwidth()
    h=root.winfo_screenheight()
    root.geometry("%rx%r+%r+%r" % (w//3,h,500,100))
    root.mainloop() 

#Start program!

if __name__ == '__main__':
    main()
