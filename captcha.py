
import setting
import time, requests, sys, os, json
# from twocaptcha import TwoCaptcha

LOCAL_IMAGE_PATH = 'inputs/grid-capcha-images/%s.jpeg'
API_KEY = setting.configSecret['gridCaptcha']['key']

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

def saveImage(imageUrl: str, threadIndex: int, loopIndex: int):
    fileName = '%d-%d-%s' % (threadIndex, loopIndex, time.time())
    data = requests.get(imageUrl).content
    f = open(__getImagePath(fileName), 'wb')
    f.write(data)
    f.close()
    return fileName

# def sendQuestion(instruction: str, fileName: str):
#     api_key = setting.configSecret['gridCaptcha']['key']
#     solver = TwoCaptcha(api_key)
#     try:
#         result = solver.grid(__getImagePath(fileName),
#             textinstructions=instruction,
#             # rows=3,
#             # cols=3,
#             # lang='vi',
#             # json=1,
#             # header_acao=1
#         )
#         result = result['code'].replace('click:', '').split('/')
#         return result
#     except Exception as e:
#         print(e)
#         return []

def sendQuestion(instruction: str, fileName: str):
    print('instruction: %s' % instruction)
    instruction = instruction.replace("\n", " ")
    print('instruction: %s' % instruction)

    captchaIdResult = getCaptchaIdResult(instruction, fileName)
    time.sleep(5)
    result = getCaptchaResult(captchaIdResult)
    return result

def getCaptchaIdResult(instruction: str, fileName: str):
    url = 'https://2captcha.com/in.php'
    # api_key = setting.configSecret['gridCaptcha']['key']
    data = {
        'key': API_KEY,
        'method': 'post',
        'recaptcha': 1,
        'textinstructions': instruction,
        'json': 1
    }

    with open(__getImagePath(fileName), 'rb') as file:
        response = requests.post(url, data=data, files={'file': file})
        response = json.loads(response.text)
        print(response)

        if 'payload' not in fileName : os.remove(__getImagePath(fileName))
        return response['request']
    
def getCaptchaResult(captchaIdResult: int):
    url = 'https://2captcha.com/res.php'
    # api_key = setting.configSecret['gridCaptcha']['key']
    params = {
        'key': API_KEY,
        'action': 'get',
        'id': captchaIdResult,
        'json': 1
    }

    response = requests.get(url, params=params)
    response = json.loads(response.content)
    print(response)

    if response['request'] == 'CAPCHA_NOT_READY':
        time.sleep(5)
        response = requests.get(url, params=params)
        response = json.loads(response.content)
        print(response)

    return response['request'].replace('click:', '').split('/')

def __getImagePath(fileName: str):
    return LOCAL_IMAGE_PATH % fileName


# imageUrl = 'https://static.remove.bg/sample-gallery/graphics/bird-thumbnail.jpg'
# saveImage(imageUrl, 0, 1)

# t1 = 'Chọn tất cả hình ảnh có xe buýt'
# t2 = 'payload'

# t1 = "Select all squares with\nbuses"
# t2 = 'payload_2'

# t1 = "Select all squares with bicycles"
# t2 = 'payload_3'

# result = sendQuestion(t1, t2)
# print(result)

