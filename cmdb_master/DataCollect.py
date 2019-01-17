#coding=utf8
from pysnmp.hlapi import *
# pip3 install pysnmp-mibs
import chardet
import sys
# snmp 配置服务 对远程机器可访问。
#get

class DataCollect():

    def __init__(self, host, community="public", protocol=1, port=161):
        self.community = community
        self.protocol = protocol
        self.host = host
        self.port = port

    def get_by_oid(self, oid):
        community=self.community; protocol=self.protocol; host=self.host; port=self.port
        for (errorIndication,
             errorStatus,
             errorIndex,
             varBinds)  in getCmd(SnmpEngine(),
                    CommunityData(community, mpModel=protocol),
                    UdpTransportTarget((host, port)),
                    ContextData(),
                    ObjectType(ObjectIdentity(oid)), 
                    lexicographicMode=False):
            para = [x.prettyPrint() for x in varBinds[0]][1]
            return para


    # 对table形式的数据walk  
    # 网卡部分  windows linux 通用
    def inet_collect(self):
        #【ifindex, ifName,ifDescr, ifType, ifMtu, ifSpeed ifPhysAddress, ifAddress, ifnetMask】
        # {1:{},2:{},3:{}} 数字索引编号，字典存储详情
        card_dict = {}
        community=self.community; protocol=self.protocol; host=self.host; port=self.port
        for (errorIndication,
             errorStatus,
             errorIndex,
             varBinds) in nextCmd(SnmpEngine(),
                                  CommunityData(community, mpModel=protocol),
                                  UdpTransportTarget((host, port)),
                                  ContextData(),
                                  ObjectType(ObjectIdentity('IF-MIB', 'ifName')),
                                  ObjectType(ObjectIdentity('IF-MIB', 'ifDescr')),
                                  ObjectType(ObjectIdentity('IF-MIB', 'ifType')),
                                  ObjectType(ObjectIdentity('IF-MIB', 'ifMtu')),
                                  ObjectType(ObjectIdentity('IF-MIB', 'ifSpeed')),
                                  ObjectType(ObjectIdentity('IF-MIB', 'ifPhysAddress')),
                                  ObjectType(ObjectIdentity('IF-MIB', 'ifIndex')),
                                  lexicographicMode=False):
            if errorIndication:
                print(errorIndication)
                break
            elif errorStatus:
                print('%s at %s' % (errorStatus.prettyPrint(),
                                    errorIndex and varBinds[int(errorIndex)-1][0] or '?'))
                break
            else:
                ifName = [x.prettyPrint() for x in varBinds[0]][1]
                ifDescr = [x.prettyPrint() for x in varBinds[1]][1]
                ifType = [x.prettyPrint() for x in varBinds[2]][1]
                ifMtu = [x.prettyPrint() for x in varBinds[3]][1]
                ifSpeed = [x.prettyPrint() for x in varBinds[4]][1]
                ifPhysAddress = [x.prettyPrint() for x in varBinds[5]][1]
                ifindex =  [x.prettyPrint() for x in varBinds[6]][1]
                card_dict[ifindex] = {"ifName":ifName,
                                      "ifDescr":ifDescr,
                                      "ifType":ifType,
                                      "ifMtu":ifMtu,
                                      "ifSpeed":ifSpeed,
                                      "ifPhysAddress":ifPhysAddress,
                                      "ipAdentAddr":"",
                                      "ipAdEntNetMask":""
                                      }
    # IP 地址 使用ifindex 和 ipAdEntifindex 对应
        for (errorIndication,
             errorStatus,
             errorIndex,
             varBinds) in nextCmd(SnmpEngine(),
                                  CommunityData(community, mpModel=protocol),
                                  UdpTransportTarget((host, port)),
                                  ContextData(),
                                  ObjectType(ObjectIdentity('.1.3.6.1.2.1.4.20.1.1')),  # ipAdEntAddr
                                  ObjectType(ObjectIdentity('.1.3.6.1.2.1.4.20.1.2')),  # ipAdEntifindex
                                  ObjectType(ObjectIdentity('.1.3.6.1.2.1.4.20.1.3')),	# ipAdEntNetMask
                                  lexicographicMode=False):
            if errorIndication:
                print(errorIndication)
                break
            elif errorStatus:
                print('%s at %s' % (errorStatus.prettyPrint(),
                                    errorIndex and varBinds[int(errorIndex)-1][0] or '?'))
                break
            else:
                ipAdEntAddr = [x.prettyPrint() for x in varBinds[0]][1]
                ipAdEntifindex = [x.prettyPrint() for x in varBinds[1]][1]
                ipAdEntNetMask = [x.prettyPrint() for x in varBinds[2]][1]
                card_dict[ipAdEntifindex]["ipAdentAddr"]=ipAdEntAddr
                card_dict[ipAdEntifindex]["ipAdEntNetMask"]=ipAdEntNetMask
        #print(card_dict)
        return card_dict







    # 存储 windows linux 通用   # 虚拟内存 ，内存  硬盘 |占用率，空间大小
    def storage_collect(self):
        community=self.community; protocol=self.protocol; host=self.host; port=self.port
        storage_dict = {}
        for (errorIndication,
             errorStatus,
             errorIndex,
             varBinds) in nextCmd(SnmpEngine(),
                                  CommunityData(community, mpModel=protocol),
                                  UdpTransportTarget((host, port)),
                                  ContextData(),
                                  ObjectType(ObjectIdentity('.1.3.6.1.2.1.25.2.3.1.1')), # 索引
                                  ObjectType(ObjectIdentity('.1.3.6.1.2.1.25.2.3.1.2')), # 类型
                                  ObjectType(ObjectIdentity('.1.3.6.1.2.1.25.2.3.1.3')), # 介绍
                                  ObjectType(ObjectIdentity('.1.3.6.1.2.1.25.2.3.1.4')), # 簇
                                  ObjectType(ObjectIdentity('.1.3.6.1.2.1.25.2.3.1.5')), # 大小（簇数量）
                                  ObjectType(ObjectIdentity('.1.3.6.1.2.1.25.2.3.1.6')), # 已用
                                  lexicographicMode=False):    

            if errorIndication:
                print(errorIndication)
                break
            elif errorStatus:
                print('%s at %s' % (errorStatus.prettyPrint(),
                                    errorIndex and varBinds[int(errorIndex)-1][0] or '?'))
                break
            else:
                ifindex = [x.prettyPrint() for x in varBinds[0]][1]
                ifType = [x.prettyPrint() for x in varBinds[1]][1]
                if ifType == '1.3.6.1.2.1.25.2.1.3':
                	ttype = "hrStorageVirtualMemory"		# 虚拟内存
                elif ifType == '1.3.6.1.2.1.25.2.1.2':
                	ttype = "hrStorageRam"					# 内存
                elif ifType == '1.3.6.1.2.1.25.2.1.4':
                	ttype = "hrStorgeFixedDisk"				# 硬盘
                elif ifType  == '1.3.6.1.2.1.25.2.1.5':
                	ttype = "hrStorageRemovableDisk"		# 可移动硬盘
                elif ifType == '1.3.6.1.2.1.25.2.1.6':
                	ttype = "hrStorageFloppyDisk"			# 软盘
                elif ifType == '1.3.6.1.2.1.25.2.1.7':
                	ttype = "hrStorageCompactDisc"			# 光盘
                elif ifType == '1.3.6.1.2.1.25.2.1.8':
                	ttype = "hrStorageRamDisk"				# 内存模拟的硬盘
                elif ifType == '1.3.6.1.2.1.25.2.1.9':
                	ttype = "hrStorageFlashMemory"			# 闪存卡
                elif ifType == '1.3.6.1.2.1.25.2.1.10':
                	ttype = "hrStorageNetworkDisk"			# 网络硬盘
                else:
                	ttype = "hrStorageOther"				# 其他
                ifDescr = [x.prettyPrint() for x in varBinds[2]][1]
                ifunits = [x.prettyPrint() for x in varBinds[3]][1]
                ifSize = [x.prettyPrint() for x in varBinds[4]][1]
                ifused = [x.prettyPrint() for x in varBinds[5]][1]    

                #print(ifindex)  #序号
                #print(ttype)	#类型
                if "0x" in ifDescr: 
                    y=bytearray.fromhex(ifDescr[2:])
                    ifDescr = y.decode("utf-8")
                #[lsl[::2][i] + lsl[1::2][i] for i in range(int(len(lsl)/2))]
                #print(ifDescr) # 描述（挂载处、盘符）
                #print(ifunits)
                #print(ifSize)
                #print(ifused)
                storage_dict[ifindex]={
                    "type":ttype,
                    "desc":ifDescr,
                    "units":ifunits,
                    "size":ifSize,
                    "used":ifused
                }
        return storage_dict


    # walk 
    # 通用 CPU 多核负载  # 核数，占用率
    def cpu_collect(self):
        community=self.community; protocol=self.protocol; host=self.host; port=self.port
        cpu_p = []
        for (errorIndication,
             errorStatus,
             errorIndex,
             varBinds) in nextCmd(SnmpEngine(),
                                  CommunityData(community, mpModel=protocol),
                                  UdpTransportTarget((host, port)),
                                  ContextData(),
                                  ObjectType(ObjectIdentity('.1.3.6.1.2.1.25.3.3.1.2')), #  每个核心 CPU%
                                  lexicographicMode=False):
            if errorIndication:
                print(errorIndication)
            else:
                cpu_per = [x.prettyPrint() for x in varBinds[0]][1]
                cpu_p.append(cpu_per)
        #print(cpu_p)
        return cpu_p
        # 计算并入库

    # get CPU linux # 停用，使用windows方法
    def linuxcpu_collect(self):
        community=self.community; protocol=self.protocol; host=self.host; port=self.port
        for (errorIndication,
             errorStatus,
             errorIndex,
             varBinds) in getCmd(SnmpEngine(),
                                  CommunityData(community, mpModel=protocol),
                                  UdpTransportTarget((host, port)),
                                  ContextData(),
                                  ObjectType(ObjectIdentity('.1.3.6.1.4.1.2021.11.9.0')), #  用户CPU%
                                  ObjectType(ObjectIdentity('.1.3.6.1.4.1.2021.11.10.0')),  # 系统CPU%
                                  ObjectType(ObjectIdentity('.1.3.6.1.4.1.2021.11.11.0')), # 空闲CPU%
                                  lexicographicMode=False):
            if errorIndication:
                print(errorIndication)
                break
            elif errorStatus:
                print('%s at %s' % (errorStatus.prettyPrint(),
                                    errorIndex and varBinds[int(errorIndex)-1][0] or '?'))
                break
            else:
                cpu_user = [x.prettyPrint() for x in varBinds[2]][1]
                cpu_sys = [x.prettyPrint() for x in varBinds[3]][1]
                cpu_idle = [x.prettyPrint() for x in varBinds[4]][1]
                print(cpu_user)
                print(cpu_sys)
                print(cpu_idle)
        # 计算占用，入库

    # 系统版本信息 get
    # windows linux 通用  系统，机器名，| 进程数，服务数，
    def sys_get(self):
        community=self.community; protocol=self.protocol; host=self.host; port=self.port
        for (errorIndication,
             errorStatus,
             errorIndex,
             varBinds) in getCmd(SnmpEngine(),
                                  CommunityData(community, mpModel=protocol),
                                  UdpTransportTarget((host, port)),
                                  ContextData(),
                                  ObjectType(ObjectIdentity('.1.3.6.1.2.1.1.1.0')), #sysDesc
                                  ObjectType(ObjectIdentity('.1.3.6.1.2.1.1.5.0')), #sysName
                                  lexicographicMode=False):
            if errorIndication:
                print(errorIndication)
                break
            elif errorStatus:
                print('%s at %s' % (errorStatus.prettyPrint(),
                                    errorIndex and varBinds[int(errorIndex)-1][0] or '?'))
                break
            else:
                sysDesc = [x.prettyPrint() for x in varBinds[0]][1]
                sysName = [x.prettyPrint() for x in varBinds[1]][1]
                # do update sysName and system info
                #
                return sysDesc


    # 内存大小 windows linux 通用 
    def memery_get(self):
        community=self.community; protocol=self.protocol; host=self.host; port=self.port
        for (errorIndication,
             errorStatus,
             errorIndex,
             varBinds) in getCmd(SnmpEngine(),
                                  CommunityData(community, mpModel=protocol),
                                  UdpTransportTarget((host, port)),
                                  ContextData(),
                                  ObjectType(ObjectIdentity('.1.3.6.1.2.1.25.2.2.0')), #sysDesc
                                  lexicographicMode=False):
            if errorIndication:
                print(errorIndication)
                break
            elif errorStatus:
                print('%s at %s' % (errorStatus.prettyPrint(),
                                    errorIndex and varBinds[int(errorIndex)-1][0] or '?'))
                break
            else:
                para = [x.prettyPrint() for x in varBinds[0]][1]
                print(para)


    def test(self):
        community=self.community; protocol=self.protocol; host=self.host; port=self.port
        for (errorIndication,
             errorStatus,
             errorIndex,
             varBinds) in getCmd(SnmpEngine(),
                                  CommunityData(community, mpModel=protocol),
                                  UdpTransportTarget((host, port)),
                                  ContextData(),
                                  ObjectType(ObjectIdentity('.1.3.6.1.2.1.25.2.2.0')), #sysDesc
                                  lexicographicMode=False):
            if errorIndication:
                print(errorIndication)
                break
            elif errorStatus:
                print('%s at %s' % (errorStatus.prettyPrint(),
                                    errorIndex and varBinds[int(errorIndex)-1][0] or '?'))
                break
            else:
                para = [x.prettyPrint() for x in varBinds[0]][1]
                print(para)

    def main(self):
    	# 系统探测
        system = self.sys_get()
        # 通用存储探测（内存硬盘等）
        self.storage_collect()
        # 通用网卡探测
        self.inet_collect()
        # CPU信息探测
        self.cpu_collect()
        # 其他需区分系统的检测
        if "indows" in system:
            print("windows")
        elif "inux" in system:
            print("linux")

