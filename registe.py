import tkinter,tkinter.messagebox
root1 = tkinter.Tk()
root1.title('Log in')
root1['height'] = 140
root1['width'] = 270
root1.resizable(0, 0)  # 限制窗口大小

IP1 = tkinter.StringVar()
IP1.set('')  # 默认显示的ip和端口
User = tkinter.StringVar()
User.set('')
Psw = tkinter.StringVar()
Psw.set('')


# 用户名标签
labelIP = tkinter.Label(root1, text='Username')
labelIP.place(x=20, y=10, width=100, height=20)

entryIP = tkinter.Entry(root1, width=80, textvariable=IP1)
entryIP.place(x=120, y=10, width=130, height=20)

# 密码标签
labelUser = tkinter.Label(root1, text='Password')
labelUser.place(x=30, y=40, width=80, height=20)

entryUser = tkinter.Entry(root1, width=80, textvariable=User)
entryUser.place(x=120, y=40, width=130, height=20)

#密码1标签
labelPsw = tkinter.Label(root1, text='Password_s')
labelPsw.place(x=32, y=70, width=80, height=20)

entryPsw = tkinter.Entry(root1, width=80,textvariable=Psw)
entryPsw.place(x=120, y=70, width=130, height=20)


def write_in_psw(username, password):
    with open('psw', 'a') as f:
        str = username + ':' + password + '\n'  # 写入成功后即换行  咋个换行呢
        f.write(str)

def registe(*args):
    global IP, PORT, user,psw
    name = entryIP.get()  # 获取IP和端口号
    psw = entryUser.get()
    psw1=entryPsw.get()
    print(name,psw,psw1)
    if psw==psw1:
        write_in_psw(name,psw)
    else:
        tkinter.messagebox.showerror('Name type error', message='确认密码不正确')


root1.bind('<Return>', registe)            # 回车绑定登录功能
but = tkinter.Button(root1, text='Registe', command=registe)
but.place(x=100, y=100, width=70, height=30)

root1.mainloop()