from django.contrib import admin

# Register your models here.
# 在users下面创建adminx.py
import xadmin

from .models import EmailVerifyecord, Banner
from xadmin import views

# xadmin中这里继承object ，不是继承admin
# 创建 xadmin的最基本管理器配置，并与view绑定


class BaseSetting(object):
    # 开启主题功能
    enable_themes = True
    use_bootswatch = True
# 将基本配置管理与view绑定


xadmin.site.register(views.BaseAdminView,BaseSetting)


# 全局修改，固定写法
class GlobalSettings(object):
    # 修改title
    site_title = '阿钰后台管理界面'
    # 修改footer
    site_footer = '阿钰的公司'
    # 收起菜单
    menu_style = 'accordion'

    # 将title和footer信息进行注册


xadmin.site.register(views.CommAdminView, GlobalSettings)



class EmailVerifyRecordAdmin(object):
    # 显示的列
    list_display = ['code','email','send_type','send_time']
    # 搜索的地址段，不要添加时间搜索
    search_fields = ['code', 'email', 'send_type']
    # 过滤
    list_filter = ['code', 'email', 'send_type','send_time']


class BannerAdmin(object):
    list_display = ['title','image','url','index','add_time']
    search_fields = ['title', 'image', 'url', 'index']
    list_filter = ['title','image', 'url', 'index', 'add_time']


# 注册到总admin中，把写好的EmailVerifyecord和引入EmailVerifyRecordAdmin注册到当中
xadmin.site.register(EmailVerifyecord,EmailVerifyRecordAdmin)
xadmin.site.register(Banner,BannerAdmin)