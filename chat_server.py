"""
chat room
env:python3.6
socket udp and process
"""
from multiprocessing import Process
from socket import *
#用户信息存储{name：address}
user={}
# 服务器地址
HOST = "0.0.0.0"
PORT = 9422
ADDR = (HOST, PORT)

#处理进入聊天室
def do_login(s,name,address):
    if name in user:
        s.sendto("该用户名已存在".encode(),address)
        return
    else:
        s.sendto(b"OK",address)
       #告知其他人
        msg = "欢迎%s进入聊天室" % name
        for i in user:
            s.sendto(msg.encode(),user[i])

        user[name]=address #字典中增加一项
#处理聊天
def do_chat(s,name,text):
    msg="\n%s: %s"%(name,text)
    for i in user:
        #除去本人
        if i != name:
            s.sendto(msg.encode(),user[i])
#处理退出
def do_quit(s,name):
    del user[name]#删除用户
    msg="\n%s 退出聊天室"%name
    for i in user:
        s.sendto(msg.encode(),user[i])




# 接受各个客户端请求
def request(s):
    """

    :param s:套接字
    :return:
    """
    while True:
        data, addr = s.recvfrom(1024)  # 接受请求
        tmp=data.decode().split(" ")#对请求解析
        if tmp[0]=="L":
            #处理进入聊天室 tmp --> ["L","name"]
            do_login(s,tmp[1],addr)
        # 处理聊天 tmp --> [C,name,xxxx]
        elif tmp[0]=="C":
            do_chat(s,tmp[1],tmp[2])
        elif tmp[0]=="Q":
    # 处理退出 tmp --> ["Q","name"]
            do_quit(s,tmp[1])
#发送管理员消息
def manager(s):
    while True:
        msg=input("管理员消息：")
        msg="C管理员 "+msg
        s.sendto(msg.encode(),ADDR)#从父进程将消息发送给子进程


# 搭建基本结构
def main():
    # 创建一个udp套接字
    s = socket(AF_INET, SOCK_DGRAM)
    s.bind(ADDR)
    #创建新的进程用于给客户端发送管理员消息
    p=Process(target=request,args=(s,))

    p.start()
    manager(s)  # 处理发过来的请求
    p.join()

if __name__ == '__main__':
    main()
