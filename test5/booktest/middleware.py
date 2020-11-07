from django.http import HttpResponse


'''中间件，在执行views函数之前先执行该类中的函数'''
'''该中间件类要在setting中注册'''
class ForbiddenIpMiddleware(object):
	ip_list = []
	def process_view(self, request, view_func, *view_args, **view_kwargs):
		user_ip = request.META['REMOTE_ADDR']
		if user_ip in ForbiddenIpMiddleware.ip_list:
			return HttpResponse('FORBIDDEN')


class TestMiddleware(object):
	def __init__(self):
		"""服务器启动后接受第一个请求后调用__init__()"""
		print('__init__')

	def process_request(self, request):
		"""浏览器发起请求后，服务器生成一个request对象保存提交的内容，然后讲request传入process——request()
		   中执行该函数，然后在执行url的匹配"""
		print('---process_request---')

	def process_view(self, request, view_func, *view_args, **view_kwargs):
		'''执行URL匹配后，将url和request传入执行该函数，在执行对应的视图函数'''
		print('---process_view---')

	def process_response(self, request, response):
		'''执行对应的视图函数后执行process_response（），在返回给浏览器'''
		print('---process_response---')
		return response