import Var
import Func
import random
import urllib2
import urllib
import Queue
import time

__author__ = 'vilsol'


class General:

    def __init__(self):
        pass

    def runMethod(self, target, msg, match):
        return target(self, msg, *match.groups())

    def cmd_ping(self, msg):
        return "Sponge is Gay"

    def cmd_topkek(self, msg):
        return "https://topkek.mazenmc.io/ Gotta be safe while keking!"

    def cmd_help(self, msg):
        Func.sendMessage("Available Commands:")
        for m, module in Func.getBot().modules.items():
            commands = m + ": "
            for name, target in module.commands.items():
                if name[1:2] != "@":
                    continue

                if commands != m + ": ":
                    commands += ", "

                if name[0:1] == "^":
                    name = name[1:]

                if name[-1] == "$":
                    name = name[0:-1]

                cmd = name.split(" ")

                full = ""

                for i in cmd:
                    if i[0:1] != "*" and i[0:1] != "(":
                        if full != "":
                            full += " "

                        full += i

                commands += full

            Func.sendMessage(commands)

    def cmd_doc(self, msg):
        return "https://docs.google.com/document/d/1LoTYCauVyEiiLZ5Klw3UB8rbEtkzNn7VLmgm87Fzyy0/edit#"

    def cmd_drama(self, msg):
        return urllib2.urlopen('http://asie.pl/drama.php?2').read().split('<h1>')[1].split('</h1><h3>')[0]

    def cmd_youtube(self, msg, search):
        return Func.youtube_search(search)

    def cmd_google(self, msg, search):
        return Func.google_search(search)

    def cmd_bot(self, msg, act):
        return "/me " + act

    def cmd_spoon(self, msg):
        return "There is no spoon"

    def cmd_fish_go_moo(self, msg):
        return "/me notes that " + msg.FromHandle + " is truly enlightened."

    def cmd_random(self, msg, low, high):
        if Func.isInteger(low) and Func.isInteger(high):
            return random.randint(int(low), int(high))

    def cmd_calc(self, msg, calc):
        return msg.Body[6:] + " = " + str(eval(msg.Body[6:]))

    def cmd_chuck(self, msg):
        return eval(urllib2.urlopen("http://api.icndb.com/jokes/random").read())["value"]["joke"]

    def cmd_alpha(self, msg, alpha):
        res = Var.client.query(alpha)
        try:
            interpretation = res.pods[0].text
            link = "http://wolframalpha.com/input/?i=" + urllib.quote_plus(alpha)

            Func.sendMessage(interpretation + " ('" + alpha + "') " + link)

            first = True
            for i in res.pods:
                if first:
                    first = False
                    continue

                Func.sendMessage(i.text)

        except Exception:
            return "No results found on WolframAlpha for '" + alpha + "'"

    def cmd_about(self, msg):
        Func.sendMessage("Bot made by Vilsol")
        Func.sendMessage("Current version: " + Var.version)

    def cmd_a(self, msg, alpha):
        if not (msg.FromHandle in Var.lastalpha):
            Var.lastalpha[msg.FromHandle] = 0

        if Var.lastalpha[msg.FromHandle] > time.time() - 60:
            return "Please wait for " + str(round(60 - (time.time() - Var.lastalpha[msg.FromHandle]), 2)) + " seconds!"

        Var.lastalpha[msg.FromHandle] = time.time()

        res = Var.client.query(alpha)
        try:
            interpretation = res.pods[0].text
            result = res.pods[1].text
            link = "http://wolframalpha.com/input/?i=" + urllib.quote_plus(alpha)

            Func.sendMessage(interpretation + " ('" + alpha + "') " + link)
            return result
        except Exception:
            return "No results found on WolframAlpha for '" + alpha + "'"

    def cmd_restart(self, msg):
        if msg.FromHandle == "vilsol":
            Func.sendMessage("/me " + Var.version + " Restarting...")
            Var.run = False
        else:
            Func.sendMessage("Access Denied")

    def cmd_c(self, msg, question):
        return Var.cleverbot.ask(question)

    def cmd_capture(self, msg):
        if Var.lastcapture > time.time() - 60:
            return "Please wait for " + str(round(60 - (time.time() - Var.lastcapture), 2)) + " seconds!"

        lastcapture = time.time()

        newChat = Queue.Queue()
        oldChat = []

        while not Var.chat.empty():
            message = Var.chat.get()
            newChat.put(message)
            oldChat.append(message)

        code, paste = Func.pastebin(oldChat)

        chat = newChat

        if code == 1:
            return paste
        else:
            return "Capture: " + paste

    def cmd_9gag(self, msg):
        return "Shut up 9fag!"

    def cmd_8ball(self, msg, what):
        options = ["It is certain",
                   "It is decidedly so",
                   "Without a doubt",
                   "Yes definitely",
                   "You may rely on it",
                   "As I see it, yes",
                   "Most likely",
                   "Outlook good",
                   "Yes",
                   "Signs point to yes",
                   "Reply hazy try again",
                   "Ask again later",
                   "Better not tell you now",
                   "Cannot predict now",
                   "Concentrate and ask again",
                   "Don't count on it",
                   "My reply is no",
                   "My sources say no",
                   "Outlook not so good",
                   "Very doubtful"]

        chosen = random.randint(0, len(options) - 1)
        return options[chosen]

    commands = {
        "^@ping$": cmd_ping,
        "^@topkek$": cmd_topkek,
        "^@help$": cmd_help,
        "^@doc$": cmd_doc,
        "^@drama$": cmd_drama,
        "^@youtube (.*)$": cmd_youtube,
        "^@bot (.*)$": cmd_bot,
        "^@spoon$": cmd_spoon,
        "^fish go moo$": cmd_fish_go_moo,
        "^@random (-?[0-9]+) (-?[0-9]+)$": cmd_random,
        "^@about$": cmd_about,
        # "@calc ([0-9]?[\%\*\(\)\+\-\/]?)+": cmd_calc
        "^@chuck$": cmd_chuck,
        # "@alpha *(.*)": cmd_alpha,
        "^@a (.*)$": cmd_a,
        "^@restart$": cmd_restart,
        "^@c (.*)$": cmd_c,
        "^@capture$": cmd_capture,
        ".*9gag.*": cmd_9gag,
        "^@8ball (.*)$": cmd_8ball
    }