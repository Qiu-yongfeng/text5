from django.contrib import admin
from booktest.models import AreaInfo,PicTest	#导入模型
# Register your models here.

'''模型管理类'''
class AreaInfoAdmin(admin.ModelAdmin):
	list_per_page = 20	#定义每页显示的条数
	list_display = ['id', 'aname', 'title', 'parent']	#可以是函数对象
	actions_on_top = False		#关闭顶部的动作栏
	actions_on_bottom = True	#打开顶部的动作栏
	list_filter = ['aname']		#增加过滤栏（比如以aname）
	search_fields = ['aname']	#增加搜索栏

'''注册'''
admin.site.register(AreaInfo, AreaInfoAdmin)
admin.site.register(PicTest)
