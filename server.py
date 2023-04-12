

import socket
import threading
import json

import tkinter as tk
from tkinter import   ttk
from tkinter.constants import BOTH, HORIZONTAL, RIGHT, VERTICAL, Y


HOST="127.0.0.1"
SERVER_PORT= 5050
FORMAT="utf8"
EXIT="exit"
SEEMENU="see menu"
ORDERFOOD="order food"
PAYMENT="payment"
CASH="cash"
CARD="card"
PAYMENTAGAIN="payment again"
ADDORDER="add order"

import datetime


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, SERVER_PORT))
s.listen(1)


def recvList(conn):
    list = []

    item = conn.recv(1024).decode(FORMAT)

    while (item != "end"):
        
        list.append(item)
        conn.sendall(item.encode(FORMAT))
        item = conn.recv(1024).decode(FORMAT)
    
    return list
#lấy dữ liệu từ file
def getMenu():
    fileIn = open("menu.json","r")
    data = json.loads(fileIn.read())
    fileIn.close()
    return data

def sendList(conn, list):
    data = json.dumps(list)
    conn.sendall(data.encode(FORMAT))

def exitOption(conn):
    msg=EXIT
    conn.sendall(msg.encode(FORMAT))
    return False
def seeMenuOption(conn:socket):
    # msg=SEEMENU
    # conn.sendall(msg.encode(FORMAT))
    list =getMenu()
    print (list)
    sendList(conn,list)


def countMoney(food,num):
    menu=getMenu()
    #print(food)

    for item in menu:
     #   print(item["food name"])
        if item["food name"]==food:
            return int(num)*int(item["unit price"])

def orderFoodOtion(conn:socket):
    # msg=ORDERFOOD
    # conn.sendall(msg.encode(FORMAT))
    
    #nhận số bàn khách chọn
    tableNum=conn.recv(10).decode(FORMAT)

    print(tableNum)
    # nhận list các món ăn
    m="oke"
    conn.sendall(m.encode(FORMAT))
    listFoods=recvList(conn)
    
    print(listFoods)
    m="oke"
    conn.sendall(m.encode(FORMAT))

    #số lượng từng món theo thứ tự
    listNumbers=recvList(conn)

    #tạo dictionary để ghi vào file bill.json

    datetime_object = datetime.datetime.now()
    time=str(datetime_object)    
    list={
    "table number":tableNum,
    "foods":1,
    "numbers":1,
    "price":0,
    "time":time,
    "payment":"not yet"}

    list["foods"]=listFoods
    list["numbers"]=listNumbers

    fileIn = open("bill.json","r")
    data = json.loads(fileIn.read())
    fileIn.close()

    sum=0
    index=0
    for food in list["foods"]: 
            print(food)
            print(listNumbers[index])
            sum=sum+countMoney(food,listNumbers[index])
            index=index+1
    list["price"]=sum
    list["numbers"]=listNumbers
    print(sum)    
    data.append(list)
    fileOut=open("bill.json","w")
    fileOut.write(json.dumps(data))
    fileOut.close()

    conn.sendall(str(sum).encode(FORMAT))

def paymentSucess(tableNum):
        fileIn = open("bill.json","r")
        data = json.loads(fileIn.read())
        fileIn.close()
        for item in data:
            if(str(item["table number"])==str(tableNum)
                and item["payment"]==str("not yet" )):
                item["payment"]="done"
                break
        fileOut=open("bill.json","w")
        fileOut.write(json.dumps(data))
        fileOut.close()

def payment(conn):
    # msg=PAYMENT
    # conn.sendall(msg.encode(FORMAT))

    tableNum=conn.recv(10).decode(FORMAT)

    print(tableNum)
    temp="."
    conn.sendall(temp.encode(FORMAT))

    check=conn.recv(10).decode(FORMAT)
    if(check==CASH):
        paymentSucess(tableNum)
    elif (check==CARD):                   
        cardID=conn.recv(30).decode(FORMAT)
        if(str(cardID).isnumeric() and len(cardID)==10):

            msg="oke"
            conn.sendall(msg.encode(FORMAT))
            print(cardID)
            paymentSucess(tableNum)
            
        else:
            nok="nok"
            conn.sendall(nok.encode(FORMAT))
                

def addOrderOption(conn:socket):


     #nhận số bàn khách chọn
    tableNum=conn.recv(10).decode(FORMAT)
    # nhận list các món ăn
    m="oke"
    conn.sendall(m.encode(FORMAT))
    print("số bàn"+str(tableNum))
    listFoods=recvList(conn)
    m="oke"
    conn.sendall(m.encode(FORMAT))    


    #số lượng từng món theo thứ tự
    listNumbers=recvList(conn)
    print(listFoods)
    print(listNumbers)
    #tìm vị trí client trong file bill.json để cập nhật
    fileIn = open("bill.json","r")
    data = json.loads(fileIn.read())
    fileIn.close()

    for item in data:
        if(item["table number"]==tableNum
            and item["payment"]=="not yet"):
            print("oke1")
            idxi=0
            idxj=0

            
            a="bun gio heo" in item["foods"]
            b="bun bo" in item["foods"]
            c="banh canh ca loc" in item["foods"]
            d="banh canh cua" in item["foods"]

            if a==False:
                    item["foods"].insert(0,"bun gio heo")    
                    item["numbers"].insert(0,"0")
            if b==False:
                    item["foods"].insert(1,"bun bo")    
                    item["numbers"].insert(1,"0")
            if c==False:
                    item["foods"].insert(2,"banh canh ca loc")    
                    item["numbers"].insert(2,"0")
            if d==False:
                    item["foods"].insert(3,"banh canh cua")    
                    item["numbers"].insert(3,"0") 

            print(item["numbers"])
            print(listNumbers)
            for i in item["foods"]:
                idxj=0
                for j in listFoods:
                    # nếu 2 món ăn trùng nhau

                    if item["foods"][idxi]==listFoods[idxj]:
                        print("oke2")
                        item["numbers"][idxi]=str(int(item["numbers"][idxi])
                                                +int(listNumbers[idxj]))
                        #listFoods.pop(idxj)
                        #listNumbers.pop(idxj)
                    #     idxj-=1 
                    idxj+=1
                idxi+=1
            delIndex=0
            if item["numbers"][0]=="0":
                del item["numbers"][0]
                del item["foods"][0]
                delIndex+=1
            if item["numbers"][1-delIndex]=="0":
                del item["numbers"][1-delIndex]
                del item["foods"][1-delIndex]
                delIndex+=1
            if item["numbers"][2-delIndex]=="0":
                del item["numbers"][2-delIndex]
                del item["foods"][2-delIndex]
                delIndex+=1
            if item["numbers"][3-delIndex]=="0":
                del item["numbers"][3-delIndex]
                del item["foods"][3-delIndex]
            print(item)
            
            sum=0
            index=0
            for food in item["foods"]: 
                    print(food)
                    print(item["numbers"][index])
                    sum=sum+countMoney(food,item["numbers"][index])
                    index=index+1
            item["price"]=sum
            print(sum)    
    fileOut=open("bill.json","w")
    fileOut.write(json.dumps(data))
    fileOut.close()

    conn.sendall(str(sum).encode(FORMAT))

def handleClient(conn:socket,addr):
    try:
        option = None
        check=True
        while check:
            option=conn.recv(20).decode(FORMAT)
            print(option)
            if(option==EXIT):
                check=exitOption(conn)
            elif (option==SEEMENU ):
                seeMenuOption(conn)
            elif(option ==ORDERFOOD):
                orderFoodOtion(conn)
            elif(option==PAYMENT):
                payment(conn)
            elif(option==PAYMENTAGAIN):
                payment(conn)
            elif(option==ADDORDER):
                #print("add")
                addOrderOption(conn)
            print("-----------------\n")
    except:       
        conn.close()

def runServer():
    try:
        print(HOST)
        print("Waiting for Client")
        check=True
        while check==True:           
            try:
                print("enter while loop")
                conn, addr = s.accept()          
                thr = threading.Thread(target=handleClient, args=(conn,addr))
                thr.daemon = True
                thr.start()

                print("end main-loop")
            except:
                check=False
                print("Đã ngắt kết nối")
                s.close()             
    except KeyboardInterrupt:
        print("error")
        s.close()
    finally:
        s.close()
        print("end")
class CHECKIN(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.configure(bg = "#ffffff")
        self.geometry("600x400")
        canvas = tk.Canvas(
        self,
        bg = "#ffffff",
        height = 400,
        width = 600,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge")
        canvas.place(x = 0, y = 0)


        # set table
        self.Table_Frame = tk.Frame(self, bd = 4, relief="ridge", bg="#01458E") #bg = "màu"
        self.Table_Frame.place(x = 8, y = 90, width=492, height=250)

        self.scrollx = tk.Scrollbar(self.Table_Frame, orient=HORIZONTAL)
        self.scrolly = tk.Scrollbar(self.Table_Frame, orient=VERTICAL)

        self.Table = ttk.Treeview(self.Table_Frame, columns=(1,2), show="headings",xscrollcommand=self.scrollx.set, yscrollcommand=self.scrolly.set)
        # window.scrollx.pack(side=BOTTOM, fill=X)
        self.scrolly.pack(side=RIGHT, fill=Y)
        # window.scrollx.config(command=Table.xview
        self.scrolly.config(command=self.Table.yview)


        self.Table.heading(1, text="TABLE")
        self.Table.heading(2, text="STATE")


        self.Table.column(1,width=30)
        self.Table.column(2,width=30)

        self.Table.pack(fill=BOTH, expand=1)
        
        def showClient():
            fileIn = open('table_onl.json',"r")
            tablesState = json.loads(fileIn.read())
            fileIn.close()
            self.Table.delete(*self.Table.get_children())
            id = 1
            for table in tablesState:
                self.Table.insert(parent='', index='end',
                values=(table["number"], table["state"]))
                id += 1
        btn_reset=tk.Button(self,text="reset",bg="blue",fg="white",
                            font=('calibre',10,'bold'),
                            command=showClient)

        btn_reset.place(
                x = 40, y = 40)


#runServer()

sThread = threading.Thread(target=runServer)
sThread.daemon = True 
sThread.start()
app=CHECKIN()
app.mainloop()
