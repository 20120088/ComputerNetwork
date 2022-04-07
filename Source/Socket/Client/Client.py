import tkinter as tk
import socket
import os
import pickle

import subprocess
import sys
subprocess.check_call([sys.executable, "-m", "pip", "install", "tkcalendar"])
subprocess.check_call([sys.executable, "-m", "pip", "install", "pywin32"])

from tkcalendar import DateEntry
from tkinter import ttk
from tkinter.messagebox import showinfo
import win32gui, win32con

hide = win32gui.GetForegroundWindow()
win32gui.ShowWindow(hide , win32con.SW_HIDE)

PORT = 54321
MODE = "utf8"

sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #create socket

class TableFrame(tk.Frame):
    def __init__(self, parent, appController):
        tk.Frame.__init__(self, parent)

        self.columns = ('ma_so', 'cong_ty', 'nhan_hieu', 'gia_ban_ra', 'gia_mua_vao')
        self.table = ttk.Treeview(self, columns = self.columns, show = 'headings', height = 9)

        self.table.heading('ma_so', text = 'Mã số')
        self.table.heading('cong_ty', text = 'Công ty')
        self.table.heading('nhan_hieu', text = 'Nhãn hiệu')
        self.table.heading('gia_ban_ra', text = 'Giá bán ra (ngàn đồng/lượng)')
        self.table.heading('gia_mua_vao', text = 'Giá mua vào (ngàn đồng/lượng)')

        self.table.column('ma_so', width = 100)
        self.table.column('cong_ty', width = 70)
        self.table.column('nhan_hieu', width = 200)
        self.table.column('gia_ban_ra', width = 190)
        self.table.column('gia_mua_vao', width = 190)

        self.scrollbar = ttk.Scrollbar(self, orient = tk.VERTICAL, command = self.table.yview)
        self.table.configure(yscroll = self.scrollbar.set)
        
        self.table.grid(row = 0, column = 0, sticky = 'nsew')
        self.scrollbar.grid(row = 0, column = 1, sticky = 'ns')

        for gold in appController.goldTable:
            self.table.insert('', tk.END, values = gold)

class HomeFrame(tk.Frame):
    def __init__(self, parent, appController):
        tk.Frame.__init__(self, parent)

        self.sel = tk.StringVar()
        self.count = 0

        self.title_Label = tk.Label(self, text = "Trang chủ")
        self.date_Label = tk.Label(self, text = "Chọn ngày")
        self.type_Label = tk.Label(self, text = "Chọn loại vàng")
        self.notice_Label = tk.Label(self, text = "")

        self.date_Entry = DateEntry(self, selectmode = 'day', width = 12, textvariable = self.sel)
        self.type_Combobox = ttk.Combobox(self, values = appController.goldType)
        self.goldTable = TableFrame(self, appController)

        self.btn_Frame = tk.Frame()
        self.print_Btn = tk.Button(self, text = "Tìm kiếm", command=lambda: appController.loadGolds(self.goldTable, self.type_Combobox.get()))
        self.logout_Btn = tk.Button(self, text = "Đăng xuất", command=lambda: appController.sendOption(LogFrame, self, sk, '6'))
        
        self.title_Label.pack()
        self.date_Label.pack()
        self.date_Entry.pack()
        self.type_Label.pack()
        self.type_Combobox.pack()
        self.print_Btn.pack()
        self.logout_Btn.pack()
        self.notice_Label.pack()    
        self.btn_Frame.pack()
        self.goldTable.pack()

        def dateChoosen(*args):
            self.count = self.count + 1
            if (self.count == 1):return
            date = str(self.date_Entry.get_date())
            appController.loadDate(self, sk, date)
            self.count = 0
        
        self.sel.trace('w', dateChoosen)

class SignInFrame(tk.Frame):
    def __init__(self, parent, appController):
        tk.Frame.__init__(self, parent)

        self.title_Label = tk.Label(self, text = "Đăng nhập")
        self.username_Label = tk.Label(self, text = "Tài khoản")
        self.password_Label = tk.Label(self, text = "Mật khẩu")
        self.notice_Label = tk.Label(self, text = "")

        self.username_Entry = tk.Entry(self, width = 20, bg = "light yellow")
        self.password_Entry = tk.Entry(self, width = 20, bg = "light yellow")

        self.signIn_Btn = tk.Button(self, text = "Đăng nhập", width = 10, command=lambda: appController.signIn(self, sk))
        self.exit_Btn = tk.Button(self, text = "Thoát", width = 10, command=lambda: appController.sendOption(LogFrame, self, sk, '6'))

        self.title_Label.pack()
        self.username_Label.pack()
        self.username_Entry.pack()
        self.password_Label.pack()
        self.password_Entry.pack()
        self.notice_Label.pack()

        self.signIn_Btn.pack()
        self.exit_Btn.pack()

class SignUpFrame(tk.Frame):
    def __init__(self, parent, appController):
        tk.Frame.__init__(self, parent)

        self.title_Label = tk.Label(self, text = "Đăng kí")
        self.username_Label = tk.Label(self, text = "Tài khoản")
        self.password_Label = tk.Label(self, text = "Mật khẩu")
        self.repassword_Label = tk.Label(self, text = "Nhập lại mật khẩu")
        self.notice_Label = tk.Label(self, text = "")

        self.username_Entry = tk.Entry(self, width = 20, bg = "light yellow")
        self.password_Entry = tk.Entry(self, width = 20, bg = "light yellow")
        self.repassword_Entry = tk.Entry(self, width = 20, bg = "light yellow")

        self.signUp_Btn = tk.Button(self, text = "Đăng kí", width = 10, command=lambda: appController.signUp(self, sk))
        self.exit_Btn = tk.Button(self, text = "Thoát", width = 10, command=lambda: appController.sendOption(LogFrame, self, sk, '6'))

        self.title_Label.pack()
        self.username_Label.pack()
        self.username_Entry.pack()
        self.password_Label.pack()
        self.password_Entry.pack()
        self.repassword_Label.pack()
        self.repassword_Entry.pack()
        self.notice_Label.pack()

        self.signUp_Btn.pack()
        self.exit_Btn.pack()

class LogFrame(tk.Frame):
    def __init__(self, parent, appController):
        tk.Frame.__init__(self, parent)

        self.notice_Label = tk.Label(self, text = "")

        self.changeServer_Button = tk.Button(self, text = "Đổi server", command=lambda: appController.disconnectFromServer(sk))
        self.signIn_Btn = tk.Button(self, text = "Đăng nhập", width = 10, command=lambda: appController.sendOption(SignInFrame, self, sk, '2'))
        self.signUp_Btn = tk.Button(self, text = "Đăng kí", width = 10, command=lambda: appController.sendOption(SignUpFrame, self, sk, '3'))

        #self.changeServer_Button.pack()
        self.signIn_Btn.pack()
        self.signUp_Btn.pack()
        self.notice_Label.pack()

class IPFrame(tk.Frame):
    def __init__(self, parent, appController):
        tk.Frame.__init__(self, parent)

        self.title_Label = tk.Label(self, text = "Goldz")
        self.ip_Label = tk.Label(self, text = "Nhập địa chỉ IP máy chủ")
        self.ip_Entry = tk.Entry(self, width = 20)
        self.ip_Btn = tk.Button(self, text = "Kết nối tới máy chủ", command=lambda: appController.connectToServer(self, sk))
        self.notice_Label = tk.Label(self, text = "")

        self.title_Label.pack()
        self.ip_Label.pack()
        self.ip_Entry.pack()
        self.notice_Label.pack()
        self.ip_Btn.pack()

class GoldzClient(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.golds:list = []
        self.goldType:list = []
        self.goldTable:list = []

        self.title("Goldz")
        self.geometry("770x384")
        self.resizable(width = False, height = False)

        self.container = tk.Frame()
        self.container.configure(bg = "red")

        self.container.pack(side = "top", fill = "both", expand = True)
        self.container.grid_rowconfigure(0, weight = 1)
        self.container.grid_columnconfigure(0, weight = 1)

        self.frames = {}
        for F in (LogFrame, HomeFrame, IPFrame, SignInFrame, SignUpFrame):
            frame = F(self.container, self)
            frame.grid(row = 0, column = 0, sticky = "nsew")
            self.frames[F] = frame

        self.frames[IPFrame].tkraise()

        self.LogOnTop = False

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        try:
            if (self.LogOnTop == 0):
                sk.sendall(b'6')
                sk.recv(1024)
            sk.sendall(b'5')
            sk.recv(1024)
            sk.close()
            self.destroy()
        except:
            sk.close()
            self.destroy()

    def resetFrame(self, FrameClass):
        frame = FrameClass(self.container, self)
        frame.grid(row = 0, column = 0, sticky = "nsew")
        self.frames[FrameClass] = frame

    def showFrame(self, FrameClass):
        self.resetFrame(FrameClass)
        self.frames[FrameClass].tkraise()
        if (FrameClass == LogFrame): self.LogOnTop = 1
        else: self.LogOnTop = 0

    def Error(self, curFrame, errorNum):
        if (errorNum == 0): 
            curFrame.notice_Label["text"] = "Mất kết nối tới Server"
        if (errorNum == 1): 
            curFrame.notice_Label["text"] = "Lỗi gửi dữ liệu"

    def sendInfo(self, s, choice):
        s.sendall(choice.encode(MODE))
        s.recv(1024)

    def sendOption(self, FrameClass, curFrame, s, choice):
        try:
            self.sendInfo(s, choice)
            self.showFrame(FrameClass)
        except:
            self.Error(curFrame, 0)

    def connectToServer(self, curFrame, s):
        try:
            ip = curFrame.ip_Entry.get()
        
            if (ip == ""):
                curFrame.notice_Label["text"] = "Bạn chưa nhập IP"
            else:
                s.connect((ip, PORT)) #connect to server 
                self.sendInfo(s, 'connect')
                self.frames[LogFrame].tkraise()
                self.LogOnTop = 1
        except:
            self.Error(curFrame, 0)

    def disconnectFromServer(self, s):
        self.sendInfo(s, '5')
        s.close()
        self.frames[IPFrame].tkraise()

    def signIn(self, curFrame, s):
        username = curFrame.username_Entry.get()
        password = curFrame.password_Entry.get()

        if (username == "" or password == ""):
            curFrame.notice_Label["text"] = "Không được để trống giá trị"
        else:
            try:
                self.sendInfo(s, '2')
                self.sendInfo(s, username)
                self.sendInfo(s, password)
                checkInfo = s.recv(1024) 
                s.sendall(checkInfo)
                rep = int(checkInfo.decode(MODE))
                if (rep == 2):
                    curFrame.notice_Label["text"] = "Không tìm thấy Username"
                elif (rep == 1):
                    curFrame.notice_Label["text"] = "Sai mật khẩu"
                elif (rep == 0):
                    self.sendOption(HomeFrame, curFrame, s, '4')
            except:
                self.Error(curFrame, 0)

    def signUp(self, curFrame, s):  
        username = curFrame.username_Entry.get()
        password = curFrame.password_Entry.get()
        repassword = curFrame.repassword_Entry.get()

        if (username == "" or password == "" or repassword == ""):
            curFrame.notice_Label["text"] = "Không được để trống giá trị"
        else: 
            if (password != repassword): 
                curFrame.notice_Label["text"] = "Mật khẩu không khớp"
            else:
                try:
                    self.sendInfo(s, '2')
                    self.sendInfo(s, username)
                    self.sendInfo(s, password)
                    checkInfo = s.recv(1024) 
                    rep = int(checkInfo.decode(MODE))
                    if (rep == 2):
                        curFrame.notice_Label["text"] = "Đăng kí thành công"
                    elif (rep == 1):
                        curFrame.notice_Label["text"] = "Tài khoản tồn tại"
                except:
                    self.Error(curFrame, 0)

    def convertDate(self, date):
        dateConverted = date[0:4] + date[5:7] + date[8:10]
        return dateConverted

    def loadDate(self, curFrame, s, date):
        try:
            self.golds.clear()
            date = self.convertDate(date)
            self.sendInfo(s, '7')
            self.sendInfo(s, date)

            found = s.recv(1024).decode(MODE)
            s.sendall(found.encode(MODE))   
            if (found != b'0'):
                for i in range(int(found)):
                    temp = s.recv(4096)
                    s.sendall(b'0')
                    record = pickle.loads(temp)
                    self.golds.append(record)
                s.sendall('1'.encode(MODE))
                s.recv(1024)
                self.updateType(curFrame)
            else:
                print("Not found")
                return
        except:
            self.Error(curFrame, 0)

    def updateType(self, curFrame):
        self.goldType.clear()
        for x in self.golds:
            if (not (x["type"] in self.goldType)): 
                self.goldType.append(x["type"])
        curFrame.type_Combobox["value"] = self.goldType
        #curFrame.type_Combobox.current(1)

    def loadGolds(self, tableFrame, type):
        self.goldTable.clear()
        for item in tableFrame.table.get_children():
            tableFrame.table.delete(item)
        for gold in self.golds:
            if (type == gold["type"]):
                self.goldTable.append((gold["id"], gold["company"], gold["brand"], gold["buy"], gold["sell"]))
        for gold in self.goldTable:
            tableFrame.table.insert('', tk.END, values = gold)
   
goldClient = GoldzClient()
goldClient.mainloop()


