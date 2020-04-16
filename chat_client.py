"""
chat room
客户端
功能：发送请求,获取结果
"""
from socket import *
from multiprocessing import Process
import sys

# 服务器地址
ADDR = ("127.0.0.1", 9422)


# 网络结构
def recv_msg(s):
    while True:
        data, addr = s.recvfrom(4096)
        print(data.decode() + "\n发言:", end="")


def send_msg(s, name):
    while True:
        try:
            # 对异常退出的处理
            text = input("发言：")
        except KeyboardInterrupt:
            text = "quit"
        if text == "quit":
            # 退出消息
            msg = "Q " + name
            s.sendto(msg.encode(), ADDR)  # 告知服务端
            sys.exit("退出聊天室")  # 进程结束

        msg = "C %s %s" % (name, text)
        s.sendto(msg.encode(), ADDR)

#网络结构
def main():
    s = socket(AF_INET, SOCK_DGRAM)
    # 进入聊天室
    while True:
        name = input("请输入姓名：")
        msg = "L " + name  # 根据协议，组织消息格式
        s.sendto(msg.encode(), ADDR)  # 将姓名发送给服务端
        data, addr = s.recvfrom(128)  # 接受反馈
        if data.decode() == "OK":
            print("您已进入聊天室")

            break
        else:
            print(data.decode())
    p = Process(target=recv_msg, args=(s,))  # 子进程接受消息
    p.start()
    # 发送消息
    send_msg(s,name)



if __name__ == '__main__':
    main()
