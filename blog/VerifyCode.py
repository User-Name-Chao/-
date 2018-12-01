import os
from random import randint, sample

from PIL import ImageFont, Image, ImageDraw
from io import BytesIO

#　验证码类
from Bloger import settings


class VerfiyCode:
    def __init__(self,width=100,height=40,len=4):
        """
        系统初始化
        :param width: 验证码图片宽度
        :param height: 验证码图片高度
        :param len: 验证码长度
        """
        self.width = width if width > 50 else 100
        self.height = height if height > 30 else 40
        self.len = len if len >= 4 else 4

        self._code = ''  #验证码字符串
        self.__pen = None  #画笔

    @property
    def code(self):
        return self._code

    def output(self):
        """
        输出验证码
        :return: 验证码图片的二进制流
        """
        # 1　创建画布
        im = Image.new('RGB',(self.width,self.height),self.__randColor(120,200))
        self.__pen = ImageDraw.Draw(im)  #产生画笔

        # 2 产生验证码字符串
        self.generateCode()
        # print(self._code)

        # 3　画验证码
        self.__drawCode()

        # 4. 画干扰点
        self.__drawpoint()

        # 5 画干扰线
        self.__drawline()

        # 6 返回图片
        im.save('vc.png','PNG')
        buf = BytesIO()
        im.save(buf,'png')
        res = buf.getvalue()
        buf.close()
        return res


    def __randColor(self,low,high):
        return randint(low,high),randint(low,high),randint(low,high)

    def generateCode(self):
        """
        产生纯数字验证码
        :return: 无
        """
        num = ''
        for i in range(self.len):
            num += str(randint(0,9))
        self._code = num

    def __drawCode(self):
        """
        画验证码
        :return:
        """
        path = os.path.join(settings.STATICFILES_DIRS[0],'fonts/STHUPO.TTF')
        # print(path)
        font1 = ImageFont.truetype(path,size=20,encoding='utf-8')
        # print(font1)
        # 一个字符宽度
        width = (self.width - 20)/self.len

        for i in range(self.len):
            x = 10 + i * width + width / 4
            y = randint(5,self.height-25)
            self.__pen.text((x,y),self._code[i],font=font1,fill=self.__randColor(0,100))

    def __drawpoint(self):
        for i in range(300):
            x = randint(1,self.width - 1)
            y = randint(1,self.height - 1)
            self.__pen.point((x,y),fill=self.__randColor(60,160))

    def __drawline(self):
        # print(self._code)
        for i in range(6):
            #　起点坐标
            start = (randint(1,self.width - 1),randint(1,self.height - 1))
            end = (randint(1,self.width - 1),randint(1,self.height - 1))
            self.__pen.line([start,end],fill=self.__randColor(120,200))

# class StrCode(VerfiyCode):
#     def generateCode(self):
#         # s1 = 'QWERTYUPASDFGHJKLZXCVBNMqwertyupasdfghjklzxcvbnm'
#         s1 ='0123456789'
#         res = sample(s1,self.len)
#         res = ''.join(res)
#         print(res)
#         self._code = res



# if __name__ == "__main__":
#     vc = VerfiyCode()
#     print(vc.output())
#     print(vc.code)
