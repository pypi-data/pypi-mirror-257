def 获取电脑用户名():
    import getpass
    用户名 = getpass.getuser()
    return 用户名
def 获取当前精准时间():
    import datetime
    import time
    current_time = time.localtime()
    datetime = datetime.datetime.now()  # 获取当前时间
    year = datetime.year
    month = datetime.month
    day = datetime.day
    hour = current_time.tm_hour
    minute = current_time.tm_min
    second = current_time.tm_sec
    当前日期 = str(year) + "Y" + str(month) + "M" + str(day) + "D"
    当前时间 = str(hour) + "H" + str(minute) + "M" + str(second) + "S"
    当前精准时刻 = 当前日期 + 当前时间
    return 当前精准时刻
def 获取电脑公网ip以及电脑主机名称():
    from requests_html import HTMLSession
    import socket
    获取公网ip = HTMLSession()
    获取公网ip_动作 = 获取公网ip.get("https://api.ipify.org/")
    获取的内容 = 获取公网ip_动作.html.text
    分割换行符 = 获取的内容.split("\n")
    公网ip = 分割换行符[0]
    host_name = socket.gethostname()
    获取内网ip = socket.gethostbyname_ex(host_name)
    电脑基本信息 = "主机名称：" + host_name + "\n" + "内网ip列表:" + str(获取内网ip) + "\n" + "公网ip:" + 公网ip
    return 电脑基本信息
def 获取电脑的系统版本():
    import platform

    # 获取操作系统名称和版本
    os_name = platform.system()
    os_version = platform.release()
    win_ver = platform.win32_ver()
    # print(type( {win_ver[0]}))#这个是set格式的数据
    set格式的windows版本数据 = {win_ver[0]}
    str格式的windows版本数据 = str(set格式的windows版本数据)  # 现在就是str数据了
    str格式的windows版本数据 = "windows"+str格式的windows版本数据
    return str格式的windows版本数据
def 获取电脑基本架构信息():
    import platform
    获取电脑基本架构信息 = platform.architecture()
    # print(type(获取电脑基本架构信息))#这里的数据是tuple的，而不是str需要转换
    str格式的电脑基本架构信息 = str(获取电脑基本架构信息)
    return str格式的电脑基本架构信息

def 获取CPU核心数():
    import psutil

    # 获取CPU信息
    CPU核心数 = psutil.cpu_count()
    return CPU核心数

def 获取CPU频率():
    import psutil

    # 获取CPU信息
    CPU频率 = psutil.cpu_freq().current
    return CPU频率
#print(获取CPU频率())

def 获取CPU使用率():
    import psutil

    # 获取CPU信息
    CPU使用率 = psutil.cpu_percent()
    return CPU使用率

def 获取磁盘信息():
    import psutil
    磁盘信息 = psutil.disk_usage('/')
    磁盘信息 = str(磁盘信息)
    return 磁盘信息

def 获取内存信息():
    import psutil

    # 获取内存信息
    内存信息 = psutil.virtual_memory()
    内存信息 = str(内存信息)
    return 内存信息
def 获取网络信息():
    import psutil

    # 获取网络信息
    网络信息 = psutil.net_io_counters()
    网络信息 = str(网络信息)
    return 网络信息

def 获取显卡信息():
    import wmi
    显卡信息列表 = []
    c = wmi.WMI()
    video_controllers = c.Win32_VideoController()
    for controller in video_controllers:
        #print('显卡型号:', controller.Name)
        显卡信息列表.append(controller.Name)
    显卡信息列表 = str(显卡信息列表)
    return 显卡信息列表
def 获取电脑序列号():
    import wmi
    # 创建一个WMI对象
    序列号 = wmi.WMI()

    # 查询Win32_BIOS类获取序列号
    for 序列号 in 序列号.Win32_BIOS():
        # 打印并返回电脑序列号
        #print("电脑序列号为:", 序列号.SerialNumber)
        return 序列号.SerialNumber  # 直接返回序列号即可，无需在循环内部多次返回

def 获取电脑名称():
    import platform
    电脑名称 = platform.node()

    # 输出设备名称
    return 电脑名称

def 获取电脑设备和产品id():
    import wmi
    获取设备和产品id = wmi.WMI()
    for 电脑产品 in 获取设备和产品id.Win32_ComputerSystemProduct():
        设备ID = 电脑产品.UUID
        产品ID = 电脑产品.IdentifyingNumber
    设备ID和产品ID = 设备ID +"\n\n"+ 产品ID
    return 设备ID和产品ID

def 获取电脑品牌():
    电脑品牌信息 = []
    import wmi
    获取电脑品牌 = wmi.WMI()

    # 查询电脑品牌
    for instance in 获取电脑品牌.Win32_ComputerSystem():
        #print('电脑品牌:', instance.Manufacturer)
        电脑品牌信息.append(instance.Manufacturer)
        电脑品牌信息 = str(电脑品牌信息)
        return 电脑品牌信息
