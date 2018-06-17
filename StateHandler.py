from functools import reduce
from EmotionHandler import EmotionHandler
from processHandler import ProcessHandler
from moukeyHandler import MouseKeyBoardMonitorHandler
from heartbeatHandler import heartbeatHandler
import requests
import json
class StateHandler:
    n = 1
    # 临时用
    def __init__(self,img_path, timeStart, processPath,record, fileName):
        self.img_path = img_path
        self.timeStart = timeStart
        self.processPath = processPath
        self.record = record
        self.fileName = fileName

    # 正式用
    # def __init__(self,img_path, timeStart, processPath,record, hardwareId, startDate, endDate):
    #     self.img_path = img_path
    #     self.timeStart = timeStart
    #     self.processPath = processPath
    #     self.record = record
    #     self.hardwareId = hardwareId
    #     self.startDate = startDate
    #     self.endDate = endDate
    
    def getEmotionDict(self):
        emotionDict = {}
        emotionHandler = EmotionHandler(self.img_path, self.timeStart)
        emotionlist = emotionHandler.timestamp2timeWithFile()
        for emotion in emotionlist:
            emotionDict.update(json.loads(emotion))
        return emotionDict


    def getOperationDict(self):
        operationDict = {}
        a = MouseKeyBoardMonitorHandler(self.record)
        keyPressedNum, mouseClickNum, allOperationNum, content,timeDict = a.outputData()
        keys = sorted(timeDict.keys())
        date = self.timeStart.split("T")[0]
        for key in keys:
            operationDict[date+"T"+key] = str(timeDict[key])
        return operationDict

    def getHeartbeatDict(self,file_name):
        heartbeatDict = {}
        a = heartbeatHandler()
        # 临时用
        heartbeatList = a.fileS(file_name)
        # 正式版
        #heartbeatList = a.fileSerializer(self,hardwareId,startDate, endDate)
        for heartbeat in heartbeatList:
            heartbeatPart = heartbeat.split(' ')
            heartbeat = heartbeatPart[1]
            heartbeatDict[heartbeatPart[0]] = [heartbeat,]
        return heartbeatDict

    def getProcessDict(self):
        processHandler = ProcessHandler(self.processPath)
        processList = processHandler.judgeInSectionList()
        processDict = {}
        for process in processList:
            process = process[:-1]
            processPart = process.split(' ')
            processDict[processPart[0]] = processPart[1]+' '+processPart[2]
        return processDict



    def dictInsertaion(self, stateDict, individualDict):
        for key in individualDict.keys():
            if key in stateDict.keys():
                stateDict[key].append(individualDict[key])
            else:
                stateDict[key] = []            
                stateDict[key].extend(['' for i in range(self.n)])
                stateDict[key].append(individualDict[key])
        for value in stateDict.values():
            try:
                tmp = value[self.n]
            except:
                value.append('')
        self.n = self.n + 1
        return stateDict
    
    def getSerializerData(self):
        dicta = reduce(self.dictInsertaion,[self.getHeartbeatDict(self.fileName),self.getEmotionDict(),self.getOperationDict(),self.getProcessDict()])
        return dicta

    def getAuthorization(self,username,password):     
        import base64
        Authorization = username + ':' + password
        Authorization = Authorization.encode('utf-8')
        Authorization = base64.b64encode(Authorization)
        Authorization = Authorization.decode('utf-8')
        return Authorization

    def postAction(self,username,password,clipId):
        url = "http://127.0.0.1:8000/api/states/"
        header = {
            'Authorization': "Basic " + self.getAuthorization(username,password)
        }
        resultDict = self.getSerializerData()
        lista = sorted(resultDict.keys())
        for time in lista:
            result = resultDict[time]
            heartbeats = result[0]
            emotion = result[1]
            operation_num = result[2]
            if result[3] != '':
                processFragile = result[3].split(' ')
                process_flag = processFragile[0]
                process_name = processFragile[1]
            else:
                process_flag = ''
                process_name = ''
            if emotion.isspace():
                emotion = 'NoFace'
            data ={
                "clip": clipId,
                "time": time,
                "heartbeats": heartbeats,
                "emotion": emotion,
                "operation_num": operation_num,
                "process_flag": process_flag,
                "process_name": process_name
            }
            print(data)
            response = requests.post(url, data=data, headers=header)
            print(response.status_code)



# a = StateHandler("I:/cloned_win7/videos/赵冬芝/ceshi/","2017-12-20 10:35:01",'../04150133倪佳慧/processInfo.txt','../04150133倪佳慧/record.txt','3-4')
# a.postAction("heyunfan","2Gezhuoqing","2")