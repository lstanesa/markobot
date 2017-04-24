#!/bin/python3.4
import discord
import asyncio
import requests
import random
import json
import markov
import os
import sys
import re

import util
from exception import *
from config import Config

from exception import *

class MarkoBot(discord.Client):
    def __init__(self, config=None):
        super().__init__()
        self.config = config

        self.commands = {
            'quit'      : 'cmd_quit',
            'blacklist' : 'cmd_blacklist',
            'whitelist' : 'cmd_whitelist'
        }

        with open('chat.json') as chat_config:
            self.chat = json.loads(chat_config.read())
        

    @asyncio.coroutine
    def on_ready(self):
        print('%s:%s logged in' % (self.user.name, self.user.id))

    @asyncio.coroutine
    def on_message(self, message):
        if message.content.startswith(self.config.command_prefix):
            try:
                yield from self.run_command(message)
            except CommandException as e:
                print(e.message)
                yield from self.send_message(message.channel, e.message)
        elif message.content.find('alex') > -1:
            pass
        elif message.content.find('http://') == -1 and message.author.id != self.user.id and not message.author.bot:

            if message.author.mention in self.chat['blacklist'] or (self.chat['whitelist_enabled'] and not message.author.mention in self.chat['whitelist']):
                return

            if message.content.find("<@") != 0 and not message.content[0].isalnum(): 
                return

            for m in re.finditer('<@[0-9].*>', message.content):
                middle = message.content.split(m.start(), 1)[1].split(m.end(), 1)[0]
                message.content = message.content.replace(middle, '')

            f = open('markov.txt', 'a+')
            if self.user.mentioned_in(message):
                message.content = message.content[len(self.user.mention)+1:]
                generator = markov.Markov(f)
                f.seek(0, 0)
                yield from self.send_message(message.channel, message.author.mention + ' ' + generator.generate_markov_text())
                

            f.write(message.content + '\n')
            f.close()

    def write_config(self):
        with open('chat.json', 'w') as chat_config:
            chat_config.write(json.dumps(self.chat))

    @asyncio.coroutine
    def run_command(self, message):
        sp = message.content.split(' ')
        cmd = sp[0][1:]
        print("cmd: %s" % cmd)
        args = sp[1:]
        print("args: {}" % args)
        
        if cmd in self.commands.keys():
            c = self.commands[cmd]
            print("Running fn %s" % c)
            yield from getattr(self, self.commands[cmd])(message, args)

    @asyncio.coroutine
    def cmd_quit(self, message, args=[]):
        yield from self.logout()

    @asyncio.coroutine
    def cmd_blacklist(self, message, args=[]):
        if args == None or len(args) == 0:
            util.command_usage('.blacklist [add/remove] [@user]', 'blacklist')
            return

        opt = args[0]
        user = args[1]
        
        if not buser.find('<@') == 0:
            raise CommandException('first argument must be mention of user to add/remove from blacklist')

        if opt == 'add':
            if not buser in self.chat['blacklist']:
                self.chat['blacklist'].append(buser)
                yield from self.send_message(message.channel, 'user blacklisted')
            else:
                yield from self.send_message(message.channel, 'user is already blacklisted')
        elif opt == 'remove':
            if buser in self.chat['blacklist']:
                self.chat['blacklist'].remove(buser)
                yield from self.send_message(message.channel, 'user removed from blacklist')
            else:
                yield from self.send_message(message.channel, 'user was not blacklisted')
            

    @asyncio.coroutine
    def cmd_whitelist(self, message, args=[]):
        if args == None or len(args) == 0:
            util.command_usage('.whitelist [add/remove/list] [@user]', 'whitelist')
            return

        opt = args[0]
        user = args[1]

        if not buser.find('<@') == 0:
            raise CommandException('second argument must be mention of user to add/remove from whitelist')

        if opt == 'add':
            if not buser in self.chat['whitelist']:
                self.chat['whitelist'].append(buser)
                yield from self.send_message(message.channel, 'user added to whitelist')
        elif opt == 'remove':
            if buser in self.chat['whitelist']:
                self.chat['whitelist'].remove(buser)
                yield from self.send_message(message.channel, 'user removed from whitelist')
            else:
                yield from self.send_message(message.channel, 'user was not whitelisted')

    @asyncio.coroutine
    def cmd_ebooks(self, message, args=[]):
        search_word = ''
        if len(args) > 0:
            search_word = args[0]

        with open('markov.txt', 'a+') as f:
            generator = markov.Markov(f)
            yield from self.send_message(message.channel, message.author.mention + ' ' + generator.generate_markov_text(size=len(message.content) + random.randint(0, 3)))



def error(message, code=1):
    print("[error] " + message)
    sys.exit(code)

def main():
    if not os.path.isfile('settings.json'):
        print('settings.json could not be found')
        sys.exit(1)

    bot = MarkoBot(Config('settings.json'))

    if bot.config.login_method == 'token':
       bot.run(bot.config.token)
    elif bot.config.login_method == 'account':
       bot.run(bot.config.username, bot.config.password)

if __name__ == "__main__":
    main()
