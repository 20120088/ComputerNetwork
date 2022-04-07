import socket
import select
import json
import os
import re
import pickle
import time
import datetime
import urllib.request
import tkinter as tk
from tkinter import ttk

import subprocess
import sys

subprocess.check_call([sys.executable, "-m", "pip", "install", "pywin32"])

from tkinter.messagebox import showinfo
from _thread import *
import threading
import win32gui, win32con

hide = win32gui.GetForegroundWindow()
win32gui.ShowWindow(hide , win32con.SW_HIDE)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Create socket use TCP protocol

HOST = "127.0.0.1"
PORT = 54321
MODE = "utf8"

def Error(addr, errorNum, w):
    if (errorNum == 0):
        newline = "Connection_with_" + str(addr[0]) + ':' + str(addr[1]) + '_lost'
        w.updateConsole(newline)
    elif (errorNum == 1):
        newline = "Cannot_load_file"
        w.updateConsole(newline)
    elif (errorNum == 2):
        newline = "User_" + str(addr[0]) + ':' + str(addr[1]) + '_exit'
        w.updateConsole(newline)

def loadJson(filename, addr):
    try:
        if (os.path.exists(filename)):
            f = open(filename, "r",encoding = 'utf-8-sig')
            data = json.loads(f.read())
            f.close()
            return data
        else:
            return '0'
    except:
        Error(addr, 1)

def downloadFile(newFileName):
    url = 'https://tygia.com/json.php?ran=0&rate=0&gold=1&bank=VIETCOM&date=now'
    urllib.request.urlretrieve(url, newFileName)

def addAccount(username:str, password:str):
    newAccount = {"username" : username,
                  "password" : password}
    f = open('Account.json', 'r+',encoding = 'utf-8-sig')
    data = json.load(f)
    data['Account'].append(newAccount)
    f.seek(0)
    json.dump(data, f, indent = 4)
    f.close()

def checkInfo(username, password, addr):
    accountData = loadJson('Account.json',addr)
    for i in accountData['Account']:
        if (username == i['username']): 
            if (password == i['password']):
                return '0'
            else:
                return '1'
    return '2'

def signIn(c, addr, w):
    newline = str(addr[0]) + ':' + str(addr[1]) + "_signing_in"
    w.updateConsole(newline)
    try:
        while True:
            msg = c.recv(1024)
            c.sendall(msg)
            if (int(msg.decode(MODE)) == 2):
                username = c.recv(1024)
                c.sendall(username)
                newline = "Username_recieved_from_" + str(addr[0]) + ':' + str(addr[1])
                w.updateConsole(newline)

                password = c.recv(1024)
                c.sendall(password)
                newline = "Password_recieved_from_" + str(addr[0]) + ':' + str(addr[1])
                w.updateConsole(newline)

                check = checkInfo(str(username.decode(MODE)), str(password.decode(MODE)), addr)
                try:
                    if (check == '2'): #Username not found
                        rep = check
                        c.sendall(rep.encode(MODE))
                        c.recv(4096)
                        newline = "Cannot_find_user_from" + str(addr[0]) + ':' + str(addr[1])
                        w.updateConsole(newline)
                    elif(check == '1'): #Wrong password
                        rep = check
                        c.sendall(rep.encode(MODE))
                        c.recv(4096)
                        newline = "Password_from" + str(addr[0]) + ':' + str(addr[1]) + "_is_wrong"
                        w.updateConsole(newline)
                    elif(check == '0'): #Match
                        rep = check
                        c.sendall(rep.encode(MODE))
                        c.recv(4096)
                        newline = str(addr[0]) + ':' + str(addr[1]) + "_sign_in_complete"
                        w.updateConsole(newline)
                        break
                except:
                    Error(addr, 1)
                    break
            elif (int(msg.decode(MODE)) == 6):
                newline = str(addr[0]) + ':' + str(addr[1]) + "_exit_singing_in"
                w.updateConsole(newline)
                break
    except:
        Error(addr, 0)
        return

def signUp(c, addr, w):
    newline = str(addr[0]) + ':' + str(addr[1]) + "_signing_up"
    w.updateConsole(newline)
    try:
         while True:
            msg = c.recv(1024)
            c.sendall(msg)
            if (int(msg.decode(MODE)) == 2):
                username = c.recv(1024)
                c.sendall(username)
                newline = "Username_recieved_from_" + str(addr[0]) + ':' + str(addr[1])
                w.updateConsole(newline)

                password = c.recv(1024)
                c.sendall(password)
                newline = "Password_recieved_from_" + str(addr[0]) + ':' + str(addr[1])
                w.updateConsole(newline)

                check = checkInfo(str(username.decode(MODE)), "dummy", addr)
                if (check == '2'): #Username not found
                    rep = check
                    c.sendall(rep.encode(MODE))
                    addAccount(str(username.decode(MODE)), str(password.decode(MODE)))
                    newline = str(addr[0]) + ':' + str(addr[1]) + "_sign_up_complete"
                    w.updateConsole(newline)
                else:
                    rep = check
                    c.sendall(rep.encode(MODE))
                    newline = "Username_from" + str(addr[0]) + ':' + str(addr[1]) + '_exists'
                    w.updateConsole(newline)
            elif (int(msg.decode(MODE)) == 6):
                newline = str(addr[0]) + ':' + str(addr[1]) + "_exit_signing_up"
                w.updateConsole(newline)
                break
    except:
        Error(addr, 0)
        return

def no_accent_vietnamese(s):
    s = re.sub('[áàảãạăắằẳẵặâấầẩẫậ]', 'a', s)
    s = re.sub('[ÁÀẢÃẠĂẮẰẲẴẶÂẤẦẨẪẬ]', 'A', s)
    s = re.sub('[éèẻẽẹêếềểễệ]', 'e', s)
    s = re.sub('[ÉÈẺẼẸÊẾỀỂỄỆ]', 'E', s)
    s = re.sub('[óòỏõọôốồổỗộơớờởỡợ]', 'o', s)
    s = re.sub('[ÓÒỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢ]', 'O', s)
    s = re.sub('[íìỉĩị]', 'i', s)
    s = re.sub('[ÍÌỈĨỊ]', 'I', s)
    s = re.sub('[úùủũụưứừửữự]', 'u', s)
    s = re.sub('[ÚÙỦŨỤƯỨỪỬỮỰ]', 'U', s)
    s = re.sub('[ýỳỷỹỵ]', 'y', s)
    s = re.sub('[ÝỲỶỸỴ]', 'Y', s)
    s = re.sub('đ', 'd', s)
    s = re.sub('Đ', 'D', s)
    return s

def lookUp(time, addr):
    filename = time + '.json'
    golds = loadJson(filename, addr)
    return golds

def lookUpWin(c, addr, w):
    newline = str(addr[0]) + ':' + str(addr[1]) + "_looking_up"
    w.updateConsole(newline)
    try:
        while True:
            msg = c.recv(1024)
            c.sendall(msg)
            if (int(msg.decode(MODE)) == 7):
                time = c.recv(1024)
                rep = time
                c.sendall(rep)
                res = lookUp(str(time.decode(MODE)), addr)
        
                if (res == '0'):
                    newline = "Cannot_find_file_for_" + str(addr[0]) + ':' + str(addr[1])
                    w.updateConsole(newline)
                    c.sendall(res.encode(MODE))
                    c.recv(4096)
                else:
                    newline = "Sending_data_to_" + str(addr[0]) + ':' + str(addr[1])
                    w.updateConsole(newline)
                    rep = len(res["golds"][0]["value"])
                    c.sendall((str(rep)).encode(MODE))
                    c.recv(4096)
                    for x in res["golds"][0]["value"]:
                        c.sendall(pickle.dumps(x))
                        c.recv(1024)
                    c.recv(1024)
                    c.sendall('1'.encode(MODE))
                    newline = "Finish_sending_data_to_" + str(addr[0]) + ':' + str(addr[1])
                    w.updateConsole(newline)
            elif (int(msg.decode(MODE)) == 6):
                newline = str(addr[0]) + ':' + str(addr[1]) + "_exit_looking_up"
                w.updateConsole(newline)
                break
    except:
        Error(addr, 0)
        return 

def updateThread(w):
    while (True):
        year = str(datetime.datetime.now().year)
        month = str(datetime.datetime.now().month)
        day = str(datetime.datetime.now().day)

        fileName = year + month + day + '.json'
        downloadFile(fileName)

        w.updateConsole("Data_update")
        time.sleep(1800)

def mainThread(c , addr, w):
    try:
        msg = c.recv(1024)
        c.sendall(msg)
        while True:
            msg = c.recv(1024)
            if(int(msg.decode(MODE)) == 2):
                c.sendall(msg)
                signIn(c, addr, w)
            elif(int(msg.decode(MODE)) == 3):
                c.sendall(msg)
                signUp(c, addr, w)
            elif(int(msg.decode(MODE)) == 4):
                c.sendall(msg)
                lookUpWin(c, addr, w)
            if(int(msg.decode(MODE)) == 5): 
                c.sendall(msg)
                newline = "Disconnect_from_" + str(addr[0]) + ":" + str(addr[1])
                w.updateConsole(newline)
                client = str(addr[0]) + ':' + str(addr[1])
                w.deleteClient(client)
                break
    except:
        Error(addr, 0, w)
        client = str(addr[0]) + ':' + str(addr[1])
        w.deleteClient(client)
        return

class GoldzServer(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self) 
    
        self.title("Goldz Server")
        self.geometry("600x500")
        self.resizable(width = False, height = False)

        self.clientList:list = []

        self.columns1 = ('client')
        self.columns2 = ('console')
        self.clientTable = ttk.Treeview(self, columns = self.columns1, show = 'headings', height = 23)
        self.consoleTable = ttk.Treeview(self, columns = self.columns2, show = 'headings', height = 23)

        self.clientTable.heading('client', text = 'Client: 0')
        self.clientScroll = ttk.Scrollbar(self, orient = tk.VERTICAL, command = self.clientTable.yview)
        self.clientTable.configure(yscroll = self.clientScroll.set)
        self.clientTable.column('client', width = 280)

        self.consoleTable.heading('console', text = 'Console')
        self.consoleScroll = ttk.Scrollbar(self, orient = tk.VERTICAL, command = self.consoleTable.yview)
        self.consoleTable.configure(yscroll = self.consoleScroll.set)
        self.consoleTable.column('console', width = 280)

        self.clientTable.grid(row = 0, column = 0, sticky = 'nsew')
        self.clientScroll.grid(row = 0, column = 1, sticky = 'ns')
        self.consoleTable.grid(row = 0, column = 2, sticky = 'ns')
        self.consoleScroll.grid(row = 0, column = 3, sticky = 'ns')

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        s.close()
        self.destroy()

    def updateClient(self):
        for item in self.clientTable.get_children():
            self.clientTable.delete(item)
        for client in self.clientList:
            self.clientTable.insert('', tk.END, values = (client))
        newHeading = 'Client: ' + str(len(self.clientList))
        self.clientTable.heading('client', text = newHeading)

    def addClient(self, client):
        self.clientList.append(client)
        self.updateClient()

    def deleteClient(self, client):
        self.clientList.remove(client)
        self.updateClient()

    def updateConsole(self, newline:str):
        self.consoleTable.insert('', 0, values = newline)

class App(threading.Thread):
    def __init__(self, tk_root):
        self.root = tk_root
        threading.Thread.__init__(self)
        self.start()

    def  run(self):
    
        start_new_thread(updateThread, (self.root,))
        
        s.bind((HOST, PORT)) 
        newline = "Socket_bind_to_PORT_" + str(PORT)
        self.root.updateConsole(newline)
        
        s.listen(5) #server is ready to get request
        self.root.updateConsole('Socket_is_listening')
        
        try:
            while (True):  
                c, addr = s.accept() #server get request
                newline = "Connected_to_" + str(addr[0]) + ':' + str(addr[1])
                self.root.updateConsole(newline)
                newClient = str(addr[0]) + ':' + str(addr[1])
                self.root.addClient(newClient)
                start_new_thread(mainThread, (c,addr, self.root)) 
        except:
            return

wd = os.getcwd()
wd = wd + '/Data/json'
os.chdir(wd)
goldServer = GoldzServer()
APP = App(goldServer)
goldServer.mainloop()