

AZ_IRANIAN_BANK_GATEWAYS = {
    "GATEWAYS": {
        # "BMI": {
        #     "MERCHANT_CODE": "<YOUR MERCHANT CODE>",
        #     "TERMINAL_CODE": "<YOUR TERMINAL CODE>",
        #     "SECRET_KEY": "<YOUR SECRET CODE>",
        # },
        # "SEP": {
        #     "MERCHANT_CODE": "<YOUR MERCHANT CODE>",
        #     "TERMINAL_CODE": "<YOUR TERMINAL CODE>",
        # },
        # "ZARINPAL": {
        #     "MERCHANT_CODE": "<YOUR MERCHANT CODE>",
        #     "SANDBOX": 0,  # 0 disable, 1 active
        # },
        # "IDPAY": {
        #     "MERCHANT_CODE": "<YOUR MERCHANT CODE>",
        #     "METHOD": "POST",  # GET or POST
        #     "X_SANDBOX": 0,  # 0 disable, 1 active
        # },
        # "ZIBAL": {
        #     "MERCHANT_CODE": "<YOUR MERCHANT CODE>",
        # },
        # "BAHAMTA": {
        #     "MERCHANT_CODE": "<YOUR MERCHANT CODE>",
        # },
        # "MELLAT": {
        #     "TERMINAL_CODE": "<YOUR TERMINAL CODE>",
        #     "USERNAME": "<YOUR USERNAME>",
        #     "PASSWORD": "<YOUR PASSWORD>",
        # },
        "PAYV1": {
            "MERCHANT_CODE": "<YOUR MERCHANT CODE>",
            "X_SANDBOX": 1,  # 0 disable, 1 active
        },
    },
    "IS_SAMPLE_FORM_ENABLE": True,  # اختیاری و پیش فرض غیر فعال است
    "DEFAULT": "PAYV1",  # "BMI",
    "CURRENCY": "IRR",  # اختیاری
    "TRACKING_CODE_QUERY_PARAM": "tc",  # اختیاری
    "TRACKING_CODE_LENGTH": 16,  # اختیاری
    "SETTING_VALUE_READER_CLASS": "azbankgateways.readers.DefaultReader",  # اختیاری
    # "BANK_PRIORITIES": [
    #     "BMI",
    #     "SEP",
    #     # and so on ...
    # ],  # اختیاری
    "IS_SAFE_GET_GATEWAY_PAYMENT": False,  # اختیاری، بهتر است True بزارید.
    "CUSTOM_APP": None,  # اختیاری
}


# برای استفاده از درگاه بانک ملی و سامان تنظیم SECURE_REFERRER_POLICY در setting جنگو به صورت زیر الزامیست

SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"


# az-iranian-bank-gateways https://stackoverflow.com/questions/62047354/build-absolute-uri-with-https-behind-reverse-proxy/65934202#65934202
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
