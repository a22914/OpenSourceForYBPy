# 这个Python脚本给出的只是最简单的没有加密的版本，有加密的版本请自行学习后自行编写 碰壁后可咨询熊之大

import json
import requests
import datetime

# 请求头  部分直播接口不加请求头会报错，因为服务器会判断你的请求头是否为软件请求头
headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/75.0.3770.100 Mobile Safari/537.36"}
# 请求地址 即直播首页接口地址  这里的链接为示例
url = "http://xxxxxxx.com/appapi/?service=Home.getHot&p=1"

# 发送请求
response = requests.get(url, headers=headers)

# 请了解JSON后再进行一下操作 因为直播接口返回的是JSON格式的数据 而且是嵌套的JSON格式的数据 所以需要进行多次转换
# 而且这里的转换是为了获取到直播列表的数据 也就是主播名称，主播头像和地址
# 还有就是后面的写入操作我就不给出了 你们自己看着写吧

# 将返回的json字符串转换为字典
ret1 = json.loads(response.text)
# 获取字典中的data键对应的值
content_list = ret1["data"]

# 将data内数据转换为json字符串
js1 = json.dumps(content_list)

ret2 = json.loads(js1)
content_list2 = ret2["info"]

# 将info内数据转换为json字符串
js2 = json.dumps(content_list2)
# 去掉json字符串的首尾中括号，因为info内数据是一个列表，列表的首尾是中括号，去掉才符合json格式
js2 = js2[1:-1]

ret3 = json.loads(js2)
content_list3 = ret3["list"]

# 获取当前时间
nowtime = datetime.datetime.now().strftime('%H:%M:%S')
items = ret3

# 标准格式的m3u需要首行声明#EXTM3U并回车  这里不写希望各位了解m3u标准后自己加
with open("文件路径+文件名", "w+", encoding='utf-8') as f:
    # 方式一 不声明tvg-name
    # 将时间写入文件第一行
    f.write('#EXTINF:-1 tvg-logo="m3u图片地址"' + ' group-title="分类名",时间' + nowtime + '\n' + 'https://\n')

    # 遍历列表 将列表中的JSON数据写入文件
    for key in range(len(items['list'])):
        f.write('#EXTINF:-1 tvg-logo="' + items['list'][key]['头像JSON键'] + '"' + ' group-title="分类名",'
                + items['list'][key]['主播昵称JSON键'] + '\n' + items['list'][key]['推流JSON键'] + '\n')
    # 方式二 声明tvg-name  这里希望格子自己尝试

print("验证执行过程", end=' ')

# 非标准格式的m3u写入举例
with open("文件路径+文件名", "w+", encoding='utf-8') as f:
    # 声明两次分类名是为了能够在不同的非标准识别分类名的软件中显示分类名
    f.write("分类名\n分类名,#genre#\n")
    # 在第一个列表写入时间
    f.write(nowtime + ',' + "https://\n")
    # 遍历列表 将列表中的JSON数据写入文件
    for key in range(len(items['list'])):
        f.write(items['list'][key]['主播昵称JSON键'] + ',' + items['list'][key]['推流地址JSON键'] + '\n')

print("验证执行过程", end=' ')