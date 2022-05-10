import discord
from nfa2 import Compiler
from regex import Regex
from discord.ext import commands
import time
from re import sub

# from sympy import li


class MyClient(commands.Bot):
    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')


client = MyClient(command_prefix=".")
# client=commands.Bot(command_prefix=".")

@client.slash_command(name="ping", description="Ping the bot")
async def ping(interaction):
    await interaction.response.defer()
    embed = discord.Embed(color=0xff9300)
    embed.add_field(name="Pong!", value=f"{client.latency*1000}ms", inline=False)
    await interaction.followup.send(embed=embed)

@client.slash_command(name="regex", description="Parse a regex")
async def about(interaction,
                expression: discord.Option(str, "The expression to parse", required=True),
                success: discord.Option(str, "The string to test to see if it passes", required=True),
                fail: discord.Option(str, "The string to test to see if it fails", required=False),
                flatten: discord.Option(bool, "Wether to remove epsilon transitions", required=False),
                ):

    # Give the bot time to respond
    await interaction.response.defer()

    # Start time for response time
    start_time = time.time()

    # format expression
    expression_formatted = sub(r'([\*])', r'\\\1', expression)

    # Build the embed
    embed = discord.Embed(color=0xff9300)
    embed.set_author(name=interaction.user.name,
                     icon_url=interaction.user.display_avatar.url)
    embed.set_thumbnail(
        url="https://cdn.discordapp.com/attachments/887748266761007125/971808149109633094/unknown.png")
    # embed.add_field(name="String Fail Check", value="Success!", inline=True)

    # Pass the regex
    regex_compiled = False
    try:

        regex_to_test = Regex(expression)
        regex_match = Compiler(regex_to_test.postfix)
        regex_compiled = True
    except:
        regex_compiled = False

    # fname = "".join([c for c in random.shuffle(ascii_letters)])
    # temp_regex_pic = tempfile.NamedTemporaryFile(suffix='.png')

    fname = "pics/testing"
    path2fname = "pics/testing.gv.png"

    if flatten:
        regex_match.transition_table()
        regex_match.flatten()
    regex_match.draw_transition_table(fname, format="png")
    regex_match.transition_table()

    if regex_compiled:

        embed.add_field(name="Regex compiled successfully!", value=f"The regex was compiled in {(time.time() - start_time)*100}ms", inline=False)

        # Process the passed string
        if regex_match.automata.match(success):
            embed.add_field(name="String Pass Check Success",
                            value=f"The regex {expression_formatted} passed the test {success}", inline=False)
        else:
            embed.add_field(name="String Pass Check Failed!",
                            value=f"The regex {expression_formatted} passed the test {success}", inline=False)

        # If there is a fail string, process it
        if fail != None:
            if not regex_match.automata.match(fail):
                embed.add_field(name="String Reject Check Success",
                                value="The regex {expression_formatted} passed the test of rejecting {fail}", inline=False)

        file2disc = discord.File(path2fname)
        embed.set_image(url=f"attachment://{path2fname}")

        await interaction.followup.send(embed=embed, file=file2disc)

    else:
        embed.add_field(name="Regex crashed",
                        value=f"The regex {expression_formatted} crashed the program in {(time.time() - start_time)*100}ms", inline=False)
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
