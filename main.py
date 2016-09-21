import urllib
from urllib import request, parse
import http.cookiejar, re,work, threading, queue,math



posturl = 'https://www.tumblr.com/login'
cj = http.cookiejar.MozillaCookieJar('tmp.txt')

# cj.load('tmp.txt',ignore_discard=True, ignore_expires=True)
# cookie_support = urllib.request.HTTPCookieProcessor(cj)
# opener = urllib.request.build_opener(cookie_support)
# # urllib.request.install_opener(opener)
# req = urllib.request.Request(posturl)
# resp = opener.open(req)
# content = resp.read()
# print(content.decode('UTF-8'))


req = request.Request(posturl)
res = request.urlopen(req)
content = res.read().decode('UTF-8')
reStr = '<meta name="tumblr-form-key" content="(.*?)" id="tumblr_form_key">'
formkey = re.findall(reStr, content)[0]

print(formkey)

cookie_support = urllib.request.HTTPCookieProcessor(cj)
opener = urllib.request.build_opener(cookie_support)
urllib.request.install_opener(opener)


postData = {'determine_email':"411745019@qq.com",
            'user[email]':'411745019@qq.com',
            'user[password]':'1234527xmq',
            'context':"home_signup",
            'version':"STANDARD",
            'http_referer':"https://www.tumblr.com/",
            'form_key':formkey,
            'seen_suggestion':"0",
            'used_suggestion':"0",
            'used_auto_suggestion':"0",
            'about_tumblr_slide':"",
            'tumblelog[name]':"",
            'user[age]':"",
            'follow':""}
data = urllib.parse.urlencode(postData)
data = data.encode('UTF-8')
req = urllib.request.Request(posturl, data)
resp = urllib.request.urlopen(req)
html = resp.read().decode('UTF-8')
if html.find('logout_button'):
    print('login ok!')
else:
    exit()
# print(content.decode('UTF-8'))

def unfollow(userid):
    unfollowURL = 'https://www.tumblr.com/svc/unfollow'
    headers = {
    'Host': 'www.tumblr.com',
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:48.0) Gecko/20100101 Firefox/48.0',
    'Accept': '*/*',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-tumblr-form-key': formkey,
    'X-Requested-With': 'XMLHttpRequest',
    'Referer': 'https://www.tumblr.com/following/0',
    'Content-Length': '110',
    'Connection': 'keep-alive'}

    postData = {
    'form_key':formkey,
    'data[tumblelog]':userid,
    'data[source]':'UNFOLLOW_SOURCE_FOLLOWING_PAGE'}

    data = urllib.parse.urlencode(postData)
    data = data.encode('UTF-8')
    req = urllib.request.Request(unfollowURL, data=data, headers=headers)
    resp = urllib.request.urlopen(req)
    print(resp)

followingURL = "https://www.tumblr.com/following"
res = request.urlopen(followingURL).read().decode('UTF-8')
reStr = '<a class="tab selected" href="/following">在 Tumblr 上关注 (.*?)</a>'
followCnt = re.findall(reStr, res)[0]

followingURL = "https://www.tumblr.com/following"
res = request.urlopen(followingURL).read().decode('UTF-8')
reStr = '<meta name="tumblr-form-key" content="(.*?)" id="tumblr_form_key">'
formkey = re.findall(reStr, res)[0]

pageCnt = int(followCnt)/25
reLink = '<a class="name-link" href="(.*?)"'
reLastUpdate = '<span class="last_updated" style="color:#606060;">已于 (.*?) 更新</span>'
pattern = re.compile(reLink+'[\s\S]*?'+reLastUpdate)

arrUnfollow = []
for i in range(0, math.ceil(pageCnt)):
    url = followingURL+'/'+str(i*25)
    res = request.urlopen(url).read().decode('UTF-8')
    res = re.findall(pattern, res)
    print('page : ' + str(i))
    for obj in res:
        timeStr = obj[1]
        link = 0
        if timeStr.find('月') > 0:
            if int(timeStr[:1]) > 3:
                arrUnfollow.append(obj[0])
        elif timeStr.find('年') > 0:
            arrUnfollow.append(obj[0])

print('old :'+str(len(arrUnfollow)))
headers = {
    'Host': 'www.tumblr.com',
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:48.0) Gecko/20100101 Firefox/48.0',
    'Accept': '*/*',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-tumblr-form-key': formkey,
    'X-Requested-With': 'XMLHttpRequest',
    'Referer': 'https://www.tumblr.com/following/0',
    'Content-Length': '110',
     'Connection': 'keep-alive'}
unfollowURL = 'https://www.tumblr.com/svc/unfollow'
for userLink in arrUnfollow:
    userid = userLink[7: userLink.find('.tumblr.com')]
    print(userid)
    postData = {
    'form_key':formkey,
    'data[tumblelog]':userid,
    'data[source]':'UNFOLLOW_SOURCE_FOLLOWING_PAGE'}
    data = urllib.parse.urlencode(postData)
    data = data.encode('UTF-8')
    req = urllib.request.Request(unfollowURL, data=data, headers=headers)
    resp = urllib.request.urlopen(req)
    print(resp)
