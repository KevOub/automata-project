import discord
from itsdangerous import exc
import requests
import io
import os
from nfa2 import Compiler 
from regex import Regex


# from sympy import li



class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return

        if message.content.startswith('!regex'):
            msg = "".join([c for c in message.content if c != '"'])
            output = ""
            # for m in message.content.split(":"):
                # output += f"{m}\n"

            try:
                _,regex,p,f = msg.split(":")
                    
                regex_to_test = Regex(regex)
                # await message.send(regex_to_test.postfix)


                regex_match = Compiler(regex_to_test.postfix)
                
                if regex_match.automata.match(p):
                    await message.reply(f"The regex {regex} passed the test {p}")                    
                else:
                    await message.reply(f"FAILURE!:\nThe regex {regex} passed the test {p}")
                if f != None:    
                    if  not regex_match.automata.match(f):
                        await message.reply(f"The regex {regex} passed the test of rejecting {f}")                    
            except:
                await message.reply(f"stop that. the syntax is !regex:\"regular expression\":\"pass\":\"fail\"")


client = MyClient()

token = ""

# try:
#     with open("secret.key","wb") as s:
#         token = s.read()
#         print(token)
#         client.run(token)
# except:
#     print("Psst... put the discord token into the secret.key file")


with open("secret.key","rb") as s:
    token = s.read()
    print(token)
    client.run(token.decode())
