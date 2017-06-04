import sys
import requests
import keys

def caption_stored_image(img_file_path):
    url = keys.CV_END_POINT + "/analyze/"
    json = None
    data = open(img_file_path, "rb").read()
    headers = dict()
    headers["Ocp-Apim-Subscription-Key"] = keys.CV_KEY
    headers["Content-Type"] = "application/octet-stream"
    params = {"visualFeatures" : "Description"}

    try:
        print("m001\n")
        res = requests.request("POST", url, json=json, data=data,
                                    headers=headers, params=params)
        print("m002\n")
        result = res.json()
        print("m003\n")
        print(result)
        return result["description"]["captions"][0]["text"]
    except Exception as e:
        print("e.args", e.args)

def get_access_token(access_key):
    access_token_url = keys.TT_END_POINT + "/issueToken"
    headers = {"Ocp-Apim-Subscription-Key" : access_key}
    res = requests.request("POST", access_token_url, headers=headers)
    return res.text

def get_translation(text, lang1, lang2, access_token):
    headers = {"Accept" : "application/xml",
               "Authorization" : "Bearer " + access_token}
    params = {"from" : lang1, "to" : lang2,
              "maxTranslations" : 1000,
              "text" : text}
    url = "https://api.microsofttranslator.com/v2/http.svc/GetTranslations"
    try:
        print("m011\n")
        res = requests.request("POST", url,
                               headers=headers, params=params)
        print("m012\n")
        print(res.text)
        return res.text
    except Exception as e:
        print("e.args", e.args)

if __name__ == '__main__':
    print("main\n")
    argvs = sys.argv
    argc = len(argvs)
    if (argc != 2):
        print("argument error\n")
        quit()

    print("filename: {0}".format(argvs[1]))
    caption = caption_stored_image(argvs[1])
    print(caption)
    access_token = get_access_token(keys.TT_KEY)
    print(access_token)
    text = get_translation(caption, "en-us", "ja-jp", access_token)
    print(text)
