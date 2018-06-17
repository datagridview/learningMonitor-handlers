from EmotionHandler import EmotionHandler
from processHandler import ProcessHandler
from moukeyHandler import MouseKeyBoardMonitorHandler
from heartbeatHandler import heartbeatHandler
from UserHandler import UserHandler
from StateHandler import StateHandler
import argparse
# def _argparse():
    # parser = argparse.ArgumentParser(description='learningStateAnalyzeOutput')
    # parser.add_argument('-a','--addStu')
    # parser.add_argument()
    # parser.add_argument()
    # parser.add_argument()
    # parser.add_argument()
    # parser.add_argument()

def getVideo2Img(videoPath,videoName):
    os.mkdir(videoPath + videoName)
    os.system("ffmpeg -ss 00:00 -i "+ videoPath + videoName + ".mp4 -f image2 -r 0.2 " + videoPath + videoName + "/%3d.jpg")
    return videoPath + videoName

def addStu(username,password):
    user = UserHandler()
    return user.createStudent(username,password)

def createNewclip(username,password,clip_outer_id,tested):
    user = UserHandler()
    return user.createClip(username,password,clip_outer_id,tested)

def nowhandleState(username,password,clip_id,img_path, timeStart, process_path,record,fileName):
    handler = StateHandler(img_path, timeStart, process_path,record,fileName)
    return handler.postAction(username,password,clip_id)

def handleState(username,password,clip_id,img_path, timeStart, processPath,record,hardwareId, startDate, endDate):
    handler = StateHandler(img_path, timeStart, processPath,record,hardwareId, startDate, endDate)
    return handler.postAction(username,password,clip_id)

def handleEmotion(username,password,clip_id,imgSet_path,timeStart):
    handler = EmotionHandler(imgSet_path,timeStart)
    return handler.postAction(username,password,clip_id)

def handleProcess(username,password,clip_id,process_path):
    handler = ProcessHandler(process_path)
    return handler.postAction(username,password,clip_id)

def handleMoukey(username,password,clipId,date,record):
    handler = MouseKeyBoardMonitorHandler(record)
    return handler.postAction(username,password,clipId,date)

def handleHeartbeat(username, password, clipId, hardwareId):
    handler = heartbeatHandler()
    return handler.postAction(username, password, clipId, hardwareId)

def nowhandleHeartbeat(username, password, clip_id, fileName):
    handler = heartbeatHandler()
    return handler.postTmp(username, password, clip_id, fileName)

# def __main__():
    # videoPath mp4存在的路径
    # videoName mp4文件名
    # tested 什么时候学习的 2017-12-20T14:20:01
    # timeStart 视频文件第一帧时间 2017-12-20 14:20:01
    # process_path 路径+processInfo.txt
    # record 路径+record.txt
    # date 2017-12-20
    # hardwareId 
    # startDate/endDate 2017-12-20T08
        ##要求 handleEmotion要在handleState之前执行

    # imgSet_path = getVideo2Img(videoPath,videoName)
    # clip_id = createClip(admin,adminPassword,username,password,clip_outer_id,tested)
    # handleState(username,password,clip_id,imgSet_path, timeStart, process_path,record)
    # handleEmotion(username,password,clip_id,imgSet_path,timeStart)
    # handleProcess(username,password,clip_id,process_path)
    # handleMoukey(username,password,clip_id,date,record)
    # handleHeartbeat(username, password, clip_id, hardwareId, startDate, endDate)
    # nowhandleHeartbeat(username, password, clip_id, fileName)#目前
    # nowhandleState(username,password,clip_id,img_path, timeStart, process_path,record,fileName) #目前
    # handleState(username,password,clip_id,img_path, timeStart, processPath,record,hardwareId, startDate, endDate) #未来，这种模式适合把handleState放在最前面执行

    
    
# addStu("xueyu","wasd123456")
# clip_id = createNewclip("xueyu","wasd123456","薛禹的第一次测试","2017-12-20T11:42:00")
# handleEmotion("xueyu","wasd123456", 14 ,"C:/Users/yunfa/Desktop/进程处理/04140226薛禹/cut/", "2017-12-20T11:42:04")
# nowhandleHeartbeat("xueyu","wasd123456", 14, '3-4')
# handleProcess("xueyu","wasd123456", 14, "C:/Users/yunfa/Desktop/进程处理/04140226薛禹/processInfo.txt")
# handleMoukey("xueyu","wasd123456", 14, "2017-12-20","C:/Users/yunfa/Desktop/进程处理/04140226薛禹/Record.txt")
# nowhandleState("xueyu","wasd123456", 14 ,"C:/Users/yunfa/Desktop/进程处理/04140226薛禹/cut/", "2017-12-20T11:42:04", "C:/Users/yunfa/Desktop/进程处理/04140226薛禹/processInfo.txt","C:/Users/yunfa/Desktop/进程处理/04140226薛禹/Record.txt","3-4") #以此为例
