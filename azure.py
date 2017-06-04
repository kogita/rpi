import sys
import requests
import xml.etree.ElementTree as ET
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
        res = requests.request("POST", url, json=json, data=data,
                                    headers=headers, params=params)
        result = res.json()
#        print(result)
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
        res = requests.request("POST", url,
                               headers=headers, params=params)
        return extract_transleted_text(res.text.encode('utf-8'))
    except Exception as e:
        print("e.args", e.args)

def extract_transleted_text(xml_string):
    try:
        parsed = ET.fromstring(xml_string)
        return parsed[1][0][4].text
    except Exception as e:
        print("e.args", e.args)

if __name__ == '__main__':
    argvs = sys.argv
    argc = len(argvs)
    if (argc != 2):
        print("argument error\n")
        quit()

    print("filename: {0}".format(argvs[1]))
    caption = caption_stored_image(argvs[1])
    print(caption)
    access_token = get_access_token(keys.TT_KEY)
#    print(access_token)
    text = get_translation(caption, "en-us", "ja-jp", access_token)
    print(text)
