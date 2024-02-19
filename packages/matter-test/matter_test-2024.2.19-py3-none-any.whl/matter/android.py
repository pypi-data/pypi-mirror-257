# -*- encoding: utf-8 -*-
'''
@File		:	android.py
@Time		:	2024/01/05 14:40:26
@Author		:	dan
@Description:	matter 安卓测试入口
'''



from matter.group import Group
from matter.manager.group_manager import GroupManager
import matter.utils.system_utils as system_utils
import os
import threading
import cv2
import random
import time


def touch(arr: tuple | list):
    """ 模拟点击

    Parameters
    ----------
    arr : array
        两种格式
        1、[x, y]，表示点击确定的点
        2、[x1, y1, x2, y2]，表示点击某个区域（会在该区域点击随机的点）

    Returns
    -------
    None
    """

    if len(arr) == 2:
        x = arr[0]
        y = arr[1]
    elif len(arr) == 4:
        x = arr[0]
        y = arr[1]
        x1 = arr[2]
        y1 = arr[3]

    touch_x = None
    if x1 and y1:
        touch_x = random.randrange(x, x1)
        touch_y = random.randrange(y, y1)
    else:
        touch_x = x;
        touch_y = y;
    group = current_group()
    for client in group.android_clients:
        client.adb.touch(touch_x, touch_y)
    if group.interval > 0:
        time.sleep(group.interval)
    return True
    


def slide(begin : tuple | list, end : tuple | list, speed : float | int = 200):
    """ 模拟滑动

    Parameters
    ----------
    begin : tuple | list
        起始点坐标，格式为 [x, y]

    end : tuple | list
        结束点坐标，格式为 [x, y]

    speed : float | int
        滑动经过的时间

    Returns
    -------
    None
    """
    # group_manager = GroupManager()
    # return group_manager.current_group.append_step(android_steps.SlideStep(begin, end, speed))

    group = current_group()
    for client in group.android_clients:
        client.adb.slide(begin, end, speed)
    if group.interval > 0:
        time.sleep(group.interval)
    return True





def touch_by_image(image_path : str):
    """ 匹配图片并且点击（会将匹配分数最高的进行点击）

    Parameters
    ----------
    image_path : str
        图片在本地的位置

    Returns 
    -------
    None
    """
    group = current_group()
    screen_image = image_path + ".screen.jpg"
    if len(group.android_clients) <= 0:
        system_utils.exit('没有连接到任何的android设备')
    
    client = group.android_clients[0]
    client.adb.screenshot(screen_image);
    img1 = cv2.imread(screen_image)
    img2 = cv2.imread(image_path)
    result = cv2.matchTemplate(img1, img2, cv2.TM_CCOEFF_NORMED)

    # 找到最大匹配值的位置
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # 返回最大匹配位置的坐标
    if max_val > 0.8:
        x, y = max_loc
        for cli in group.clients:
            cli.adb.touch(x, y)
        os.remove(screen_image)
    else:
        os.remove(screen_image)
        system_utils.exit(f"找不到匹配的图片{image_path}")
    if group.interval > 0:
        time.sleep(group.interval)
    return True



def find_element_by_text(value : str) -> dict:
    ''' 
    
    Parameters
    ----------
    
    
    Returns
    -------
    
    
    '''
    
    group = current_group()
    if len(group.android_clients) <= 0:
        system_utils.exit('没有连接到任何的android设备')
    
    client = group.android_clients[0]
    return client.adb.find_element('text', value)


def find_element_by_id(value : str) -> dict:
    ''' 
    
    Parameters
    ----------
    
    
    Returns
    -------
    
    
    '''
    
    group = current_group()
    if len(group.android_clients) <= 0:
        system_utils.exit('没有连接到任何的android设备')
    
    client = group.android_clients[0]
    return client.adb.find_element('id', value)




def find_element_by_xpath(value : str) -> dict:
    ''' 
    
    Parameters
    ----------
    
    
    Returns
    -------
    
    
    '''
    
    group = current_group()
    if len(group.android_clients) <= 0:
        system_utils.exit('没有连接到任何的android设备')
    
    client = group.android_clients[0]
    return client.adb.find_element('xpath', value)

def exist_image(image_path : str) -> bool:
    """ 匹配图片并且点击（会将匹配分数最高的进行点击）

    Parameters
    ----------
    image_path : str
        图片在本地的位置

    Returns 
    -------
    None
    """
    group = current_group()
    screen_image = image_path + ".screen.jpg"
    if len(group.android_clients) <= 0:
        system_utils.exit('没有连接到任何的android设备')
    
    client = group.android_clients[0]
    client.adb.screenshot(screen_image);
    img1 = cv2.imread(screen_image)
    img2 = cv2.imread(image_path)
    result = cv2.matchTemplate(img1, img2, cv2.TM_CCOEFF_NORMED)

    # 找到最大匹配值的位置
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # 返回最大匹配位置的坐标
    if max_val > 0.8:
        return True
    else:
        return False


def touch_by_text(text : str):
    """ 匹配文本内容并且点击（会点击匹配到的第一个按钮，没有则不点击）

    Parameters
    ----------
    text : str
        文本内容

    Returns 
    -------
    None
    """
    group = current_group()
    if len(group.android_clients) <= 0:
        system_utils.exit('没有连接到任何的android设备')
    
    client = group.android_clients[0]
    element = client.adb.find_element('text', text)
    for client in current_group().android_clients:
        client.adb.touch_element(element)
    if group.interval > 0:
        time.sleep(group.interval)
    return True

def touch_by_content(text : str):
    """ 匹配文本内容并且点击（会点击匹配到的第一个按钮，没有则不点击）

    Parameters
    ----------
    text : str
        文本内容

    Returns 
    -------
    None
    """
    group = current_group()
    if len(group.android_clients) <= 0:
        system_utils.exit('没有连接到任何的android设备')
    
    client = group.android_clients[0]
    element = client.adb.find_element('content', text)
    for client in current_group().android_clients:
        client.adb.touch_element(element)
    if group.interval > 0:
        time.sleep(group.interval)
    return True




def touch_by_id(id : str):
    """ 匹配id并且点击（会点击匹配到的第一个按钮，没有则不点击）

    Parameters
    ----------
    id : str
        id 的值

    Returns 
    -------
    None
    """
    group = current_group()
    if len(group.android_clients) <= 0:
        system_utils.exit('没有连接到任何的android设备')
    
    client = group.android_clients[0]
    element = client.adb.find_element('id', id)
    for client in current_group().android_clients:
        client.adb.touch_element(element)
    if group.interval > 0:
        time.sleep(group.interval)
    return True



def touch_by_xpath(xpath : str):
    """ 匹配xpath并且点击（会点击匹配到的第一个按钮，没有则不点击）

    Parameters
    ----------
    xpath : str
        xpath 的值

    Returns 
    -------
    None
    """
    group = current_group()
    if len(group.android_clients) <= 0:
        system_utils.exit('没有连接到任何的android设备')
    
    client = group.android_clients[0]
    element = client.adb.find_element('xpath', xpath)
    for client in current_group().android_clients:
        client.adb.touch_element(element)
    if group.interval > 0:
        time.sleep(group.interval)
    return True


def input(text : str):
    """ 模拟键盘输入文本

    Parameters
    ----------
    text : str
        文本 内容

    Returns 
    -------
    bool
        输入成功 True
        输入失败 False
    """
    group = current_group()
    for client in group.android_clients:
        client.adb.send_keys(text)
    if group.interval > 0:
        time.sleep(group.interval)
    return True




def keyevent(text : str):
    """ 模拟键盘输入文本

    Parameters
    ----------
    text : str
        文本 内容

    Returns 
    -------
    bool
        输入成功 True
        输入失败 False
    """
    group = current_group()
    for client in group.android_clients:
        client.adb.keyevent(text)
    if group.interval > 0:
        time.sleep(group.interval)
    return True


def monkey():
    """ 执行安卓monkey测试

    Parameters
    ----------

    Returns 
    -------
    bool
        执行成功 True
        执行失败 False
    """
    group = current_group()
    for client in group.android_clients:
        client.adb.monkey()
    if group.interval > 0:
        time.sleep(group.interval)
    return True


def count() -> int:
    ''' 返回已连接的终端数量
    
    Parameters
    ----------
    
    
    Returns
    -------
    int
    
    '''
    return len(current_group().android_clients);


def current_group() -> Group:
    ''' 获取当前的组
    
    Parameters
    ----------
    
    
    Returns
    -------
    Group
    获取当前的组
    '''
    group_manager = GroupManager()
    if not group_manager.is_inited:
        group_manager.init()
    current_thread = threading.current_thread()
    group = group_manager.groups_by_thread[current_thread.name]
    return group;
    