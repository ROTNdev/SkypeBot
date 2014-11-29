import Var
import Func
import Skype4Py
import re
import os
import time

import random
import urllib2
import urllib
import Queue

__author__ = 'Vilsol'


class SkypeBot(object):

    modules = {}

    def __init__(self):
        self.skype = Skype4Py.Skype(Events=self)
        self.skype.Attach()
        self.loadComamnds()
        Func.sendMessage("/me " + Var.version + " Initialized")

    def loadComamnds(self):
        for i in os.listdir("modules"):
            if i[-3:] != ".py":
                continue

            execfile("modules/" + i)

            module = eval(i[:-3] + "()")
            self.modules[i[:-3]] = module

    def AttachmentStatus(self, status):
        if status == Skype4Py.apiAttachAvailable:
            self.skype.Attach()

    def MessageStatus(self, msg, status):
        print(msg.FromHandle + ": " + msg.Body)

        if Var.chat.qsize() >= 100:
            Var.chat.get()
            pass

        Var.chat.put("[" + Func.now() + "] " + msg.FromHandle + ": " + msg.Body + "\n")

        for m, module in self.modules.items():
            for regexp, target in module.commands.items():
                match = re.match(regexp, msg.Body, re.IGNORECASE)

                if match:
                    msg.MarkAsSeen()

                    #try:s

                    reply = module.runMethod(target, msg, match)

                    if reply:
                        Func.sendMessage(reply)

                    #except Exception as ex:
                    #    e = traceback.format_stack()
                    #    e[-1] += "\n"
                    #    e.append(ex[0])

                    #    code, error = Func.pastebin(e)
                    #    Func.sendMessage("Error: " + error)

                    return

        if len(msg.Body) > 0:
            if msg.Body[0:1] == "@":
                Func.sendMessage("Command Not Found")

if __name__ == "__main__":
    Var.bot = SkypeBot()

    while Var.run:
        time.sleep(1.0)

    print("Restarting...")
