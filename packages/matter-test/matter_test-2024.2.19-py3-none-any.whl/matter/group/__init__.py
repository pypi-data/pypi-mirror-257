# -*- encoding: utf-8 -*-
'''
@File		:	group.py
@Time		:	2024/01/05 10:03:26
@Author		:	dan
@Description:	组对象
'''


from matter.client import Client
from matter.manager.case_manager import CaseManager
from matter.steps.base_step import BaseStep
import matter.utils.system_utils as system_utils
import threading
import warnings
import matter.utils.console as console

class AndroidSetting:
    '''
    安卓端的设置
    '''

    @property
    def apk(self) -> str:
        '''
        安卓端apk位置
        '''
        return self.__apk

    @property
    def package_name(self) -> str:
        '''
        需要测试的包名
        '''
        return self.__package_name
        

    @property
    def android_test(self) -> str:
        '''
        使用apk测试还是 package_name测试
        '''
        return self.__android_test
        

    @property
    def uninstall(self) -> bool:
        '''
        安装apk之前是否卸载原来的apk
        '''
        return self.__uninstall
        

    @property
    def restart(self) -> bool:
        '''
        每次测试是否重启应用
        '''
        return self.__restart

    def __init__(self, apk, package_name, android_test, uninstall, restart) -> None:
        self.__apk = apk
        self.__package_name = package_name
        self.__android_test = android_test
        self.__uninstall = uninstall
        self.__restart = restart




class BrowserSetting:
    '''
    浏览器的设置
    '''

    @property
    def url(self) -> str:
        '''
        浏览器打开时候第一个页面
        '''
        return self.__url

    @property
    def window_size(self) -> str:
        '''
        浏览器打开的大小
        '''
        return self.__window_size
        

    def __init__(self, url, window_size) -> None:
        self.__url = url
        self.__window_size = window_size





class DesktopSetting:
    '''
    桌面程序的设置
    '''

    @property
    def restart(self) -> bool:
        '''
        开启测试时是否重新启动应用
        '''
        return self.__restart

    @property
    def window_size(self) -> str:
        '''
        测试程序窗口大小
        '''
        return self.__window_size

    @property
    def bin(self) -> str:
        '''
        测试程序位置
        '''
        return self.__bin
        
        

    def __init__(self, restart, window_size, bin) -> None:
        self.__restart = restart
        self.__window_size = window_size
        self.__bin = bin


class HttpSetting:
    '''
    Http请求的设置
    '''

    @property
    def host(self) -> str:
        return self.__host

    def __init__(self, host : str) -> None:
        self.__host = host


class SocketSetting:
    '''
    Socket请求的设置
    '''
    @property
    def host(self) -> str:
        return self.__host

    def __init__(self, host : str) -> None:
        self.__host = host

class Group:
    '''
    组的对象，一个group对多个client
    '''

    @property
    def steps(self) -> list[BaseStep]:
        warnings.warn('step不再使用', DeprecationWarning)
        return self.__steps

    @property
    def clients(self) -> list[Client]:
        return self.__clients

    @property
    def group_name(self) -> str:
        return self.__group_name

    @property
    def interval(self) -> int:
        return self.__interval

    @property
    def width(self) -> int:
        return self.__width

    @property
    def height(self) -> int:
        return self.__height

    @property
    def repeat(self) -> int:
        return self.__repeat
    

    @property
    def android_clients(self) -> list[Client]:
        ''' 
        安卓的客户端        
        '''
        
        return self.__android_clients


    @property
    def browser_clients(self) -> list[Client]:
        ''' 
        浏览器的客户端        
        '''
        
        return self.__browser_clients


    @property
    def desktop_clients(self) -> list[Client]:
        ''' 
        桌面程序的客户端        
        '''
        
        return self.__desktop_clients


    @property
    def http_clients(self) -> list[Client]:
        ''' 
        http请求的客户端        
        '''
        
        return self.__http_clients


    @property
    def socket_clients(self) -> list[Client]:
        ''' 
        socket的客户端        
        '''
        
        return self.__socket_clients

    @property
    def clients(self) -> list[Client]:
        ''' 
        已连接的终端数量        
        '''
        
        return self.__clients
    
    @property
    def thread(self) -> threading.Thread:
        '''
        该组拥有的线程
        '''
        return self.__thread
    
    def __init__(self, 
                 group_name: str,
                 clients: list[Client],
                 cases: list[str],
                 android_setting : AndroidSetting = None,
                 browser_setting : BrowserSetting = None,
                 desktop_setting : DesktopSetting = None,
                 http_setting : HttpSetting = None,
                 socket_setting : SocketSetting = None,
                 interval: int = 1,
                 width : int = 1920, 
                 height : int = 1080,
                 debug : bool = False,
                 repeat : int = 1, ) -> None:
        
        

        self.__clients = clients
        self.__group_name = group_name
        self.__interval = interval
        self.__width = width
        self.__height = height
        self.__repeat = repeat
        self.__steps = []
        self.__started = False

        self.__android_setting = android_setting
        self.__browser_setting = browser_setting
        self.__desktop_setting = desktop_setting
        self.__http_setting = http_setting
        self.__socket_setting = socket_setting
        
        ## 如果是调试模式，则循环次数强制为1
        if debug:
            self.__repeat = 1


        self.__android_clients : list[Client] = []
        self.__browser_clients : list[Client] = []
        self.__desktop_clients : list[Client] = []
        self.__http_clients : list[Client] = []
        self.__socket_clients : list[Client] = []

        for client in clients:
            if client.adb:
                self.__android_clients.append(client)
            if client.browser:
                self.__browser_clients.append(client)
            if client.desktop:
                self.__desktop_clients.append(client)
            if client.http:
                self.__http_clients.append(client)
            if client.socket:
                self.__socket_clients.append(client)


        self.__case_manager = CaseManager()
        for case_name in cases:
            test_case = self.__case_manager.find_case(case_name)
            if not test_case:
                system_utils.exit(f'不存在测试用例 {test_case}')
        self.__cases = cases
        

        self.__thread = threading.Thread(target=self.run)
        


    def run(self) -> None:
        ''' 线程内运行的方法
        
        Parameters
        ----------
        
        
        Returns
        -------
        None
        
        '''
        ## 所有测试用例执行前运行
        self.init_test_env(waiting=True)


        ## 每个测试用例重复执行的次数
        if self.__repeat <= 1:
            self.__repeat = 1

        for i in range(self.__repeat):
            for case_name in self.__cases:
                self.__before_run_case(case_name)
                try:
                    console.print_info(f"启动测试用例 - {case_name}")
                    self.__case_manager.run_case(case_name)
                    console.print_ok(f"测试通过 - {case_name}")
                except:
                    console.print_error(f"测试不通过 - {case_name}")
                    pass
                self.__after_run_case(case_name)


    def __before_run_case(self, case_name:str ) ->  None:
        ''' 
        在执行测试用例前执行
        '''
        if self.__android_setting:
            for client in self.__clients:
                if not client.adb:
                    continue;
                client.open_by_package(package_name=self.__package_name, 
                                        waiting=True, 
                                        restart=self.__android_setting.restart)

        if self.__browser_setting:
            for client in self.__clients:
                if not client.browser:
                    continue;
                client.open_by_browser(waiting=True)

        if self.__http_setting:
            for client in self.__clients:
                if not client.http:
                    continue;
                client.open_by_http(waiting=True)

        if self.__desktop_setting:
            for client in self.__clients:
                if not client.desktop:
                    continue;
                client.open_by_desktop(waiting=True)

        if self.__socket_setting:
            for client in self.__clients:
                if not client.socket:
                    continue;
                client.open_by_socket(waiting=True)


    def __after_run_case(self, case_name:str) ->  None:
        ''' 
        在执行测试用例前执行
        '''
        
        if self.__android_setting:
            for client in self.__clients:
                if not client.adb:
                    continue;
                client.close_by_package(package_name=self.__android_setting.package_name, 
                                        waiting=True)

        if self.__browser_setting:
            for client in self.__clients:
                if not client.browser:
                    continue;
                client.close_by_browser(waiting=True)

        if self.__http_setting:
            for client in self.__clients:
                if not client.http:
                    continue;
                client.close_by_http(waiting=True)

        if self.__desktop_setting:
            for client in self.__clients:
                if not client.desktop:
                    continue;
                client.close_by_desktop(waiting=True)

        if self.__socket_setting:
            for client in self.__clients:
                if not client.socket:
                    continue;
                client.close_by_socket(waiting=True)
        


    def init_test_env(self, waiting : bool = True) -> None:
        ''' 初始化测试环境

        对于安卓，则是安装必要的apk，和启动程序

        对于desktop程序，则是打开位置的程序

        对于浏览器，则是打开浏览器并打开特定网址
        
        Parameters
        ----------
        waiting : bool 是否等待所有客户端完成
        
        Returns
        -------
        None
        
        '''
        
        if self.__android_setting:
            print("正在启动安卓测试环境")
            for client in self.__clients:
                if not client.adb:
                    continue;
                if self.__android_setting.android_test == 'apk':
                    package_name = client.init_by_apk(self.__android_setting.apk, 
                                       waiting = waiting, 
                                       uninstall=self.__android_setting.uninstall)
                    self.__package_name = package_name
                else:
                    self.__package_name = self.__android_setting.package_name
                    package_name = client.init_by_package(package_name=self.__package_name, 
                                       waiting = waiting)
            print("安卓测试环境启动完毕")

        if self.__browser_setting:
            print("正在启动浏览器测试环境")
            for client in self.__clients:
                if not client.browser:
                    continue;
                client.init_by_browser(waiting=waiting)
            print("浏览器测试环境启动完毕")

        if self.__http_setting:
            print("正在启动HTTP测试环境")
            for client in self.__clients:
                if not client.http:
                    continue;
                client.init_by_http(waiting=waiting)
            print("HTTP测试环境启动完毕")

        if self.__desktop_setting:
            print("正在启动桌面程序测试环境")
            for client in self.__clients:
                if not client.desktop:
                    continue;
                client.init_by_desktop(waiting=waiting)
            print("桌面程序测试环境启动完毕")

        if self.__socket_setting:
            print("正在启动Socket测试环境")
            for client in self.__clients:
                if not client.socket:
                    continue;
                client.init_by_socket(waiting=waiting)
            print("Socket测试环境启动完毕")


    def start(self) -> None:
        ''' 开始执行测试组
        
        Parameters
        ----------
        
        
        Returns
        -------
        None
        
        '''
        
        if self.__started:
            return;
        self.__started = True
        self.__thread.start()