
from django.conf.urls import url


from blog import views

urlpatterns = [

    #url(r'^index/', views.index, name='index'),
    url(r'^about/', views.about,name='about'),

    # url(r'^life/', views.life,name='life'),
    # url(r'^time/', views.time,name='time'),
    url(r'^gbook/(\d+)/$', views.gbook,name='gbook'),

    url(r'^share/', views.share,name='share'),
    # url(r'^info/', views.info,name='info'),
    #登录注册
    url(r'^login/', views.login,name='login'),
    # url(r'^dologin/', views.dologin,name='dologin'),
    url(r'^regist/', views.regist,name='regist'),
    url(r'^loginout/', views.loginout,name='loginout'),

    #富文本
    url(r'^rtfedit/', views.rtfedit, name='rtfedit'),
    url(r'^save/', views.save, name='save'),
    url(r'^showboke/$', views.showboke, name='showboke'),
    url(r'^showboke/(\d*)/$',views.showboke,name='showboke1'),

    #邮件激活
    url(r'^active/', views.active, name='active'),

    #登录验证码
    url(r'^vcode/', views.vcode, name='vcode'),

    #发表评论
    url(r'^show_talk/$', views.show_talk, name='show_talk1'),
    url(r'^show_talk/(\d*)/$', views.show_talk, name='show_talk'),
    # url(r'^show', views.show, name='show'),


    #管理员
    url(r'^houtai/', views.houtai, name='houtai'),

    #删除
    url(r'^del_blog/(\d+)/$', views.del_blog, name='del_blog'),

    #修改
    url(r'^alter_html/(\d+)/$', views.alter_html, name='alter_html'),
    url(r'^alter_blog/(\d+)/$', views.alter_blog, name='alter_blog'),

    #搜索
    url(r'^search/$', views.search, name='search'),
    url(r'^search/([\w.]+)/(\d+)/$', views.search, name='search1'),


    #草稿箱
    url(r'^draft/$', views.draft,name='draft'),
    url(r'^ca_push/(\d+)/$', views.ca_push,name='ca_push'),
    url(r'^delete_cao/(\d+)/$', views.delete_cao,name='delete_cao'),

    #回收站
    url(r'^huifu_hui/(\d+)/$', views.huifu_hui,name='huifu_hui'),
    url(r'^delete_hui/(\d+)/$', views.delete_hui,name='delete_hui'),
    url(r'^qingkong_hui/', views.qingkong_hui,name='qingkong_hui'),

    #分页
    url(r'^index/$', views.index,name='index'),

    url(r'^index/(\d*)/$',views.index,name='index1'),

    #用户管理
    #禁止评论
    url(r'^forbid_users/(\d+)/$', views.forbid_users,name='forbid_users'),

    #删除用户
    #彻底删除
    url(r'^del_user/(\d+)/$', views.del_user,name='del_user'),
    #逻辑删除
    url(r'^del_user1/(\d+)/$', views.del_user1,name='del_user1'),
    #恢复
    url(r'^recover_user1/(\d+)/$', views.recover_user1,name='recover_user1'),

    #文章置顶
    url(r'^zhiding/(\d+)/$', views.zhiding,name='zhiding'),
    #文章分类
    #目前url暂时设置成这样，可扩展性太差，待修改！
    url(r'^fenlei/([\w.]+)/$', views.fenlei,name='fenlei'),
    url(r'^fenlei/([\w.]+)/(\d+)/$', views.fenlei,name='fenlei1'),
    # url(r'^fenlei/([a-z35.]+)/(\d+)/$', views.fenlei,name='fenlei1'),
    #添加分类
    url(r'^add_kind/', views.add_kind,name='add_kind'),
    #修改分类
    url(r'^alter_kind/(\d+)/$', views.alter_kind,name='alter_kind'),

    #收藏
    url(r'^collects/', views.collects,name='collects'),
    url(r'^cancel_collect/', views.cancel_collect,name='cancel_collect'),

    url(r'^personal/', views.personal,name='personal'),

]
