from kavenegar import *


def Send_Otp_Code(*, phone_number, token1):
    print(str(token1) + "" + phone_number)
    try:
        api = KavenegarAPI(
            "6D656F3272486C44396C513973596A6D35374474786A7567414836636973364E754B7A4A6C6A56385575773D")
        params = {
            'receptor': phone_number,
            'template': 'otp',
            'token': token1,
            'token2': '',
            'token3': '',
            'type': 'sms',  # sms vs call
        }
        response = api.verify_lookup(params)
        print(response)
    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)


def Send_Otp_Code_Forgot_Link(*, phone_number, address="http://127.0.0.1:8000/account/reset-pass/", random_str):
    print(phone_number)
    try:
        token1 = random_str
        print(token1)
        api = KavenegarAPI(
            "6D656F3272486C44396C513973596A6D35374474786A7567414836636973364E754B7A4A6C6A56385575773D")
        params = {
            'receptor': phone_number,
            'template': 'link',
            'token': token1,
            'token2': '',
            'token3': '',
            'type': 'sms',  # sms vs call
        }
        response = api.verify_lookup(params)
        print(response)
    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)
