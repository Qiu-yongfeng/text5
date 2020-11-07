from django.db import models

# Create your models here.
class BookInfo(models.Model):
	bname = models.CharField(max_length=40)
	bpub_date = models.DateField()
	bread = models.IntegerField(default=0)
	bcomment = models.IntegerField(default=0)
	isDelete = models.BooleanField(default=False)

	class Meta():
		"""元选项,指定该类对应的数据表"""
		db_table = 'bookinfo'


class AreaInfo(models.Model):
	aname = models.CharField(verbose_name='标题', max_length=20)		#verbose_name='标题'更改在管理页面中的字段名
	aParent = models.ForeignKey('self', null=True, blank=True)	#自关联，允许为空，后台允许为空
	
	def __str__(self):
		"""返回要返回的字段"""
		return self.aname

	"""可以传递给list_display"""
	def title(self):
		return self.aname
	title.admin_order_field = 'aname'	#给在admin中list_display中的属性增加以xxx排序的功能
	title.short_description = '地区'		#给标题栏改名

	def parent(self):
		if self.aParent is None:
			return ''
		else:
			return self.aParent.aname
	parent.admin_order_field = 'aname'
	parent.short_description = '父级地区'


class PicTest(models.Model):
	goods_pic = models.ImageField(upload_to='booktest')		#指定上传位置，相对于media中的路劲