#!/usr/bin/python3
import os
import re
import zipfile
import requests

#url = "https://assrt.net/xml/sub/461/461289.xml?suggest_from=603584"
url = "https://assrt.net/xml/sub/610/610293.xml"


def download(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}
    req = requests.get(url, headers=headers)
    # print(str(req.content,"utf8"))
    ans = re.search(u"(/download/.*?)\"", str(req.content, 'utf8'))

    if not ans:
        return

    download_url = "https://assrt.net" + ans.group(1)
    # print(download_url)
    print(download_url[download_url.rfind('/')+1:])
    #print("获得文件类型 "+download_url[-3:])

    data = requests.get(download_url, headers=headers)

    adr = "C:\\Users\\XU\\Desktop\\" + str( download_url[download_url.rfind('/')+1:] )
    with open(adr,"wb") as code:
     code.write(data.content)
    #print(data.content)
    print(adr+'  '+str(len(data.content)))

    return adr

def unzip(adr):
    if(adr[-3:]=='zip'):
        f = zipfile.ZipFile(adr, 'r')
        os.chdir("C:\\Users\\XU\\Desktop")
        for file in f.namelist(): 
            f.extract(file,"temp/")
        f.close()
        fileList = os.listdir( "C:\\Users\\XU\\Desktop\\temp")
        os.chdir("C:\\Users\\XU\\Desktop\\temp")
        return fileList
    else:
        os.chdir("C:\\Users\\XU\\Desktop\\")
        return [adr,]

def search(fileList,msg):
    ans = []

    for file in fileList:
        with open(file, encoding='utf8', errors='ignore') as file_obj:
            for line in file_obj.readlines():
                line = line.lower()
                if line.find(msg)!= -1:
                    ans.append(last_line+line+'\n') #information
                last_line = line
        if len(ans)!=0:
            break

    return ans

def write_down(ans):
    with open('ans.txt','w') as f:
        f.writelines(ans)
        f.close()
    print("查找到"+str(len(ans))+'句话，已保存至ans')

adr = download(url)
fileList = unzip(adr)
ans = search(fileList,'love')
write_down(ans)
