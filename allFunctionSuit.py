import requests
import json

class FaceDetect:
    # 免费的API账户
    api_key = 'YYWlWM1jThu4ZrMSqbId8CNJxWOkwvji'
    api_secret = '9fKu-BvIatXz02sto-j43R8cdwQIb1SC'
    # api_key = 'pwvmRPNkC0DGacq3ydWkZT18nKKa5TyD' #正式key
    # api_secret = 'ADQS6ca0h_jqd1UyhNjJVm3dmPgGzWLd'  #正式密码

    # 检测人脸（图或图url）
    _urlDetectFace = 'https://api-cn.faceplusplus.com/facepp/v3/detect'
    # 分析人脸（face_tokens最多五个人）
    _urlAnalyze = 'https://api-cn.faceplusplus.com/facepp/v3/face/analyze'
    # 在人群中找有没有这个人
    _urlSearch = 'https://api-cn.faceplusplus.com/facepp/v3/search'
    # 获取已经分析过的facetoken 细节
    _urlGetFaceDetail = 'https://api-cn.faceplusplus.com/facepp/v3/face/getdetail'
    # 设置facetoken的值，即人名
    _urlSetPersonName = 'https://api-cn.faceplusplus.com/facepp/v3/face/setuserid'
    # 创建faceset
    _urlSetCreate = 'https://api-cn.faceplusplus.com/facepp/v3/faceset/create'
    # 获取faceset细节
    _urlGetFaceSetDetail = 'https://api-cn.faceplusplus.com/facepp/v3/faceset/getdetail'
    # 在已有的faceset中加入facetoken
    _urlAddFace = 'https://api-cn.faceplusplus.com/facepp/v3/faceset/addface'
    # 在已有的faceset中移除facetoken
    _urlDeleteFace = 'https://api-cn.faceplusplus.com/facepp/v3/faceset/removeface'
    # 查看所有的Faceset
    _urlSelectAllFaceset = 'https://api-cn.faceplusplus.com/facepp/v3/faceset/getfacesets'


    # 创建faceset
    def _createFaceSet(self, display_name):
        payload = {
            'api_key': self.api_key, 
            'api_secret': self.api_secret,
            'display_name': display_name,
            'outer_id': display_name}
        response = requests.post(self._urlSetCreate, data=payload)
        # print(response.text)
        result = json.loads(response.text)
        faceSet_token = result["faceset_token"]
        return faceSet_token
        
    
    # 将face添加到faceset中
    def _addFace2Set(self, face_token, outer_id):
        payload = {
            'api_key': self.api_key, 
            'api_secret': self.api_secret,
            'outer_id': outer_id,
            # 待改进，太浪费钱了这里
            'face_tokens': face_token}
        response = requests.post(self._urlAddFace, data=payload)
        jsonDict = json.loads(response.text)
        face_count = jsonDict['face_count']
        return face_token, face_count, outer_id

    # 将faceset中某几个face移除
    def _removeFaceFromSet(self, face_token, outer_id):
        payload = {
            'api_key': self.api_key, 
            'api_secret': self.api_secret,
            'outer_id': outer_id,
            # 待改进，太浪费钱了这里
            'face_tokens': face_token}
        response = requests.post(self._urlDeleteFace,data=payload)
        jsonDict = json.loads(response.text)
        face_count = jsonDict['face_count']
        return face_token, face_count, outer_id

    # 移除所有face
    def _removeFaceSetAll(self, outer_id):
        self._removeFaceFromSet('RemoveAllFaceTokens',outer_id)

    # 查看所有faceSet
    def _checkAllFacesets(self):
        facesetTokens = []
        payload = {
            'api_key': self.api_key, 
            'api_secret': self.api_secret}
        response = requests.post(self._urlSelectAllFaceset,data=payload)
        jsonDict = json.loads(response.text)
        for obj in jsonDict['facesets']:
            facesetTokens.append(obj['faceset_token'])
        return facesetTokens
    
    #TODO:删除facesetsAPI


    # 查看faceset的细节1 此处可添加 中有多少人脸的具体token（未做）
    def _getFacesetDetailByID(self, outer_id):
        payload = {
            'api_key': self.api_key, 
            'api_secret': self.api_secret,
            'outer_id': outer_id}
        response = requests.post(self._urlGetFaceSetDetail, data=payload)
        jsonDict = json.loads(response.text)
        if 'faceset_token' in jsonDict.keys():
            faceset_token = jsonDict['faceset_token']
            face_count = jsonDict['face_count']
            return faceset_token, face_count, outer_id
        else:
            return None,None,None

    # 查看faceset的细节2
    def _getFacesetDetailByToken(self, faceset_token):
        payload = {
            'api_key': self.api_key, 
            'api_secret': self.api_secret,
            'faceset_token': faceset_token}
        response = requests.post(self._urlGetFaceSetDetail, data=payload)
        jsonDict = json.loads(response.text)
        face_count = jsonDict['face_count']
        outer_id =jsonDict['outer_id']
        return face_count, outer_id

    # 检测人脸(返回tokenlist)
    def _getFacetoken(self, image_file):
        face_tokenList = []
        files = {
            'image_file':('myface.jpg',open(image_file,'rb'))
        }
        payload = {
            'api_key': self.api_key, 
            'api_secret': self.api_secret
        }
        response = requests.post(self._urlDetectFace, data=payload, files=files)
        resultDict = json.loads(response.text)
        faceList = resultDict['faces']
        for paramDict in faceList:
            face_tokenList.append(paramDict['face_token'])
            print(paramDict['face_token'])
        return face_tokenList

    #检测人脸（针对情绪，对于毕业设计就行）
    def _getEmotion(self, image_file):
        files = {
            'image_file':('myface.jpg',open(image_file,'rb'))
        }
        payload = {
            'api_key': self.api_key, 
            'api_secret': self.api_secret,
            # value：值为一个 [0,100] 的浮点数，小数点后3位有效数字。数值越大表示笑程度高。threshold：代表笑容的阈值，超过该阈值认为有笑容。
            # pitch_angle：抬头roll_angle：旋转（平面旋转）yaw_angle：摇头(单位为角度)
            # 嘴部状态信息，包括以下字段。每个字段的值都是一个浮点数，范围 [0,100]，小数点后 3 位有效数字。字段值的总和等于 100。
                # surgical_mask_or_respirator：嘴部被医用口罩或呼吸面罩遮挡的置信度
                # other_occlusion：嘴部被其他物体遮挡的置信度
                # close：嘴部没有遮挡且闭上的置信度
                # open：嘴部没有遮挡且张开的置信度
            # 眼球位置与视线方向信息。返回值包括以下属性：
                # left_eye_gaze：左眼的位置与视线状态
                # right_eye_gaze：右眼的位置与视线状态
                # 每个属性都包括以下字段，每个字段的值都是一个浮点数，小数点后 3 位有效数字。
                # position_x_coordinate: 眼球中心位置的 X 轴坐标。
                # position_y_coordinate: 眼球中心位置的 Y 轴坐标。
                # vector_x_component: 眼球视线方向向量的 X 轴分量。
                # vector_y_component: 眼球视线方向向量的 Y 轴分量。
                # vector_z_component: 眼球视线方向向量的 Z 轴分量。
            'return_attributes': 'smiling,headpose,emotion,facequality,mouthstatus,eyegaze'
        }
        response = requests.post(self._urlDetectFace, data=payload, files=files)
        # print(response.text)
        return response.text

    # 检测此人在不在指定faceset中
    def _searchInFaceset(self, face_token, outer_id):
        payload = {
            'api_key': self.api_key, 
            'api_secret': self.api_secret,
            'outer_id': outer_id,
            'face_token': face_token}
        response = requests.post(self._urlSearch, data=payload)
        resultDict = json.loads(response.text)
        thresholds = resultDict['thresholds']
        millionLevel = thresholds['1e-5']
        confidence = resultDict['results'][0]['confidence']
        if confidence >= millionLevel:
            return resultDict['results'][0]['user_id']
        else:
            return '不存在这个人，请重试。'

    # 命名优质facetoken
    def _setfacetokenName(self, face_token, name):
        payload = {
            'api_key': self.api_key, 
            'api_secret': self.api_secret,
            'face_token': face_token,
            'user_id': name}
        response = requests.post(self._urlSetPersonName, data=payload)
        print(response.text)
    

    # 分析人脸(返回原生response，未经处理)
    def _analyzeFace(self, face_token):
        payload = {
            'api_key': self.api_key, 
            'api_secret': self.api_secret,
            'face_tokens': face_token,
            'return_attributes': 'smiling,headpose,emotion,facequality,mouthstatus,eyegaze'
        }
        response = requests.post(self._urlAnalyze, data=payload)
        return response.text


    # 创建faceset
    def createFaceset(self, outer_id):
        faceset_token = self._createFaceSet(outer_id)
        print('[MESSAGE]:' + faceset_token[:6] + ' 已创建成功<' + outer_id + '>！')
    
    # 添加face(TODO：添加错误信息提示)
    def addFace2Set(self, face_token, outer_id):
        face_token, face_count, outer_id = self._addFace2Set(face_token, outer_id)
        print('[MESSAGE]:' + face_token[:6] + ' 已成功添加到<' + outer_id + '>！')

    #删除face(TODO：添加错误信息提示)
    def removeFaceFromSet(self, face_token, outer_id):
        face_token, face_count, outer_id = self._removeFaceFromSet(face_token, outer_id)
        print('[MESSAGE]:' + face_token[:6] + ' 已从<' + outer_id + '>中删除！')

    # 删除指定faceset中所有facetoken(TODO：添加错误信息提示)
    def removeFaceSetAll(self, outer_id):
        self._removeFaceSetAll(outer_id)
        print('[MESSAGE]:所有facetoken已从<' + outer_id + '>中删除！')

    # 查看所有facesets
    def checkAllFacesets(self):
        facesetTokenList = self._checkAllFacesets()
        print('[MESSAGE]:您的这个账号下的面部数据集')
        for facesetToken in facesetTokenList:
            face_count, outer_id = self._getFacesetDetailByToken(facesetToken)
            print('   ' + facesetToken[:6] + ' '+ str(face_count) +'份 '+ outer_id)

    # 查看某个faceset
    def checkFacesets(self,outer_id):
        faceset_token, face_count, outer_id = self._getFacesetDetailByID(outer_id)
        if not faceset_token:
            print('[MESSAGE]:there is no facetokenSet')
            return False
        else:
            print('   ' + faceset_token[:6] + ' '+ str(face_count) +'份 '+ outer_id )
            return True

    # 检测此人在不在faceset中(image输入方法)
    def searchInFacesetWithImage(self, image_file, outer_id):
        token_list = self._getFacetoken(image_file)
        result = self._searchInFaceset(token_list[0], outer_id)
        print('查询的结果是：' + result)
    
    # 检测此人在不在faceset中(群体token输入方法，要for 遍历)
    def searchInFacesetWithToken(self, face_token, outer_id):
        result = self._searchInFaceset(face_token, outer_id)
        print('查询的结果是：' + result)
    
    # 从图像到表情的识别过程流图(DetectFace方法部分) 
    ### 待优化（更为可读性和文件输出）
    def outputEmotionAsFileWithDetect(self, image_file):
        jsonString = self._getEmotion(image_file)
        jsonDict = json.loads(jsonString)
        faceList = jsonDict['faces']
        for obj in faceList:
            faceAttr = obj['attributes']
            emotionAll = faceAttr['emotion']
            for k,j in emotionAll.items():
                if j == max(emotionAll.values()):
                    emotion = k
            headpose = faceAttr['headpose']
            eyegaze = faceAttr['eyegaze']
            smile = faceAttr['smile']
            mouthstatus = faceAttr['mouthstatus']
            facequality =  faceAttr['facequality']
            Attributes = {
                'emotion': emotion,
                'headpose': headpose,
                'eyegaze': eyegaze,
                'smile': smile,
                'mouthstatus': mouthstatus, 
                'facequality': facequality
            }
            print(Attributes)
    #只输出表情
    def outputEmotionAsFileWithDetectJustEmotion(self, image_file):
        try:
            jsonString = self._getEmotion(image_file)
            jsonDict = json.loads(jsonString)
            faceList = jsonDict['faces']
            for obj in faceList:
                faceAttr = obj['attributes']
                emotionAll = faceAttr['emotion']
                for k,j in emotionAll.items():
                    if j == max(emotionAll.values()):
                        emotion = k
                # Attributes = {
                #     "emotion": "\"" + emotion + "\""
                # }
                Attributes = "{\"emotion\":\"" + emotion + "\"}"
            return Attributes
        except:
            # ErrorAttr = {}
            ErrorAttr = "{\"emotion\":\" \"}"
            return ErrorAttr
            

    # 从图像到表情的识别过程流图(AnalyzeFace方法部分)
    def outputEmotionAsFileWithAnalyze(self, image_file):
        dictEasyRead = {}
        face_tokenList = self._getFacetoken(image_file)
        for face_token in face_tokenList:
            thisResult = self._analyzeFace(face_token)
            resultDict = json.loads(thisResult)
            face = resultDict['faces'][0]['attributes']            
            emotionAll = face['emotion']
            for k,j in emotionAll.items():
                if j == max(emotionAll.values()):
                    emotion = k
            headpose = face['headpose']
            eyegaze = face['eyegaze']
            smile = face['smile']
            mouthstatus = face['mouthstatus']
            facequality =  face['facequality']
            Attributes = {
                'emotion': emotion,
                'headpose': headpose,
                'eyegaze': eyegaze,
                'smile': smile,
                'mouthstatus': mouthstatus, 
                'facequality': facequality
            }
            dictEasyRead[face_token] = Attributes
        print(dictEasyRead)

    # 命名图片中的人脸并把他加入到某个faceset中（最好使用在只有一张清晰人脸时）
    def faceInfoInit(self, image_file, Name, outer_id):
        facetokenList = self._getFacetoken(image_file)
        self._setfacetokenName(facetokenList[0], Name)
        if not self.checkFacesets(outer_id):
            self.createFaceset(outer_id)
            self._addFace2Set(facetokenList[0], outer_id)
        else:
            self._addFace2Set(facetokenList[0], outer_id)
        print('[MESSAGE]:成功添加人像' + facetokenList[0][:6] + '到' + outer_id + '中')

    # 查看输入的照片里有谁
    def checkWhoIsInPhoto(self, image_file, outer_id):
        tokenList = self._getFacetoken(image_file)
        for token in tokenList:
            self.searchInFacesetWithToken(token, outer_id)



# a = FaceDetect()
# # ab = a._getFacetoken('C:/Users/yunfa/Pictures/Camera Roll/TIM图片20171127141157.jpg')
# # print(len(ab))
# # a.faceInfoInit('C:/Users/yunfa/Pictures/Camera Roll/WIN_20171128_15_33_00_Pro.jpg', '眭景明', 'wangsuihechao')
# a.searchInFacesetWithImage('C:/Users/yunfa/Pictures/Camera Roll/IMG_2401.JPG', 'wangsuihechao')

# a.checkFacesets('test201712131912')
# a.addFace2Set('d4981f4896d1490087928fef6cea2e61', '第一次中文转码尝试')
# a.removeFaceSetAll('第一次中文转码尝试')
# a.outputEmotionAsFileWithAnalyze('C:/Users/yunfa/Pictures/Camera Roll/WIN_20171123_11_28_50_Pro.jpg')\

if __name__== '__main__':
    a = FaceDetect()
    a.checkFacesets('wangsuihechao')
    # a.faceInfoInit('C:/Users/yunfa/Pictures/Camera Roll/IMG_2401.JPG', '曽琦', 'wangsuihechao')
    # a.checkWhoIsInPhoto('C:/Users/yunfa/Pictures/Camera Roll/TIM图片20171127141157.jpg','wangsuihechao')