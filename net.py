#bilibili_spider
#uid_to_download_all_video

import sys
import json
import jsonpath
import requests
from you_get import common        #如果无法下载视频，需要下载you-get库

def getBvid():        #该函数获取目标用户的视频列表
    resData=True
    pid=1
    data=[]

    try:
        uid=sys.argv[1]
    except:        #如果用户没有附加命令行参数，则提示程序用例
        print('[*]Usage:xxx.py uid')
        print('[*]Example:ThisSpider.py 517717593')        #正常来说，这条命令会下载 上海爱丽丝幻乐团 的视频
        exit()

    try:
        while resData!=False:        #反复执行翻页，直到获取了所有的返回值
            res=requests.get('https://api.bilibili.com/x/space/arc/search?mid='+uid+'&ps=30&tid=0&pn='+str(pid)+'&keyword=&order=pubdate&jsonp=jsonp').content.decode('utf-8')
            try:
                resJson=json.loads(res)
                resData=jsonpath.jsonpath(resJson,"$..bvid")
                if resData!=False:
                    data=data+resData        #将获取到的bv号拼接起来
            except:
                print('[-]Data load error.')
            pid=pid+1
    except:
        print('[-]Connect error.')

    if data!=[]:
        return data        #将获取到的bv号列表返回给调用者

def downloadvideo(returnData):        #该函数用于下载bv号列表内的视频
    for i in returnData:
        try:
            bvUrl='https://www.bilibili.com/video/'+str(i)
            common.any_download(url=bvUrl,stream_id='',info_only=False,output_dir=r'.\/',merge=True)
        except:
            print('[-]Download error.')

if __name__ == '__main__':
    returnData=getBvid()
    downloadvideo(returnData)

