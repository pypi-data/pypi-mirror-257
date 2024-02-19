# -*- encoding: utf-8 -*-
'''
@File		:	socket_utils.py
@Time		:	2024/01/18 12:26:31
@Author		:	dan
@Description:	socket相关客户端
'''



import socket
import selectors
import time
import json
from threading import Thread, Lock

class Protocol:
    udp = 'udp'
    tcp = 'tcp'

class SocketClient:
    '''
    socket的客户端程序
    '''
    @property
    def host(self) -> str:
        """
        代理服务器的地址 格式为  protocol://IP:Port  例如  tcp://192.168.2.5:8888 或者 udp://192.168.2.6:9999
        """
        return f"{self.__protocol}://{self.__server_host}:{self.__server_port}"
    
    @property
    def connected(self) -> bool:
        """
        是否连接到远程代理
        """
        if self.__protocol == 'udp':
            return True
        return self.__connected

    def __init__(self, protocol : str , server_host : str, server_port : int = 6666, heartbeat_time :int = 10) -> None:
        self.__server_host = server_host
        self.__server_port = server_port
        self.__protocol = protocol
        self.__selector = selectors.DefaultSelector()
        self.__started = False
        self.__running = False
        self.__buffer = []
        self.__lock = Lock()
        self.__heartbeat_time = heartbeat_time
        self.__last_heartbeat_time = 0
        self.__last = b''
        self.__connected = False;
        pass


    def start(self) -> None:
        ''' 开始连接服务器并且发送数据
        
        Parameters
        ----------
        
        
        Returns
        -------
        None
        
        '''
        self.__thread = Thread(target=self.run)
        self.__thread.start()
        self.__started = True
        pass

    def run(self) -> None:
        ''' 线程内执行的内容
        
        Parameters
        ----------
        
        
        Returns
        -------
        None
        
        '''
        if self.__protocol == 'udp':
            self.run_udp()

        else:
            self.run_tcp()

    

    def run_udp(self) -> None:
        ''' 
        
        Parameters
        ----------
        
        
        Returns
        -------
        None
        
        '''
        try:
            self.__socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # self.__socket.connect((self.__server_host, self.__server_port))
            self.__socket.setblocking(False)

            self.__selector.register(
                self.__socket,
                selectors.EVENT_READ | selectors.EVENT_WRITE
            )
            self.__running = True

            while self.__running:

                for key, mask in self.__selector.select(timeout=1):

                    if mask & selectors.EVENT_READ:
                        data = self.__socket.recv(1024)
                        if data:
                            data_list = str(self.__last + data, encoding='utf8').split("\n")
                            self.__last = bytes(data_list[-1], encoding='utf8')
                            data = data_list[:-1]
                            if data:
                                for line in data:
                                    print('    接收 {!r}'.format(line))
                        self.__selector.modify(self.__socket, selectors.EVENT_WRITE)

                    if mask & selectors.EVENT_WRITE:
                        

                        next_msg = self.__next_msg()
                        while next_msg:
                            print('    发送 {!r}'.format(next_msg))
                            self.__socket.sendto(next_msg, (self.__server_host, self.__server_port))         
                            next_msg = self.__next_msg()

                        # 发送心跳
                        # if time.time() - self.__last_heartbeat_time > self.__heartbeat_time:
                        #     heartbeat = '1';
                        #     self.__socket.sendall(bytes(heartbeat + '\n', encoding='utf8'));
                        #     self.__last_heartbeat_time = time.time()
                        # else:
                        self.__selector.modify(self.__socket, selectors.EVENT_READ)
                            
                        # self.__selector.modify(self.__socket, selectors.EVENT_WRITE)
        except Exception as ex:
            print(ex)
            pass

        self.__selector.unregister(self.__socket)
        self.__socket.close()

    def run_tcp(self) -> None:
        ''' 如果是tcp协议，则初始化tcp
        
        Parameters
        ----------
        
        
        Returns
        -------
        None
        
        '''
        
        try:
            self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.__socket.connect((self.__server_host, self.__server_port))
            self.__socket.setblocking(False)

            self.__selector.register(
                self.__socket,
                selectors.EVENT_READ | selectors.EVENT_WRITE
            )
            self.__running = True

            while self.__running:

                for key, mask in self.__selector.select(timeout=1):

                    if mask & selectors.EVENT_READ:
                        data = self.__socket.recv(1024)
                        if data:
                            data_list = str(self.__last + data, encoding='utf8').split("\n")
                            self.__last = bytes(data_list[-1], encoding='utf8')
                            data = data_list[:-1]
                            if data:
                                for line in data:
                                    print('    接收 {!r}'.format(line))
                        self.__selector.modify(self.__socket, selectors.EVENT_WRITE)

                    if mask & selectors.EVENT_WRITE:
                        

                        next_msg = self.__next_msg()
                        while next_msg:
                            print('    发送 {!r}'.format(next_msg))
                            self.__socket.sendall(next_msg)         
                            next_msg = self.__next_msg()

                        # 发送心跳
                        # if time.time() - self.__last_heartbeat_time > self.__heartbeat_time:
                        #     heartbeat = '1';
                        #     self.__socket.sendall(bytes(heartbeat + '\n', encoding='utf8'));
                        #     self.__last_heartbeat_time = time.time()
                        # else:
                        self.__selector.modify(self.__socket, selectors.EVENT_READ)
                            
                        # self.__selector.modify(self.__socket, selectors.EVENT_WRITE)

        except Exception as ex:
            print(ex)
            pass
        self.__selector.unregister(self.__socket)
        self.__socket.close()


    def __next_msg(self) -> any:
        ''' 获取下一个要发送的消息
        
        Parameters
        ----------
        
        
        Returns
        -------
        
        
        '''
        with self.__lock:
            if self.__buffer:
                next_msg = self.__buffer.pop()
            else :
                next_msg = None
        return next_msg


    def close(self) -> None:
        ''' 关闭客户端
        
        Parameters
        ----------
        
        
        Returns
        -------
        None
        
        '''
        self.__running = False
        self.__started = False
        


    def write(self, msg : str | dict | bytes) -> None:
        ''' 向远端写出数据
        
        Parameters
        ----------
        
        
        Returns
        -------
        None
        
        '''
        if not self.__running:
            raise ConnectionError()
        if type(msg) == str:
            msg = bytes(msg + "\n", encoding='utf8')
        elif type(msg) == dict:
            msg = json.dump(msg)
            msg = bytes(msg + "\n", encoding='utf8')
        with self.__lock:
            self.__buffer.append(msg)


if __name__ == '__main__':
    client = SocketClient(protocol='udp', server_host="127.0.0.1", server_port=9999)
    client.start()
    time.sleep(3)
    for i in range(10):
        client.write("123")

    time.sleep(1000)
    client.close()