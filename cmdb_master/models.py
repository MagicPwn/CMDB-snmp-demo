from django.db import models

# Create your models here.



# 用户信息
class UserProfile(models.Model):
	name = models.CharField(u'姓名', max_length=32)
	email = models.EmailField(u'邮箱')
	phone = models.CharField(u'座机', max_length=32)
	mobile = models.CharField(u'手机', max_length=32)

	class Meta:
		verbose_name_plural = "用户表"

	def __str__(self):
		return self.name



# 用户登录信息表
class AdminInfo(models.Model):
	user_info = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
	username = models.CharField(u'用户名', max_length=64)
	password = models.CharField(u'密码', max_length=64)

	class Meta:
		verbose_name_plural = "管理员表"

	def __str__(self):
		return self.user_info.name


# 用户组
class UserGroup(models.Model):
	name = models.CharField(max_length=32, unique=True)
	users = models.ManyToManyField(UserProfile)

	class Meta:
		verbose_name_plural = "用户组表"

	def __str__(self):
		return self.name


# 业务线
class BusinessUnit(models.Model):
	name = models.CharField('业务线', max_length=64, unique=True)
	group = models.ForeignKey(UserGroup, on_delete=models.CASCADE, null = True, blank = True, verbose_name='业务组', related_name='c')
	manager = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null = True, blank = True,  verbose_name='系统管理员', related_name='m')

	class Meta:
		verbose_name_plural = "业务线表"

	def __str__(self):
		return self.name


# 机房
class IDC(models.Model):
	name = models.CharField('机房', max_length=32)
	floor = models.IntegerField('楼层', default=1)

	class Meta:
		verbose_name_plural = "机房表"

	def __str__(self):
		return self.name

## 资产标签
#class Tag(models.Model):
#	name = models.CharField('标签', max_length=32)
#	desc = models.CharField('描述', null= True, blank= True, max_length=100)
#	class Meta:
#		verbose_name_plural = "标签表"
#

#	def __str__(self):
#		return self.name

## 资产标签
#class Tago(models.Model):
#	name = models.CharField('标签', max_length=32)
#	desc = models.CharField('描述', null= True, blank= True, max_length=100)
#	class Meta:
#		verbose_name_plural = "标签表"
#

#	def __str__(self):
#		return self.name

# 资产（硬件）所有资产公共信息（交换机，服务器，防火墙等）位置
class Asset(models.Model):
	device_type_choices = (
        (1, '服务器'),
        (2, '交换机'),
        (3, '防火墙'),
        (4, '路由器'),
        (5, 'IDS'),
        (6, 'IPS'),
        (7, 'WAF'),
        (8, '负载均衡'),
	)
	device_status_choices = (
        (1, '上架'),
        (2, '在线'),
        (3, '离线'),
        (4, '下架'),
    )

	device_type_id = models.IntegerField(choices=device_type_choices, default=1)
	device_status_id = models.IntegerField(choices=device_status_choices, default=1)

	cabinet_num = models.CharField('机柜号', max_length=30, null=True, blank=True)
	cabinet_order = models.CharField('机柜中序号', max_length=30, null=True, blank=True)

	idc = models.ForeignKey(IDC, on_delete=models.CASCADE, verbose_name='IDC机房', null=True, blank=True)
	business_unit = models.ForeignKey(BusinessUnit, on_delete=models.CASCADE, verbose_name='属于的业务线', null=True, blank=True)
	#tag = models.OneToManyField(Tago)
	latest_date = models.DateField(null=True)
	create_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name_plural = "资产表"

	def __str__(self):
		return "%s-%s-%s-%s" % (self.idc.name, self.cabinet_num, self.cabinet_order, self.device_type_choices[int(self.device_type_id)-1][1])


# 服务器
class Server(models.Model):
	s_v = (
		("1", "1"),
		("2", "2c"),
		('3', "3"),
		)
	asset = models.OneToOneField(Asset, on_delete=models.CASCADE,)

	hostname = models.CharField(max_length=128, unique=True)
	sn = models.CharField('SN号', max_length=64, db_index=True)
	manufacturer = models.CharField(verbose_name='制造商', max_length=64, null=True, blank=True)
	model = models.CharField('型号', max_length=64, null=True, blank=True)

	manage_ip = models.GenericIPAddressField('管理IP', null=True, blank=True)

	os_platform = models.CharField('系统', max_length=16, null=True, blank=True)
	os_version = models.CharField('系统版本', max_length=16, null=True, blank=True)

	cpu_count = models.IntegerField('CPU个数', null=True, blank=True)
	cpu_physical_count = models.IntegerField('CPU物理个数', null=True, blank=True)
	cpu_model = models.CharField('CPU型号', max_length=128, null=True, blank=True)

	create_at = models.DateTimeField(auto_now_add=True, blank=True)
	snmp_version = models.CharField('snmp版本', choices=s_v,  max_length=25, default= '2')
	snmp_community = models.CharField('Snmp团体名', max_length=128, default="public")
	auth_key = models.CharField('Snmp_authkey', max_length=128, null=True, blank=True)
	priv_key = models.CharField('snmp_privkey', max_length=128, null=True, blank=True)
	class Meta:
		verbose_name_plural = "服务器表"

	def __str__(self):
		return self.hostname


# 网络设备
class NetworkDevice(models.Model):
	s_v = (
		("1", "1"),
		("2", "2c"),
		('3', "3"),
		)
	asset = models.OneToOneField(Asset, on_delete=models.CASCADE,)
	management_ip = models.CharField('管理IP', max_length=64, blank=True, null=True)
	vlan_ip = models.CharField('VlanIP', max_length=64, blank=True, null=True)
	intranet_ip = models.CharField('内网IP', max_length=128, blank=True, null=True)
	sn = models.CharField('SN号', max_length=64, unique=True)
	manufacture = models.CharField(verbose_name=u'制造商', max_length=128, null=True, blank=True)
	model = models.CharField('型号', max_length=128, null=True, blank=True)
	port_num = models.SmallIntegerField('端口个数', null=True, blank=True)
	device_detail = models.CharField('设置详细配置', max_length=255, null=True, blank=True)
	snmp_version = models.CharField('snmp版本', choices=s_v, max_length=25, default= '2')
	snmp_community = models.CharField('Snmp团体名', max_length=128, default="public")
	auth_key = models.CharField('Snmp_authkey', max_length=128, null=True, blank=True)
	priv_key = models.CharField('snmp_privkey', max_length=128, null=True, blank=True)

	class Meta:
		verbose_name_plural = "网络设备"

# 硬盘
class CPU(models.Model):
	core = models.CharField('核心数', max_length=32)
	percent = models.IntegerField('占用',default = 192)
	server_obj = models.ForeignKey(Server,on_delete=models.CASCADE, related_name='CPU')

	class Meta:
		verbose_name_plural = "CPU负载"

	def __str__(self):
		return self.persent


# 硬盘
class Disk(models.Model):
	slot = models.CharField('插槽位', max_length=8)  #索引
	model = models.CharField('类型', null=True,blank=True, max_length=100)
	desc = models.CharField('介绍',null=True,blank=True,max_length=100)
#	bunch = models.CharField('簇', max_length=32)
#	bunchNum = models.CharField('大小', max_length=32)
	used= models.CharField('已用',null=True,blank=True,  max_length=32)
	capacity= models.CharField('总空间',null=True,blank=True,  max_length=32)
	persent = models.CharField('已用百分比',null=True,blank=True,  max_length=32)
	server_obj = models.ForeignKey(Server,on_delete=models.CASCADE, related_name='disk')

	class Meta:
		verbose_name_plural = "硬盘表"

	def __str__(self):
		return self.slot


# 网卡
class NIC(models.Model):
	name = models.CharField('网卡名称', max_length=128)
	ifDesc = models.CharField('描述',null=True,blank=True, max_length=128)
	hwAddr = models.CharField('网卡mac地址',null=True,blank=True, max_length=64)
	ipAddr = models.CharField('网卡IP地址',null=True,blank=True, max_length=64)
	netmask = models.CharField(max_length=64,null=True,blank=True,)
	ifType = models.CharField('类型',null=True,blank=True, max_length=256)
	ifMtu = models.CharField('MTU', null=True,blank=True, max_length=256)
	ifSpeed = models.CharField('速率',null=True,blank=True, max_length=256)
	up = models.BooleanField(default=True)
	server_obj = models.ForeignKey(Server, on_delete=models.CASCADE, related_name='nic')


	class Meta:
		verbose_name_plural = "网卡表"

	def __str__(self):
		return self.name


# 内存
class Memory(models.Model):
	slot = models.CharField('插槽位', max_length=32)  # 标号
	desc = models.CharField('介绍', max_length=32, null=True, blank=True)
	model = models.CharField('型号',null=True,blank=True, max_length=100)
	capacity = models.FloatField('容量', null=True, blank=True)
	used= models.CharField('已用',null=True,blank=True, max_length=32)
	persent = models.CharField('已用比例',null=True,blank=True, max_length=32)
	sn = models.CharField('内存SN号', max_length=64, null=True, blank=True)
	speed = models.CharField('速度', max_length=16, null=True, blank=True)

	server_obj = models.ForeignKey(Server, on_delete=models.CASCADE,related_name='memory')


	class Meta:
		verbose_name_plural = "内存表"

	def __str__(self):
		return self.slot


# 资产变更记录,creator为空时，表示是资产汇报的数据。
class AssetRecord(models.Model):
	asset_obj = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='ar')
	content = models.TextField(null=True)  # 新增硬盘
	creator = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True) #
	create_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name_plural = "资产记录表"

	def __str__(self):
		return "%s-%s-%s" % (self.asset_obj.idc.name, self.asset_obj.cabinet_num, self.asset_obj.cabinet_order)


# 错误日志,如：agent采集数据错误 或 运行错误
class ErrorLog(models.Model):
	asset_obj = models.ForeignKey(Asset, on_delete=models.CASCADE, null=True, blank=True)
	title = models.CharField(max_length=16)
	content = models.TextField()
	create_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name_plural = "错误日志表"

	def __str__(self):
		return self.title
