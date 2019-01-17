# Register your models here.
from __future__ import absolute_import
# from .models import *
#from .resources import *
import xadmin
from xadmin import views
from import_export.admin import ImportExportModelAdmin, ImportExportActionModelAdmin
from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side
from xadmin.plugins.inline import Inline
from xadmin.plugins.batch import BatchChangeAction
from xadmin.plugins.actions import BaseActionView
from .models import *

import datetime
import random
from django.http import HttpResponseRedirect



@xadmin.sites.register(views.BaseAdminView)
class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


@xadmin.sites.register(views.CommAdminView)
class GlobalSetting(object):
    global_models_icon = {
    }
    # todo
    site_title = "CMDB测试系统"
    site_footer = "易霖博"
    menu_style = "accordion"

    # 菜单设置
    def get_site_menu(self):
        return (
            {'title': '人员管理',  'menus': (
                {'title': '用户信息', 'icon': 'fa fa-stack-overflow'
                    , 'url': self.get_model_url(UserProfile, 'changelist')},
                {'title': '用户组信息', 'icon': 'fa fa-stack-overflow'
                    , 'url': self.get_model_url(UserGroup, 'changelist')},
                {'title': '业务线', 'icon': 'fa fa-stack-overflow'
                    , 'url': self.get_model_url(BusinessUnit, 'changelist')},
                )},
            {'title': '资产管理', 'menus': (
                {'title': '机房', 'icon': 'fa fa-stack-overflow'
                    , 'url': self.get_model_url(IDC, 'changelist')},
                {'title': '设备', 'icon': 'fa fa-stack-overflow'
                    , 'url': self.get_model_url(Asset, 'changelist')},
                {'title': '服务器', 'icon': 'fa fa-stack-overflow'
                    , 'url': self.get_model_url(Server, 'changelist')},
                {'title': '网络设备', 'icon': 'fa fa-stack-overflow'
                    , 'url': self.get_model_url(NetworkDevice, 'changelist')},
                {'title': '硬盘', 'icon': 'fa fa-stack-overflow'
                    , 'url': self.get_model_url(Disk, 'changelist')},
                {'title': '网卡', 'icon': 'fa fa-stack-overflow'
                    , 'url': self.get_model_url(NIC, 'changelist')},
                {'title': '内存', 'icon': 'fa fa-stack-overflow'
                    , 'url': self.get_model_url(Memory, 'changelist')},
                {'title': 'CPU', 'icon': 'fa fa-stack-overflow'
                    , 'url': self.get_model_url(CPU, 'changelist')},
            )},
        )


    
@xadmin.sites.register(UserProfile)
class UserProfile_admin(object):
    list_display = ["name", "email", "phone", "mobile"]
    

@xadmin.sites.register(UserGroup)
class UserGroup_admin(object):
    list_display = ("name", "users")
    
    
@xadmin.sites.register(BusinessUnit)
class BusinessUnit_admin(object):
    list_display = ("name", "group", "manager")
    

@xadmin.sites.register(IDC)
class IDC_admin(object):
    list_display = ("name", "floor")

#@xadmin.sites.register(Tag)
#class Tag_admin(object):
#   list_display = ("name")

@xadmin.sites.register(Asset)
class Asset_admin(object):
    list_display = ("device_type_id", "device_status_id", "cabinet_num", "cabinet_order", "idc", "business_unit", "latest_date", "create_at")



class ImoprtEventAction(BaseActionView):
    action_name = "监控启动"    #: 相当于这个 Action 的唯一标示, 尽量用比较针对性的名字
    description = u'监控启动'  #: 描述, 出现在 Action 菜单中, 可以使用 ``%(verbose_name_plural)s`` 代替 Model 的名字.
    model_perm = 'change'    #: 该 Action 所需权限

    def do_action(self, queryset):
        # queryset 是包含了已经选择的数据的 queryset
        # 跳转到  autoexploit/file/choice/
        return HttpResponseRedirect("/cmdb/on_watch")


@xadmin.sites.register(Server)
class Server_admin(object):
    list_display = ("asset", "hostname", "model", "manage_ip","snmp_version","snmp_community")
    actions = [ImoprtEventAction, ]  # 导入事件
    





@xadmin.sites.register(NetworkDevice)
class NetworkDevice_admin(object):
    list_display = ("asset", "management_ip", "vlan_ip", "intranet_ip", "model", "port_num", "snmp_version","snmp_community")

@xadmin.sites.register(Disk)
class Disk_admin(object):
    list_display = ("slot","desc", "model", "used","capacity",  "persent", "server_obj")


@xadmin.sites.register(NIC)
class NIC_admin(object):
    list_display = ("name","ifDesc","ifType", "hwAddr", "ipAddr","netmask", "ifMtu","ifSpeed", "up","server_obj")


@xadmin.sites.register(Memory)
class Memory_admin(object):
    list_display = ("slot", "desc", "model","used", "capacity","persent" , "server_obj")

@xadmin.sites.register(CPU)
class CPU_admin(object):
    list_display = ( "server_obj","core", "percent")
