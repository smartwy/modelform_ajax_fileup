from django.shortcuts import render, HttpResponse
from django.forms import ModelForm
from django.forms import fields as Ffields
from app01 import models
from django.forms import widgets as bwidgets
from io import BytesIO
from utils.check_code import create_validate_code
import os
import time
import json


def home(request):
	return render(request, 'home.html')

class UModelForm(ModelForm):
	date = Ffields.CharField( # 额外定制字段
		widget = bwidgets.CheckboxInput(),
		label='两周免登陆:', # 在登陆成功设置cookie与session的缓存两周时间
		required=True,
	)
	class Meta:
		model = models.user_info
		fields = '__all__' # 全部字段
		# fields = ['username', 'email'] # 指定字段
		# exclude = ['email'] # 排除字段
		labels= {
			'username':'用户名',
			'email':'E妹儿',
			'usertype':'用户级别',
			'u2g':'部门',
		}
		widgets = {
			'username':bwidgets.TextInput(attrs={'calss':'c1', 'style':'color: red'}),
		}
		error_messages = {
			'email':  {
				'required':'邮箱不能为空！',
				'invalid':'邮箱格式错误！',
			}
		}

	def clean_username(self):  # 自定义验证，与form相同
		old = self.cleaned_data['username']
		if old == 'hack':
			return 'ABC'
		return old

def modelForm(request):
	if request.method == 'GET':
		obj = UModelForm()
		return render(request, 'mf.html', {'obj':obj})
	elif request.method == 'POST':
		obj = UModelForm(request.POST)
		if obj.is_valid():
			print(obj.cleaned_data['date'])
			obj.save() # 添加保存到数据库默认保存多对多，obj.save(commit=False):不做任何操作，保存需再执行：obj.save()和obj.save_m2m()对单表与多对多保存
			# obj.save(commit=False)
			# obj.save() # 保存单表
			# obj.save_m2m() # 保存多对多
			return render(request, 'mf.html', {'obj': obj, 'mes':'添加成功！'})
		else:
			print(obj.errors.as_json())
		return render(request, 'mf.html', {'obj':obj})

def ulist(request):
	li = models.user_info.objects.all().select_related('usertype')
	ll = models.user_info.objects.all().prefetch_related('u2g')
	return render(request, 'ulist.html', {'li':li, 'll':ll})

def edit(request, nid):
	obj = models.user_info.objects.get(id=nid)
	if request.method == 'GET':
		gobj = UModelForm(instance=obj) # 根据传入的querySet数据初始化
		# gobj = UModelForm(initial={'username':'单纯初始化'}) # 根据传入的字典初始化
		return render(request, 'edit.html', {'gobj':gobj, 'nid':nid})
	elif request.method == 'POST':
		mobj = UModelForm(request.POST, instance=obj) # 更新instance=obj根据传入的POST数据
		if mobj.is_valid():
			mobj.save() # 保存
			return HttpResponse('OK')
		else:
			gobj = UModelForm(instance=obj)
		return render(request, 'edit.html', {'gobj': gobj, 'nid':nid, 'err':'某项填写不对！'})

def ajax(request):
	# n = request.GET.get('name')
	# p = request.GET.get('pwd')
	# print(n, p)
	return render(request, 'ajax.html')

def ajax_json(request):
	# print(request.POST)
	ret = {'low-name':request.POST.get('username'), 'low-email':request.POST.get('email')}
	import json
	return HttpResponse(json.dumps(ret))

def upload(request):

	return render(request, 'upload.html')

def upload_f(request):
	fd = request.FILES.get('filename')
	u = request.POST.get('username')
	file_path = os.path.join('static/imgs/', fd.name) # 静态文件放在特定的目录下，setting.py有设置
	ret = {'status':'Success', 'data':file_path}
	with open(file_path, 'wb') as file:
		for item in fd.chunks():
			file.write(item)
	import json
	return HttpResponse(json.dumps(ret)) # 字典转字符串

def check_code(request):
	stream = BytesIO() # 开辟内存对象
	img, code = create_validate_code() # 调用函数返回图片与随机字符串
	img.save(stream, 'PNG')
	request.session['CheckCode'] = code # 写入session
	return HttpResponse(stream.getvalue()) # 从内存中获取返回给用户

def ulogin(request):
	if request.method == 'GET':
		return render(request, 'ulogin.html')
	else:
		n = request.POST.get('name')
		p = request.POST.get('pwd')
		code = request.POST.get('check_code')
		if code.upper() == request.session['CheckCode'].upper():
			return render(request, 'kind.html')
			# return render(request, 'ulogin.html', {'mes':'图片验证测试成功'})
		else:

			return render(request, 'ulogin.html', {'mes': '图片验证测试失败'})

def kind(request):
	print(request.POST)
	return render(request, 'kind.html')

def upload_img(request):
	# print(request.POST.get('localUrl'))
	print(request.POST)
	print(request.FILES)
	fd = request.FILES.get('imgFile')
	img_path = os.path.join('static/imgs/', fd.name)
	with open(img_path, 'wb') as f:
		for item in fd.chunks():
			f.write(item)
	dic = {
		'error':0,
		'url':"/" + img_path, # 必须加/，否则会去/kind/下的static下找图片
		'message':'qq7',
	}
	return HttpResponse(json.dumps(dic))

def file_manager(request):
	"""
    文件管理 获取目录与文件信息，按照指定的格式返回
    :param request:
    :return:
    {
        moveup_dir_path: # 上一级目录
        current_dir_path: # 当前目录
        current_url:
        file_list: [ # 当前目录文件列表
            {
                'is_dir': True, # 是否是目录
                'has_file': True, # 当前目录是否有文件
                'filesize': 0, # 文件大小
                'dir_path': '', # 目录路径
                'is_photo': False, # 是否是图片
                'filetype': '', # 文件类型
                'filename': xxx.png, # 文件名称
                'datetime': time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(os.path.getctime(abs_item_path)))
            },
            {
                'is_dir': True,
                'has_file': True,
                'filesize': 0,
                'dir_path': '',
                'is_photo': False,
                'filetype': '',
                'filename': xxx.png,
                'datetime': time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(os.path.getctime(abs_item_path)))
            }
        ]

    }
    """
	dic = {}
	root_path = r'E:/python_project_dir/modelform_ajax_fileup/static/imgs/'
	static_root_path = '/static/imgs/'
	request_path = request.GET.get('path')
	if request_path:
		abs_current_dir_path = os.path.join(root_path, request_path)
		move_up_dir_path = os.path.dirname(request_path.rstrip('/'))
		dic['moveup_dir_path'] = move_up_dir_path + '/' if move_up_dir_path else move_up_dir_path

	else:
		abs_current_dir_path = root_path
		dic['moveup_dir_path'] = ''

	dic['current_dir_path'] = request_path
	dic['current_url'] = os.path.join(static_root_path, request_path)

	file_list = []
	for item in os.listdir(abs_current_dir_path):
		abs_item_path = os.path.join(abs_current_dir_path, item)
		a, exts = os.path.splitext(item)
		is_dir = os.path.isdir(abs_item_path)
		if is_dir: # 目录的返回信息
			temp = {
				'is_dir': True,
				'has_file': True,
				'filesize': 0,
                'dir_path': '',
                'is_photo': False,
                'filetype': '',
                'filename': item,
                'datetime': time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(os.path.getctime(abs_item_path)))
            }
		else:
			temp = { # 图片的返回信息
                'is_dir': False,
                'has_file': False,
                'filesize': os.stat(abs_item_path).st_size,
                'dir_path': '',
                'is_photo': True if exts.lower() in ['.jpg', '.png', '.jpeg'] else False,
                'filetype': exts.lower().strip('.'),
                'filename': item,
                'datetime': time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(os.path.getctime(abs_item_path)))
            }

		file_list.append(temp)
	dic['file_list'] = file_list
	return HttpResponse(json.dumps(dic))
