from subprocess import call
import requests,time,math,os

#专辑ID
ChannelId = 262151
#登录信息
Phone = 138516731192
Password = 'nvT70FtC2Hev'
#文件下载路径
FilePath = r'D:\有声小说'
#IDM路径
IdmPath = 'C:\Program Files (x86)\Internet Download Manager\IDMan.exe'
def IdmDownLoad(DownloadUrl, Mp3Name):
    call([IdmPath, '/d',DownloadUrl,'/p',FilePath,'/f',Mp3Name,'/n','a'])
#文件名格式化
def ChangeFileName(filename):
    filename = filename.replace('\\','')
    filename = filename.replace('/','')
    filename = filename.replace('：','')
    filename = filename.replace('*','')
    filename = filename.replace('“','')
    filename = filename.replace('”','')
    filename = filename.replace('<','')
    filename = filename.replace('>','')
    filename = filename.replace('|','')
    filename = filename.replace('?','？')
    filename = filename.replace('（','(')
    filename = filename.replace(' ','(')
    filename = filename.replace(chr(65279),'') # UTF-8+BOM
    filename = filename.split('(')[0]
    return filename
LoginUrl = 'https://u2.qingting.fm/u2/api/v4/user/login'
data = {'account_type': '5','device_id': 'web','user_id': Phone,'password': Password}
Conn = requests.session()
Response = Conn.post(LoginUrl,data)
ResponseJson = Response.json()
errorno = ResponseJson['errorno']
if errorno ==0:
    print('登录成功！')
else:
    print('登录失败！')
QingtingID = ResponseJson['data']['qingting_id']
AudioDetail = 'https://webapi.qingting.fm/api/mobile/channels/%d'%ChannelId
AudioDetailJson = Conn.get(AudioDetail)
AudioDetailJson = AudioDetailJson.json()
Title = AudioDetailJson['channel']['title']
ProgramCount = AudioDetailJson['channel']['programCount']
Page = math.ceil(ProgramCount/30)
print('---')
print('书名：',Title)
print('章节数：',ProgramCount)
print('页熟：',Page)
print('---')
Version = AudioDetailJson['channel']['v']
AlreadyDown = [FileName.replace('.mp3','',1) for FileName in os.listdir(FilePath)]
for i in range(Page):
    page = i + 1
    print('正在抓取第%d页'%page)
    pageurl = 'https://webapi.qingting.fm/api/mobile/channels/%d/programs?version=%s&page_index=%d'%(ChannelId,Version,page)
    pagedetail = Conn.get(pageurl)
    pagejson = pagedetail.json()
    programs = pagejson['programs']
    for program in programs:
        programId = program['programId']
        title = program['title']
        audiodetail = 'https://webapi.qingting.fm/api/mobile/channels/%d/programs/%d?user_id=%s'%(ChannelId,programId,QingtingID)
        print(audiodetail)
        programResponse = Conn.get(audiodetail)
        programJson = programResponse.json()
        programInfo = programJson['programInfo']
        AudioName = programInfo['title']
        AudioName = ChangeFileName(AudioName)
        if AudioName in AlreadyDown:
            print('目录已有该文件，跳过下载。')
            continue
        audioUrl = programInfo['audioUrl']
        IdmDownLoad(audioUrl, AudioName+'.mp3')
        time.sleep(10)
