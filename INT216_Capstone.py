import colorsys
import re
from tkinter import *
import csv
import datetime
from tkinter.ttk import Treeview
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
class MovingMessage:
    def __init__(self, canvas, message, start_x, start_y, end_y):
        self.canvas = canvas
        self.message = message
        self.text_id = None
        self.x = start_x
        self.y = start_y
        self.dx =1.0  # change in x per frame
        self.dy = 0.0# change in y per frame
        self.width = 0
        self.height = 0
        self.hue = 0  # initial hue value
    def start(self):
        self.text_id = self.canvas.create_text(self.x, self.y, text=self.message, anchor='w', fill=self.get_color(),font=("Helvetica", 25))
        self.width = self.canvas.bbox(self.text_id)[2] - self.canvas.bbox(self.text_id)[0]
        self.height = self.canvas.bbox(self.text_id)[3] - self.canvas.bbox(self.text_id)[1]
        self.move()
    def move(self):
        self.canvas.move(self.text_id, self.dx, self.dy)
        self.x += self.dx
        self.y += self.dy
        if self.x - self.width >= self.canvas.winfo_width():
            # message has gone off the right edge of the canvas
            self.x = -self.width  # reset to start position on left edge
            self.hue = 0  # reset hue value
        elif self.x <= 0 - self.width:
            # message has gone off the left edge of the canvas
            self.x = self.canvas.winfo_width()  # reset to start position on right edge
            self.hue = 0  # reset hue value
        self.canvas.coords(self.text_id, self.x, self.y)
        self.canvas.itemconfigure(self.text_id, fill=self.get_color())
        self.hue += 0.01  # increase hue value over time
        self.canvas.after(5, self.move)
    def get_color(self):
        # convert hue value to RGB values
        rgb = colorsys.hsv_to_rgb(self.hue % 1, 1, 1)
        # convert RGB values to hexadecimal color code
        hex_code = '#%02x%02x%02x' % tuple(int(x * 255) for x in rgb)
        return hex_code
root = Tk()
root.geometry("1024x600")
root.maxsize(1024, 600)
root.minsize(500, 600)
root.title("*_*....Furit's  Heavenu...*_*")
bg = PhotoImage(file=r"C:\old stuff\Desktop\PhOTosTOre\fruits.png")
cv1 = Canvas(root, width=1024, height=600)
cv1.pack(fill="both", expand=False)
cv1.create_image(0, 0, image=bg, anchor="nw")
cv1.create_text(500, 50, text="*_*....Furit's  Heavenu...*_*", font=('serif', 50, 'bold'),fill="gold")
message = MovingMessage(cv1, "W..E..L.C..O..M..E!", 1, 150, 150)
message.start()
def sell():
    global bg1
    top1 = Toplevel(root)
    top1.geometry('900x600')
    top1.maxsize(900, 600)
    top1.minsize(900, 600)
    bg1 = PhotoImage(file=r"C:\old stuff\Desktop\PhOTosTOre\fruits.png")
    cv2 = Canvas(top1, width=900, height=600)
    cv2.pack(fill='both', expand=True)
    cv2.create_image(0, 0, image=bg1, anchor="nw")
    cv2.create_text(435, 35, text="Let's Sell", font=('Helvetica', 23, 'bold'), fill='orange')
    message = MovingMessage(cv2, "SELLING....HISTORY!", 1, 100, 100)
    message.start()
    label1 = Label(top1, text='Date', font=('Arial', 13, 'bold'), bg='grey', fg='aqua')
    label2 = Label(top1, text='Fruit', font=('Arial', 13,'bold'), bg='grey', fg='aqua')
    label3 = Label(top1, text='Quantiy', font=('Arial', 13, 'bold'), bg='grey', fg='aqua')
    label4 = Label(top1, text='Price', font=('Arial', 13, 'bold'), bg='grey', fg='aqua')
    label1.place(x=250, y=260)
    label2.place(x=250, y=420)
    label3.place(x=750, y=260)
    label4.place(x=750, y=420)
    e1 = Entry(top1, width=23)
    e2 = Entry(top1, width=23)
    e3 = Entry(top1, width=23)
    e4 = Entry(top1, width=23)
    e1.place(x=200, y=300)
    e2.place(x=200, y=450)
    e3.place(x=700, y=300)
    e4.place(x=700, y=450)
    cdf=pd.read_csv('qtable.csv')
    flist=cdf['Fruit'].tolist()
    def check2():
        global inp
        inp = []
        entry = [e1, e2, e3, e4]
        for i in entry:
            inp.append(i.get())
        checklist2 = [False] * 4
        try:
            # Check if input value is a valid date in the format of dd-mm-yyyy
            datetime.datetime.strptime(inp[0], '%d-%m-%Y')
            checklist2[0] = True
        except ValueError:
            # If input is invalid, display error message and destroy after 1 sec
            message_label1 = Label(top1, text="Input is invalid!", fg="red", font=('Arial', 12, 'bold'))
            message_label1.place(x=120, y=330)
            message_label1.after(1200, lambda: message_label1.destroy())
        try:
            # Check if input value only contains alphabets using regex
            if not re.match("^[a-zA-Z]+$", inp[1]) or inp[1] not in flist :
                raise ValueError
            else:
                checklist2[1] = True
        except ValueError:
            # If input is invalid, display error message and destroy after 1 sec
            if not inp[1] in flist:
                message_label2 = Label(top1, text="Fruit is not available", fg="red", font=('Arial', 12, 'bold'))
            else:
                message_label2 = Label(top1, text="Input is invalid!", fg="red", font=('Arial', 12, 'bold'))
            message_label2.place(x=120, y=480)
            message_label2.after(1000, lambda: message_label2.destroy())
        try:
            if not re.match("^[0-9]+$", inp[2]):
                   raise ValueError
            else:
                if inp[2] != '' and inp[2] != "^[a-zA-Z]+$":
                   if int(inp[2]) > int(cdf.loc[cdf['Fruit'] == e2.get(), 'C-quantity']):
                      raise ValueError
                   else:
                        checklist2[2] = True
        except ValueError:
            if inp[2] != '' and inp[2]!="^[a-zA-Z]+$":
                temp = cdf.loc[cdf['Fruit'] == e2.get(), 'C-quantity']
                if int(inp[2]) > int(temp):
                    message_label3 = Label(top1, text="insufficient quantity", fg="red", font=('Arial', 12, 'bold'))
            else:
                message_label3 = Label(top1, text="Input is invalid!", fg="red", font=('Arial', 12, 'bold'))
            message_label3.place(x=700, y=330)
            message_label3.after(1000, lambda: message_label3.destroy())
        try:
            # Check if input value only contains alphabets using regex
            if not re.match("^[0-9]+$", inp[3]) :
                raise ValueError
            else:
                checklist2[3] = True
        except ValueError:
            # If input is invalid, display error message and destroy after 1 sec
            message_label4 = Label(top1, text="Input is invalid!", fg="red", font=('Arial', 12, 'bold'))
            message_label4.place(x=700, y=480)
            message_label4.after(1000, lambda: message_label4.destroy())
        if all(checklist2):
            save2()
            success_label = Label(top1, text="successfully saved buddy", fg="green", font=('Arial', 12, 'bold'))
            success_label.place(x=350, y=250)
            success_label.after(1200, lambda: success_label.destroy())
    def save2():
        global data
        df1 = pd.read_csv("qtable.csv")
        temp1 = e2.get()
        temp2 = e3.get()
        df1.loc[df1['Fruit'] == temp1, 'C-quantity'] -= int(temp2)
        df1.to_csv('qtable.csv', index=False)
        data = [e1.get(), e2.get(), e3.get(), e4.get()]
        file = open('sold.csv', 'a', newline='')
        writer = csv.writer(file)
        writer.writerow(data)
        file.close()
    def clear2():
        e1.delete(0, END)
        e2.delete(0, END)
        e3.delete(0, END)
        e4.delete(0, END)
    top1.title('Sell Fruits')
    btn = Button(top1, text='Save', width=10, padx=4, pady=3, fg='black', bg='spring green', activebackground='grey',command=check2)
    btn.place(x=170, y=550)
    btn1 = Button(top1, text='Quit', width=10, padx=4, pady=3, fg='black', bg='aqua', activebackground='red',
                  command=top1.destroy)
    btn1.place(x=650, y=550)
    btn2 = Button(top1, text='clear', width=10, padx=4, pady=3, fg='black', bg='purple', activebackground='blue',
                  command=clear2)
    btn2.place(x=420, y=550)
def buy():
    global bg2
    top2 = Toplevel(root)
    top2.title('Restocking')
    top2.geometry('1024x600')
    top2.maxsize(1024, 600)
    top2.minsize(500, 500)
    bg2 = PhotoImage(file=r"C:\old stuff\Desktop\PhOTosTOre\fruits.png")
    ca2 = Canvas(top2, width=600, height=400)
    ca2.pack(fill="both", expand=True)
    ca2.create_image(0, 0, image=bg2, anchor="nw")
    ca2.create_text(500, 50, text=" LET's ReSTOCK It :)...", font=('Helvetica', 30, 'bold'))
    message = MovingMessage(ca2, "LeT uS ReFResh :)", 1, 90, 90)
    message.start()
    label1 = Label(top2, text='Date', font=('Arial', 12, 'bold'), bg='grey', fg='aqua')
    label2 = Label(top2, text='Fruit', font=('Arial', 12, 'bold'), bg='grey', fg='aqua')
    label3 = Label(top2, text='Quantiy', font=('Arial', 12, 'bold'), bg='grey', fg='aqua')
    label4 = Label(top2, text='Price', font=('Arial', 12, 'bold'), bg='grey', fg='aqua')
    e1 = Entry(top2, width=23)
    e2 = Entry(top2,  width=23)
    e3 = Entry(top2,  width=23)
    e4 = Entry(top2,  width=23)
    label1.place(x=120, y=300)
    label2.place(x=120, y=450)
    label3.place(x=600, y=300)
    label4.place(x=600, y=450)
    e1.place(x=200, y=300)
    e2.place(x=200, y=450)
    e3.place(x=700, y=300)
    e4.place(x=700, y=450)
    def check1():
        global usi1, usi2, usi3, usi4
        usi1 = e1.get()
        usi2 = e2.get()
        usi3 = e3.get()
        usi4 = e4.get()
        checklist=[False]*4
        try:
            # Check if input value is a valid date in the format of dd-mm-yyyy
            datetime.datetime.strptime(usi1, '%d-%m-%Y')
            checklist[0]=True
        except ValueError:
            # If input is invalid, display error message and destroy after 1 sec
            message_label4 = Label(top2, text="Input is invalid!", fg="red",font=('Arial', 12, 'bold'))
            message_label4.place(x=120, y=330)
            message_label4.after(1000, lambda: message_label4.destroy())
        try:
            # Check if input value only contains alphabets using regex
            if not re.match("^[a-zA-Z]+$", usi2):
                raise ValueError
            else:
                checklist[1] = True
        except ValueError:
            # If input is invalid, display error message and destroy after 1 sec
            message_label = Label(top2, text="Input is invalid!", fg="red",font=('Arial', 12, 'bold'))
            message_label.place(x=120, y=480)
            message_label.after(1000, lambda: message_label.destroy())
        try:
            # Check if input value only contains alphabets using regex
            if not re.match("^[0-9]+$", usi3):
                raise ValueError
            else:
                checklist[2] = True
        except ValueError:
            # If input is invalid, display error message and destroy after 1 sec
            message_label1 = Label(top2, text="Input is invalid!", fg="red",font=('Arial', 12, 'bold'))
            message_label1.place(x=700, y=330)
            message_label1.after(1000, lambda: message_label1.destroy())
        try:
            # Check if input value only contains alphabets using regex
            if not re.match("^[0-9]+$", usi4):
                raise ValueError
            else:
                checklist[3] = True
        except ValueError:
            # If input is invalid, display error message and destroy after 1 sec
            message_label2 = Label(top2, text="Input is invalid!", fg="red",font=('Arial', 12, 'bold'))
            message_label2.place(x=700, y=480)
            message_label2.after(1000, lambda: message_label2.destroy())
        if all(checklist):
            save1()
            success_label = Label(top2, text="successfully saved buddy", fg="green",font=('Arial', 12, 'bold'))
            success_label.place(x=350, y=250)
            success_label.after(1200, lambda: success_label.destroy())
    def save1():
        global data
        df1 = pd.read_csv("qtable.csv")
        temp1 = e2.get()
        temp2 = e3.get()
        df1.loc[df1['Fruit'] == temp1, 'C-quantity'] += int(temp2)
        df1.to_csv('qtable.csv', index=False)
        data = [e1.get(), e2.get(), e3.get(), e4.get()]
        file = open('bought.csv', 'a',newline='')
        writer = csv.writer(file)
        writer.writerow(data)
        file.close()
    def clear1():
        e1.delete(0, END)
        e2.delete(0, END)
        e3.delete(0, END)
        e4.delete(0, END)
    btn = Button(top2, text='Save', width=10, padx=4, pady=3, fg='black', bg='#CCFFCC', activebackground='green',
                 command=check1)
    btn.place(x=200, y=500)
    btn2 = Button(top2, text='Quit', fg='black', bg='#CCFFCC', activebackground='red', command=top2.destroy, width=10,
                  padx=4, pady=3)
    btn2.place(x=600, y=500)
    btn3 = Button(top2, text='clear', width=10, padx=4, pady=3, fg='black', bg='#CCFFCC', activebackground='green',
                  command=clear1)
    btn3.place(x=400, y=500)
def conclusion1():
    top3 = Toplevel(root)
    top3.title('View sold info')
    top3.geometry('1000x600')
    top3.maxsize(1000, 400)
    top3.minsize(600, 400)
    class CSVViewer(Frame):
        def __init__(self, parent):
            Frame.__init__(self, parent)
            # Add label with text above the treeview
            title_label = Label(self, text="This is the sold history", font=("Arial", 16))
            title_label.pack(pady=10)
            self.tree = Treeview(self)
            self.tree.pack(fill="both", expand=True)
            with open("sold.csv", "r") as f:
                reader = csv.reader(f)
                header = next(reader)
                self.tree["columns"] = header
                self.tree.heading("#0", text="S.no")
                for col in header:
                    self.tree.heading(col, text=col)
                i = 1
                for row in reader:
                    self.tree.insert("", "end", text=str(i), values=row)
                    i += 1
    viewer = CSVViewer(top3)
    viewer.pack(fill="both", expand=True)
def conclusion2():
    top4 = Toplevel(root)
    top4.title('View Buy info')
    top4.geometry('1000x600')
    top4.maxsize(1000, 400)
    top4.minsize(600, 400)
    class CSVViewer(Frame):
        def __init__(self, parent):
            Frame.__init__(self, parent)
            # Add label with text above the treeview
            title_label = Label(self, text="This is the bought history", font=("Arial", 16))
            title_label.pack(pady=10)
            self.tree = Treeview(self)
            self.tree.pack(fill="both", expand=True)
            with open("bought.csv", "r") as f:
                reader = csv.reader(f)
                header = next(reader)
                self.tree["columns"] = header
                self.tree.heading("#0", text="S.no")
                for col in header:
                    self.tree.heading(col, text=col)
                i = 1
                for row in reader:
                    self.tree.insert("", "end", text=str(i), values=row)
                    i += 1
    viewer = CSVViewer(top4)
    viewer.pack(fill="both", expand=True)
def current_availability():
    top4 = Toplevel(root)
    top4.title('View Stats')
    top4.geometry('900x600')
    top4.maxsize(900, 600)
    top4.minsize(600, 400)
    df = pd.read_csv("qtable.csv") #quantity table
    fig = Figure(figsize=(15, 15),
                 dpi=90)
    # adding the subplot
    plot2 = fig.add_subplot(111)
    # plotting the graph
    plot2.bar(df['Fruit'], df['C-quantity'])
    plot2.set_xlabel('Fruits')
    plot2.set_ylabel('Quantity')
    plot2.set_title('Fruits vs Current Quantity')
    # creating the Tkinter canvas
    # containing the Matplotlib figure
    canvas = FigureCanvasTkAgg(fig, master=top4)
    canvas.draw()
    # placing the canvas on the Tkinter window
    canvas.get_tk_widget().pack()
    btn4 = Button(top4, text='Quit', fg='black', bg='#FF3333', activebackground='red', command=top4.destroy, width=10,
                  padx=4, pady=3)
    btn4.place(x=400, y=10)
# Create Buttons
button1 = Button(root, text="Vend", width=20,height=2, bg="mistyrose", fg='black', command=sell)
button2 = Button(root, text="Purchase", width=20,height=2, bg='mistyrose', fg='black', command=buy)
button3 = Button(root, text="Sold_History", width=20, height=2,bg='mistyrose', fg='black', command=conclusion1)
button4 = Button(root, text="Buy_History", width=20, height=2,bg='mistyrose', fg='black', command=conclusion2)
button5 = Button(root, text="Cr-Aval", width=20, height=2,bg='mistyrose', fg='black', command=current_availability)
button1_canvas = cv1.create_window(250, 300, window=button1)
button2_canvas = cv1.create_window(750, 300, window=button2)
button3_canvas = cv1.create_window(250, 500, window=button3)
button4_canvas = cv1.create_window(750, 500, window=button4)
button5_canvas = cv1.create_window(510, 550, window=button5)
root.mainloop()
