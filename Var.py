import wolframalpha
import cleverbot
import Queue

__author__ = 'vilsol'

bot = None
chat = Queue.Queue()
lastalpha = {}
lastcapture = 0
version = "v2.0"
devkey = "6c71766cdadff9f33347e80131397ac2"
run = True
locked = False
client = wolframalpha.Client("8WP4PE-KHQAPVYKK4")
cleverbot = cleverbot.Cleverbot()
