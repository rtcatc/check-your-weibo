#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
    微博互关检测脚本 V1.0
    作者: Poc-Sir Github:@rtcatc
    环境: Python3.X 需安装"requests"包
    仅供交流学习使用，请勿用于其他任何用途，谢谢！
    Mon site Internet:https://www.hackinn.com
"""

import requests,time
follow_uids=[]
fans_uids=[]
url = ""

def TellTime(): #时间输出
    localtime = "[" + str(time.strftime('%H:%M:%S',time.localtime(time.time()))) + "]"
    return localtime

def GetMiddleStr(content,startStr,endStr): #获取中间字符串通用函数
    startIndex = content.index(startStr)
    if startIndex>=0:
        startIndex += len(startStr)
    endIndex = content.index(endStr)
    return content[startIndex:endIndex]

def CheckLogin(cookies):
    try:
       headers={"User-Agent": "Weibo/44006 CFNetwork/1098.7 Darwin/19.0.0"}
       url1 = "https://weibo.cn/laizong-haoshuai" #不存在地址，可自己修改
       response = requests.get(url=url1, headers=headers, cookies=cookies).text
       if (response[2:5] == "xml"): #此版本为xml格式，绕过获取限制
           print(TellTime() + "系统登陆成功！")
           print(TellTime() + "开始获取关注列表...")
           GetFollow(cookies,1,1)
           print(TellTime() + "开始获取粉丝列表...")
           GetFans(cookies,1,1)
           return 1
       else:
           print(TellTime() + "登录失败请检查Cookies数据")
           return 0
    except:
       print(TellTime() + "网络连接失败请检查！")
       exit()

def GetFollow(cookies,page_number,page_total):
    try:
       headers={"User-Agent": "Weibo/44006 CFNetwork/1098.7 Darwin/19.0.0"}
       url1 = url + "follow"
       params = "page=" + str(page_number)
       response = requests.get(url=url1, params=params, headers=headers, cookies=cookies).text
       if (page_number == 1):
           page_total = int(GetMiddleStr(GetMiddleStr(response,"name=\"mp\"","-wap-input-format"),"value=\"","\" />"))
           print(TellTime() + "关注列表共计: " + str(page_total) + "页")
       if (page_number > page_total):
           print(TellTime() + "关注列表获取完毕")
           return 0 #获取完毕退出循环
       try:
           list_follow = GetMiddleStr(response,"</div></div>","<div class=\"c\">").split(" <div class=\"s\"></div>")
           for follow_uid in list_follow:
               try:
                   follow_uid = GetMiddleStr(follow_uid,"/attention/add?uid=","&amp;")
                   follow_uids.append(follow_uid)
               except: #cookie账户已关注的情况
                   try:
                       follow_uid = GetMiddleStr(follow_uid,"<a href=\"https://weibo.cn/u/","\"><img src=")
                       follow_uids.append(follow_uid)
                   except: #只能获取个性化域名
                       follow_uid = GetMiddleStr(follow_uid,"<a href=\"https://weibo.cn/","\"><img src=")
                       follow_uids.append(follow_uid)
           GetFollow(cookies,page_number+1,page_total)
       except:
           if (response.find("class=\"ps\"") != -1): #微博反垃圾策略
               GetFollow(cookies,page_number+1,page_total)
    except:
       print(TellTime() + "网络连接失败请检查！")
       exit()

def GetFans(cookies,page_number,page_total):
    try:
       headers={"User-Agent": "Weibo/44006 CFNetwork/1098.7 Darwin/19.0.0"}
       url1 = url + "fans"
       params = "page=" + str(page_number)
       response = requests.get(url=url1, params=params, headers=headers, cookies=cookies).text
       if (page_number == 1):
           page_total = int(GetMiddleStr(GetMiddleStr(response,"name=\"mp\"","-wap-input-format"),"value=\"","\" />"))
           print(TellTime() + "粉丝列表共计: " + str(page_total) + "页")
       if (page_number > page_total):
           print(TellTime() + "粉丝列表获取完毕")
           return 0 #获取完毕退出循环
       try:
           list_fans = GetMiddleStr(response,"</div></div>","<div class=\"c\"><form action").split(" <div class=\"s\"></div>")
           for fans_uid in list_fans:
               try:
                   fans_uid = GetMiddleStr(fans_uid,"/attention/add?uid=","&amp;")
                   fans_uids.append(fans_uid)
               except: #cookie账户已关注的情况
                   try:
                       fans_uid = GetMiddleStr(fans_uid,"<a href=\"https://weibo.cn/u/","\"><img src=")
                       fans_uids.append(fans_uid)
                   except: #只能获取个性化域名
                       fans_uid = GetMiddleStr(fans_uid,"<a href=\"https://weibo.cn/","\"><img src=")
                       fans_uids.append(fans_uid)
           GetFans(cookies,page_number+1,page_total)
       except:
           if (response.find("class=\"ps\"") != -1): #微博反垃圾策略
               GetFans(cookies,page_number+1,page_total)
    except:
       print(TellTime() + "网络连接失败请检查！")
       exit()

def GetDetial(uid,cookies):
    try:
       headers={"User-Agent": "Weibo/44006 CFNetwork/1098.7 Darwin/19.0.0"}
       url1 = "https://weibo.cn/" + uid
       print("用户UID:" + uid)
       response = requests.get(url=url1, headers=headers, cookies=cookies).text
       response = GetMiddleStr(response,"<span class=\"ctt\"","/span><br /><a")
       uname = GetMiddleStr(response,">","<")
       if (uname.find("&nbsp;") != -1): #二次过滤
           uname = GetMiddleStr("aa#" + uname,"aa#","&nbsp;")
       ubase = GetMiddleStr(response,"&nbsp;","    &nbsp;")
       uinfo = GetMiddleStr(response+"aa","width:50px;\">","<aa") #防止去错
       print("用户名:" + uname)
       print("用户基础信息:" + ubase)
       if (uinfo == ""):
           print("")
       else:
           print("用户简介:" + uinfo + "\n")
    except:
       print(TellTime() + "网络连接失败请检查！")
       exit()

if __name__ == '__main__':
    print("+------------------------------------------------------------+")
    print("| 欢迎使用微博互关检测脚本  Coucou, Je Suis Poc-Sir!         |")
    print("| 请在任意浏览器中登录weibo.cn (注意不是.com)                |")
    print("| 此程序需要您提供登录之后名为SUB的cookie信息                |")
    print("| 仅供交流学习使用，请勿用于其他任何用途，谢谢！             |")
    print("| 请注意保护个人数据，不要提供给他人，本程序不会保存您的数据 |")
    print("| 造成一切后果均由使用者本人承担，本人概不负责               |")
    print("+------------------------------------------------------------+\n")
    cookies = "SUB=" + input("请粘贴您获取到的SUB数据：")
    cookies2 = dict(map(lambda x:x.split('='),cookies.split(";"))) #一键转换饼干
    url = "https://weibo.cn/" + input("请粘贴要检测用户UID数据：") + "/"
    CheckLogin(cookies2) #登录微博系统
    follow_uids = list(filter(None,follow_uids)) #list数组去空
    fans_uids = list(filter(None,fans_uids))
    print(TellTime() + "正在对比交集部分...")
    intersection_uids = list(set(follow_uids) & set(fans_uids)) #求交集
    print(TellTime() + "获取互关成功:" + str(intersection_uids))
    print(TellTime() + "正在提取互关详细信息...\n")
    for uid in intersection_uids:
        GetDetial(uid,cookies2)
