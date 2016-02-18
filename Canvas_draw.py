from Tkinter import *
from ttk import Frame, Button, Style
from ttk import Entry
import time
import math


class Example(Frame):
#Initialise values
    ctrlpt1=[55,55]
    ctrlpt2=[150,120]
    ctrlpt3=[55,215]
    pt1=[50,50]
    pt2=[100,100]
    clickno=2
    toggle = 1
    div_num = 10

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
        self.rowconfigure(7, pad=3)
        self.rowconfigure(8, pad=3)


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
        set_point.grid(row=3, columnspan=2)
     
        self.stop_place = Button(self, text="Toggle delete",\
        command=self.change_toggle)
        self.stop_place.grid(row = 3, column = 2,columnspan=2) 
    
        clr_btn = Button(self, text="Clear Canvas", command=self.clear_canvas)
        clr_btn.grid(row = 4, column = 0,columnspan=2)

        drw_btn = Button(self, text="Draw lines", command=self.draw_ctrllines)
        drw_btn.grid(row = 4, column = 2,columnspan=2)

        div = Button(self, text="Divide", command=self.draw_divide)
        div.grid(row = 5, column = 0,columnspan=2)

        strart = Button(self, text="Strings", command=self.string_art)
        strart.grid(row = 5, column = 2,columnspan=2)

        plotpar = Button(self, text="Parabola", command=self.plot_para)
        plotpar.grid(row = 6, column = 0,columnspan=2)

        self.w = Canvas(self, width=200, height=900)
        self.w.grid(row=7, columnspan=4)


#Draw initial control points for user

        self.id1=self.w.create_oval(self.ctrlpt1[0] - 2, self.ctrlpt1[1] - 2,\
        self.ctrlpt1[0] + 2,self.ctrlpt1[1] + 2,fill="black",tags='maybe')
        self.w.tag_bind(self.id1,'<Button-1>',self.del_elem)


        id2=self.w.create_oval(
                            self.ctrlpt2[0] - 2, self.ctrlpt2[1] - 2,
                            self.ctrlpt2[0] + 2,self.ctrlpt2[1] + 2,fill="black"
                              )
        self.w.tag_bind(id2,'<Button-1>',self.del_elem)

        self.id3=self.w.create_oval(self.ctrlpt3[0] - 2, self.ctrlpt3[1] - 2,\
        self.ctrlpt3[0] + 2,self.ctrlpt3[1] + 2,fill="black")
        self.w.tag_bind(self.id3,'<Button-1>',self.del_elem)
        self.w.bind('<Motion>',self.motion)  
        print self.id1

        movebut = Button(self, text="Grass", command=self.grass_polygon)
        movebut.grid(row = 6, column = 2,columnspan=2)
        
        #self.w.bind('<Button-1>',self.clicky) 
 
        self.pack()    

    def get_div(self):
        try:
            self.div_num=int(self.entry1.get())
            self.lbl1.config(text="Division number set")
            self.lbl3.config(text="Divisions =%r"%self.div_num)
        except ValueError:
            self.lbl1.config(text="Incorrect entry type")

    def draw_divide(self):
        self.w.delete("all")
        list1=self.divide_line(self.ctrlpt1,self.ctrlpt2)
        for n in range(len(list1)):  
            id=self.w.create_oval(
                                list1[n][0] - 2, list1[n][1] - 2, 
                                list1[n][0] + 2,list1[n][1] + 2,fill="black"
                                  )
            self.w.tag_bind(id,'<Button-1>',self.del_elem)
        list2=self.divide_line(self.ctrlpt2,self.ctrlpt3)  
        for n in range(len(list2)):  
            id=self.w.create_oval(
                                list2[n][0] - 2, list2[n][1] - 2, 
                                list2[n][0] + 2,list2[n][1] + 2,fill="black"
                                  )
            self.w.tag_bind(id,'<Button-1>',self.del_elem)
    
    def grass_polygon(self):
        lst=self.intersect_list()
        for n in range(len(lst)-1):
            width=5+10*(1-abs(1-2*(n+1)/float(len(lst))))
            m1 = self.slope(lst[n],lst[n+1])
            m = -1/self.slope(lst[n],lst[n+1])
            print lst[n],m1,m
            dx = math.sqrt(width**2/(1+m**2))
            dy = math.sqrt(width**2/(1+1/m**2))
            x1=math.ceil(lst[n][0]-dx)
            y1=math.ceil(lst[n][1]-dy)
            x2=math.ceil(lst[n][0]+dx)
            y2=math.ceil(lst[n][1]+dy)
            x3=lst[n+1][0]+dx
            y3=lst[n+1][1]+dy
            x4=lst[n+1][0]-dx
            y4=lst[n+1][1]-dy
            if n==0:
                x2=x1=lst[n][0]
                y2=y1=lst[n][1]
                
            self.w.create_polygon(x1,y1,x2,y2,x3,y3,x4,y4,fill='green')
    

    def dist(self,point1,point2):
        x1,y1 = point1
        x2,y2 = point2
        distance = math.sqrt(float((x2-x1))**2+(y2-y1)**2)
        return distance
    
    def slope(self,point1,point2):
        x1,y1 = point1
        x2,y2 = point2
        if abs(x2-x1) > 0.00001:
            m1=(y2+y1)/float(x2-x1)
            return m1
        else:
            return none

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
            
    def plot_para(self):
        plotlist=self.intersect_list()
        for n in range(len(plotlist)):  
            id=self.w.create_oval(
                                plotlist[n][0]-2, plotlist[n][1]-2, 
                                plotlist[n][0]+2, plotlist[n][1]+2,fill="black"
                                  )
            self.w.tag_bind(id,'<Button-1>',self.del_elem)
                    
    def string_art(self):
        list1 = self.divide_line(self.ctrlpt1,self.ctrlpt2)
        list2 = self.divide_line(self.ctrlpt2,self.ctrlpt3)
        zplst = zip(list1[0:len(list1)-1],list2[1:len(list1)])
        for n in range(len(zplst)):  
            id=self.w.create_line(
                                zplst[n][0][0], zplst[n][0][1], 
                                zplst[n][1][0], zplst[n][1][1],fill="black"
                                  )
            self.w.tag_bind(id,'<Button-1>',self.del_elem)

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
                yint=(y2-y1)*x3/float(x2-x1)+y1-float((y2-y1)/float(x2-x1))*x1
            
        return [xint,yint]

    def draw_ctrllines(self):
        x1,y1=self.ctrlpt1
        x2,y2=self.ctrlpt2
        x3,y3=self.ctrlpt3
        line1 = self.w.create_line(x1, y1, x2, y2)
        self.w.tag_bind(line1,'<Button-1>',self.del_elem)
        line2 = self.w.create_line(x2, y2, x3, y3)
        self.w.tag_bind(line2,'<Button-1>',self.del_elem)

    def divide_line(self,point1,point2):
        x1,y1 = point1
        x2,y2 = point2
        list = [0]*(self.div_num+1)
        for n in range(self.div_num+1):
            list[n]=[x1+(n)*(x2-x1)/float(self.div_num),y1+(n)*(y2-y1)/float(self.div_num)]
        return list            

    def change_toggle(self):
        self.toggle=(self.toggle+1)%2
        if self.toggle == 1:
            self.stop_place.config(text="Delete mode off")
        else:
            self.stop_place.config(text="Delete mode on")
    
       
    def del_elem(self,event):
        if self.toggle==1:
            pass
        else:
            print "Hello"
            event.widget.delete("current")
            
    def midpoint(self,x1,x2,y1,y2):
        xmid=(x1+x2)/2
        ymid=(y1+y2)/2
        return xmid,ymid

    def motion(self,event):
        w=self.parent.winfo_screenwidth()
        h=self.parent.winfo_screenheight()
        x,y = self.w.winfo_pointerxy()
        print x-536,y-353
    
    def clear_canvas(self):
        self.w.delete("all") 

                      

def main():
  
    root = Tk()
    app = Example(root)
    w=root.winfo_screenwidth()
    h=root.winfo_screenheight()
    root.geometry("%rx%r+%r+%r" % (w//5,2*h//3,500,100))
    root.mainloop() 



if __name__ == '__main__':
    main()
