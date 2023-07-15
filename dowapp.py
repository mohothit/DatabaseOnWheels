from tkinter import messagebox
from tkinter import ttk
from tkinter import *
import mysql.connector
con=mysql.connector.connect(host="localhost",user="root",password="Lakshmi12#",database="dow2")
check=0

def enter():
    def addcar():

        e1=ent1.get()
        e2=ent2.get()
        e3=ent3.get()
        e4=ent4.get()
        e5=ent5.get()
        cur=con.cursor()
        x='y'
        cur.execute("insert into cars(car_id,make,model,rent,available) values(%s,%s,%s,%s,%s)",(e1,e2,e3,e4,x))
        cur.execute("insert into descr(car_id,des) values(%s,%s)",(e1,e5))
        con.commit()
        carid.delete(0,END)
        make.delete(0,END)
        model.delete(0,END)
        price.delete(0,END)
        description.delete(0,END)
        messagebox.showinfo('Success',"Car Inserted!")
    

#Function for deleting a car
    def delcar():
        e1=ent1.get()
        
        cur=con.cursor()
        x='y'
        cur.execute("delete from cars where car_id=%s and available=%s",(e1,x))
        con.commit()
        carid.delete(0,END)
        make.delete(0,END)
        model.delete(0,END)
        price.delete(0,END)
        description.delete(0,END)
        messagebox.showinfo('Success','Car deleted!!')

#creating the main window
    root=Toplevel()
    root.geometry("1200x1200")
    root.title("Database On Wheels")

    #creating a notebook for tabs
    notebook=ttk.Notebook(root)
    notebook.pack()

    #creating 3 frames 
    frame1=Frame(notebook,width=1200,height=1200)
    frame2=Frame(notebook,width=1200,height=1200)  
    frame3=Frame(notebook,width=1200,height=1200)

    frame1.pack(fill="both",expand=1)
    frame2.pack(fill="both",expand=1)
    frame3.pack(fill="both",expand=1)

    notebook.add(frame1,text="Admin")
    notebook.add(frame2,text="Book")
    notebook.add(frame3,text="Return")


    ent1=IntVar()
    ent2=StringVar()
    ent3=StringVar()
    ent4=IntVar()
    ent5=StringVar()

    #adding and droping car window
    if access == 'a':
        lab=Label(frame1,text="Admin Page",font=('arial',15),foreground='#191970').pack()

        lab1=Label(frame1,text="CARID",font=('arial',9),foreground='#191970').place(x=150,y=50)
        carid=Entry(frame1,textvariable=ent1)
        carid.place(x=200,y=50)

        lab2=Label(frame1,text="MAKE",font=('arial',9),foreground='#191970').place(x=150,y=80)
        make=Entry(frame1,textvariable=ent2)
        make.place(x=200,y=80)

        lab3=Label(frame1,text="MODEL",font=('arial',9),foreground='#191970').place(x=150,y=110)
        model=Entry(frame1,textvariable=ent3)
        model.place(x=200,y=110)

        lab4=Label(frame1,text="RENT",font=('arial',9),foreground='#191970').place(x=150,y=140)
        price=Entry(frame1,textvariable=ent4)
        price.place(x=200,y=140)

        lab5=Label(frame1,text="DESCRIPTION",font=('arial',9),foreground='#191970').place(x=110,y=170)
        description=Entry(frame1,textvariable=ent5,width=100)
        description.place(x=200,y=170)

        but1=Button(frame1,text="ADD CAR",font=('arial',9),foreground='#191970',command=addcar).place(x=200,y=200)
        but2=Button(frame1,text="DROP CAR",font=('arial',9),foreground='#191970',command=delcar).place(x=300,y=200)

    #displaying available cars
    labf=Label(frame2,text="AVAILABLE CARS",font=('arial',15),foreground='#191970').pack()

    treescroll=Frame(frame2)
    treescroll.pack()

    scroll=Scrollbar(frame2)
    scroll.pack(side=RIGHT,fill=Y)
    tree=ttk.Treeview(frame2,yscrollcommand=scroll.set) 
    scroll.config(command=tree.yview)


    tree['show']='headings'
    s=ttk.Style(root)
    s.theme_use("clam")
    tree.pack()

    tree['columns']=("Car_id","Make","Model","Rent","Description")
    cur=con.cursor()
    y='y'
    cur.execute("select c.car_id,c.make,c.model,c.rent,d.des from cars c,descr d where c.car_id=d.car_id and c.available='y'")
        
    tree.column("Car_id",width=60,minwidth=60,anchor=CENTER)
    tree.column("Make",width=100,minwidth=100,anchor=CENTER)
    tree.column("Model",width=180,minwidth=180,anchor=CENTER)
    tree.column("Rent",width=80,minwidth=80,anchor=CENTER)
    tree.column("Description",width=500,minwidth=500,anchor=CENTER)

        #headings
    tree.heading("Car_id",text="Car_id",anchor=CENTER)
    tree.heading("Make",text="Make",anchor=CENTER)
    tree.heading("Model",text="Model",anchor=CENTER)
    tree.heading("Rent",text="Rent",anchor=CENTER)
    tree.heading("Description",text="Description",anchor=CENTER)

    i=0
    for row in cur:
        tree.insert('',i,text='',values=(row[0],row[1],row[2],row[3],row[4]))
        i+=1

    con.commit()

    ent6=IntVar()
    ent7=StringVar()
    ent8=StringVar()
    ent9=StringVar()
    ent10=StringVar()

    #function to book a car
    def bookcar():
        a=ent6.get()
        b=ent7.get()
        c=ent8.get()
        d=ent9.get()
        e=ent10.get()
        cur=con.cursor()
        cur.execute("insert into users(name,email,startdate,loc) values(%s,%s,%s,%s)",(b,c,d,e))
        con.commit()
        cur=con.cursor()
        cur.execute("select user_id from users where name=%s and email=%s",(b,c))
        ac=0
        for r in cur:
            ac=r[0]
        con.commit()
        cur=con.cursor()
        n='n'
        cur.execute("insert into manages(user_id,car_id) values(%s,%s)",(ac,a))
        x='n'
        cur.execute("update cars set available=%s where car_id=%s",(x,a))
        con.commit()


        cur.execute("delete from manages where car_id not in (select car_id from cars)")
        con.commit()
        cur.execute("delete from users where user_id not in (select user_id from manages)")
        con.commit()
        messagebox.showinfo("Success","Car Booked")
        carbook.delete(0,END)
        carname.delete(0,END)
        carmail.delete(0,END)
        cardate.delete(0,END)
        carloc.delete(0,END)

    def returncar():
        root1=Toplevel()
        root1.geometry("1200x1200")
        root1.title("RETURN CAR")
        lab=Label(root1,text="CARS TO BE RETURNED",font=('arial',9),foreground='#191970').pack()
        tree1=ttk.Treeview(root1)
        tree1["show"]="headings"
        s=ttk.Style(root1)
        s.theme_use("clam")
        tree1["columns"]=("Carid","Userid","Name","Email")
        tree1.column("Carid",width=50,minwidth=50,anchor=CENTER)
        tree1.column("Userid",width=50,minwidth=50,anchor=CENTER)
        tree1.column("Name",width=120,minwidth=120,anchor=CENTER)
        tree1.column("Email",width=180,minwidth=180,anchor=CENTER)

        tree1.heading("Carid",text="Car_id",anchor=CENTER)
        tree1.heading("Userid",text="User_id",anchor=CENTER)
        tree1.heading("Name",text="Name",anchor=CENTER)
        tree1.heading("Email",text="Email",anchor=CENTER)

        cur=con.cursor()
        cur.execute("select car_id,user_id,name,email from manages natural join users natural join cars where available='n'")
        i=0
        for row in cur:
            tree1.insert('',i,text='',values=(row[0],row[1],row[2],row[3]))
            i+=1
        con.commit()

        
        def rccar():
            s1=bt1.get()
            s2=bt2.get()
            s3=bt3.get()
            y='y'
            cur=con.cursor()
            cur.execute("update cars set available=%s where car_id=%s",(y,s1))
            con.commit()
            cur.execute("delete from manages where car_id=%s and user_id=%s",(s1,s2))
            con.commit()
            messagebox.showinfo("Car Returned","Thank You Come Again!")
            b1.delete(0,END)
            b2.delete(0,END)
            b3.delete(0,END)
            
        bt1=IntVar()
        bt2=IntVar()
        bt3=StringVar()
        
        
        
        l1=Label(root1,text="CARID",font=('arial',9),foreground='#191970').place(x=210,y=270)
        b1=Entry(root1,textvariable=bt1)
        b1.place(x=260,y=270)

        l2=Label(root1,text="USERID",font=('arial',9),foreground='#191970').place(x=210,y=300)
        b2=Entry(root1,textvariable=bt2)
        b2.place(x=260,y=300)
        
        l3=Label(root1,text="NAME",font=('arial',9),foreground='#191970').place(x=210,y=330)
        b3=Entry(root1,textvariable=bt3)
        b3.place(x=260,y=330)

        b4=Button(root1,text="RETURN CAR",font=('arial',9),foreground='#191970',command=rccar).place(x=250,y=370)

        vsb=ttk.Scrollbar(root1,orient="vertical")
        vsb.configure(command=tree1.yview)
        tree1.configure(yscrollcommand=vsb.set)
        vsb.pack(fill=Y,side=RIGHT)
        
        
        tree1.pack()    
        root1.mainloop()



    lab6=Label(frame2,text="CARID",font=('arial',9),foreground='#191970').place(x=150,y=270)
    carbook=Entry(frame2,textvariable=ent6)
    carbook.place(x=200,y=270)

    lab7=Label(frame2,text="NAME",font=('arial',9),foreground='#191970').place(x=150,y=300)
    carname=Entry(frame2,textvariable=ent7)
    carname.place(x=200,y=300)

    lab8=Label(frame2,text="EMAIL",font=('arial',9),foreground='#191970').place(x=150,y=330)
    carmail=Entry(frame2,textvariable=ent8)
    carmail.place(x=200,y=330)

    lab9=Label(frame2,text="DATE",font=('arial',9),foreground='#191970').place(x=150,y=360)
    cardate=Entry(frame2,textvariable=ent9)
    cardate.place(x=200,y=360)

    lab10=Label(frame2,text="LOCATION",font=('arial',9),foreground='#191970').place(x=130,y=390)
    carloc=Entry(frame2,textvariable=ent10)
    carloc.place(x=200,y=390)

    but3=Button(frame2,text="BOOK CAR",font=('arial',9),foreground='#191970',command=bookcar).place(x=200,y=420)
    b10=Button(frame2,text="REFRESH",font=('arial',9),foreground='#191970',command=enter).place(x=290,y=420)

    la=Label(frame3,text="RETURN CAR PORTAL",font=('arial',20),foreground='#191970').place(x=400,y=10)
    but4=Button(frame3,text="GO TO RETURN CAR",font=('arial',9),foreground='#191970',command=returncar).place(x=500,y=100)

    frame2.mainloop()
    root.mainloop()



def submit():
    c=0
    username=a.get()
    password=b.get()
    cur.execute("select * from admin")
    for i in cur:
        if i[0]==username and i[1]==password:
            global check
            c=1
            check=1
    if c==1:
        messagebox.showinfo("Admin Login","Welcome!")
        global access
        access='a'
        enter()
    else:
        messagebox.showwarning("Admin Login!","Invalid Paramters,Try Again!")

def signup():
    usrn=a.get()
    pswd=b.get()
    cur=con.cursor()
    cur.execute("insert into userlog(usern,passw) values (%s,%s)",(usrn,pswd))
    con.commit()
    g.delete(0,END)
    h.delete(0,END)
    messagebox.showinfo("Signup","Signed up!")

def usubmit():
    c=0
    username=a.get()
    password=b.get()
    cur.execute("select * from userlog")
    for i in cur:
        if i[0]==username and i[1]==password:
            global check
            c=1
            check=1
    if c==1:
        messagebox.showinfo("User Login","Welcome!")
        global access
        access='u'
        enter()
    else:
        messagebox.showwarning("User Login","Invalid Parameters,Try Again!")



    
r=Tk()
r.title("Database on Wheels Login")
r.geometry("500x500")
s=ttk.Style(r)
s.theme_use("clam")
cur=con.cursor()
a=StringVar()
b=StringVar()
t=Label(r,text="Welcome to Database on Wheels",font=('arial black',20),foreground='#191970').pack()
user=Label(r,text="USERNAME",font=('arial',9),foreground='#191970').place(x=145,y=150)
g=Entry(r,textvariable=a)
g.place(x=220,y=150)
passw=Label(r,text="PASSWORD",font=('arial',9),foreground='#191970').place(x=145,y=180)
h=Entry(r,textvariable=b,show="*")
h.place(x=220,y=180)
bo=Button(r,text="Login as Admin",font=('arial',9),foreground='#191970',command=submit)
bo.place(x=180,y=220)
bo1=Button(r,text="Login as User",font=('arial',9),foreground='#191970',command=usubmit)
bo1.place(x=290,y=220)
bo2=Button(r,text="Sign Up",font=('arial',9),foreground='#191970',command=signup)
bo2.place(x=270,y=260)
con.commit()
r.mainloop()

