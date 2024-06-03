def Send_Otp_Code(*, phone_number, message):
    print(message + "" + phone_number)
    # try:
    #     api = KavenegarAPI("61535137624C4B30383758576C77624C5774772F36315133764D4B6D57786C746F356F392F3967757145493D")
    #     params = {"sender": "", "receptor": phone_number, "message": message}
    #     response = api.sms_send(params)
    #     print(response)
    # except APIException as e:
    #     print(e)
    # except HTTPException as e:
    #     print(e)


# def Send_Otp_Code_Forgot_Link(*, to, address="http://127.0.0.1:8000/account/reset-pass/", random_str):
def Send_Otp_Code_Forgot_Link(*, to, address="http://192.168.43.123:3030/forgot-password/", random_str):
    print(to)
    print(f"{address}{random_str}/")