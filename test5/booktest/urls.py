from django.conf.urls import url
from booktest import views

urlpatterns = [
    url(r'^index$', views.index),
    url(r'^inherit$', views.inherit),
    url(r'^login$', views.login),
    url(r'^login_check$', views.login_check),
    url(r'^change_psw$', views.change_psw),
    url(r'^change_psw_action$', views.change_psw_action),
    url(r'^verify_code$', views.verify_code),
	url(r'^static_test$', views.static_test),
	url(r'^upload_pic$', views.upload_pic),				#上传图片
	url(r'^upload_handle$', views.upload_handle),		#处理上传的图片
    url(r'^show_area(?P<pindex>\d*)', views.show_area),	#显示地区名字,传给视图要看第几页page
	url(r'^area_choose$', views.area_choose),
	url(r'^prov$', views.prov),				#ajax请求获取的jsonresponse发送的数据
]
