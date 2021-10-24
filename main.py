#coding:utf-8
import tkinter as tk
from tkinter import messagebox as msg
import easygui
from tkinter import ttk
from tkinter import filedialog as filemsg
from psutil import disk_partitions
from time import sleep
import threading
import os       
import sys      
import shutil


root = tk.Tk()
root.title('99U盘图标安装器')
root.geometry("400x200")
sw = root.winfo_screenwidth()
sh = root.winfo_screenheight()
ww = 450
wh = 200
x = (sw-ww) / 2
y = (sh-wh) / 2
root.geometry("%dx%d+%d+%d" %(ww,wh,x,y))
root.resizable(0, 0)

path = None
upan = None
driver = None

def help_use():
    easygui.msgbox('这个程序的原理是将您所选择的ico文件放入您的U盘\n然后修改您U盘里的autorun.inf\n已达到更换图标的效果\n默认隐藏图标文件和autorun文件!','99')
    
def about():
    msg.showinfo('99', '版权所有:张凯涵')
    
def choose_ico_path():
    global path
    path = filemsg.askopenfile(filetypes=[("ICO", ".ico")])
    path = path.name
    choose_ico_bar.configure(state='normal')
    choose_ico_bar.insert("insert", path)
    choose_ico_bar.configure(state='disabled')

def xFunc(event):
    global upan
    print(choose_usb_bar.get())            
    if choose_usb_bar.get() == "选择U盘":
        upan = None
    else:
        upan = choose_usb_bar.get()
        
def install():
    ico_path = choose_ico_bar.get('1.0',tk.END)
    #print(path)
    print(driver)
    if upan == None:
        msg.showerror('99', '不存在的盘符或没有设定U盘')
        return
    if path == None:
        msg.showerror('99', '您没有输入图标路径!')
        return
    if not yn:
        easygui.msgbox('用户取消了安装','99')
        return 
    if run_search(driver):
        yn = msg.askyesno('99', '您想要安装的U盘中有autorun.inf，是否追加写入？(详情请查看帮助)')
        if yn:
            ico_name = ico_path.split('/')[-1]
            ico_path = ico_path.split('\n')[0]
            ico_name = ico_name.split('\n')[0]
            shutil.copyfile(ico_path, upan+ico_name)
            with open(f'{upan}autorun.inf', 'a') as f:
                f.write("""

ICON={},0
""".format(ico_name))
        msg.showinfo('99','安装完成，拔出U盘后再次插入即可查看效果!')
    else:
        ico_name = ico_path.split('/')[-1]
        ico_path = ico_path.split('\n')[0]
        ico_name = ico_name.split('\n')[0]
        shutil.copyfile(ico_path, upan+ico_name)
        with open(f'{upan}autorun.inf', 'w') as f:
            f.write("""
[autorun] 

ICON={},0
""".format(ico_name))
        msg.showinfo('99','安装完成，拔出U盘后再次插入即可查看效果!')
    
    
    
def search(path,name):

    for root, dirs, files in os.walk(path):  # path 为根目录
        if name in dirs or name in files:
            flag = 1      #判断是否找到文件
            root = str(root)
            dirs = str(dirs)
            return os.path.join(root, dirs)
    return -1

def run_search(upan):
    path = upan
    name = "autorun.inf"  #标准输入,其中rstrip()函数把字符串结尾的空白和回车删除
    answer = search(path,name)
    if answer == -1:
        return False
    else:
        return True
    
def check_usb():
    global driver,choose_usb_bar
    while True:
        sleep(1)
        for item in disk_partitions():
            if 'removable' in item.opts:
                driver = item.device
                #print('发现usb驱动：', driver)
                choose_usb.append(driver)
                choose_usb_bar["value"] = choose_usb
                break
        else:
            #print('没有找到可移动驱动器')
            continue
        break
    
def help_exe():
    easygui.msgbox('如果您之间新建过autorun文件，那不用担心。如果您没有或不知道这回事，有可能是你的U盘感染了病毒，建议立即查杀，当然大多数autorun都是隐藏的，也有的U盘天生自带autorun，这些咱们不用担心!  :)','99')
    
#获取移动盘符

choose_usb = ['选择U盘']
t1 = threading.Thread(target=check_usb)
t1.start()



    

welcome_text = tk.Label(root, text="欢迎来到99U盘图标安装器!",font=('微软雅黑',15))

menubar = tk.Menu(root)  
menubar.add_command(label="关于", command=about)  
menubar.add_command(label="如何使用", command=help_use)
menubar.add_command(label="帮助", command=help_exe)
menubar.add_command(label="退出软件", command=root.quit)  

choose_ico_bar = tk.Text(root, width=20,height=1)
choose_ico_bar.configure(state='disabled')
choose_ico_label = tk.Label(root, text="图标(ico)文件路径:")
choose_usb_bar = ttk.Combobox(root, width=10)     
choose_usb_bar.place(x=38,y=85)     
choose_usb_bar["value"] = choose_usb 
choose_usb_bar.current(0)   
choose_usb_bar.configure(state = "readonly") 
choose_usb_label = tk.Label(root, text="U盘:")
choose_ico_btn = tk.Button(root, text="选择路径", command = choose_ico_path)
ok_btn = tk.Button(root, text="准备好了，安装!", width = 30, command = install)

welcome_text.pack()
root.config(menu=menubar) 
choose_ico_bar.place(x=240,y=90)
choose_ico_label.place(x=130,y=85)
choose_usb_bar.bind("<<ComboboxSelected>>", xFunc)
choose_ico_btn.place(x=387,y=85)
choose_usb_label.place(x=0,y=85)
ok_btn.place(x=105,y=150)

root.mainloop()