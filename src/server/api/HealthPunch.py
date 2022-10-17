# 自动健康打卡，取上次上传数据作为本次打卡数据
import json
import time
import traceback
import requests



# 如果需要修改提交的最新核酸检测的日期，请在此处修改，默认为上次填写的值（返回日期格式为"%Y-%m-%d"的字符串）
def getLastestPicker(lastDate):
    return lastDate


def healthFill(Authentication):
    pageHeaders = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Linux; U; Android 5.0.2; zh-cn; MI 2C Build/LRX22G) AppleWebKit/533.1 (KHTML, like Gecko)Version/4.0 MQQBrowser/5.4 TBS/025469 Mobile Safari/533.1 MicroMessenger/6.2.5.53_r2565f18.621 NetType/WIFI Language/zh_CN",
        "Authentication": Authentication,
    }
    try:
        # 获取wid
        response = requests.get("http://pdc.njtech.edu.cn/dfi/formOpen/loadFormListBySUrl?sUrl=wbfjIwyK",
                                headers=pageHeaders, allow_redirects=False)

        wid = json.loads(response.content)['data'][0]['WID']

        # 获取历史提交记录
        response = requests.get("http://pdc.njtech.edu.cn/dfi/formData/loadFormFillHistoryDataList?formWid={}&auditConfigWid=".format(
            wid), headers=pageHeaders, allow_redirects=False)
        jsonData = json.loads(response.content)

        # 判断Authentication是否有效
        if jsonData['code'] == 3001:
            message="❗❗❗健康打卡提交失败！\n身份认证失效，请重新获取Authentication"
            return AttributeError,message

        # 取最近一次提交数据，数据的结构和提交所需的结构不完全一致，进行修改后作为此次提交数据
        lastData = jsonData["data"][0]

        healthCode = []
        tourCode = []

        # 判断健康码、行程码是否过期
        try:
            healthCode = lastData['ONEIMAGEUPLOAD_KWYTQFT3'][1:-
                                                                1].split(', ')
            tourCode = lastData['ONEIMAGEUPLOAD_KWYTQFT5'][1:-
                                                            1].split(', ')
        except Exception as e:
            message="❗❗❗健康打卡提交失败！\n健康码或身份码过期，请手动打卡一次，下次即可继续自动打卡"
            return AttributeError,message

        dataMap = {
            "wid": "",
            "RADIO_KWYTQFSU": "本人知情承诺",   # 知情承诺
            "INPUT_KWYTQFSO": lastData['INPUT_KWYTQFSO'],   # 学号
            "INPUT_KWYTQFSP": lastData['INPUT_KWYTQFSP'],   # 姓名
            "SELECT_KX3ZXSAE": lastData['SELECT_KX3ZXSAE'],  # 学院
            "INPUT_KWYTQFSS": lastData['INPUT_KWYTQFSS'],   # 班级
            "INPUT_KX3ZXSAD": lastData['INPUT_KX3ZXSAD'],   # 手机号
            "INPUT_KWYUM2SI": lastData['INPUT_KWYUM2SI'],   # 辅导员
            "RADIO_KWYTQFSZ": lastData['RADIO_KWYTQFSZ'],   # 当前位置
            "RADIO_KWYTQFT0": lastData['RADIO_KWYTQFT0'],
            # 所在省市区
            "CASCADER_KWYTQFT1": lastData['CASCADER_KWYTQFT1'][1:-1].split(', '),
            "RADIO_KWYTQFT2": lastData['RADIO_KWYTQFT2'],   # 身体状况
            # 最新核酸检测时间
            "DATEPICKER_L8Z744C5": getLastestPicker(lastData['DATEPICKER_L8Z744C5']),
            # 下面这两行如果报出现异常一般是健康码行程码过期（一般两周左右会过期一次），需要自己重新打卡一次
            "ONEIMAGEUPLOAD_KWYTQFT3": healthCode,   # 健康码
            "ONEIMAGEUPLOAD_KWYTQFT5": tourCode,   # 行程码
            "LOCATION_KWYTQFT7": lastData['LOCATION_KWYTQFT7'],  # 定位
        }

        # 构建AMID（不知道有啥意义，可能用于迷惑人，就是个时间戳，前面可能会加一个随机数，但是不加也可以）
        AMID = "AM@"+str(int(time.time()*1000))

        # 发送表单数据
        postData = json.dumps({
            "auditConfigWid": "",
            "commitDate": time.strftime("%Y-%m-%d", time.localtime()),
            "commitMonth": time.strftime("%Y-%m", time.localtime()),
            "dataMap": dataMap,
            "formWid": wid,
            "userId": AMID,
        })
        response = requests.post('http://pdc.njtech.edu.cn/dfi/formData/saveFormSubmitData',
                                 data=postData.encode("utf-8"), headers=pageHeaders, allow_redirects=False)
        if json.loads(response.content)["message"] == "请求成功":
            response = requests.get("http://pdc.njtech.edu.cn/dfi/formData/loadFormFillHistoryDataList?formWid={}&auditConfigWid=".format(
                wid), headers=pageHeaders, allow_redirects=False)
            response = json.loads(response.content)["data"][0]
            result = {
                '学号': response['INPUT_KWYTQFSO'],
                '姓名': response['INPUT_KWYTQFSP'],
                '学院': response['SELECT_KX3ZXSAE'],
                '班级': response['INPUT_KWYTQFSS'],
                '当前位置': response['RADIO_KWYTQFSZ'],
                '所在省市区': response['CASCADER_KWYTQFT1'],
                '定位': response['LOCATION_KWYTQFT7'],
                '身体状况': response['RADIO_KWYTQFT2'],
                '最新核酸检测时间': response['DATEPICKER_L8Z744C5'],
            }
            message="健康打卡提交成功！\n此次提交的数据内容如下：\n%s"%(result)
            return 0,message
        else:
            message="❗❗❗健康打卡提交失败！\n数据提交失败，服务器未响应"
            return AttributeError,message
    except Exception as e:
        message="❗❗❗健康打卡提交失败！\n报错信息如下：\n"+traceback.format_exc()
        return AttributeError,message


# 如果第二个参数填True，会将健康码行程码填为不存在的图片，一样可以成功打卡，永远不会提示过期。（此举有风险，造成任何后果本人概不负责）

if __name__ == '__main__':
    authentication=''
    print(healthFill(authentication))