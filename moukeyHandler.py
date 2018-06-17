import sys
import requests
import json
class MouseKeyBoardMonitorHandler:

    keyPressedNum = ''
    mouseClickNum = ''
    allOperationNum = ''

    def __init__(self,file):
        self.file = file

    def file2Str(self):
       f = open(self.file,'r')
       lines = f.readlines()
       result = ''.join(lines)
       return result

    def file2List(self):
        result = self.file2Str()
        resultSectionList = result.split('\n')
        return resultSectionList[:-2]

    def collectNumbers(self):
        result = self.file2Str()
        self.keyPressedNum = result.count('pressed at')
        self.mouseClickNum = result.count('Released at')
        self.allOperationNum = len(self.file2List())
        return self.keyPressedNum, self.mouseClickNum, self.allOperationNum
    
    def getContentTyped(self):
        contentList = []
        dictArrow = {'Key.right':'→','Key.left':'←','Key.up':'↑','Key.down':'↓','Key.space':' ','Key.enter':'\\n','Key.backspace':'\\b','Key.caps_lock':'(caseUpDown)'}
        SectionList = self.file2List()
        for content in SectionList:
            lineSection = content.split(' ')
            if lineSection[1] != 'pressed':
                continue
            elif lineSection[0] in dictArrow.keys():
                singleContent = dictArrow[lineSection[0]]
                contentList.append(singleContent)
            else:
                contentList.append(lineSection[0])
        return ''.join(contentList)

    def getOperationTimestamp(self):
        timeList = []
        tmp = []
        timeDict = {}
        timeFeatureList = []
        SectionList = self.file2List()
        for content in SectionList:
            lineSection = content.split(' ')
            timeList.append(lineSection[-1])
        for timeSection in timeList:
            timeFragils = timeSection.split(':')
            timeFeature = timeFragils[0] + ':' + timeFragils[1]
            timeFeatureList.append(timeFeature)
        List = timeFeatureList.copy()
        timeFeatureSet = set(List)
        for timefeature in timeFeatureSet:
            timeDict[timefeature] = timeFeatureList.count(timefeature)
        return timeDict

    def getAuthorization(self,username,password):     
        import base64
        Authorization = username + ':' + password
        Authorization = Authorization.encode('utf-8')
        Authorization = base64.b64encode(Authorization)
        Authorization = Authorization.decode('utf-8')
        return Authorization

    def outputData(self):
        keyPressedNum, mouseClickNum, allOperationNum = self.collectNumbers()
        content = self.getContentTyped()
        timeDict = self.getOperationTimestamp()
        return keyPressedNum, mouseClickNum,allOperationNum,content,timeDict
    
    def postAction(self,username,password,clipId,date):
        operationurl = "http://127.0.0.1:8000/api/operations/"
        operationAccurateurl = "http://127.0.0.1:8000/api/operationtimes/"
        header = {
            'Authorization': "Basic " + self.getAuthorization(username,password)
        }
        keyPressedNum, mouseClickNum,allOperationNum,content,timeDict = self.outputData()
        data ={
            "clip": clipId,
            "keypressed_num": keyPressedNum,
            "mouseclicked_num": mouseClickNum,
            "alloperation_num": allOperationNum,
            "content": content
        }
        print(data)
        response = requests.post(operationurl, data=data, headers=header)
        print(response.text,response.status_code)

        clipUrl = "http://127.0.0.1:8000/api/clips/"+str(clipId)+"/"
        preRes = requests.get(clipUrl)
        preResult = preRes.text
        preResult = json.loads(preResult)
        operation = preResult["operations"]
        
        operationTmp = operation[0]
        operationId = operationTmp["id"]
        print(operationId)
        keys = sorted(timeDict.keys())
        for key in keys:
            data ={
                "operation": operationId,
                "time": date +'T'+ key,
                "times": str(timeDict[key])
            }
            print(data)
            response = requests.post(operationAccurateurl, data=data, headers=header)
            print(response.status_code)




# a = MouseKeyBoardMonitorHandler('../04150133倪佳慧/record.txt')
# # keyPressedNum, mouseClickNum, allOperationNum = a.collectNumbers()
# # print('该生输入的次数是：' + str(keyPressedNum) )
# # print('该生点击鼠标的次数是：' + str(mouseClickNum))
# # print('该生总体操作次数是：'+ str(allOperationNum))
# # print('该生输入的内容是：' + a.getContentTyped())
# # timeDict = a.getOperationTimestamp()
# # keys = sorted(timeDict.keys())
# # for key in keys:
# #     f = open('tmp','a')
# #     f.write(key + ':00 ' + str(timeDict[key]) + '\n')
# #     f.close()
# a.postAction("heyunfan","2Gezhuoqing",6,"2017-12-20")
