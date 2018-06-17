import requests
import json
import logging
import math
class heartbeatHandler:
    host = "192.168.235.130" #根据实际情况变化
    Tenant = "sitewhere1234567890"
    httpPort = "8080"
    tokenDict = {}
    headers = {
        "Host": host + ":"+ httpPort,
        "Authorization": "Basic YWRtaW46cGFzc3dvcmQ=",
        "X-Sitewhere-Tenant": Tenant,
    }
    n = 1
    # 修改
    def getHeartbeatMetaData(self, hardwareId, startDate, endDate):

        #此处时间区间可以改格式
        startDate = startDate + ":00:00.000+0800"
        endDate = endDate + ":00:00.000+0800"

        getTokenUrl = "http://" + self.host + ":" + self.httpPort +"/sitewhere/api/devices/" + hardwareId
        payload = {'includeSpecification': 'false', 'includeAssignment': 'true','includeSite': 'false','includeAsset':'false','includeNested':'false'}
        response = requests.get(getTokenUrl, headers=self.headers,params=payload)
        jsonText = json.loads(response.text)
        assignment = jsonText["assignment"]
        token = assignment["token"]
        getHeartBeatUrl = "http://" + self.host + ":"+ self.httpPort + "/sitewhere/api/assignments/" + token +"/measurements"     
        resultsLenList = []
        rawList = []
        payloadOri = {'page': str(self.n), 'pageSize': '1000',"startDate":startDate,"endDate":endDate}
        response = requests.get(getHeartBeatUrl, headers=self.headers, params=payloadOri)
        jsonTextOri = json.loads(response.text)
        results = jsonTextOri["results"]
        for measurement in results:
            date = measurement["eventDate"]          
            rawList.append(date.split('.')[0]+" "+ str(measurement["measurements"]["heartbeatRate"]))
        while len(results):
            self.n = self.n + 1
            resultsLenList.append(len(results))
            ###输入字典
            for result in results:
                date = result["eventDate"]
                rawList.append(date.split('.')[0]+ " " +str(result["measurements"]["heartbeatRate"]))
                # if tested == date：
                #     todayList.append(date.split('.')[0]+ " " +str(result["measurements"]["heartbeatRate"]))
                ###
                # with open(tokenDict[token] + ".json","a") as f:
                #     for result in results:
                #         f.write(json.dumps(result["eventDate"])+ " " +json.dumps(result["measurements"]["heartbeatRate"]) + '\n')
            payloadLas = {'page': str(self.n), 'pageSize': '1000',"startDate":startDate,"endDate":endDate}
            # print("其他请求"+ getHeartBeatUrl + payloadLas['page'])
            response = requests.get(getHeartBeatUrl, headers=self.headers, params=payloadLas)
            jsonTextLas = json.loads(response.text)
            results = jsonTextLas["results"]
        return rawList        



    def fileSerializer(self,hardwareId,startDate, endDate):
        heartList = []
        dataDict = {}
        heartbeatArrary = []
        rawList = self.getHeartbeatMetaData(hardwareId, startDate, endDate)
        heartbeatGenerator = (x for x in rawList)
        value = next(heartbeatGenerator)
        while value:
            try:
                time, heartbeat = self.getTimeAndHeartbeat(value)
                value = next(heartbeatGenerator)
                if value:
                    timeLat, heartbeatLat = self.getTimeAndHeartbeat(value)
                    heartbeatArrary.append(math.floor(float(heartbeat)))
                    if timeLat != time:
                        dataDict[time] = math.floor(sum(heartbeatArrary)/len(heartbeatArrary))
                        heartbeatArrary = []
                    value = next(heartbeatGenerator)
            except StopIteration:
                break 
        keys = sorted(dataDict.keys())
        for key in keys:
            heartList.append(key + ' ' + str(dataDict[key]))
        f = open("heartbeat",'w')
        for content in heartList:
            f.write(content)
        f.close()
        return heartList

    def getTimeAndHeartbeat(self,dataLine):
        dataList = dataLine.split(' ')
        return dataList[0], dataList[1]

    def getAuthorization(self,username,password):     
        import base64
        Authorization = username + ':' + password
        Authorization = Authorization.encode('utf-8')
        Authorization = base64.b64encode(Authorization)
        Authorization = Authorization.decode('utf-8')
        return Authorization

    

    def postAction(self,username, password, clipId, hardwareId,startDate, endDate):
        url = 'http://127.0.0.1:8000/api/heartbeats/'
        content = self.fileSerializer(hardwareId, startDate, endDate)
        header = {
            'Authorization': "Basic " + self.getAuthorization(username,password)
        }
        for line in content:
            listTmp = line.split(' ')
            time = listTmp[0]
            beat_nums = listTmp[1]
            data ={
                "clip": clipId,
                "beat_nums": beat_nums,
                "time": time
            }
            # response = requests.post(url, data=data, headers=header)
            # print(response.status_code)
            print(data)


    ###
    ##以下是临时方法，正是方法将被删除
    ###



    def fileS(self,file):
        heartList = []
        dataDict = {}
        heartbeatArrary = []
        f = open(file,'r')
        value = f.readline()
        while value:
            try:
                time, heartbeat = self.getTimeAndHeartbeat(value)
                value = f.readline()
                if value:
                    timeLat, heartbeatLat = self.getTimeAndHeartbeat(value)
                    heartbeatArrary.append(math.floor(float(heartbeat)))
                    if timeLat != time:
                        dataDict[time] = math.floor(sum(heartbeatArrary)/len(heartbeatArrary))
                        heartbeatArrary = []
                    value = f.readline()
            except StopIteration:
                break 
        keys = sorted(dataDict.keys())
        for key in keys:
            heartList.append(key + ' ' + str(dataDict[key]))
        return heartList
        
    def postTmp(self,username, password, clipId, file):
        url = 'http://127.0.0.1:8000/api/heartbeats/'
        content = self.fileS(file)
        header = {
            'Authorization': "Basic " + self.getAuthorization(username,password)
        }
        # print(startDate)
        for line in content:
            listTmp = line.split(' ')
            time = listTmp[0]
            beat_nums = listTmp[1]
            data ={
                "clip": clipId,
                "beat_nums": beat_nums,
                "time": time
            }
            print(data)
            response = requests.post(url, data=data, headers=header)
            print(response.status_code)
            
# a = heartbeatHandler()
# a.postTmp("heyunfan","2GEzhuoqing",2,"C:/Users/yunfa/Desktop/新建文件夹/getHeartBeatRate/heartbeatsCollection/1-1")
# for n in range(1,10):
#     a.fileSerializer("Arduino0" + str(n))