import os
import discord
from dotenv import load_dotenv
from PIL import Image
from PIL import ImageFilter
import asyncio
from io import BytesIO
from random import randint
from Dict import mikes, help1, help2, help3
import requests
import json
import threading

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
TICTACCHANNEL = os.getenv('TICTACTOE')
tictac = []
tick = 0
client = discord.Client()
sentence = ""
shoot = []
rps = []
rps_emotes = ['rock', 'paper', 'scissors']
emotes = ['<:rock:722536684431999007>', '<:paper:722548284643737703>', '<:scissors:722550422409052261>']

@client.event
async def on_ready():
    print(f"{client.user.name} is now running on discord.py version {discord.__version__}")
    await client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name="for !mikehelp"))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
        #F in chat for story
    # tictactoe
    global tick
    if message.content.lower().startswith("!tictactoe"):
        game = True
        partner = None
        if len(message.content) > 11 and len(message.mentions) == 1:
            partner = message.mentions[0]
            for i in range(len(tictac)):
                if int(message.author.id) in tictac[i][0]:
                    await message.channel.send("You are already in a game!")
                    game = False
                if partner.id in tictac[i][0]:
                    await message.channel.send("Your partner is already in a game!")
                    game = False

            if game:
                if partner is not None:
                    tictac.append([])
                    tictac[tick].append([message.author.id, partner.id, 0])
                    # Big list is each game in progress
                    # Next is each section   tictac[x][0] is list of players
                    tictac[tick].append([[":black_square_button:", ":black_square_button:", ":black_square_button:"],
                                         [":black_square_button:", ":black_square_button:", ":black_square_button:"],
                                         [":black_square_button:", ":black_square_button:", ":black_square_button:"]])
                    await message.channel.send(
                        '3 ' + tictac[tick][1][2][0] + tictac[tick][1][2][1] + tictac[tick][1][2][2] + "\n" +
                        '2 ' + tictac[tick][1][1][0] + tictac[tick][1][1][1] + tictac[tick][1][1][2] + "\n" +
                        '1 ' + tictac[tick][1][0][0] + tictac[tick][1][0][1] + tictac[tick][1][0][2] + "\n" +
                        '     a ' + '   b' + '    c'
                        )
                    await message.channel.send(message.author.mention + " it's your turn")
                    tick += 1
    game = False
    rows = ['1', '2', '3']
    columns = ['a', 'b', 'c']
    xo = [':o:', ':x:']
    if message.content != "" and message.content.lower()[0] in columns and message.content.lower()[1] in rows and len(message.content.lower()) == 2:
        for i in range(len(tictac)):
            if int(message.author.id) in tictac[i][0]:
                num = i
                game = True
        if game and tictac[num][0][2] % 2 == tictac[num][0].index(message.author.id) and \
                tictac[num][1][rows.index(message.content.lower()[1])][columns.index(message.content.lower()[0])] == ':black_square_button:':
            tictac[num][1][rows.index(message.content.lower()[1])][columns.index(message.content.lower()[0])] = xo[
                tictac[num][0][2] % 2]  # basically if its the correct turn
            await message.channel.send(
                '3 ' + tictac[num][1][2][0] + tictac[num][1][2][1] + tictac[num][1][2][2] + "\n" +
                '2 ' + tictac[num][1][1][0] + tictac[num][1][1][1] + tictac[num][1][1][2] + "\n" +
                '1 ' + tictac[num][1][0][0] + tictac[num][1][0][1] + tictac[num][1][0][2] + "\n" +
                '     a ' + '   b' + '    c'
            )

            # wining scenarios
            win = False
            tie = True
            turn = tictac[num][0][2] % 2
            if tictac[num][1][0][0] == xo[turn] and tictac[num][1][0][1] == xo[turn] and tictac[num][1][0][2] == xo[
                turn]:
                win = True
            if tictac[num][1][1][0] == xo[turn] and tictac[num][1][1][1] == xo[turn] and tictac[num][1][1][2] == xo[
                turn]:
                win = True
            if tictac[num][1][2][0] == xo[turn] and tictac[num][1][2][1] == xo[turn] and tictac[num][1][2][2] == xo[
                turn]:
                win = True

            if tictac[num][1][0][0] == xo[turn] and tictac[num][1][1][0] == xo[turn] and tictac[num][1][2][0] == xo[
                turn]:
                win = True
            if tictac[num][1][0][1] == xo[turn] and tictac[num][1][1][1] == xo[turn] and tictac[num][1][2][1] == xo[
                turn]:
                win = True
            if tictac[num][1][0][2] == xo[turn] and tictac[num][1][1][2] == xo[turn] and tictac[num][1][2][2] == xo[
                turn]:
                win = True

            if tictac[num][1][0][0] == xo[turn] and tictac[num][1][1][1] == xo[turn] and tictac[num][1][2][2] == xo[
                turn]:
                win = True
            if tictac[num][1][0][2] == xo[turn] and tictac[num][1][1][1] == xo[turn] and tictac[num][1][2][0] == xo[
                turn]:
                win = True

            if win:
                winner = client.get_user(tictac[num][0][turn])
                await message.channel.send(f'{winner.name} has won the game!')
                tictac.pop(num)
                tick -= 1

            for i in range(3):
                for j in range(3):
                    if tictac[num][1][i][j] == ":black_square_button:":
                        tie = False
            if tie:
                await message.channel.send("It's a tie!")
                tictac.pop(num)
                tick -= 1

            if not tie and not win:
                tictac[num][0][2] += 1
                even = tictac[num][0][2] % 2
                turn = client.get_user(tictac[num][0][even])
                await message.channel.send(turn.mention + " it's your turn!")
    num = -1

    # tictactoe resign
    if message.content.lower() == '!resign' or message.content.lower() == '!forfeit' or message.content.lower() == '!ff':
        winner = None
        loser = None
        for i in range(len(tictac)):
            if int(message.author.id) in tictac[i][0]:
                num = i
                if message.author.id == tictac[num][0][0]:
                    winner = client.get_user(tictac[num][0][1])
                    loser = client.get_user(tictac[num][0][0])
                else:
                    winner = client.get_user(tictac[num][0][0])
                    loser = client.get_user(tictac[num][0][1])
                tictac.pop(num)
                tick -= 1
                await message.channel.send(f'{winner.mention} has won against {loser.mention} due to resignation!')

        # Rock Paper Scissors resign
        winner = None
        for i in range(len(rps)):
            if message.author == rps[i][0]:
                winner = rps[i][1]
            if message.author == rps[i][1]:
                winner = rps[i][0]
            if winner is not None:
                await message.channel.send(f'{winner.name} has won due to resignation!')
                rps[i][0] = []
                rps[i][1] = []
                rps[i][5] = True
    # Rock paper scissors
    if message.content.lower().startswith("!rps ") and len(message.mentions) == 1:
        partner = message.mentions[0]
        rpsgame = True
        for i in range(len(rps)):
            if message.author in rps[i]:
                await message.channel.send("You are already in a game!", delete_after=60)
                rpsgame = False
            if partner in rps[i]:
                await message.channel.send("Your partner is already in a game!", delete_after=60)
                rpsgame = False
            if partner == message.author:
                await message.channel.send("You cant play yourself!", delete_after=60)
                rpsgame = False
            # if partner == client.user:
            #    await message.channel.send("You cant play the bot!", delete_after=60)
            #    rpsgame = False
        if rpsgame:  # p1, p2, answer1, answer, the channel, game end
            rps.append([message.author, partner, None, None, message.channel, False])
            if message.author.dm_channel is None:
                await message.author.create_dm()
            if partner != client.user and partner.dm_channel is None:
                await partner.create_dm()

            dm = await message.author.dm_channel.send("react with your move")
            await dm.add_reaction('<:rock:722536684431999007>')
            await dm.add_reaction('<:paper:722548284643737703>')
            await dm.add_reaction('<:scissors:722550422409052261>')
            if partner != client.user:
                dm = await partner.dm_channel.send("react with your move")
                await dm.add_reaction('<:rock:722536684431999007>')
                await dm.add_reaction('<:paper:722548284643737703>')
                await dm.add_reaction('<:scissors:722550422409052261>')

            # rps[len(rps)-1][4].start()
            await message.channel.send("check your dms", delete_after=60)

    # !say
    if not message.author.bot and message.author.permissions_in(message.channel).administrator:
        if message.content.lower().startswith("!say "):
            await message.channel.send(message.content[5:])
            await message.delete()

    # thanks mikebot
    if message.content.lower().startswith("thanks mike"):
        await message.channel.send("You're Welcome!")
        print(f"Received thanks from {message.author}!")

    # !purge
    if message.content.lower().startswith("!purge "):
        if message.author.permissions_in(message.channel).manage_messages:
            try:
                num = int(message.content[6:]) + 1
            except ValueError:
                await message.channel.send("That is not a valid number!")
            else:
                await message.channel.purge(limit=num)
        else:
            await message.channel.send("Not Enough Permissions!")

    # Basically dad bot
    if message.content.lower().startswith("im "):
        await message.channel.send(f"Hi {message.content[3:]}, I'm Mikebot.")
    elif message.content.lower().startswith("i'm ") or message.content.lower().startswith("i’m "):
        await message.channel.send(f"Hi {message.content[4:]}, I'm Mikebot.")
    elif message.content.lower().startswith("i am "):
        await message.channel.send(f"Hi {message.content[5:]}, I'm Mikebot.")

    # Imagine
    if message.content.lower().startswith('imagine'):
        await message.channel.send('Imagine')

    # No u
    if message.content.lower() == "no u":
        await message.channel.send(file=discord.File('Mikepics/reverse.jpg'))

    # mikeify

    if message.content.lower().startswith("!mikeify"):
        user = message.author
        if len(message.mentions) == 1:
            userX = message.mentions[0]
            if userX is not None:
                user = userX

        mikepic = randint(1, 6)
        # grabs varibles from the dictionary based on randomizer

        width = mikes[mikepic]["width"]
        height = mikes[mikepic]["height"]
        image = mikes[mikepic]["image"]
        pasteX = mikes[mikepic]["pasteX"]
        pasteY = mikes[mikepic]["pasteY"]
        overlay = mikes[mikepic]["overlay"]
        overlayFile = mikes[mikepic]["overlayFile"]
        blur = mikes[mikepic]["blur"]

        await message.channel.trigger_typing()

        response = requests.get(user.avatar_url)
        Profile = Image.open(BytesIO(response.content))

        # applies blur to pfp
        if (blur):
            Profile = Profile.filter(ImageFilter.BoxBlur(15))

        # resizes to specified size
        PFP = Profile.resize((width, height))

        # opens and pastes specified image
        mikey = Image.open(image)
        mikey.paste(PFP, (pasteX, pasteY))

        # pastes arms(or hat) back on
        if (overlay):
            overlayImage = Image.open(overlayFile)
            mikey.paste(overlayImage, (0, 0), overlayImage)

        mikey.save('mikey.png')
        await message.channel.send(file=discord.File('mikey.png'))
        os.remove("mikey.png")

    # fake
    if message.content.lower().startswith("!fake") and len(message.mentions) == 1 and message.mentions[
        0] != client.user and len(message.content) > 28:
        content = message.content[28:]
        user = message.mentions[0]
        webhook = await message.channel.create_webhook(name="mikehook")
        if "@everyone" in content:
            content = content[0:content.index("@everyone") + 1] + " " + content[content.index("@everyone") + 1:]
        if "@here" in content:
            content = content[0:content.index("@here") + 1] + " " + content[content.index("@here") + 1:]

        username = user.display_name
        avatar_url = str(user.avatar_url).strip("'<Asset url='")
        avatar_url = avatar_url.strip("'>")
        await webhook.send(content, username=username, avatar_url=avatar_url)
        await webhook.delete()
        await message.delete()
        return
    #help
    if message.content.lower() == "!mikehelp":
        for i in [help1, help2, help3]:
            help_embed = discord.Embed.from_dict(i)
            await message.channel.send(embed=help_embed)

    #spam
    if message.content.lower().startswith("!spam "):
        if message.author.permissions_in(message.channel).administrator:
            for i in range(10):
                await message.channel.send(message.content[6:])
        else:
            await message.channel.send("You need to be an admin")

    #yesno
    if message.content.lower().startswith("!yesno "):
        yesno = await message.channel.send(message.content[7:] + " -" + message.author.mention)
        await yesno.add_reaction("✅")
        await yesno.add_reaction("❌")
        await message.delete()
        return
@client.event
async def on_reaction_add(reaction, user):
    message = reaction.message

    #rps reactions    p1, p2, answer1, answer2, the timer, game end
    if message.channel.type == discord.ChannelType.private and reaction.count == 2:

        for i in range(len(rps)):
            channel = rps[i][4]
            if message.channel.recipient in rps[i]:
                if rps[i].index(message.channel.recipient) == 0:
                    rps[i][2] = rps_emotes.index(reaction.emoji.name)
                if rps[i].index(message.channel.recipient) == 1:
                    rps[i][3] = rps_emotes.index(reaction.emoji.name)

            if rps[i][2] is not None and rps[i][3] is not None and not rps[i][5]:
                #win
                if rps[i][2] == rps[i][3]:
                    await channel.send(f"{rps[i][0].mention}({emotes[rps[i][2]]}) has tied {rps[i][1].mention}({emotes[rps[i][3]]})")
                elif rps[i][2]-1 == rps[i][3] or rps[i][2]+2 == rps[i][3]:
                    await channel.send(f"{rps[i][0].mention}({emotes[rps[i][2]]}) has won against {rps[i][1].mention}({emotes[rps[i][3]]})")
                else:
                    await channel.send(f"{rps[i][1].mention}({emotes[rps[i][3]]}) has won against {rps[i][0].mention}({emotes[rps[i][2]]})")
                await asyncio.sleep(1)
                rps[i][0] = []
                rps[i][1] = []
                rps[i][5] = True
            #bot hacks
            if rps[i][2] is not None and rps[i][1] == client.user:
                if rps[i][2] == 2:
                    rps[i][3] = 0
                else:
                    rps[i][3] = rps[i][2]+1
                await channel.send(f"{rps[i][1].mention}({emotes[rps[i][3]]}) has won against {rps[i][0].mention}({emotes[rps[i][2]]})")
                await channel.send("I never lose")
                rps[i][0] = []
                rps[i][1] = []
                rps[i][5] = True
client.run(TOKEN)