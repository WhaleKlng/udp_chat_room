import socket,sys
import threading
import json  # json.dumps(some)打包   json.loads(some)解包
import tkinter
import tkinter.messagebox
from tkinter.scrolledtext import ScrolledText  # 导入多行文本框用到的包

IP = ''
PORT = ''
user = ''
listbox1 = ''  # 用于显示在线用户的列表框   pip freeze > requirements.txt
ii = 0  # 用于判断是开还是关闭列表框
users = []  # 在线用户列表
chat = '------Group-------'  # 聊天对象, 默认为群聊
# 登陆窗口
root1 = tkinter.Tk()
root1.title('Log in')
root1['height'] = 140
root1['width'] = 270
root1.resizable(0, 0)  # 限制窗口大小

IP1 = tkinter.StringVar()
IP1.set('127.0.0.1:50007')  # 默认显示的ip和端口
User = tkinter.StringVar()
User.set('zyx')
Psw = tkinter.StringVar()
Psw.set('1133')


# 服务器标签
labelIP = tkinter.Label(root1, text='Server address')
labelIP.place(x=20, y=10, width=100, height=20)

entryIP = tkinter.Entry(root1, width=80, textvariable=IP1)
entryIP.place(x=120, y=10, width=130, height=20)

# 用户名标签
labelUser = tkinter.Label(root1, text='Username')
labelUser.place(x=30, y=40, width=80, height=20)

entryUser = tkinter.Entry(root1, width=80, textvariable=User)
entryUser.place(x=120, y=40, width=130, height=20)

#密码标签
labelPsw = tkinter.Label(root1, text='Password')
labelPsw.place(x=40, y=70, width=80, height=20)

entryPsw = tkinter.Entry(root1, width=80, show='*',textvariable=Psw)
entryPsw.place(x=120, y=70, width=130, height=20)

def check_psw(username,password):
    fin=0
    with open('psw','r') as f:
        list1=f.readlines()
    for i in range(0, len(list1)):
        list1[i] = list1[i].rstrip('\n')
    for i in  list1:
        user=i.split(':')[0]
        psw=i.split(':')[1]
        if (username==user) and (psw==password):
            fin=1
            break
    return fin

# 登录按钮
def login(*args):
    global IP, PORT, user,psw
    IP, PORT = entryIP.get().split(':')  # 获取IP和端口号
    PORT = int(PORT)                     # 端口号需要为int类型
    user = entryUser.get()
    psw=entryPsw.get()
    if not check_psw(user,psw):
        tkinter.messagebox.showerror('Name type error', message='Username Empty!')
    else:
        root1.destroy()                  # 关闭窗口


root1.bind('<Return>', login)            # 回车绑定登录功能
but = tkinter.Button(root1, text='Log in', command=login)
but.place(x=100, y=100, width=70, height=30)

root1.mainloop()

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# s.bind((IP, PORT))
if user:
    text = 'login;;'+ user
    data = text.encode('ascii')
    s.sendto(data, ((IP, PORT)))






root = tkinter.Tk()
root.title(user)  # 窗口命名为用户名
root['height'] = 400
root['width'] = 580
root.resizable(0, 0)  # 限制窗口大小

# 创建多行文本框
listbox = ScrolledText(root)
listbox.place(x=5, y=0, width=570, height=320)
# 文本框使用的字体颜色
listbox.tag_config('red', foreground='red')
listbox.tag_config('blue', foreground='blue')
listbox.tag_config('green', foreground='green')
listbox.tag_config('pink', foreground='pink')
listbox.insert(tkinter.END, 'Welcome to the chat room!', 'blue')

# 创建多行文本框, 显示在线用户
listbox1 = tkinter.Listbox(root)
listbox1.place(x=445, y=0, width=130, height=320)
def users():
    global listbox1, ii
    if ii == 1:
        listbox1.place(x=445, y=0, width=130, height=320)
        ii = 0
    else:
        listbox1.place_forget()  # 隐藏控件
        ii = 1


# 查看在线用户按钮
button1 = tkinter.Button(root, text='Users online', command=users)
button1.place(x=485, y=320, width=90, height=30)



# 创建输入文本框和关联变量
a = tkinter.StringVar()
a.set('')
entry = tkinter.Entry(root, width=120, textvariable=a)
entry.place(x=5, y=350, width=570, height=40)

def send(*args):
    # 没有添加的话发送信息时会提示没有聊天对象
    global users
    users.append('------Group-------')
    print(chat)
    if chat not in users:
        tkinter.messagebox.showerror('Send error', message='There is nobody to talk to!')
        return
    if chat == user:
        tkinter.messagebox.showerror('Send error', message='Cannot talk with yourself in private!')
        return
    mes = 'speak;;'+entry.get() + ':;' + user + ':;' + chat  # 添加聊天对象标记
    s.sendto(mes.encode(),(IP,PORT))
    a.set('')  # 发送后清空文本框


# 创建发送按钮
button = tkinter.Button(root, text='Send', command=send)
button.place(x=515, y=353, width=60, height=30)
root.bind('<Return>', send)  # 绑定回车发送信息


# 私聊功能
def private(*args):
    global chat
    # 获取点击的索引然后得到内容(用户名)
    indexs = listbox1.curselection()
    index = indexs[0]
    if index > 0:
        chat = listbox1.get(index)
        # 修改客户端名称
        if chat == '------Group-------':
            root.title(user)
            return
        ti = user + '  -->  ' + chat
        root.title(ti)


# 在显示用户列表框上设置绑定事件
listbox1.bind('<ButtonRelease-1>', private)


# 用于时刻接收服务端发送的信息并打印
def recv():
    global users
    while True:
        data,address = s.recvfrom(65535)
        data = data.decode()
        print(data)
        # 没有捕获到异常则表示接收到的是在线用户列表
        try:
            data = json.loads(data)
            users = data
            listbox1.delete(0, tkinter.END)  # 清空列表框
            number = ('   Users online: ' + str(len(data)))
            listbox1.insert(tkinter.END, number)
            listbox1.itemconfig(tkinter.END, fg='green', bg="#f0f0ff")
            listbox1.insert(tkinter.END, '------Group-------')
            listbox1.itemconfig(tkinter.END, fg='green')
            for i in range(len(data)):
                listbox1.insert(tkinter.END, (data[i]))
                listbox1.itemconfig(tkinter.END, fg='black')
        except:
            data = data.split(':;')
            data1 = data[0].strip()  # 消息
            data2 = data[1]  # 发送信息的用户名
            data3 = data[2]  # 聊天对象
            # markk = data1.split('：')[1] #消息内容
            data1 = '\n' + data1
            if data3 == '------Group-------':
                if data2 == user:  # 如果是自己则将则字体变为蓝色
                    listbox.insert(tkinter.END, data1, 'blue')
                else:
                    listbox.insert(tkinter.END, data1, 'green')  # END将信息加在最后一行
                if len(data) == 4:
                    listbox.insert(tkinter.END, '\n' + data[3], 'pink')
            elif data2 == user or data3 == user:  # 显示私聊
                listbox.insert(tkinter.END, data1, 'red')  # END将信息加在最后一行
            listbox.see(tkinter.END)  # 显示在最后


r = threading.Thread(target=recv)
r.start()  # 开始线程接收信息

root.mainloop()
mes = 'quit;;'
s.sendto(mes.encode(),(IP,PORT))
s.close()