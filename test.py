
# iOS 测试 iOS-remote 安装篇之 WebDriverAgent 安装使用完全指南
# https://testerhome.com/topics/10463


import wda
from PIL import Image, ImageDraw


######## config

###############

c=wda.Client()
# c.home()

# s =  c.session('com.tencent.xin')
# e = s(text='杨秋怡').get(timeout=10.0)
# s(text='Dashboard') is Selector
# e is Element object


# s =  c.session('com.tencent.xin')
# # print(s.window_size())
# s.tap_hold(170, 650, 10) # tap element


cnt = 19
while input("Enter CMD: ")!="n":
	c.screenshot('img_data/screenshot{}.png'.format(cnt))
	cnt += 1

