# discord_pog_tracker.py

# import multiprocessing so that searches can be ran later
from multiprocessing import Pool

import os

# this loads the discord library
import discord
from dotenv import load_dotenv
from discord.ext.commands import Bot

# import numpy for arrays
import numpy as np

# import csv for reading/writing to temporary DB
from csv import writer

# import datetime for date updates
from datetime import datetime
from datetime import timezone

# import multithreading as mp

# import re package to make data parsing easier
import re

# importing pandas for csv manipulation
import pandas as pd

# import time module for sleeps
import time

# this loads async
import asyncio

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
KARUTA = int(os.getenv('DISCORD_KARUTA_CHANNEL'))
KARUTA_BOT = int(os.getenv('DISCORD_KARUTA_BOT_ID'))
KARUTA_SPAM = int(os.getenv('DISCORD_KARUTA_SPAM_ID'))

# allows for bot to detect all members belonging to the server.

intents = discord.Intents.default()
intents.members = True
intents.reactions = True
intents.messages = True

# Client is an object that represents a connection to Discord.
# This handles events, tracks state and interacts with discord APIs
client = discord.Client(intents=intents)
bot = Bot(command_prefix='pog.')

# get the server for Catwad
localServer = discord.utils.get(client.guilds, name=GUILD)

# define a function which will alter global variables like flags
baseValueFlag = True

@bot.event
# for debugging, prints into console once bot has connected
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="pog.helpme"))
    print("Bot status has been changed to list the bot help command!\n")

@bot.command(name='helpme')
# prints list of commands
async def on_message(message):
    if message.author.id == KARUTA_BOT:
        return
    # define the custom emoji we're using to wrap around the title.
    titleEmoji = '<:momopog:789975922294915092>'
    helpMessage = (f"{titleEmoji} __**COMMANDS**__ {titleEmoji} \n\n"
                   f"{titleEmoji} `effort` {titleEmoji} \n"
                   f"Saves worker information from the first page of a filter and returns it in effort order.\n"
                   f"This information is saved in the bot and gets used again for next time.\n"
                   f"Next to-do: \n      1. Making the list pretty, "
                   f"\n      2. Adding injury data to the list.\n\n"
                   f"{titleEmoji} `drops` {titleEmoji}\n"
                   f"Counts the number of drops in the server by user.\n"
                   f"Currently **broken** 🔨\n\n"
                   f"{titleEmoji} `basetracker` {titleEmoji}\n"
                   f"Turns on/off the bot's function to send base values after a card lookup is done.\n"
                   f"**On** by default.\n\n"
                   f"{titleEmoji} `flags` {titleEmoji}\n"
                   f"Shows the configurable settings for the bot. At the moment, it's just the base "
                   f"tracker flag.\n\n"
                   f"{titleEmoji} `wip` {titleEmoji}\n"
                   f"Lists the commands that are planned for implementation or in the works.")
    await message.channel.send(helpMessage)
    await bot.process_commands(message)

@bot.command(name='wip')
# prints list of WIP commands
async def on_message(message):
    if message.author.id == KARUTA_BOT:
        return
    # define the custom emoji we're using to wrap around the title.
    titleEmoji = '<:momopog:789975922294915092>'
    helpMessage = (f"👷 __WIP__ 👷\n\n"
                   f"{titleEmoji} `predict` {titleEmoji}\n"
                   f"Plug in card details and the bot will estimate what its effort will be at mint condition.\n\n"
                   f"{titleEmoji} `pogdrops` {titleEmoji}\n"
                   f"Check how many pog drops have been made in the server (for fun).\n\n"
                   f"{titleEmoji} `poggrabs` {titleEmoji}\n"
                   f"Check how many pog grabs have been made in the server (for fun).\n\n"
                   f"{titleEmoji} `troll` {titleEmoji}\n"
                   f"Brings up a leaderboard of how many times someone has trolled in Karuta.\n"
                   f"Will take additional commands to add/remove points too.\n\n"
                   f"{titleEmoji} `debts` {titleEmoji}\n"
                   f"Keep track of how much you owe people.\n"
                   f"Will take additional commands to add/remove items.\n\n"
                   f"{titleEmoji} `streak` {titleEmoji}\n"
                   f"See who's worked the longest without breaking a leg...\n"
                   f"Additional scope to check number of injuries,"
                   f"number of times 1/2/3 workers have been injured, etc.\n\n"
                   f"{titleEmoji} `nodes` {titleEmoji}\n"
                   f"Find the node that will provide the best bang for your buck in terms of bits gained and power.\n"
                   f"Needs further investigation: is effort affected by the power %?\n\n"
                   f"{titleEmoji} `export` {titleEmoji}\n"
                   f"Exports the card DB to a csv file which can be used to do other stuff.\n\n"
                   f"{titleEmoji} `injury` {titleEmoji}\n"
                   f"Pull a card's injury history up.\n\n"
                   f"{titleEmoji} `exchange` {titleEmoji}\n"
                   f"Convert between different currencies to find out if you are getting scammeth'd.")
    await message.channel.send(helpMessage)
    await bot.process_commands(message)

@bot.command(name='flags')
# prints flag settings
async def on_message(message):
    if message.author == bot.user:
        return
    baseValueHeader = '__**Karuwuta Bot Settings**__\n'
    if baseValueFlag == True:
        baseValueMessage = '✅ : Base Value Tracker\n'
    else:
        baseValueMessage = '❌ : Base Value Tracker\n'
    flagMessage = baseValueHeader + baseValueMessage
    await message.channel.send(flagMessage)
    await bot.process_commands(message)


@bot.command(name='basetracker')
# this controls the base value tracker flag
async def on_message(message):
    if message.author == bot.user:
        return

    # define a function which inverts the base tracker flag
    def flagInverter():
        global baseValueFlag
        if baseValueFlag == True:
            baseValueFlag = False
        else:
            baseValueFlag = True
        return baseValueFlag
    print(flagInverter())
    if baseValueFlag == False:
        await message.channel.send("The base value tracker has been turned off. I won't be posting any more messages "
                                   "after any lookup commands anymore.")
    else:
        await message.channel.send("The base value tracker has been turned on. I will post a message detailing the "
                                   "card's base value at mint condition following every lookup command.")
    await bot.process_commands(message)

@bot.command(name='dropcount')
# this is sample code to count drops
async def on_message(message):
    print('drop count text triggered')
    if message.author.id == KARUTA_BOT:
        return

    else:
        # define the object for the channel containing the Karuta drops
        karuta_channel = bot.get_channel(KARUTA)

        # print all messages from karuta bot into a list. first, define the array that will contain the IDs
        karuta_messages_list = list()
        total_drop_count = int(0)

        # initialise the guild array
        guild = discord.utils.find(lambda g: g.id == GUILD, bot.guilds)

        # initialise arrays for dropcount table
        member_count = len(guild.members)
        test_memb_false_name = [member.nick for member in guild.members]
        test_true_name = [member.name for member in guild.members]
        test_memb_id = [member.id for member in guild.members]
        member_drop_count = [0] * member_count

        # now set some variables. This can be set to None to pull all messages.
        message_limit = int(1000)

        async for msgElem in karuta_channel.history(limit=message_limit):
            # limits list to only posts from Karuta bot
            if msgElem.author.id == KARUTA_BOT:
                # further limits list to only posts that are a drop
                if "These card drops have expired and can no longer be grabbed." in msgElem.content:
                    karuta_messages_list.append(msgElem.content)

                    total_drop_count = total_drop_count + 1

                    # within the list of messages that are drops, look to see for any mentions and increment that value
                    for i in range(member_count):
                        if str(test_memb_id[i]) in msgElem.content:
                            member_drop_count[i] = member_drop_count[i] + 1
                            break

        # define the number of drops done by Karuta
        server_drop_count = int(total_drop_count - sum(member_drop_count))
        # define the response arrays.
        j = 0
        leaderboard = []
        for i in range(member_count):
            if member_drop_count[i] == 0:
                pass
            else:
                if str(test_memb_false_name[i]) == 'None':
                    leaderboard.append(f'{test_true_name[i]} has dropped {member_drop_count[i]} times.\n')
                else:
                    leaderboard.append(f'{test_memb_false_name[i]} has dropped {member_drop_count[i]} times.\n')
                j = j + 1
            i += 1

        total_drop_text = f'In the past {message_limit} messages, there have been {total_drop_count} drops.\n\n'
        server_drop_text = f'The server has dropped {server_drop_count} times. \n'
        response = total_drop_text + server_drop_text
        for i in range(len(leaderboard)):
            response = response + leaderboard[i]

        await message.channel.send(response)
    await bot.process_commands(message)

@bot.command(name='effort')
# this is for effort tracking
async def on_message(effort_message_request):
    # don't accept any messages from the bot itself
    if effort_message_request.author.id == KARUTA_BOT:
        return

    # define the bot channel for spam messages
    karuta_bot_channel = bot.get_channel(KARUTA_SPAM)

    # pull the user ID into a variable
    requester_user_id = effort_message_request.author.id
    # initialise the database from the csv file
    database_user_cards = pd.read_csv(
        filepath_or_buffer=r"C:\Users\Ocean\PycharmProjects\discord-karuta-tracker\karutaCardInfoTest.csv",
        sep=',',
        index_col=False,
        dtype={'cardCode': str,
               'cardEffort': np.int16,
               'lastUpdated': np.float64})
    # sort the database by effort in descending order
    database_user_cards.sort_values(by='cardEffort',
                                    ascending=False,
                                    inplace=True)

    # now, get a message which says what data already exists in the database.
    database_match_message_header = "Looks like we have some data already." \
                                    "Here are your best workers, ordered by effort.\n\n"
    database_match_message = database_match_message_header
    i = int(0)
    j = 0
    for i in range(len(database_user_cards)):
        if database_user_cards.iloc[i, 0] == requester_user_id:
            matchedUserCardsMessage = f'#{j + 1}. {database_user_cards.iloc[i, 3]} • {database_user_cards.iloc[i, 2]} • Last Updated: {datetime.utcfromtimestamp(database_user_cards.iloc[i, 4]).strftime("%H:%M %d/%m/%y")} • {database_user_cards.iloc[i, 1]}\n'
            database_match_message = database_match_message + matchedUserCardsMessage
            j += 1
    database_match_message = f'{database_match_message}\n'

    if database_match_message == database_match_message_header:
        database_match_message = "We don't have anything here in the database 🤷"
    await effort_message_request.channel.send(database_match_message)

    # request the user to summon their collection
    bot_collection_request_message = "Please specify what filter you would like to apply (the filter must contain o=w for now). I'd suggest the following:"
    # wait for the message to be sent on the channel
    await effort_message_request.channel.send(bot_collection_request_message)
    await effort_message_request.channel.send('> kc o=w q>2 i=f')
    await effort_message_request.channel.send(
        'If you have lots of mint workers with 100+ effort, try setting q=4 instead')

    # now define a check function which checks that 1) the bot has sent a msg, and 2) that the message contains the user ID.
    def checkBotCollection(m):

        # to check if the user ID is in the descriptor, we must first pull out the descriptor data.
        if m.author.id == KARUTA_BOT:
            if str(requester_user_id) in str(m.embeds[0].description):
                return True
            else:
                return False
        else:
            return False

    # wait for a message to be sent that meets the conditions of checkBotCollection (message sent by the bot which contains the user ID)
    # this will need to be refactored to specifically search for card collection text
    user_collection_message = await bot.wait_for('message', check=checkBotCollection)
    print('Message has been received from the requested user.')

    # need better error handling in case the user doesn't send the right message
    if user_collection_message:
        botCollectionCheckingMessage = 'Masterful keyboard abilities. Looking through your collection now...'
    else:
        botCollectionCheckingMessage = 'Something has gone wrong sadge'

    print('Send Discord message confirming that collection was received.')
    botCollectionReviewMessage = await effort_message_request.channel.send(botCollectionCheckingMessage)

    # define a function which takes in the collection message and parses each entry into an array.
    # cardCollectionMessage must be be the message in the normal Discord format.
    # the function returns the array of card info, with each element containing raw data from each line.
    def extractCardDetails(cardCollectionMessage):
        # parse this description by using the newline as the delimiter
        cardListTemp = cardCollectionMessage.embeds[0].description.split('\n')

        # remove the non card text
        del cardListTemp[0]
        del cardListTemp[0]

        return cardListTemp

    # now extract the card details
    userCollection = extractCardDetails(user_collection_message)
    await botCollectionReviewMessage.edit(
        content="I've seen enough. I'm satisfied.\nDoing some fancy tech stuff, please wait a sec...")
    print('Bot has read in collection message. Proceeding to parse the array...\n')
    # we need to define error handling to handle searches which don't have o=w

    # define the array to contain all our worker info outside of the loop
    workerInfoArray = []

    # after removing non-card entries, we can now clean up the card array so that we can get the card code to search for each card
    i = 0
    for i in range(len(userCollection)):

        # parse each entry on the basis of the middle dot
        userCollection[i] = userCollection[i].split('·')
        # now pull out the element containing the card code
        card_code_array = userCollection[i][1].split('`')
        card_code = card_code_array[1]

        # define the string to be searched through in the job history
        card_code_search_string = f'kwi {card_code}'

        # define the character name for message identification
        card_name_search = userCollection[i][6].split('**')
        print(f'Now we search for entry {i + 1} in the array with {card_name_search[1]} with code {card_code}.')

        # define out card searching algorithm here so that we can multi-thread it. Variables:
        # card_code_search_string: message that the bot searches for
        # karutaBotChannel: channel where messages are contained
        # card_name_search: element of the
        # def cardSearch(card_code_search_string, karutaBotChannel):
        j = 0
        async for elem in karuta_bot_channel.history(limit=500):
            # check to see if there are no embeds, i.e. it is a message from a user.
            # Can alternatively use elem.bot = True
            if not elem.embeds:
                # if not a bot message, then check to see if the message contains the required string
                if card_code_search_string in elem.content:
                    # if it does,then break the loop
                    break
                else:
                    # if it's not in the loop, then we increment i+1. This happens in all cases,
                    # so we take the counter outside the loop (but this is just for debugging anyway)
                    pass
            else:
                # otherwise, if it is a bot message, then save the embed information to a variable
                worker_message_info = elem
            j += 1

        print(
            f'Finished looking for {card_name_search[1]}, a message was found {j} messages ago. Now verify that the message is a worker info message.')

        # can't handle nested lists,so assign the embeds to their own variable
        worker_message_embed = worker_message_info.embeds[0]
        # first, check if the message contains the name of the card that we are looking for
        if card_name_search[1] in worker_message_embed.description:
            # now see if it that message is actually a worker info message
            if 'Effort modifiers' in worker_message_embed.description:
                print('PASS: The message was the correct worker info message.')

                # now parse out the workerInfo variable for the Effort
                workerInfo = worker_message_embed.description.split('\n')
                print(workerInfo)
                # now parse out the effort value from this array
                # first, split up the effort value string
                cardEffort = workerInfo[1].split('**')

                # repeat this process for the character name
                cardName = workerInfo[0].split('**')

                # pull the message info from the original message array
                updateTime = worker_message_info.created_at.strftime("%H:%M %d/%m/%y")

                # and feed these effort value back into the array
                cardInfo = [cardName[1], card_code, int(cardEffort[1]), updateTime]

                # we now want to compare if we should append the value, or update it.
                # iterate through each card code in the DB and check if one of the cards we're pulling exists
                print(f'Checking for {cardName[1]} in our database...')

                # in the event that there is nothing in the DB, just add the cards in.
                if len(database_user_cards) == 0:
                    newEntry = [requester_user_id, cardName[1], card_code, int(cardEffort[1]),
                                worker_message_info.created_at.timestamp()]
                    database_user_cards.loc[database_user_cards.index.max() + 1] = newEntry
                    print('There were no entries in the DB, so entries were added in directly\n')
                else:
                    i = 0
                    for i in range(len(database_user_cards)):
                        # if the card is in the DB already, then run an update
                        if cardInfo[1] == database_user_cards.iloc[i, 2]:
                            # find the index that matches the code in the DB, assumes that only one entry can be added.
                            matchIndex = int(
                                database_user_cards[database_user_cards['cardCode'] == cardInfo[1]].index.values)
                            database_user_cards.iat[matchIndex, 3] = cardEffort[1]
                            database_user_cards.iat[matchIndex, 4] = worker_message_info.created_at.timestamp()
                            print('ENTRY FOUND: updating existing entry in DB\n')
                            # break the loop once found to avoid further iterations
                            break
                        # otherwise, we keep looping through the list of cards until we find a match
                        else:
                            # if we get to the end of the database and there's no match, then the code doesn't exist.
                            # add it as a new entry.
                            i += 1
                            if i == len(database_user_cards):
                                newEntry = [requester_user_id, cardName[1], card_code, int(cardEffort[1]),
                                            worker_message_info.created_at.timestamp()]
                                database_user_cards.loc[database_user_cards.index.max() + 1] = newEntry
                                print('NO ENTRY FOUND: adding new entry to DB\n')
            # if it's not a worker info message, then it's some other message that has the card name in
            else:
                workerInfoArray.append([card_name_search[1], card_code, 0, ''])
                print(f'FAIL: The message had the card name, but was not the worker info message.\n')
        # if it doesn't have the card name in, then it's some other message from the bot.
        else:
            workerInfoArray.append([card_name_search[1], card_code, 0, ''])
            print(f'FAIL: The message was from the bot, but did not have the card name.\n')

    # first, filter out all workers by the requested user id

    print('Sorting the database by effort now..')
    database_user_cards.sort_values(by='cardEffort',
                                    ascending=False,
                                    inplace=True)

    # now, generate the message that displays the worker info.
    workerMessageTitle = f"I'm done <@{requester_user_id}>! Your best workers are listed below (´• ω •`)ﾉ \n\n"
    workerMessageFinal = workerMessageTitle

    print('Generating worker list to push to Discord...')
    i = 0
    j = 0
    # now generate the message to display to the requester. we iterate though the whole database and look for cards
    # that belong to the person requesting the command.
    # since we need to do some formatting in markdown, we will assign this to an array first before writing any messages.
    for i in range(len(database_user_cards)):
        # if there's a match, generate a string which is appended to a final string to be sent out.
        if database_user_cards.iloc[i, 0] == requester_user_id:
            workerEntry = f'#{j + 1}. {database_user_cards.iloc[i][3]} • {database_user_cards.iloc[i][2]} • Last Updated: {datetime.utcfromtimestamp(database_user_cards.iloc[i, 4]).strftime("%H:%M %d/%m/%y")} • {database_user_cards.iloc[i][1]}\n'
            workerMessageFinal = workerMessageFinal + workerEntry
            j += 1

    # filter the database on the requested user Id.
    # this code should be contiued to format in markdown.
    databaseViewUserId = database_user_cards[database_user_cards['userid'] == requester_user_id]
    # markdownCloser = "```"
    # workerMessageFinal = workerMessageFinal + markdownCloser



    print('Worker list has been generated.')

    # earlier, we specified a workerInfoArray, which contains cards for which worker info could not be found.
    # the card codes of these are printed
    failedMatch = ''
    for i in range(len(workerInfoArray)):
        if workerInfoArray[i][2] == 0:
            failedMatch = failedMatch + f'{workerInfoArray[i][1]} '

    print('Failure list has been generated.')

    # now write the dataframe to the csv
    database_user_cards.to_csv('karutaCardInfoTest.csv',
                               float_format='%.5f',
                               index=False)

    if not failedMatch:
        pass
    else:
        workerMessageFinal = workerMessageFinal + f"\nI couldn't find anything again for these cards, please try kwi'ing them again: {failedMatch}"
    await effort_message_request.channel.send(workerMessageFinal)
    await bot.process_commands(effort_message_request)

@bot.event
# this is to find the klu
async def on_message(message):
    if message.author.id == KARUTA_BOT:
        # first, we only want messages with embeds. if this is empty, then break.
        if baseValueFlag == False:
            return

        # we define a function that takes in a message and parses each required piece of information into an array.
        # array index - data
        # 0     - character
        # 1     - series
        # 2     - Wishlisted
        # 3     - empty space
        # 4     - Edition
        # 5     - empty space
        # 6     - total generated
        # 7     - total claimed
        # 8     - total burned
        # 9     - total in circulation
        # 10    - claim rate. not needed to write into our array
        # 11    - average claim rate
        # 12    - empty space
        # 13    - 4* circulation
        # 14    - 3* circulation
        # 15    - 2* circulation
        # 16    - 1* circulation
        # 17    - 0* circulation
        def lookupParser(lookup_message):
            # first, check that the message is from the bot.
            if int(lookup_message.author.id) == KARUTA_BOT:
                # taking input as the lookup message, if the message does not embeds then it's not a lookup message.
                if lookup_message.embeds:
                    # we now check if this is actually the lookup by searching on text that only appears in
                    # the lookup message.
                    # we assign a variable to the embed description due to python limitations
                    message_text = lookup_message.embeds[0].description
                    # once the message is confirmed to be a lookup message, parse the message by a new line
                    if 'Average claim time' in message_text:
                        card_stats = message_text.split("\n")
                        # initialise the array to store all this data
                        card_stats_parsed = []
                        # iterate through each element/line of the message
                        for i in range(len(card_stats)):
                            # there are new line entries: if those are present, then we want to remove these later
                            # we write them to a list
                            j=[]
                            if card_stats[i] == '':
                                pass
                            else:
                                card_stats[i] = card_stats[i].split('·')
                                # remove trailing spaces from the category names
                                card_stats[i][0] = card_stats[i][0].strip()
                                # we now want to remove the formatting on the data. For non-integers, we must
                                # specify the specific elements (character, series, claim time)
                                character_string_elements = [0,1,11]
                                if i in character_string_elements:
                                    card_stats[i][1] = re.sub('[*]', '', card_stats[i][1])
                                    # for the claim time, we must have a more tailored solution. this isn't exactly
                                    # the most elegant solution though.
                                    if i == 11:
                                        card_stats[11][1] = card_stats[11][1].strip()
                                        card_stats[11][1] = card_stats[11][1].split()[0]
                                # all other elements are required in integer form.
                                else:
                                    card_stats[i][1] = re.sub('\D','',card_stats[i][1])
                        return card_stats

        # define a function that calculates the base value
        def baseValueCalculation(generated, claimed, burned):
            arg1 = (float(claimed) / float(generated)) * 100
            arg2 = (float(burned) / float(generated)) * 100

            value = round((arg1 - arg2) * 0.98 - 0.04)
            return value

        # define a function which prints the messages to be sent.
        trash_cutoff = 20
        worker_cutoff = 70
        god_cutoff = 80
        edition_count = 2
        def baseValueResponse(lookup_data):
            if lookup_data:
                base_value = baseValueCalculation(lookup_data[6][1], lookup_data[7][1], lookup_data[8][1])
                # now do some flair to show cutoffs.
                base_message_main = f'The ◈{lookup_data[4][1]} edition{lookup_data[0][1]} has a base value of around {base_value} at ★★★★. '

                if base_value > worker_cutoff:
                    if base_value > god_cutoff:
                        base_value_message_flavour = f'This is god-tier status! (Nezuko has a value of 84)'

                    else:
                        base_value_message_flavour = f"They'll make a good worker (70+ range)."
                else:
                    base_value_message_flavour = ''
                base_message = base_message_main + base_value_message_flavour
                return base_message

        data = lookupParser(message)
        if data:
            responseText = baseValueResponse(data)
            response = await message.channel.send(responseText)
            # if the card has a second edition, then we wait to see if the user want to see the second edition.
            # this can be made more robust in the future. For now, we do a simple check on if the message has been edited.
            # wait for the message to be edited
            await bot.wait_for('message_edit')
            # first, check if the message is updated with second edition info
            if int(lookupParser(message)[4][1]) == 2:
                # we now need to check that the array is of the correct length. we do not want to take messages
                # that have not been released yet.
                if len(lookupParser(message)) > 10:
                    # apply the text generator function to get the second edition message
                    data2 = lookupParser(message)
                    responseText2 = baseValueResponse(data2)
                    await response.edit(content=f"{responseText}\n{responseText2}\n\n*Base value numbers for 2nd"
                                                f" edition cards are not accurate at the moment due to the new release."
                                                f" This should stabilise once more of the cards are printed.* ")
            await bot.process_commands(message)

# @bot.event
# async def on_message(message):
#
#     # define a function that parses out a worker info message
#     # 0     - character
#     # 1     - effort
#     # 2     - healthy | injured for x days
#     # 3     - effort modifiers
#     # 4     - x Base Value
#     # the following are in random order
#     # 5     - x <grade> Wellness
#     # 6     - x <grade> Purity
#     # 7     - x <grade> Quickness
#     # 8     - x <grade> Grabber
#     # 6     - x <grade> Dropper
#     # 6     - x <grade> Style
#     # 6     - x <grade> Toughness
#     def workerInfoParser(lookup_message):
#         # first, check that the message is from the bot.
#         if int(lookup_message.author.id) == KARUTA_BOT:
#             # taking input as the lookup message, if the message does not contain embeds then it's not a lookup message.
#             if lookup_message.embeds:
#                 # we now check if this is actually the lookup by searching on text that only appears in
#                 # the lookup message.
#                 # we assign a variable to the embed description due to python limitations
#                 message_text = lookup_message.embeds[0].description
#                 # once the message is confirmed to be a lookup message, parse the message by a new line
#                 if 'Effort modifiers' in message_text:
#                     worker_stats = message_text.split("\n")
#
#
#         return worker_stats
#
#     print(workerInfoParser(message))

# ---- DEPRECATED CODE ----

# flower detection bot the Valentine's day event 2021. Needs to be refactored to use the bot object.

@client.event
# this event is for the flower event
async def on_reaction_add(reaction, user):
    # define the list of flowers that require a wait time.
    flowers = np.array([
        ['🌹', 809464733320347678],
        ['🌻', 809464799364120586],
        ['🌼', 809498603865243658],
        ['🌷', 809464596539637820]])

    # define how many seconds we want to give for people to grab the flower.
    mentions_cutoff = int(5)
    free_for_all_cutoff = int(45)

    # check if the message was sent by karuta bot
    if user.id == KARUTA_BOT:

        # defining flowerEmoji as our emoji in the list that we check against. we now check each element
        i = 0
        for flowerEmoji in flowers[:, 0]:

            # if the emoji is not matched, then increment by 1
            if str(reaction) != flowerEmoji:
                i += 1

            # if the emoji is matched, then proceed with the rest of the code
            else:
                # pull out the role ID that corresponds to this flower
                flower_role_id = flowers[i, 1]

                # now that we've identified a flower has spawned, send a message in the chat.
                flower_spawn_message = await reaction.message.channel.send(
                    "A flower has spawned! Let me see what kind of flower it is... 🧐")

                # at this point, we will also set the time that the flower spawned.
                spawn_time = time.time()

                # now define the cutoff time after which we want to send the cutoff message.
                mentions_cutoff_time = spawn_time + mentions_cutoff

                # finally for later, we define the free for all time,
                # after which we edit the message to say that anyone can grab it.
                free_for_all_cutoff_time = spawn_time + free_for_all_cutoff

                payload_sent = False
                # wait for a reaction to be added. we want to keep iterating within the cutoff time period and stop
                while time.time() < mentions_cutoff_time:

                    try:
                        # code will wait for a specified period for any reaction to be sent (any)
                        payload = await client.wait_for('raw_reaction_add', timeout=mentions_cutoff)

                        # if none are sent at all, then terminate the code and proceed to send a mention out.
                    except asyncio.exceptions.TimeoutError:
                        print(f'no emoji was received')
                        payload_sent = False

                        # if an emoji was sent in the server, we want to check that it's the right one.
                    else:
                        reacted_emoji = payload.emoji
                        payload_sent = True

                        # now, check if the emoji is the same as the flower we're interested in.
                        if str(reacted_emoji) == flowers[i, 0]:
                            print('the emoji is the same')

                            # before we can proceed, we also want to check that the react was on the initial message.
                            if payload.message_id == reaction.message.id:
                                print('the react is on the same message')

                                # if we have got a flower mention on the same message,
                                # then we set the flag to be False and break the loop.
                                send_mentions = False
                                print('success!')
                                break
                            else:
                                print('the react is on the wrong message')
                                send_mentions = True
                        else:
                            print('the emoji is not the same')
                            send_mentions = True

                print(
                    f'time is up. the cutoff time was {mentions_cutoff_time} '
                    f'and it is now {time.time()}\n The payload flag is {payload_sent}')

                # we need to first check on time in case the payload has not been sent.
                # assuming that we've passed the cutoff time, check if a payload has been sent.
                # if it hasn't, then we can just send the mentions message.
                flower_role_title = discord.utils.get(client.guilds[0].roles, id=int(flower_role_id))
                if payload_sent == False:
                    flower_confirmation_message = await reaction.message.channel.send(
                        f"I've got it: it's a {flowerEmoji} ! "
                        f"I think {flower_role_title.mention} knows how to care for them.")
                    print(
                        'payload sent was False, meaning that either no-one reacted with an emoji, or an emoji was added but not with the appropriate flower.')
                else:
                    # if a payload has been sent, then we check if we should sendMentions or not.
                    # if sendMentions is False, it means that someone claimed the flower.
                    send_followup_mentions = ''
                    if send_mentions == False:
                        await flower_spawn_message.edit(
                            content="I couldn't identify it, looks like someone else has picked it up before I could 😖")
                        print(
                            'payload sent was true, but sendMentions flag was false,'
                            'meaning that someone picked up the flower within the limit.')
                    else:
                        # get the role object for the flower
                        # this will need to be refactored if connected to more than one server
                        flower_confirmation_message = await reaction.message.channel.send(
                            f"I've got it: it's a {flowerEmoji} ! "
                            f"I think {flower_role_title.mention} knows how to care for them.")
                        print(
                            'sendMentions was True, meaning that no-one reacted with the right flower'
                            'and 5 seconds had passed')
                        try:
                            print(
                                f'now that 5s has passed, we wait for the next reaction. '
                                f'This will last {free_for_all_cutoff_time - time.time()} seconds.')
                            payload_second = await client.wait_for('raw_reaction_add',
                                                                   timeout=free_for_all_cutoff_time - time.time())
                        # if no reaction was added, then time it out
                        except asyncio.exceptions.TimeoutError:
                            print(
                                f'a payload still was not received, so we edit our old message,'
                                f'saying that someone should grab the flower.')
                            await flower_confirmation_message.edit(
                                content="That flower looks like it's going to disappear soon,"
                                        "someone should grab it before it does!")
                        # if a reaction was added, first check if it's the right emoji and on the right message.
                        else:
                            # now, check if the emoji is the same as the flower we're interested in.
                            if str(reacted_emoji) == flowers[i, 0]:
                                print('a payload was sent after 5s and the emoji is the same')

                                # before we can proceed, we also want to check that
                                # the react was on the initial message.
                                if payload_second.message_id == reaction.message.id:
                                    print('a payload was sent after 5s the react is on the same message')

                                    # if we have got a flower mention on the same message,
                                    # then we set the flag to be False and break the loop.
                                    send_followup_mentions = False
                                    print('success! the payload was the right flower')
                                    break
                                else:
                                    print('for the second payload, the react is on the wrong message')
                                    send_followup_mentions = True
                            else:
                                print('the emoji is not the same')
                                send_followup_mentions = True

                        # now we've determined if it was the right message. using the usual logic:
                        if send_followup_mentions == True:
                            # if emojis have been placed but not the flower, ie. it still hasn't been claimed, then send out the message.
                            await flower_confirmation_message.edit(
                                content="That flower looks like it's going to disappear soon, someone should grab it before it does!")
                        # if it has been claimed, then send out the claim message instead.
                        else:
                            # write the time left on the timer.
                            timeRemaining = 60 - (time.time() - spawn_time)
                            await flower_confirmation_message.edit(
                                content=f"Phew, looks like someone grabbed it in time. You had {timeRemaining} seconds left to claim it! ")



bot.run(TOKEN)
# client.run(TOKEN)
