import os
import discord
from dotenv import load_dotenv
from PIL import Image
from PIL import ImageFilter
import requests
from io import BytesIO
from random import randint
from Dict import mikes
import requests
import json

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
WORDCHANNEL = os.getenv('STORYCHANNEL')
STORYARCHIVES = os.getenv('STORYARCHIVES')
STORYPINS = os.getenv('STORYPINS')
EMOJI = os.getenv('PIN_EMOJI')
VOTES = int(os.getenv('PIN_VOTES'))
TICTACCHANNEL = os.getenv('TICTACTOE')
tictac = []
tick = 0
client = discord.Client()
sentence = ""

@client.event
async def on_ready():
    print("ready")

@client.event
async def on_message(message):
    def getuser(start, end):
        userID = message.content[start:end].strip("<@")
        userID = userID.strip(">")
        userID = userID.strip("!")
        return client.get_user(int(userID))

    global tick
    global sentence
    story = []
    archivechannel = client.get_channel(int(STORYARCHIVES))
    storychannel = client.get_channel(int(WORDCHANNEL))
    tictacchannel = client.get_channel(int(TICTACCHANNEL))
    if message.author == client.user:
        if archivechannel == message.channel and message.content == sentence.strip():
            await message.add_reaction(EMOJI)     # adds the emoji used for voting
        else:
            return

    if message.channel is storychannel:  # going through the channel history to find the end of the last sentence
        if message.content == '.' or message.content == '?' or message.content == '!':
            await archivechannel.trigger_typing()
            lastdot = await storychannel.history(limit=100, before=message.created_at).get(content='.')
            lastquestion = await storychannel.history(limit=100, before=message.created_at).get(content='?')
            lastexclaim = await storychannel.history(limit=100, before=message.created_at).get(content='!')
            last=lastdot.created_at
            for i in [lastdot, lastquestion, lastexclaim]:
                if i != None and i.created_at>last:
                    last=i.created_at

            word = []
            sentence = ''
            # adding all the words to an array(stack) to make reversing/editing words it easier
            word.append(message.content)
            async for i in storychannel.history(limit=100):
                if last < i.created_at < message.created_at:
                    word.append(i.content)  # add

            x = len(word) - 2
            for i in range(len(word)):
                stuff = word.pop()
                # if apostrophe or hyphen or comma it will edit out the space
                if stuff[0] == "'" or stuff[0] == "," or stuff[0] == "’" or stuff[0] == ":" or stuff[0] == "‘":
                    sentence = sentence[:-1]
                    sentence += f'{stuff} '
                elif stuff[0] == '-':
                    sentence = sentence[:-1]
                    sentence += f'{stuff[1:]} '
                else:
                    sentence += f'{stuff} '  # otherwise just add with a space
            x=len(sentence)-2
            sentence= sentence[:x-1] + sentence[x:]
            spamfix = sentence.replace(".", "")
            spamfix = spamfix.replace("?", "")
            spamfix = spamfix.replace("!", "")
            spamfix = spamfix.replace(" ", "")
            if spamfix != '':
                await archivechannel.send(sentence)
                print(f'sent: {sentence}')
    # easter eggs/commands
    # tic tac toe
    if message.channel == tictacchannel:
        move=message.content.lower()
        if message.content.lower().startswith("!tictactoe"):
            game = True

            if len(message.content)>11:
                partner = getuser(11, len(message.content))

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
                        await message.channel.send('3 '+tictac[tick][1][2][0] + tictac[tick][1][2][1] + tictac[tick][1][2][2]+"\n"+
                                                   '2 '+tictac[tick][1][1][0] + tictac[tick][1][1][1] + tictac[tick][1][1][2]+"\n"+
                                                   '1 '+tictac[tick][1][0][0] + tictac[tick][1][0][1] + tictac[tick][1][0][2]+"\n"+
                                                   '     a '+'   b'+'    c'
                                                   )
                        await message.channel.send(message.author.mention+" it's your turn")
                        tick += 1
        game = False
        rows = ['1', '2', '3']
        columns = ['a', 'b', 'c']
        xo = [':o:', ':x:']
        if move.lower()[0] in columns and move.lower()[1] in rows and len(move) == 2:
            for i in range(len(tictac)):
                if int(message.author.id) in tictac[i][0]:
                    num = i
                    game = True
            if game and tictac[num][0][2] % 2 == tictac[num][0].index(message.author.id) and tictac[num][1][rows.index(move[1])][columns.index(move[0])] == ':black_square_button:':
                tictac[num][1][rows.index(move[1])][columns.index(move[0])] = xo[tictac[num][0][2] % 2] # basically if its the correct turn
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
                if tictac[num][1][0][0] == xo[turn] and tictac[num][1][0][1] == xo[turn] and tictac[num][1][0][2] == xo[turn]:
                    win = True
                if tictac[num][1][1][0] == xo[turn] and tictac[num][1][1][1] == xo[turn] and tictac[num][1][1][2] == xo[
                    turn]:
                    win = True
                if tictac[num][1][2][0] == xo[turn] and tictac[num][1][2][1] == xo[turn] and tictac[num][1][2][2] == xo[
                    turn]:
                    win = True

                if tictac[num][1][0][0] == xo[turn] and tictac[num][1][1][0] == xo[turn] and tictac[num][1][2][0] == xo[turn]:
                    win = True
                if tictac[num][1][0][1] == xo[turn] and tictac[num][1][1][1] == xo[turn] and tictac[num][1][2][1] == xo[turn]:
                    win = True
                if tictac[num][1][0][2] == xo[turn] and tictac[num][1][1][2] == xo[turn] and tictac[num][1][2][2] == xo[turn]:
                    win = True

                if tictac[num][1][0][0] == xo[turn] and tictac[num][1][1][1] == xo[turn] and tictac[num][1][2][2] == xo[turn]:
                    win = True
                if tictac[num][1][0][2] == xo[turn] and tictac[num][1][1][1] == xo[turn] and tictac[num][1][2][0] == xo[turn]:
                    win = True

                if win:
                    winner = client.get_user(tictac[num][0][turn])
                    await message.channel.send(f'{winner.name} has won the game!')
                    tictac.pop(num)
                    tick-=1

                for i in range(3):
                    for j in range(3):
                        if tictac[num][1][i][j] == ":black_square_button:":
                            tie = False
                if tie:
                    await message.channel.send("It's a tie!")
                    tictac.pop(num)
                    tick-=1

                if not tie and not win:
                    tictac[num][0][2] += 1
                    even = tictac[num][0][2] % 2
                    turn = client.get_user(tictac[num][0][even])
                    await message.channel.send(turn.mention + " it's your turn!")
        num = -1
        if message.content.lower()== '!resign' or message.content.lower()=='!forfeit':
            for i in range(len(tictac)):
                if int(message.author.id) in tictac[i][0]:
                    num = i
            if num>-1:
                if message.author.id == tictac[num][0][0]:
                    winner = client.get_user(tictac[num][0][1])
                else:
                    winner = client.get_user(tictac[num][0][0])

                tictac.pop(num)
                tick-=1
                await message.channel.send(f'{winner.name} has won due to resignation!')



    # !say
    if not message.author.bot and message.author.permissions_in(message.channel).administrator:
        if message.content.lower().startswith("!say "):
            await message.channel.send(message.content[5:])
            await message.delete()

    # other commands
    if not message.author.bot and message.channel != storychannel and message.channel != archivechannel:
        # thanks mikebot
        if message.content.lower().startswith("thanks mike"):
            await message.channel.send("You're Welcome!")
            print(f"Received thanks from {message.author}!")

        # !purge
        if message.content.lower().startswith("!purge "):
            if message.author.permissions_in(message.channel).manage_messages:
                try:
                    num = int(message.content[6:])+1
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
            if len(message.content.strip()) > 8:
                print(len(message.content))
                userX = getuser(9, len(message.content))
                print(userX)
                if userX is not None:
                    user=userX

            mikepic = randint(1,6)
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
            if(overlay):
                overlayImage = Image.open(overlayFile)
                mikey.paste(overlayImage, (0,0), overlayImage)




            mikey.save('mikey.png')
            await message.channel.send(file=discord.File('mikey.png'))
            os.remove("mikey.png")

        # fake
        if message.content.lower().startswith("!fake") and len(message.mentions) == 1 and message.mentions[0] != client.user and len(message.content) > 28:
            content = message.content[28:]
            user = message.mentions[0]
            webhook = await message.channel.create_webhook(name = "mikehook")
            if "@everyone" in content:
                content=content[0:content.index("@everyone")+1]+" "+content[content.index("@everyone")+1:]
            if "@here" in content:
                content=content[0:content.index("@here")+1]+" "+content[content.index("@here")+1:]

            username = user.display_name
            avatar_url = str(user.avatar_url).strip("'<Asset url='")
            avatar_url = avatar_url.strip("'>")
            await webhook.send(content, username=username, avatar_url=avatar_url)
            await webhook.delete()
            await message.delete()


@client.event
async def on_reaction_add(reaction, user):
    archivechannel = client.get_channel(int(STORYARCHIVES))
    pinchannel = client.get_channel(int(STORYPINS))
    # Pins message if has more or equal reactions than PIN_VOTES
    if reaction.message.channel == archivechannel and f"<:{reaction.emoji.name}:{reaction.emoji.id}>" == EMOJI:
        if reaction.count == VOTES+1:
            content = reaction.message.content
            repeat = False
            async for i in pinchannel.history(limit=7):
                if i.content == content:
                      repeat = True

            if not repeat:
                await pinchannel.send(content)
                print(f'pinned {reaction.message.content}')

client.run(TOKEN)
