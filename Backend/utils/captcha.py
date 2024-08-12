from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random
import string
from io import BytesIO


# 获取随机字符组合
def get_random_char(num: int):
    chr_all = string.ascii_letters + string.digits
    strings = ''.join(random.sample(chr_all, num))
    return strings


# 获取随机颜色
def get_random_color(low, high):
    return random.randint(low, high), random.randint(low, high), random.randint(low, high)


# 制作验证码图片
def get_picture():
    width, height = 180, 60
    # 创建空白画布
    image = Image.new('RGB', (width, height), get_random_color(20, 100))
    # 验证码的字体
    font = ImageFont.truetype('C:/Windows/fonts/stxinwei.ttf', 40)
    # 创建画笔
    draw = ImageDraw.Draw(image)
    # 获取验证码
    chr_4 = get_random_char(4)
    # 向画布上填写验证码
    for i in range(4):
        draw.text((40 * i + 10, 0), chr_4[i], font=font, fill=get_random_color(100, 200))
    # 绘制干扰点
    for x in range(random.randint(200, 600)):
        x = random.randint(1, width - 1)
        y = random.randint(1, height - 1)
        draw.point((x, y), fill=get_random_color(50, 150))
    # 模糊处理
    image = image.filter(ImageFilter.BLUR)
    # 将图片保存为"数据流"直接返回，而不用保存到本地
    # 具体做法是：将图片对象保存到 BytesIO 对象中，然后返回
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    buffered.seek(0)
    return chr_4, buffered
