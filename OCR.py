import requests
import base64

def baidu_ocr(image_path, recognize_granularity='small'):
    
    access_token = "24.dc3e85384fb5991797758fac4bb5fe39.2592000.1715675942.282335-48885010"
    
    url = "https://aip.baidubce.com/rest/2.0/ocr/v1/numbers"
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    params = {'access_token': access_token, 'recognize_granularity': recognize_granularity}
    with open(image_path, 'rb') as file:
        image_data = file.read()
    image_base64 = base64.b64encode(image_data).decode()
    data = {'image': image_base64}
    
    # Send OCR request
    response = requests.post(url, headers=headers, params=params, data=data)
    return response