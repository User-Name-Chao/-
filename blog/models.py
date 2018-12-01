from django.db import models

# Create your models here.

class User(models.Model):
    username=models.CharField(max_length=32)
    password=models.CharField(max_length=64)
    icon = models.ImageField(upload_to='icons')
    email=models.CharField(max_length=64)
    u_token = models.CharField(max_length=136)
    is_activite = models.BooleanField(default=False)
    user_tag=models.IntegerField(default=1)
    #注册时间
    resgist_time=models.CharField(max_length=32,null=True)
    #是否被禁止评论
    forbid_talk=models.IntegerField(default=0)
    #逻辑删除用户
    deluser_tag=models.IntegerField(default=0)



class selfboke(models.Model):
    title=models.CharField(max_length=64)
    show_time=models.CharField(max_length=32)
    content=models.TextField()
    like_num=models.IntegerField(default=0)
    talk_num=models.IntegerField(default=0)
    intro=models.TextField()
    #逻辑删除标记
    del_tag=models.IntegerField(default=0)
    # 是否置顶
    draft_tag=models.IntegerField(default=0)
    #文章分类(报废）
    kind_tag=models.IntegerField(default=0)
    # 文章分类
    kind_tags =models.CharField(max_length=32,default='散文')



class talk(models.Model):
    blke_id=models.IntegerField(default=0)
    talk_user_id=models.IntegerField(default=0)
    talk_content=models.TextField()

    talk_user_name=models.CharField(max_length=32)



class drafts(models.Model):
    title=models.CharField(max_length=64)
    show_time=models.CharField(max_length=32)
    content=models.TextField()
    intro=models.TextField()



class classify(models.Model):
    kind_name=models.CharField(max_length=32)
    kind_article_num = models.CharField(max_length=32,null=True)

