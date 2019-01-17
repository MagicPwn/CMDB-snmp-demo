from django.shortcuts import render
from .DataCollect import DataCollect
from . import models
from django.http import HttpResponse
# Create your views here.
# ajax 更新 任务执行情况
def storage_save(storages, server):
	for k,v in storages.items():
		typeof = v['type']
		desc = v['desc']
		units = int(v['units'])
		size = int(v['size'])
		used = int(v['used'])
		if size ==0:
			used = 0
			size = 1
		if typeof == 'hrStorageRam' or typeof == 'hrStorageVirtualMemory': # 内存
			has = models.Memory.objects.filter(slot=k,server_obj=server)
			if has:
				has.update(desc=desc, model=typeof, capacity= units*size,used=units*used,persent=used/size)
			else:
				models.Memory.objects.create(slot=k,desc=desc, model=typeof, capacity= units*size,used=units*used,persent=used/size,server_obj=server)
		else:
			has = models.Disk.objects.filter(slot=k,server_obj=server)
			if has:
				has.update(desc=desc, model=typeof, capacity= units*size,used=units*used,persent=used/size)
			else:
				models.Disk.objects.create(slot=k, desc=desc,  model=typeof, capacity= units*size,used=units*used,persent=used/size,server_obj=server)

#'ifPhysAddress': '', 'ipAdentAddr': '127.0.0.1', 'ipAdEntNetMask': '255.0.0.0'

def ifnets_save(ifnets, server):
	for k,v in ifnets.items():
		ifName = v['ifName']
		ifType = v['ifType']
		ifDesc = v['ifDescr']
		ifMtu = v['ifMtu']
		ifSpeed = v['ifSpeed']
		ifPhysAddress = v['ifPhysAddress']
		ipAdentAddr = v['ipAdentAddr']
		ipAdEntNetMask = v['ipAdEntNetMask']
		has = models.NIC.objects.filter(name=ifName,server_obj=server)
		if has:
			has.update(ifDesc=ifDesc,  hwAddr=ifPhysAddress, ipAddr= ipAdentAddr,netmask= ipAdEntNetMask,ifType=ifType,ifMtu=ifMtu,ifSpeed=ifSpeed)
		else:
			models.NIC.objects.create(name=ifName,ifDesc=ifDesc,  hwAddr=ifPhysAddress, ipAddr= ipAdentAddr,netmask= ipAdEntNetMask,ifType=ifType,ifMtu=ifMtu,ifSpeed=ifSpeed,server_obj=server)


def cpu_save(cpus, server):
	count = len(cpus)
	addup = 0
	for i in cpus:
		addup += float(i)
	persent = addup/count
	has = models.CPU.objects.filter(server_obj=server)
	if has:
		has.update(core= count, percent= persent)
	else:
		models.CPU.objects.create(core= count, percent= persent, server_obj=server)


def on_watch(request):
	# 获取所有主机
	# 遍历主机信息 使用DC搜集信息入库
	# 数据传回 再此方法内保存到数据库
	servers = models.Server.objects.all()
	if len(servers)>0:
		for ser in servers:
			ip = ser.manage_ip
			print(ip)
			dc = DataCollect(host=ip)
			#system = dc.sys_get()
			# 通用存储探测（内存硬盘等）
			storages = dc.storage_collect()
			storage_save(storages, ser)
			# 通用网卡探测
			ifnets = dc.inet_collect()
			ifnets_save(ifnets, ser)
			# CPU信息探测
			cpus = dc.cpu_collect()
			cpu_save(cpus, ser)


	response = HttpResponse()
	response.write("OK")
	return response