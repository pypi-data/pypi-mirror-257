# -*- encoding: utf-8 -*-
'''
@File		:	__init__.py
@Time		:	2024/01/05 09:50:06
@Author		:	dan
@Description:	客户端的封装，包含adb、browser、http、desktop
'''



from matter.client.adb import Adb
from matter.client.browser import Browser
from matter.client.desktop import Desktop
from matter.client.http_utils import Http
from matter.client.socket_utils import SocketClient
from matter.manager.proxy_manager import PROXY_MANAGER
from matter.proxy.proxy_client import ProxyClient
import matter.utils.system_utils as system_utils


class Client:

    @property
    def proxys(self) -> list[ProxyClient]:
        return self.__proxys
    
    @property
    def adb(self) -> Adb:
        return self.__adb
    
    @property
    def browser(self) -> Browser:
        return self.__browser
    
    @property
    def desktop(self) -> Desktop:
        return self.__desktop
    
    @property
    def http(self) -> Http:
        return self.__http
    
    @property
    def socket(self) -> SocketClient:
        return self.__socket

    def __init__(self, 
                 adb : Adb = None, 
                 browser : Browser = None, 
                 desktop : Desktop = None, 
                 socket : SocketClient = None, 
                 http : Http = None) -> None:
        self.__adb = adb;
        self.__browser = browser;
        self.__desktop = desktop;
        self.__http = http;
        self.__socket = socket;
        self.__proxys : list[str] = []
        pass


    def append_proxy(self, server_host: str ) -> None:
        ''' 添加代理，当此Client执行某些内容时，会传递到代理服务器中，让代理执行相同内容
        
        Parameters
        ----------
        server_host : str 远端代理服务器的地址
        
        Returns
        -------
        None

        
        '''
        self.__proxys.append(server_host)
        pass


    def send_to_proxy(self, msg : str | dict) -> None:
        ''' 发送给该client对应的远程设备
        
        Parameters
        ----------
        
        
        Returns
        -------
        None
        
        '''
        if not self.__proxys:
            return;
        for host in self.__proxys:
            PROXY_MANAGER.send_to_proxy(host, msg)
        pass


    def init_by_apk(self, apk : str, package_name : str, waiting : bool = True, uninstall : bool = False, run_app : bool = False) -> None:
        ''' 根据apk初始化
        
        Parameters
        ----------
        apk : str apk文件位置

        package_name : str apk文件 对应的包名

        waiting : bool = True 是否等待apk安装完成
        
        uninstall : bool = False 安装前是否卸载
        
        restart : bool = True 是否重新运行app
        
        Returns
        -------
        None
        
        '''
        if not self.adb:
            return;
    
        self.adb.package_name = package_name

        if not self.adb.connected:
            self.adb.connect()
        self.adb.unlock(check_status=True)
        installed = self.adb.is_installed()
        if not installed:
            self.adb.install(apk, uninstall=uninstall)
        elif uninstall:
            self.adb.install(apk, uninstall=uninstall)

        current = self.adb.app_current();
        current_package = current['package_name']
        if current_package == package_name:
            if not run_app:
                self.adb.app_stop(current_package)

        if self.__proxys:
            # TODO 代理处理
            pass

        return package_name


    def init_by_package(self, package_name : str, waiting : bool = True) -> None:
        ''' 根据apk初始化
        
        Parameters
        ----------
        apk : str apk文件位置

        package_name : str apk文件 对应的包名

        waiting : bool = True 是否等待apk安装完成
        
        uninstall : bool = False 安装前是否卸载
        
        restart : bool = True 是否重新运行app
        
        Returns
        -------
        None
        
        '''
        if not self.adb:
            return;
    
        self.adb.package_name = package_name

        if not self.adb.is_installed(package_name):
            system_utils.exit(f'在安卓{self.adb.host}设备找不到应用{package_name}')

        self.adb.unlock(check_status=True)
        current = self.adb.app_current();
        current_package = current['package_name']
        if current_package == package_name:
            self.adb.app_stop(current_package)

        if self.__proxys:
            # TODO 代理处理
            pass

        return package_name

    def open_by_package(self, package_name : str, waiting : bool = True, restart : bool = True) -> None:
        ''' 根据apk初始化
        
        Parameters
        ----------
        package_name : str app 的包名
        
        waiting : bool = True 是否等待apk安装完成
        
        restart : bool = True 是否重新运行app
        
        Returns
        -------
        None
        
        '''
        if not self.adb:
            return;

    
        self.adb.package_name = package_name
        if not self.adb.connected:
            self.adb.connect()

        self.adb.unlock(check_status=True)
        current = self.adb.app_current();
        current_package = current['package_name']
        if current_package != package_name or restart:
            if current_package:
                self.adb.app_stop(current_package)
            self.adb.app_start(package_name)
            return;


    def close_by_package(self, package_name : str, waiting : bool = True) -> None:
        ''' 关闭应用
        
        Parameters
        ----------
        package_name : str app 的包名
        
        waiting : bool = True 是否等待apk安装完成
        
        Returns
        -------
        None
        
        '''
        if not self.adb:
            return;

    
        self.adb.package_name = package_name
        if not self.adb.connected:
            self.adb.connect()

        self.adb.unlock(check_status=True)
        self.adb.app_stop(package_name)

    def init_by_browser(self, waiting : bool = True) -> None:
        ''' 为浏览器初始化
        
        Parameters
        ----------
        
        
        Returns
        -------
        
        
        '''
        if not self.__browser:
            return;
        ## TODO 改为用线程开启，应该会更快
        self.__browser.init_driver()

        if self.__proxys:
            # TODO 代理处理
            for proxy in self.__proxys:
                self.__init_remote_browser(self.__browser)
            pass


    def open_by_browser(self, waiting : bool = True) -> None:
        ''' 为浏览器初始化
        
        Parameters
        ----------
        
        
        Returns
        -------
        
        
        '''
        if not self.__browser:
            return;
        ## TODO 改为用线程开启，应该会更快
        self.__browser.open()

        if self.__proxys:
            # TODO 代理处理
            for proxy in self.__proxys:
                self.__open_remote_browser(self.__browser)
            pass


    def close_by_browser(self, waiting : bool = True) -> None:
        ''' 为浏览器初始化
        
        Parameters
        ----------
        
        
        Returns
        -------
        
        
        '''
        if not self.__browser:
            return;
        ## TODO 改为用线程开启，应该会更快
        self.__browser.close()

        if self.__proxys:
            # TODO 代理处理
            for proxy in self.__proxys:
                self.__close_remote_browser(self.__browser)
            pass

    def init_by_http(self, waiting : bool = True) -> None:
        ''' 为http请求初始化
        
        Parameters
        ----------
        
        
        Returns
        -------
        
        
        '''
        if not self.__http:
            return;

        ## TODO 待补充


    def open_by_http(self, waiting : bool = True) -> None:
        ''' 为http请求初始化
        
        Parameters
        ----------
        
        
        Returns
        -------
        
        
        '''
        if not self.__http:
            return;

        ## TODO 待补充


    def close_by_http(self, waiting : bool = True) -> None:
        ''' 为http请求初始化
        
        Parameters
        ----------
        
        
        Returns
        -------
        
        
        '''
        if not self.__http:
            return;

        ## TODO 待补充


    def init_by_socket(self, waiting : bool = True) -> None:
        ''' 为http请求初始化
        
        Parameters
        ----------
        
        
        Returns
        -------
        
        
        '''
        if not self.__socket:
            return;


        # self.__socket.close()
        # self.__socket.start()


    def close_by_socket(self, waiting : bool = True) -> None:
        ''' 为http请求初始化
        
        Parameters
        ----------
        
        
        Returns
        -------
        
        
        '''
        if not self.__socket:
            return;


        self.__socket.close()

    def open_by_socket(self, waiting : bool = True) -> None:
        ''' 为http请求初始化
        
        Parameters
        ----------
        
        
        Returns
        -------
        
        
        '''
        if not self.__socket:
            return;


        self.__socket.close()
        self.__socket.start()


    def init_by_desktop(self, waiting : bool = True) -> None:
        ''' 为desktop程序初始化
        
        Parameters
        ----------
        
        
        Returns
        -------
        
        
        '''

        if self.__proxys:
            # TODO 代理处理
            pass


    def open_by_desktop(self, waiting : bool = True) -> None:
        ''' 为desktop程序初始化
        
        Parameters
        ----------
        
        
        Returns
        -------
        
        
        '''
        if not self.__desktop:
            return;

        self.__desktop.open()

        if self.__proxys:
            # TODO 代理处理
            pass


    def close_by_desktop(self, waiting : bool = True) -> None:
        ''' 为desktop程序初始化
        
        Parameters
        ----------
        
        
        Returns
        -------
        
        
        '''
        if not self.__desktop:
            return;

        self.__desktop.close()

        if self.__proxys:
            # TODO 代理处理
            pass