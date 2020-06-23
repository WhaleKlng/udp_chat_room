import socket,threading,sys,os,queue,json


MAX_BYTES = 65535
lock = threading.Lock()                         # 创建锁, 防止多个线程写入数据的顺序打乱
que = queue.Queue()                             # 用于存放客户端发送的信息的队列

users=[] #[(user,addr)]

def onlines():
    online = []
    for i in range(len(users)):
        online.append(users[i][0])
    return online

class ChatServer(threading.Thread):
    global users, que, lock, IP
    def __init__(self, ip,port): #构造函数
        threading.Thread.__init__(self)
        self.ADDR = (ip, port)
        os.chdir(sys.path[0])
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def recv(self, data, addr):
        lock.acquire()
        try:
            que.put((addr, data))
        finally:
            lock.release()

        # 判断断开用户在users中是第几位并移出列表, 刷新客户端的在线用户显示

    def delUsers(self, addr):
        a = 0
        for i in users:  # 循环遍历 看看要删除的用户是第几个用户
            if i[1] == addr:
                users.pop(a)  # 注意a用的很好
                print(' Remaining online users: ', end='')  # 打印剩余在线用户(conn)
                d = onlines()
                self.recv(d, addr)
                print(d)
                break
            a += 1

    def udp_connect(self,):
        while True:
            data, address = self.s.recvfrom(MAX_BYTES)
            # print(data.decode())
            msglist = data.decode().split(';;') # login
            met = msglist[0]        #模式： 登录 退出 发言
            mes = msglist[1]
            # datalist = mes.split(':;')
            if met == 'login':# 进入聊天室请求
                users.append((msglist[1],address))
                d = onlines()
                self.recv(d, address)
            elif met == 'speak':
                self.recv(mes,address)
            elif met == 'quit':
                self.delUsers(address)
            # print(data.decode())


    def sendData(self): #队列中(addr,data)
        while True:
            if not que.empty():
                data=''
                message = que.get()#addr , data
                print(message[1])
                if isinstance(message[1],str):
                    for i in range(len(users)):#给用户列表中的每一个人通报

                        for j in range(len(users)): #只是为了找出发出者的username（用户体验高）
                            if message[0]==users[j][1]:
                                data = '' + users[j][0] + ':' + message[1]

                        self.s.sendto(data.encode(), users[i][1])


                if isinstance(message[1], list):  # 同上
                    # 如果是list则打包后直接发送
                    data = json.dumps(message[1])
                    for i in range(len(users)):
                        try:
                            self.s.sendto(data.encode(),users[i][1]) #conn的对象
                        except:
                            pass

    def run(self):
        self.s.bind(self.ADDR)
        print('Chat server listening at',self.s.getsockname())

        t = threading.Thread(target=self.udp_connect)
        t.start()
        q = threading.Thread(target=self.sendData)
        q.start()



if __name__ == '__main__':
    IP = ''
    PORT = int(50007)
    cserver = ChatServer(IP,PORT)
    cserver.start()








