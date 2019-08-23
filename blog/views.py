import hashlib
import json
import urllib.request
from django.db.models import Q
import uuid
from datetime import datetime
from django.core.cache import cache
from django.core.mail import send_mail, EmailMultiAlternatives
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.template import loader, Context
from django.urls import reverse
from blog.VerifyCode import VerfiyCode
from blog.models import User, selfboke, talk, drafts, classify
from Bloger import settings

def personal(request):
    datas={

    }
    userid = request.session.get('user_id')
    uu = User.objects.get(id=userid)
    blogs = uu.us.all()
    blogs=paging(request,blogs,8)
    lens=len(blogs)
    user_id=request.session.get('user_id')
    datas['user_id'] = user_id
    datas['blogs']=blogs
    datas['lens'] = lens
    return render(request,'personal.html',context=datas)

def cancel_collect(request):
    user_id = request.GET.get('user_id')
    blog_id = request.GET.get('blog_id')
    s = User.objects.get(id=user_id)
    c = selfboke.objects.filter(id=blog_id)
    s.us.remove(*c)
    return redirect(reverse('blog:personal'))


def collects(request):
    user_id = request.GET.get('user_id')
    blog_id = request.GET.get('blog_id')
    #取出判断是否收藏过
    user=User.objects.filter(id=user_id).first()
    articl=selfboke.objects.filter(id=blog_id)
    users=articl.first().user_set.all()
    if user in users:
        return JsonResponse({'msg': 'no'})
    user.us.add(*articl)
    return JsonResponse({'msg':'ok'})


def index(request,num='1'):
    datas = {
        'title': 'Jenkins测试',
    }
    kinds=classify.objects.all()
    userid = request.session.get('user_id')
    users = User.objects.filter(pk=userid)

    # 根据博客like_num排序
    article_list = selfboke.objects.filter(del_tag=0).order_by('-like_num').all()
    top_article = selfboke.objects.filter(del_tag=0).filter(draft_tag=1)
    # 创建分页器   查询集, 每页显示的条数
    paginator = Paginator(article_list, 12)
    # print(paginator.count,paginator.page_range)

    # 创建分页对象            - page(num) 返回page对象 如果给定的页码不存在 则抛出异常
    current = int(num)

    page = paginator.page(current)
    # print(page.number,page.object_list)

    # 自定义页码范围　
    if paginator.num_pages > 10:
        # 　如果当前页码减去5小于0
        if current - 5 <= 0:
            customRange = range(1, 11)
        elif current + 5 > paginator.num_pages:
            customRange = range(paginator.num_pages - 9, paginator.num_pages + 1)
        else:
            customRange = range(current - 5, current + 5)
    else:
        customRange = paginator.page_range

    datas['one_page'] = page.object_list
    datas['pagerange'] = customRange
    datas['page'] = page
    if users.exists():
        user = users.first()
        datas['username'] = user.username
        datas['icon'] = '/static/uploadfiles/' + user.icon.url
        datas['is_login'] = True
        datas['user_tag']=user.user_tag
        #置顶的文章
        datas['top_article'] = top_article
        # 取前5排行榜
        datas['article_list'] = article_list[:5]
        #取出所有的分类
        datas['kinds'] = kinds
        return render(request, 'index.html', context=datas)

    datas['one_page'] = page.object_list
    datas['pagerange'] = customRange
    datas['page'] = page

    datas['is_login'] = False
    # 置顶的文章
    datas['top_article'] = top_article
    # 取前5排行榜
    datas['article_list'] = article_list[:5]
    # 取出所有的分类
    datas['kinds'] = kinds
    return render(request, 'index.html', context=datas)

#找的json接口拿的动态数据填到首页
def json_data():
    response=urllib.request.urlopen('https://www.vmovier.com/apiv3/post/getPostInCate?cateid=0&p=1')
    info=response.read().decode('utf-8')
    temp=json.loads(info)
    data=temp['data']
    return data

# #分页
# def userlist(request,num='1'):
#     # 取出所有未删除的文章并根据博客like_num排序
#     article_list = selfboke.objects.filter(del_tag=0).order_by('-like_num')
#
#     # 创建分页器   查询集, 每页显示的条数
#     paginator = Paginator(article_list,3)
#     # print(paginator.count,paginator.page_range)
#
#     # 创建分页对象            - page(num) 返回page对象 如果给定的页码不存在 则抛出异常
#     current = int(num)
#
#     page = paginator.page(current)
#     # print(page.number,page.object_list)
#
#     # 自定义页码范围　
#     if paginator.num_pages > 10:
#         #　如果当前页码减去5小于0
#         if current - 5 <=0:
#             customRange = range(1,11)
#         elif current + 5 > paginator.num_pages:
#             customRange = range( paginator.num_pages - 9,paginator.num_pages + 1)
#         else:
#             customRange = range(current - 5,current + 5)
#     else:
#         customRange = paginator.page_range
#     dic = {
#         'data':page.object_list,    #   object_list 当前页码上的所有数据
#         'pagerange':customRange,    #   页码范围
#         'page':page                 #   page对象具体负责每页的处理
#     }
#     return render(request,'blog/index.html',context=dic)


#个人页面
def about(request):
    userid = request.session.get('user_id')

    users = User.objects.filter(pk=userid)
    kinds = classify.objects.all()
    datas = {
        'kinds': kinds,
    }

    if users.exists():
        user = users.first()
        datas['username']=user.username

        return render(request,'about.html', context=datas)
    return redirect(reverse('blog:login'))


#
def share(request):
    userid = request.session.get('user_id')

    users = User.objects.filter(pk=userid)
    datas = {

    }
    if users.exists():
        user = users.first()
        datas['username'] = user.username

        return render(request, 'share.html', context=datas)
    return redirect(reverse('blog:login'))


#登录
def login(request):
    if request.method == "GET":
        return render(request, 'login.html')

    elif request.method == "POST":
        scode=request.session.get('scode')
        code=request.POST.get('code')
        username = request.POST.get('username')
        password = request.POST.get('password')
        users = User.objects.filter(username=username)
        if scode==code:
            if users.exists():
                user = users.first()
                if user.is_activite:
                    if user.password == make_pwd(password):
                        if user.is_activite==True:
                            request.session.set_expiry(0)
                            request.session['user_id'] = user.id
                            return redirect(reverse('blog:index'))

                        return render(request, 'notice.html', context={
                            'code': -1,
                            'msg': "用户未激活请前去邮箱激活，如未收到邮件可重新注册！",
                            'wait': 2,
                            'url': "/blog/login"
                        })
                    return render(request, 'notice.html', context={
                        'code': -1,
                        'msg': "用户名或密码输入错误",
                        'wait': 2,
                        'url': "/blog/login"
                    })
                return render(request, 'notice.html', context={
                    'code': -1,
                    'msg': "用户未激活，请先前去激活！",
                    'wait': 2,
                    'url': "/blog/login"
                })
            return render(request, 'notice.html', context={
                'code': -1,
                'msg': "用户不存在请确保用户名输入正确",
                'wait': 2,
                'url': "/blog/login"
            })
        return render(request, 'notice.html', context={
            'code': -1,
            'msg': "验证码错误",
            'wait': 2,
            'url': "/blog/login"
        })
    return HttpResponse("无效请求")

#密码加密
def make_pwd(password):
    md5 = hashlib.md5()
    md5.update(password.encode('utf-8'))
    return md5.hexdigest()
#画验证码
def vcode(request):

    vc = VerfiyCode()
    res = vc.output()
    # 将验证码字符串添加到ｓｅｓｓｉｏｎ
    request.session['scode'] = vc.code
    return HttpResponse(res,'image/png')

#退出
def loginout(request):
    request.session.flush()
    # return render(request, 'admin.html')
    return redirect(reverse('blog:index'))


def regist(request):
    if request.method == "GET":
        return render(request, 'regist.html')

    elif request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        icon = request.FILES.get('icon')

        users=User.objects.filter(username=username)
        # print(users)
        # print(type(users))
        if users.exists():
            #
            return render(request, 'notice.html', context={
                'code': -1,
                'msg': "用户名已存在",
                'wait': 2,
                'url': "/blog/regist"
            })
        user = User()
        user.username = username
        user.password = make_pwd(password)
        user.email = email
        user.icon = icon
        user.resgist_time=datetime.today().strftime("%Y/%m/%d/%H/%M/%S")
        request.session["user_id"] = user.id
        request.session["user_name"] = user.username


        #生成token
        token = str(uuid.uuid4())
        user.u_token = token
        user.save()

        # 发送邮箱内部的模板并且将token值和username传过去;将邮件发给表单传过来的用户邮箱。
        subject, from_email, to = 'html', settings.EMAIL_FROM, email
        html_content = loader.get_template('activite.html').render({'username': username,'u_token':token})
        msg = EmailMultiAlternatives(subject, from_email=from_email, to=[to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        cache.set('token', token, timeout=1800)

        return render(request, 'notice.html', context={
            'code': 1,
            'msg': "注册成功,请尽快去邮箱激活！",
            'wait': 3,
            'url': "/blog/index"
        })

#激活
def active(request):
    token = request.GET.get('u_token')
    #print(token)
    cache_token = cache.get('token')
    #print(cache_token)
    cache.delete('token')
    if token == cache_token:
        user = User.objects.filter(u_token = token).first()
        # print(user)
        # print(type(user))
        if user:
            user.is_activite = True
            user.save()
            request.session['user']=user.id

            return HttpResponse('激活成功')
        else:
            return HttpResponse('用户不存在')
    else:
        # 如果token值不相等,就去根据url传过来的token值进行查询操作
        user = User.objects.filter(u_token = token).first()
        # 如果查询出来的对象没有激活,那么就将该对象删除掉
        if not user.is_activite:
            user.delete()
            request.session.flush()
            # request.session.commit()#没有commit（）属性
            return HttpResponse("激活时间过期，请重新去注册")
        # 如果已经激活,就返回已经激活
        return HttpResponse('已经激活过了')


# 富文本写博客
def rtfedit(request):

    return render(request, 'rtf.html')

#保存富文本
def save(request):
    #判断表单是点击的那个按钮进行提交，判断是保存还是发布
    if 'publish' in request.POST:
        boke=selfboke()
        boke.title = request.POST.get('title')
        boke.intro=request.POST.get('intro')
        boke.content = request.POST.get('content')
        boke.kind_tags= request.POST.get('kinds')
        # print(boke.kind_tags)
        boke.show_time = datetime.today().strftime("%Y/%m/%d/%H/%M/%S")

        # print(boke.content)
        boke.save()

        return redirect(reverse('blog:showboke'))
    elif 'saves' in request.POST:
        bokes = drafts()
        bokes.title = request.POST.get('title')
        bokes.intro = request.POST.get('intro')
        bokes.content = request.POST.get('content')
        bokes.show_time = datetime.today().strftime("%Y/%m/%d/%H/%M/%S")

        bokes.save()
        return redirect(reverse('blog:houtai'))

#发表展示博客
def showboke(request,num='1'):
    texts=selfboke.objects.filter(del_tag=0).order_by('-id')
    kinds=classify.objects.all()
    data = {
        'kinds': kinds,
    }
    # 创建分页器   查询集, 每页显示的条数
    paginator = Paginator(texts, 11)
    # print(paginator.count,paginator.page_range)

    # 创建分页对象            - page(num) 返回page对象 如果给定的页码不存在 则抛出异常
    current = int(num)

    page = paginator.page(current)
    # print(page.number,page.object_list)

    # 自定义页码范围　
    if paginator.num_pages > 10:
        # 　如果当前页码减去5小于0
        if current - 5 <= 0:
            customRange = range(1, 11)
        elif current + 5 > paginator.num_pages:
            customRange = range(paginator.num_pages - 9, paginator.num_pages + 1)
        else:
            customRange = range(current - 5, current + 5)
    else:
        customRange = paginator.page_range

    data['one_info'] = page.object_list
    data['pagerange'] = customRange
    data['page'] = page
    return render(request,'info.html',context=data)

#将草稿箱的文章发表
def ca_push(request,blog_id):
    blogs=drafts.objects.filter(id=blog_id)
    blog=blogs.first()
    boker=selfboke()
    boker.title=blog.title
    boker.intro=blog.intro
    boker.content=blog.content
    boker.show_time=blog.show_time
    boker.save()
    blogs.delete()
    return redirect(reverse('blog:showboke'))
#直接将草稿箱的文章彻底删除
def delete_cao(request,blog_id):
    drafts.objects.filter(id=blog_id).delete()
    return redirect(reverse('blog:houtai'))


#将回收站的文章彻底删除
def delete_hui(request,blog_id):
    selfboke.objects.filter(id=blog_id).delete()
    return redirect(reverse('blog:houtai'))
#清空回收站
def qingkong_hui(request):
    selfboke.objects.filter(del_tag=1).delete()
    return redirect(reverse('blog:houtai'))


#将回收站的文章恢复
def huifu_hui(request,blog_id):
    selfboke.objects.filter(id=blog_id).update(del_tag=0)
    return redirect(reverse('blog:houtai'))

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
#分页的一个静态方法
def paging(reques,pro_list,show_nums):
    paginator = Paginator(pro_list, show_nums)  # Show 25 contacts per page
    page = reques.GET.get('page')
    try:
        blg = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        blg = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        blg = paginator.page(paginator.num_pages)
    return blg

#管理员后台//#在草稿箱展示草稿//回收站
def houtai(request):
    #所有未删除的文章
    blogs=selfboke.objects.filter(del_tag=0)
    #所有逻辑删除的文章
    blogs1=selfboke.objects.filter(del_tag=1)
    #草稿箱
    blog_draft = drafts.objects.all()

    users = User.objects.filter(user_tag=1).filter(deluser_tag=0)
    users2=User.objects.filter(user_tag=1).filter(deluser_tag=1)
    #所有的文章分类
    kinds = classify.objects.all()

    blg=paging(request,blogs,6)
    blogs1 = paging(request, blogs1, 6)
    blog_draft = paging(request, blog_draft, 6)
    users = paging(request, users, 6)
    users2 = paging(request, users2, 6)
    kinds = paging(request, kinds, 5)
    datas={
        'blg':blg,
        'blogs1': blogs1,
        'blog_draft': blog_draft,
        'users':users,
        'users2': users2,
        'kinds': kinds,
    }
    return render(request,'admin/admin.html',context=datas)
#草稿箱
def draft(request):
    datas={

    }
    # 草稿箱
    blog_draft = drafts.objects.all()
    datas['blog_draft']=blog_draft
    return render(request, 'admin/article.html', context=datas)
#逻辑删除删除文章
def del_blog(request,bl_id):
    selfboke.objects.filter(id=bl_id).update(del_tag=1)

    return redirect(reverse('blog:houtai'))
#修改文章
def alter_html(request,bl_id):
    datas={
        'bl_id':bl_id,
    }
    blogs=selfboke.objects.filter(id=bl_id).first()
    datas['blogs']=blogs

    return render(request,'admin/alter.html',context=datas)

def alter_blog(request,bl_id):
    title=request.POST.get('title')
    content=request.POST.get('content')
    intro=request.POST.get('intro')
    selfboke.objects.filter(id=bl_id).update(title=title,content=content,intro=intro)
    return redirect(reverse('blog:houtai'))
#文章置顶
def zhiding(request,bl_id):
    selfboke.objects.filter(id=bl_id).update(draft_tag=1)
    return redirect(reverse('blog:houtai'))

#文章分类标签显示
def fenlei(request,kind,num='1'):
    # print('种类%%%%%%%%',kind,'页码%%%%%%%%%',num)
    kind_num=selfboke.objects.filter(del_tag=0).filter(kind_tags=kind).all()
    kind=kind
    kinds = classify.objects.all()
    datas={
        'kind_num':kind_num,
        'kind': kind,
        'kinds': kinds,
    }

    # 创建分页器   查询集, 每页显示的条数
    paginator = Paginator(kind_num, 12)
    # print(paginator.count,paginator.page_range)
    # 创建分页对象            - page(num) 返回page对象 如果给定的页码不存在 则抛出异常
    current = int(num)
    page = paginator.page(current)
    # print(page.number,page.object_list)
    # 自定义页码范围　
    if paginator.num_pages > 10:
        # 　如果当前页码减去5小于0
        if current - 5 <= 0:
            customRange = range(1, 11)
        elif current + 5 > paginator.num_pages:
            customRange = range(paginator.num_pages - 9, paginator.num_pages + 1)
        else:
            customRange = range(current - 5, current + 5)
    else:
        customRange = paginator.page_range

    datas['one_info'] = page.object_list
    datas['pagerange'] = customRange
    datas['page'] = page
    return render(request,'share.html',context=datas)

#分类后台管理
def add_kind(request):

    kinds1=classify()
    kinds1.kind_name=request.POST.get('kindname')
    # print(kinds1.kind_name)
    kinds1.save()
    return redirect(reverse('blog:houtai'))
#修改分类
def alter_kind(request,kindid):
    kidname=request.POST.get('kidname')
    classify.objects.filter(id=kindid).update(kind_name=kidname)
    return redirect(reverse('blog:houtai'))


#用户管理
#禁止评论
def forbid_users(request,userid):
    # print(userid)
    User.objects.filter(id=userid).update(forbid_talk=1)
    return redirect(reverse('blog:houtai'))
    # return render(request,'admin/admin.html')

#删除用户
#彻底删除
def del_user(request,userid):
    User.objects.filter(id=userid).delete()
    return redirect(reverse('blog:houtai'))
#逻辑删除
def del_user1(request,userid):
    User.objects.filter(id=userid).update(deluser_tag=1)
    return redirect(reverse('blog:houtai'))
#用户恢复
def recover_user1(request,userid):
    User.objects.filter(id=userid).update(deluser_tag=0)
    return redirect(reverse('blog:houtai'))


book_list=[]
#查询搜索
def search(request,ke, num=1):
        datas = {

        }
        if ke=='search':
            keys=request.POST.get('keyboard')
            datas['keys']=keys
            blog_list=selfboke.objects.filter(Q(title__contains=keys) | Q(intro__contains=keys))
            book_list.append(blog_list)
            # 创建分页器   查询集, 每页显示的条数
            paginator = Paginator(blog_list, 12)
            # print(paginator.count,paginator.page_range)
            # 创建分页对象            - page(num) 返回page对象 如果给定的页码不存在 则抛出异常__contains
            current = int(num)
            page = paginator.page(current)
            # print(page.number,page.object_list)
            # 自定义页码范围　
            if paginator.num_pages > 10:
                # 　如果当前页码减去5小于0
                if current - 5 <= 0:
                    customRange = range(1, 11)
                elif current + 5 > paginator.num_pages:
                    customRange = range(paginator.num_pages - 9, paginator.num_pages + 1)
                else:
                    customRange = range(current - 5, current + 5)
            else:
                customRange = paginator.page_range

            datas['one_info'] = page.object_list
            datas['pagerange'] = customRange
            datas['page'] = page

            return render(request, 'life.html', context=datas)
        else:
            # 创建分页器   查询集, 每页显示的条数
            paginator = Paginator(book_list[0], 12)
            # print(paginator.count,paginator.page_range)
            # 创建分页对象            - page(num) 返回page对象 如果给定的页码不存在 则抛出异常
            current = int(num)
            page = paginator.page(current)
            # print(page.number,page.object_list)
            # 自定义页码范围　
            if paginator.num_pages > 10:
                # 　如果当前页码减去5小于0
                if current - 5 <= 0:
                    customRange = range(1, 11)
                elif current + 5 > paginator.num_pages:
                    customRange = range(paginator.num_pages - 9, paginator.num_pages + 1)
                else:
                    customRange = range(current - 5, current + 5)
            else:
                customRange = paginator.page_range

            datas['one_info'] = page.object_list
            datas['pagerange'] = customRange
            datas['page'] = page
            return render(request,'life.html',context=datas)

#短信验证


# 阅读全文
def gbook(request, num='1'):
    # print(num)
    datas = {

    }
    boke = selfboke.objects.filter(id=num).first()
    boke.like_num += 1
    boke.save()
    title = boke.title
    content = boke.content
    read_num = boke.like_num
    show_time = boke.show_time

    # 将文章信息传过去
    datas['title'] = title
    datas['content'] = content
    datas['read_num'] = read_num
    datas['show_time'] = show_time
    datas['blok_id'] = num
    talks = talk.objects.filter(blke_id=num)
    datas['talks'] = talks

    userid = request.session.get('user_id')
    if userid:
        users = User.objects.filter(id=userid).first()
        fbid_talk=users.forbid_talk
        datas['fbid_talk'] = fbid_talk
        datas['user_id'] = userid
        datas['blog_id'] = num
        datas['is_login'] = True
    else:
        datas['is_login']=False
        datas['user_id'] = userid
        datas['blog_id'] = num
    return render(request, 'gbook.html', context=datas)


#发表评论
def show_talk(request,blok_id):
    talks=talk()
    # print('文章的ID'+blok_id)
    talks.blke_id=blok_id
    contents=request.POST.get('talk')
    if len(contents)>0:
        talks.talk_content=contents
        talks.talk_user_id=request.session.get('user_id')

        # print(talks.talk_user_id)
        users=User.objects.filter(id=talks.talk_user_id).first()
        talks.talk_user_name=users.username
        talks.save()

        blog=selfboke.objects.filter(id=blok_id).first()
        blog.talk_num += 1
        blog.save()

        return redirect(reverse('blog:gbook',args=(blok_id,)))
    return render(request, 'notice.html', context={
        'code': -1,
        'msg': "评论内容不能为空",
        'wait': 2,
        'url': "/blog/gbook/{}".format(blok_id)
    })




