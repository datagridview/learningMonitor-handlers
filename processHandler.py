import sys
import requests
class ProcessHandler:
    def __init__(self,file):
        self.file = file

    def getAuthorization(self,username,password):     
        import base64
        Authorization = username + ':' + password
        Authorization = Authorization.encode('utf-8')
        Authorization = base64.b64encode(Authorization)
        Authorization = Authorization.decode('utf-8')
        return Authorization

    def divideListIntoNameSection(self,timeBlock):
        processList = []
        processTimetableList = timeBlock.split('\n')
        timeStamp = processTimetableList[0].split(' ')
        timeStamp = 'T'.join(timeStamp)
        processTimetableList = processTimetableList[2:]
        for processName in processTimetableList:
            splitedList = processName.split(' running ')
            processList.append(splitedList[0])
        return processList,timeStamp

    def compareSections(self,timeBlockPre,timeBlockLatter):
        tmpList = []
        for process in timeBlockLatter:
            try:
                index = timeBlockPre.index(process)
            except ValueError:
                continue
            bePoped = timeBlockPre.pop(index)
            tmpList.append(bePoped)
        for tmpProcess in tmpList:
            timeBlockLatter.remove(tmpProcess)
        return timeBlockPre,timeBlockLatter

    def getTwoList(self):
        SectionList = self.file2List()
        return SectionList[0:-2],SectionList[1:]

    def file2List(self):
        f = open(self.file,'r')
        lines = f.readlines()
        result = ''.join(lines)
        resultSectionList = result.split('\n\n')
        # print(len(resultSectionList))
        return resultSectionList

    def judgeInSectionList(self):
        processList = []
        cycle1,cycle2 = self.getTwoList()
        # f = open('processSerialization' ,'a')
        for processPre, processLatter in zip(cycle1,cycle2):
            processPreList, timeStampPre = self.divideListIntoNameSection(processPre)
            processLatterList, timeStampLat = self.divideListIntoNameSection(processLatter)
            pre,lat = self.compareSections(processPreList,processLatterList)
            if len(pre):
                section = timeStampLat + ' close ' +'&'.join(pre)+'\n'
                # f.write(section)
                processList.append(section)
            elif len(lat):
                section = timeStampLat + ' open '+ '&'.join(lat)+'\n'
                # f.write(section)
                processList.append(section)
            else:
                pass
                # print(timeStampLat + ' 没有变化')
        # f.close()
        return processList

    def postAction(self,username,password,clipId):
        url = "http://127.0.0.1:8000/api/processes/"
        header = {
            'Authorization': "Basic " + self.getAuthorization(username,password)
        }
        processList = self.judgeInSectionList()
        for process in processList:
            listTmp = process.split(' ')
            time = listTmp[0]
            flag = listTmp[1]
            process_name = listTmp[2]
            process_name = process_name.split('\n')[0]
            # print(process_name)
            data ={
                "clip": clipId,
                "time": time,
                "flag": flag,
                "process_name": process_name        
            }
            print(data)
            response = requests.post(url, data=data, headers=header)
            print(response.status_code)

# a = ProcessHandler('../04150133倪佳慧/processInfo.txt')
# # a.postAction('heyunfan','2Gezhuoqing',2)
# a.judgeInSectionList()