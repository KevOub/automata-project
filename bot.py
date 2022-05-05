import discord
from itsdangerous import exc
import requests
import io
import os
from nfa2 import Compiler
from regex import Regex
from discord.ext import commands


# from sympy import li


class MyClient(commands.Bot):
    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')


client = MyClient(command_prefix=".")
# client=commands.Bot(command_prefix=".")


@client.slash_command(name="regex", description="Parse a regex", guild_ids=[971807147627282482])
async def about(interaction,
                expression: discord.Option(str, "The expression to parse", required=True),
                success: discord.Option(str, "The string to test to see if it passes", required=True),
                fail: discord.Option(str, "The string to test to see if it fails", required=False)):

    # Give the bot time to respond
    await interaction.response.defer()

    # Build the embed
    embed = discord.Embed(color=0xff9300)
    embed.set_author(name=interaction.user.name,icon_url=interaction.user.display_avatar.url)
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/887748266761007125/971808149109633094/unknown.png")

    # Pass the regex
    regex_to_test = Regex(expression)

    regex_match = Compiler(regex_to_test.postfix)

    # Process the passed string
    if regex_match.automata.match(success):
        embed.add_field(name="String Pass Check Success", value=f"The regex {expression} passed the test {success}", inline=False)
    else:
        embed.add_field(name="String Pass Check Failed!", value=f"The regex {expression} passed the test {success}", inline=False)
    
    # If there is a fail string, process it
    if fail != None:    
        if  not regex_match.automata.match(fail):
            embed.add_field(name="String Reject Check Success", value=f"The regex {expression} passed the test of rejcting {success}", inline=False)
    
    await interaction.followup.send(embed=embed)

token = ""

# try:
#     with open("secret.key","wb") as s:
#         token = s.read()
#         print(token)
#         client.run(token)
# except:
#     print("Psst... put the discord token into the secret.key file")


with open("bot/secret.key", "rb") as s:
    token = s.read()
    print(token)
    client.run(token.decode())
