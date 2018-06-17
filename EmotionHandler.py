import allFunctionSuit
import glob as gb
import json
import os
import requests
class EmotionHandler:
    pathList = []
    def __init__(self,imgSet_path,timeStart):
        self.img_path = gb.glob(imgSet_path + "*.jpg")
        self.pathList = [path for path in self.img_path]
        self.faceSuit = allFunctionSuit.FaceDetect()
        self.timeStart = timeStart
        self.pictureCount = len(self.pathList)

    def getAuthorization(self,username,password):     
        import base64
        Authorization = username + ':' + password
        Authorization = Authorization.encode('utf-8')
        Authorization = base64.b64encode(Authorization)
        Authorization = Authorization.decode('utf-8')
        return Authorization

    def getEmotionList(self):
        emotionList = []
        for pic in self.pathList:
            emotion = self.faceSuit.outputEmotionAsFileWithDetectJustEmotion(pic)
            emotionList.append(emotion)
            with open("./emotionDict",'a') as f:
                f.write(emotion+"\n")
            if pic == self.pathList[-1]:
                print("表情输出完成！")
        return emotionList

    def timestamp2time(self):
        import time
        emotionList = self.getEmotionList()

        #临时
        # f =open("./emotionDict",'r')
        # emotionList=f.readlines()


        timeList = []
        emotionDict = []
        for n in range(0,self.pictureCount):
            timestamp = time.mktime(time.strptime(self.timeStart, "%Y-%m-%dT%H:%M:%S")) + n * 5
            time_local = time.localtime(timestamp)
            dt = time.strftime("%Y-%m-%dT%H:%M:%S",time_local)
            timeList.append(dt)
        # emotionList.reverse()
        # emotionList.pop()
        # emotionList.reverse()
        # timeList.pop()
        for time,emotion in zip(timeList,emotionList):
            jsonObj = json.loads(emotion)
            emotionDict.append("{\""+time+"\":\""+ jsonObj["emotion"] +"\"}")

        
        return emotionDict

    def timestamp2timeWithFile(self):
        import time

        f =open("./emotionDict",'r')
        emotionList=f.readlines()


        timeList = []
        emotionDict = []
        for n in range(0,self.pictureCount):
            timestamp = time.mktime(time.strptime(self.timeStart, "%Y-%m-%dT%H:%M:%S")) + n * 5
            time_local = time.localtime(timestamp)
            dt = time.strftime("%Y-%m-%dT%H:%M:%S",time_local)
            timeList.append(dt)
        # emotionList.reverse()
        # emotionList.pop()
        # emotionList.reverse()
        # timeList.pop()
        for time,emotion in zip(timeList,emotionList):
            jsonObj = json.loads(emotion)
            emotionDict.append("{\""+time+"\":\""+ jsonObj["emotion"] +"\"}")

        
        return emotionDict
    def postAction(self,username,password,clipId):
        url = "http://127.0.0.1:8000/api/emotions/"
        header = {
            'Authorization': "Basic " + self.getAuthorization(username,password)
        }
        emotionDict = self.timestamp2time()
        for emotion in emotionDict:
            emotionObj = json.loads(emotion)
            times = [a for a in emotionObj.keys()]
            states = [b for b in emotionObj.values()]
            time = times[0]
            state = states[0]
            if state.isspace():
                state = 'NoFace'
            data ={
                "clip": clipId,
                "time": time,
                "state": state        
            }
            print(data)
            response = requests.post(url, data=data, headers=header)
            print(response.status_code)


# a = EmotionHandler("I:/cloned_win7/videos/赵冬芝/ceshi/","2017-12-20 10:35:01")
# # a.postAction('Basic aGV5dW5mYW46Mkdlemh1b3Fpbmc=',6)
# # a.getVideo2Img("I:/cloned_win7/videos/","tangmanyun")
# a.timestamp2time()
