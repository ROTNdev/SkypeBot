from apiclient.discovery import build
from pykeyboard import PyKeyboard
from pygoogle import pygoogle

import Var
import time
import urllib2
import urllib

__author__ = 'vilsol'


def getBot():
    return Var.bot


def now():
    return time.strftime("%x %X")


def pastebin(text):
    if type(text) == str:
        text = unicode(text).encode('utf-8')
    else:
        text = unicode("".join(text)).encode('utf-8')

    target = {"content": text, "poster": "Skype Bot", "syntax": "text"}

    try:
        req = urllib2.urlopen("http://paste.ubuntu.com", urllib.urlencode(target))
    except urllib2.URLError:
        return 1, "Error uploading paste:", "Network error"
    else:
        return 0, req.geturl()


def isInteger(value):
    try:
        value = int(value)
        return value
    except ValueError:
        return False


def sendMessage(message):
    if Var.locked:
        return

    if not (type(message) is str):
        try:
            message = str(message)
        except Exception:
            pass

    try:
        message = message.encode('ascii', 'ignore')
    except Exception:
        message = message.encode('utf-8', 'ignore')

    Var.locked = True
    k = PyKeyboard()

    try:
        k.type_string(message)
    except Exception:
        k.press_key(k.control_l_key)
        k.tap_key('A')
        k.release_key(k.control_l_key)
        k.tap_key(k.backspace_key)

        k.type_string("Message Contains Unknown Characters")

    k.tap_key(k.enter_key)
    Var.locked = False


def google_search(keyword):
    p = pygoogle(keyword)
    p.pages = 1
    result = p.search().items()[0]

    return result[0] + " - " + result[1]

DEVELOPER_KEY = "AIzaSyBpOJH8Sk_LxSsd0_qVBuS9wXnvkeJuiuU"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


def youtube_search(options):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

    search_response = youtube.search().list(
        q=options,
        part="id,snippet",
        maxResults=5
    ).execute()

    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            return "%s (%s): %s" % (search_result["snippet"]["title"], search_result["id"]["videoId"], "http://youtu.be/" + search_result["id"]["videoId"])

    return "None Found"