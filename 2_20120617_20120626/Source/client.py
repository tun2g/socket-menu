
import tkinter as tk
from tkinter import   messagebox
import socket
import json



HOST="127.0.0.1"
SERVER_PORT= 5050
FORMAT="utf8"
CONNECT="connect"
SEEMENU="see menu"
ORDERFOOD="order food"
EXIT="exit"
PAYMENT="payment"
CASH="cash"
CARD="card"
ADDORDER="add order"


def sendList(client, list):
    for item in list:
        client.sendall(item.encode(FORMAT))
        #wait response
        client.recv(1024)

    msg = "end"
    client.sendall(msg.encode(FORMAT))

# class CHECKIN(tk.Frame):
#     def __init__(self, parent, appController):
#         #khởi tạo với Frame start page
#         tk.Frame.__init__(self, parent)
#         self.configure(bg = "#ffffff")
#         canvas = tk.Canvas(
#         self,
#         bg = "#ffffff",
#         height = 300,
#         width = 500,
#         bd = 0,
#         highlightthickness = 0,
#         relief = "ridge")
#         canvas.place(x = 0, y = 0)
#         btn_menu=tk.Button(self,text="menu",bg="blue",fg="white",
#                             font=('calibre',10,'bold'),
#                             command=lambda:appController.showFrame(MENU))

#         # set table
#         self.Table_Frame = tk.Frame(self, bd = 4, relief="ridge", bg="#01458E") #bg = "màu"
#         self.Table_Frame.place(x = 8, y = 90, width=492, height=250)

#         self.scrollx = tk.Scrollbar(self.Table_Frame, orient=HORIZONTAL)
#         self.scrolly = tk.Scrollbar(self.Table_Frame, orient=VERTICAL)

#         self.Table = ttk.Treeview(self.Table_Frame, columns=(1,2,3), show="headings",xscrollcommand=self.scrollx.set, yscrollcommand=self.scrolly.set)
#         # window.scrollx.pack(side=BOTTOM, fill=X)
#         self.scrolly.pack(side=RIGHT, fill=Y)
#         # window.scrollx.config(command=Table.xview
#         self.scrolly.config(command=self.Table.yview)


#         self.Table.heading(1, text="TABLE")
#         self.Table.heading(2, text="STATE")


#         self.Table.column(1,width=40)
#         self.Table.column(2,width=40)

#         self.Table.pack(fill=BOTH, expand=1)
        
#         def showClient():
#             fileIn = open('table_onl.json',"r")
#             tablesState = json.loads(fileIn.read())
#             fileIn.close()
#             self.Table.delete(*self.Table.get_children())
#             id = 1
#             for table in tablesState:
#                 self.Table.insert(parent='', index='end',
#                 values=(table["number"], table["state"]))
#                 id += 1
#         btn_reset=tk.Button(self,text="reset",bg="blue",fg="white",
#                             font=('calibre',10,'bold'),
#                             command=showClient)

#         btn_reset.place(
#                 x = 40, y = 40)


#         btn_menu.place(
#             x = 430, y = 10)
class MENU(tk.Frame):
    def __init__(self, parent, appController):
        tk.Frame.__init__(self, parent)

        self.configure(bg = "#ffffff")
        num_t1_val=tk.StringVar()
        num_t2_val=tk.StringVar()
        num_t3_val=tk.StringVar()
        num_t4_val=tk.StringVar()
        tb_num=tk.StringVar()

       
        def orderFoodoption():
            t1=num_t1_val.get()
            t2=num_t2_val.get()
            t3=num_t3_val.get()
            t4=num_t4_val.get()
            t=tb_num.get()

            if(t==""):
                messagebox.showerror("lỗi","chưa nhập số bàn")
            
            fileIn = open("table_onl.json","r")
            tablesState = json.loads(fileIn.read())
            fileIn.close()

            for item in tablesState:
                if item["number"]==t:
                    item["state"]="da co"
            fileOut=open("table_onl.json","w")
            fileOut.write(json.dumps(tablesState))
            fileOut.close()

            foodidx=[]
            numberidx=[]
            #if(check==1):
            msg=ORDERFOOD

            client.sendall(msg.encode(FORMAT))

            msg=t
            client.sendall(str(msg).encode(FORMAT))
            
            client.recv(5).decode(FORMAT)
            print(t1)
            print(t2)
            print(t3)
            print(t4)
            if(t1.isnumeric() and t1!=""):
                foodidx.append("bun gio heo")
                numberidx.append(t1)
            if(t2.isnumeric() and t2!=""):
                foodidx.append("bun bo")
                numberidx.append(t2)
            if t3.isnumeric() and t3!="":
                foodidx.append("banh canh ca loc")
                numberidx.append(t3)
            if(t4.isnumeric() and t4!=""):
                foodidx.append("banh canh cua")
                numberidx.append(t4)    
            sendList(client,foodidx)
            #print("oke")
            client.recv(10).decode(FORMAT)
            sendList(client,numberidx)

            sumMoney=client.recv(20).decode(FORMAT)

            print("Tổng số tiền là: "+sumMoney) 
            messagebox.showinfo("Tiền thanh toán","tổng số tiền là"+str(sumMoney))
            #self.showFrame(FPAYMENT)
            num_t1_val.set("")
            num_t2_val.set("")
            num_t3_val.set("")
            num_t4_val.set("")
            tb_num.set("")
        canvas = tk.Canvas(
        self,
        bg = "#ffffff",
        height = 580,
        width = 460,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge")
        canvas.place(x = 0, y = 0)
        self.background_img = tk.PhotoImage(file = f"images/menu.png")

        self.background = canvas.create_image(
            220.0, 280.0,
            image=self.background_img)

        
        btn_order=tk.Button(self,text="tính tiền",bg="blue",fg="white",
                            font=('calibre',10,'bold'),
                            command=orderFoodoption)

        btn_order.place(
            x = 390, y = 10)
        btn_add_order=tk.Button(self,text="đặt thêm",bg="blue",fg="white",
                            font=('calibre',10,'bold'),
                            command=lambda:appController.showFrame(FADDORDER))

        btn_add_order.place(
            x = 390, y = 40)

        btn_payment=tk.Button(self,text="thanh toán",bg="blue",fg="white",
                            font=('calibre',10,'bold'),
                            command=lambda:appController.showFrame(FPAYMENT))

        btn_payment.place(
            x = 390, y = 70)
        # btn_add_order=tk.Button(self,text="đặt thêm",bg="blue",fg="white",
        #                     font=('calibre',10,'bold'),
        #                     command=addOrder)

        # btn_add_order.place(
        #     x = 390, y = 40)
        tb_num_label = tk.Label(self, text = 'Số bàn:', font=('calibre',10, 'bold'))        
        tb_num_entry = tk.Entry(self,textvariable = tb_num, font=('calibre',10,'normal'))

        num_t1_label = tk.Label(self, text = 'Số lượng:', font=('calibre',10, 'bold'))        
        num_t1_entry = tk.Entry(self,textvariable = num_t1_val, font=('calibre',10,'normal'))

        num_t2_label = tk.Label(self, text = 'Số lượng:', font=('calibre',10, 'bold'))        
        num_t2_entry = tk.Entry(self,textvariable = num_t2_val, font=('calibre',10,'normal'))

        num_t3_label = tk.Label(self, text = 'Số lượng:', font=('calibre',10, 'bold'))        
        num_t3_entry = tk.Entry(self,textvariable = num_t3_val, font=('calibre',10,'normal'))

        num_t4_label = tk.Label(self, text = 'Số lượng:', font=('calibre',10, 'bold'))        
        num_t4_entry = tk.Entry(self,textvariable = num_t4_val, font=('calibre',10,'normal'))

        tb_num_label.place(x=270,y=12)
        tb_num_entry.place(x=330,y=12,width=30)

        kc=71
        num_t1_label.place(x=7,y=320)
        num_t1_entry.place(x=7+kc,y=320,width=30)

        num_t2_label.place(x=270,y=320)
        num_t2_entry.place(x=270+kc,y=320,width=30)

        num_t3_label.place(x=7,y=550)
        num_t3_entry.place(x=7+kc,y=550,width=30)

        num_t4_label.place(x=270,y=550)
        num_t4_entry.place(x=270+kc,y=550,width=30)
class FADDORDER(tk.Frame):
    def __init__(self, parent, appController):
        tk.Frame.__init__(self, parent)

        self.configure(bg = "#ffffff")
        num_t1_val=tk.StringVar()
        num_t2_val=tk.StringVar()
        num_t3_val=tk.StringVar()
        num_t4_val=tk.StringVar()
        tb_num=tk.StringVar()

       
        def addOrder():
            t1=num_t1_val.get()
            t2=num_t2_val.get()
            t3=num_t3_val.get()
            t4=num_t4_val.get()
            t=tb_num.get()

            foodidx=[]
            numberidx=[]
            #if(check==1):
            if(t==""):
                messagebox.showerror("lỗi","Chưa nhập số bàn")
             
            msg=ADDORDER

            client.sendall(msg.encode(FORMAT))

            
            client.sendall(str(t).encode(FORMAT))
            
            client.recv(5).decode(FORMAT)
            print(t1)
            print(t2)
            print(t3)
            print(t4)
            if(t1.isnumeric() and t1!=""):
                foodidx.append("bun gio heo")
                numberidx.append(t1)
            if(t2.isnumeric() and t2!=""):
                foodidx.append("bun bo")
                numberidx.append(t2)
            if t3.isnumeric() and t3!="":
                foodidx.append("banh canh ca loc")
                numberidx.append(t3)
            if(t4.isnumeric() and t4!=""):
                foodidx.append("banh canh cua")
                numberidx.append(t4)    
            sendList(client,foodidx)
            #print("oke")
            client.recv(10).decode(FORMAT)
            sendList(client,numberidx)

            sumMoney=client.recv(20).decode(FORMAT)

            print("Tổng số tiền là: "+sumMoney) 
            messagebox.showinfo("Tiền thanh toán","tổng số tiền là"+str(sumMoney))
            #self.showFrame(FPAYMENT)
            num_t1_val.set("")
            num_t2_val.set("")
            num_t3_val.set("")
            num_t4_val.set("")
            tb_num.set("")
        canvas = tk.Canvas(
        self,
        bg = "#ffffff",
        height = 580,
        width = 460,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge")
        canvas.place(x = 0, y = 0)
        self.background_img = tk.PhotoImage(file = f"images/menu.png")

        self.background = canvas.create_image(
            220.0, 280.0,
            image=self.background_img)

        
        btn_order=tk.Button(self,text="tính tiền",bg="blue",fg="white",
                            font=('calibre',10,'bold'),
                            command=addOrder)

        btn_order.place(
            x = 390, y = 10)

        btn_payment=tk.Button(self,text="thanh toán",bg="blue",fg="white",
                            font=('calibre',10,'bold'),
                            command=lambda:appController.showFrame(FPAYMENT))

        btn_payment.place(
            x = 390, y = 40)
        tb_num_label = tk.Label(self, text = 'Số bàn:', font=('calibre',10, 'bold'))        
        tb_num_entry = tk.Entry(self,textvariable = tb_num, font=('calibre',10,'normal'))

        num_t1_label = tk.Label(self, text = 'Số lượng:', font=('calibre',10, 'bold'))        
        num_t1_entry = tk.Entry(self,textvariable = num_t1_val, font=('calibre',10,'normal'))

        num_t2_label = tk.Label(self, text = 'Số lượng:', font=('calibre',10, 'bold'))        
        num_t2_entry = tk.Entry(self,textvariable = num_t2_val, font=('calibre',10,'normal'))

        num_t3_label = tk.Label(self, text = 'Số lượng:', font=('calibre',10, 'bold'))        
        num_t3_entry = tk.Entry(self,textvariable = num_t3_val, font=('calibre',10,'normal'))

        num_t4_label = tk.Label(self, text = 'Số lượng:', font=('calibre',10, 'bold'))        
        num_t4_entry = tk.Entry(self,textvariable = num_t4_val, font=('calibre',10,'normal'))

        tb_num_label.place(x=270,y=12)
        tb_num_entry.place(x=330,y=12,width=30)

        kc=71
        num_t1_label.place(x=7,y=320)
        num_t1_entry.place(x=7+kc,y=320,width=30)

        num_t2_label.place(x=270,y=320)
        num_t2_entry.place(x=270+kc,y=320,width=30)

        num_t3_label.place(x=7,y=550)
        num_t3_entry.place(x=80,y=550,width=30)

        num_t4_label.place(x=270,y=550)
        num_t4_entry.place(x=270+kc,y=550,width=30)
class FPAYMENT(tk.Frame):
    def __init__(self, parent, appController):
        tk.Frame.__init__(self, parent)

        self.configure(bg = "#ffffff")
        tb_num=tk.StringVar()
        card_num=tk.StringVar()
        def cashPayment():
            tb=tb_num.get()
            if(tb==""):
                messagebox.showerror("lỗi","chưa nhập số bàn")
                
            msg=PAYMENT
            client.sendall(msg.encode(FORMAT))

            
            client.sendall(tb.encode(FORMAT))

            client.recv(5).decode(FORMAT)

            msg=CASH
            client.sendall(msg.encode(FORMAT))

            fileIn = open("table_onl.json","r")
            tablesState = json.loads(fileIn.read())
            fileIn.close()

            for item in tablesState:
                if item["number"]==tb:
                    item["state"]="trong"
            fileOut=open("table_onl.json","w")
            fileOut.write(json.dumps(tablesState))
            fileOut.close()
            messagebox.showinfo("thanh toán","thanh toán thành công")

            messagebox.showinfo("Hẹn gặp lại","Cảm ơn quý khách!") 
            msg=EXIT
            client.sendall(msg.encode(FORMAT))
            client.close()
            app.destroy() 
        def cardPayment():
            
            tb=tb_num.get()
            card=card_num.get()

            msg=PAYMENT
            client.sendall(msg.encode(FORMAT))

            client.sendall(tb.encode(FORMAT))

            client.recv(5).decode(FORMAT)

            msg=CARD
            client.sendall(msg.encode(FORMAT))

            client.sendall(card.encode(FORMAT))

            check=client.recv(10).decode(FORMAT)

            if(check=="oke"):
                messagebox.showinfo("thanh toán","thanh toán thành công")
                fileIn = open("table_onl.json","r")
                tablesState = json.loads(fileIn.read())
                fileIn.close()

                for item in tablesState:
                    if item["number"]==tb:
                        item["state"]="trong"
                fileOut=open("table_onl.json","w")
                fileOut.write(json.dumps(tablesState))
                fileOut.close()
                messagebox.showinfo("Hẹn gặp lại","Cảm ơn quý khách!") 
                msg=EXIT
                client.sendall(msg.encode(FORMAT))
                client.close()
                app.destroy()
            else:   
                messagebox.showerror("lỗi","số thẻ không hợp lệ")

            tb_num.set("")
            card_num.set("")
            
            
        canvas = tk.Canvas(
            self,
            bg = "#ffffff",
            height = 603,
            width = 473,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge")
        canvas.place(x = 0, y = 0)
        
        tb_num_label = tk.Label(self, text = 'Số bàn:', font=('calibre',10, 'bold'))        
        tb_num_entry = tk.Entry(self,textvariable = tb_num, font=('calibre',10,'normal'))

        tb_num_label.place(x=270,y=12)
        tb_num_entry.place(x=330,y=12,width=30)

        btn_cash=tk.Button(self,text="tiền mặt",bg="blue",fg="white",
                            font=('calibre',10,'bold'),
                            command=cashPayment)
        btn_cash.place(x=10,y=100)

        card_num_label = tk.Label(self, text = 'CARD:', font=('calibre',10, 'bold'))        
        card_num_entry = tk.Entry(self,textvariable = card_num, font=('calibre',10,'normal'))

        card_num_label.place(x=10,y=150)
        card_num_entry.place(x=40,y=150,width=150)

        btn_card=tk.Button(self,text="OK",bg="blue",fg="white",
                            font=('calibre',10,'bold'),
                            command=cardPayment)
        btn_card.place(x=210,y=150)
        
        
class menu(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        container = tk.Frame(self)
        container.pack(side="top", fill = "both", expand = True)
        
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.protocol("WM_DELETE_WINDOW", self.closing)
        self.frames = {}
        for F in (MENU,FADDORDER,FPAYMENT):
            frame = F(container, self)

            self.frames[F] = frame 
            
            frame.grid(row=0, column=0,sticky='nsew')
            
            self.showFrame(MENU)      


    def setGreen(self,Title,size):
        self.title(Title)
        self.geometry(size)
    def showFrame(self, FrameClass):
        frame = self.frames[FrameClass]
        frame = self.frames[FrameClass]
        self.geometry("500x300")
        if(FrameClass == MENU or FrameClass==FADDORDER):
            self.title("MENU")
            self.geometry("460x580")
        # elif FrameClass==TEMP:
        #     self.geometry("80x80")
        frame.tkraise()
    def closing(self):
        if   messagebox.askokcancel("Quit","Bạn có thoát"):
            try:    
                self.destroy()
            except:
                self.destroy()
        return False
    def showIsOn(self):
            messagebox.showwarning("NOTICE","bàn này đã có khách rồi ạ!") 
    def paymentSuccess(self):
        messagebox.showinfo("thanh toán","thanh toán thành công")
    
    def paymentFail(self):
        messagebox.showerror("lỗi","số thẻ không hợp lệ")

        
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

app=menu()
try:
    client.connect((HOST,SERVER_PORT))
    msg=CONNECT
    client.sendall(msg.encode(FORMAT))
    app.mainloop()
except:
    app.update()
    app.destroy()
    msg=EXIT
    client.sendall(msg.encode(FORMAT))
    client.close()
finally:
    msg=EXIT
    client.sendall(msg.encode(FORMAT))
    client.close()
print ("oke")