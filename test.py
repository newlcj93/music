# -*- coding: utf-8 -*-
import requests,json,os,threading,time
urls={}
errors={}
def get_url():
    url="http://music.163.com/api/playlist/detail?id=45094703&updateTime=-1"
    data=requests.get(url)
    content=json.loads(data.content)
    track=content['result']['tracks']
    for  i in range(len(track)):
   #     artists=track[i]['artists'][0]
   #    pic_url=artists['picUrl']
        song=track[i]
        song_name=song['name'].encode("utf-8")
        mp3_url = song['mp3Url']
   #    song_id=song['id']
   #     song_url="http://music.163.com/song?id=%d" %song_id
        urls[song_name]=mp3_url
def save(name):
    print "%s is downloading" % name
    cnt=0
    while(cnt<10):
        try:
            mp3_content=requests.get(urls[name]).content
            break
        except requests.exceptions.RequestException as e:
            if hasattr(e,'reason'):
                print e.reason
                errors.append(name,urls[name])
                cnt+=1
                time.sleep(5)
                if cnt is 10 return
    fpath="/Users/jy/mp3/%s.mp3" % name
    if os.path.exists(fpath):
        print "%s already exits"
        return
    with open("/Users/jy/mp3/%s.mp3" %name,"wb") as f:
        f.write(mp3_content)
    print "%s is downloaded"
def saveall():
    threads=[]
    print "Start downloading---------------"
    for name in urls.keys():
        threads.append(threading.Thread(target=save,args=(name,),name='thread %s' %name))
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print "-------------done---------------"


if __name__=="__main__":
    get_url()
    saveall()

