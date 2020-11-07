from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.template import loader,RequestContext
from booktest.models import BookInfo,PicTest,AreaInfo
from PIL import Image, ImageDraw, ImageFont		#验证码生成
from django.utils.six import BytesIO	#内存空间
from django.conf import settings

# Create your views here.
def my_render(request, template_path, context={}):
	#1.获取模板文件，生成模板对象
	temp = loader.get_template(template_path)
	#2.定义模板上下文，给模板传输数据
	context = RequestContext(request, context)
	#3.模板渲染，生成一个替换后的html文件
	response = temp.render(context)
	return HttpResponse(response)

"""禁止默写IP访问"""
def forbidon_ip(func):
	ip_list = []
	def forbid(request, *args, **kwargs):
		user_ip = request.META['REMOTE_ADDR']
		if user_ip in ip_list:
			return HttpResponse('404')
		else:
			return func(request, *args, **kwargs)
	return forbid

#@forbidon_ip
def index(request):
	print('---index---')  #检查中间件
	bookinfo = BookInfo.objects.get(id=1)
	books = BookInfo.objects.all()
	context = {'bookinfo':bookinfo, 'list1': [1,2,3], 'dict1':{'1':'haha', '2':'xixi'},'books':books}
	return my_render(request, 'booktest/index.html', context)

def inherit(request):
	return my_render(request, 'booktest/child.html')

def login(request):
	if request.session.has_key('islogin'):
		return redirect('/index')
	else:
		if 'username' in request.COOKIES:
			username = request.COOKIES['username']
		else:
			username = ''
		return my_render(request, 'booktest/login.html', {'username': username})

def login_check(request):
	"""该视图有login.html中的button触发"""
	username = request.POST.get('账户')		#index.html中的post提交中看
	password = request.POST.get('密码')
	remember = request.POST.get('remember')

	#verify
	verify1 = request.session.get('verifycode')
	verify2 = request.POST.get('verify')

	# print(verify1,verify2)
	if verify1 != verify2:
		return redirect('/login')

	if username == 'qiuyf' and password == '1111':
		if remember == 'on':
			response =redirect('/index')
			response.set_cookie('username', username, max_age=14*24*3600)
			request.session['islogin'] = True	#设置session
			request.session['username'] = username
			return response
		else:
			return redirect('/index')
	else:
		return redirect('/login')	

def login_required(func):
	def judge(request, *args, **kwargs):
		#判断是否已经登录
		if request.session.has_key('islogin'):
			"""执行我传进来的函数func"""
			return func(request, *args, **kwargs)
		else:
			"""没登录，直接转到登录界面"""
			return redirect('/login')
	return judge

@login_required
def change_psw(request):
	return my_render(request, 'booktest/change_psw.html')

@login_required
def change_psw_action(request):
	#1.获取修改的新密码
	psw = request.POST.get('psw')
	username = request.session['username']
	#2.修改对应数据库的内容
	#3.返回应答
	return HttpResponse('已完成用户%s的新密码修改：%s' %(username,psw))

#验证码的生成
def verify_code(request):
    #引入随机函数模块
    import random
    #定义变量，用于画面的背景色、宽、高
    bgcolor = (random.randrange(20, 100), random.randrange(
        20, 100), 255)
    width = 100
    height = 25
    #创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    #创建画笔对象
    draw = ImageDraw.Draw(im)
    #调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    #定义验证码的备选值
    str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    #随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    #构造字体对象，ubuntu的字体路径为“/usr/share/fonts/truetype/freefont”
    font = ImageFont.truetype('FreeMono.ttf', 23)
    #构造字体颜色
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    #绘制4个字
    draw.text((5, 2), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, 2), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, 2), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, 2), rand_str[3], font=font, fill=fontcolor)
    #释放画笔
    del draw
    #存入session，用于做进一步验证
    request.session['verifycode'] = rand_str
    #内存文件操作
    buf = BytesIO()
    #将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    #将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')

def static_test(request):
	return my_render(request, 'booktest/static_test.html')

def upload_pic(request):
	return my_render(request, 'booktest/upload_pic.html')

def upload_handle(request):
	#1.获取上传的图片
	#当上传的文件大小小于2.5m，保存在内存中，所以类型是；大于的话写入临时文件中
	pic = request.FILES['pic']

	#2.创建一个文件保存
	#pic.chunk()	将文件分块
	#pic_name = pic.name
	save_path = "%s/booktest/%s"%(settings.MEDIA_ROOT,pic.name)
	for content in pic.chunks():
		#3.获取上传文件的内容并写入到创建的文件
		with open(save_path, "wb") as f:
			f.write(content)
	
	#4.在数据库中上传记录
	PicTest.objects.create(goods_pic = "booktest/%s"%pic.name)

	#5.返回
	return HttpResponse('OK')

#导入paginator模块用于分页处理
from django.core.paginator import Paginator
def show_area(request, pindex):
	"""
		Page类实例对象
	调用Paginator对象的page()方法返回Page对象，不需要手动构造。
	属性object_list：返回当前页对象的列表。
	属性number：返回当前是第几页，从1开始。
	属性paginator：当前页对应的Paginator对象。
	方法has_next()：如果有下一页返回True。
	方法has_previous()：如果有上一页返回True。
	方法len()：返回当前页面对象的个数。
	"""
	areas = AreaInfo.objects.filter(aParent__isnull=True)	#获得地区名字
	paginator = Paginator(areas, 10)	#生成paginator对象
	if pindex == '':
		pindex = 1
	else:
		pindex = int(pindex)
	page = paginator.page(pindex)	#返回第pindex面,url捕获的变量都是字符串 
	return my_render(request, "booktest/show_area.html", {'page':page})

def area_choose(request):
	return my_render(request, 'booktest/area_choose.html')

def prov(request):
	#1.获取省级信息
	areas = AreaInfo.objects.filter(aParent__isnull=True)

	#2.{data:'areas'}并不是jsaon格式，所以要自己拼接出一个json文件
	area_list = []
	for area in areas:
		area_list.append((area.id,area.aname))

	#3.返回ajax请求的json信息
	return JsonResponse({'data':area_list})	#data给了area_choose中的11行