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

# import google images package
from google_images_search import GoogleImagesSearch

# import datetime for date updates
from datetime import datetime, timedelta
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

# math
import math

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
bot_prefix = 'pog.'
bot = Bot(command_prefix=bot_prefix.lower())

# get the server for Catwad
localServer = discord.utils.get(client.guilds, name=GUILD)

# define a function which will alter global variables like flags
baseValueFlag = True


@bot.event
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
    requester_user_id = int(effort_message_request.author.id)
    # initialise the database from the csv file
    database_cards = pd.read_csv(filepath_or_buffer=r"initialisedDatabase.csv",
                                 sep=',',
                                 index_col=False,
                                 dtype={'cardCode': str,
                                        'cardEffort': np.int16,
                                        'recoveryDate': np.float64})
    # sort the database by effort in descending order
    database_user_cards = database_cards
    database_user_cards.sort_values(by='cardEffort',
                                    ascending=False,
                                    inplace=True)

    # filter the database on the requested user Id.
    database_user_cards = database_user_cards[database_user_cards['userId'] == requester_user_id]

    # define a function that parses out a worker info message
    # 0     - character
    # 1     - effort
    # 2     - healthy | injured for x days
    # 6     - x, Base, Value
    # the following are in random order
    #       - x, <grade>, Wellness
    #       - x, <grade>, Purity
    #       - x, <grade>, Quickness
    #       - x, <grade>, Grabber
    #       - x, <grade>, Dropper
    #       - x, <grade>, Style
    #       - x, <grade>, Toughness
    def workerInfoParser(lookup_message):
        # first, check that the message is from the bot.
        if int(lookup_message.author.id) == KARUTA_BOT:
            # taking input as the lookup message, if the message does not contain embeds then it's not a lookup message.
            if lookup_message.embeds:
                # we now check if this is actually the lookup by searching on text that only appears in
                # the lookup message.
                # we assign a variable to the embed description due to python limitations
                message_text = lookup_message.embeds[0].description
                # once the message is confirmed to be a lookup message, parse the message by a new line
                if 'Effort modifiers' in message_text:
                    worker_stats = message_text.split("\n")
                    # worker_stats now contains the array of data. To parse out this info, we need different code for
                    # each line.
                    for i in range(len(worker_stats)):
                        # this takes in the first and second elements (character, effort)
                        if i <= 1:
                            worker_stats[i] = worker_stats[i].split('·')
                            # we now remove the asterisks.
                            worker_stats[i][1] = re.sub('[*]', '', worker_stats[i][1])
                        # this condition handles the status
                        if i == 3:
                            # strip all text except for digits.
                            # If it's healthy, we'll get a null.
                            # If it's injured, we'll have a number.
                            worker_stats[i] = re.sub('\D', '', worker_stats[i])
                        if i >= 6:
                            # everything past this value can be sorted on the basis of splitting, then turning the
                            # first index to an integer.
                            worker_stats[i] = worker_stats[i].split()
                            worker_stats[i][0] = (re.sub('\D', '', worker_stats[i][0]))
                        else:
                            pass
                        # all the required information is now contained within worker stats.

        return worker_stats

    # we also define a function which will take in a message date and a time period, then return the recovery date
    # the date is returned in unix time.
    def recoveryDateCalculator(message_time, injury_days):
        if injury_days:
            recovery_date = message_time + timedelta(days=int(injury_days))
            return recovery_date.replace(tzinfo=timezone.utc).timestamp()
        # if the variable passed in is null, then we return null too.
        else:
            return

    # define a function which takes in a database and spits out an array of worker info, with each index corresponding
    # to page of worker details
    def workerInfoGenerator(database):
        # go through each column and find the max element of each column
        # define an array which contains the length of each
        # for ease of formatting, we need the lengths of all the data we are going to input.
        column_lengths = [len(str('User ID')),
                          len(str('Character Name')),
                          len(str('CardCode')),
                          len(str('Effort')),
                          len(str('Last Updated'))]
        for j in range(len(database.columns)):
            # in each column, iterate through each row and find the length of each element, keeping the longest element
            # 0     - user Id
            # 1     - character name
            # 2     - card code
            # 3     - effort
            # 4     - last updated
            for i in range(len(database)):
                if column_lengths[j] < len(str(database.iloc[i, j])):
                    column_lengths[j] = len(str(database.iloc[i, j]))

        # column_lengths now contains the maximum length of each string.
        # now, we define an array which contains the titles that we want
        embed_title_text = f"| {'Effort'.ljust(column_lengths[3])} |" \
                           f" {'CardCode'.center(column_lengths[2])} |" \
                           f" {'Character'.ljust(column_lengths[1])} |\n"
        embed_title_underline = f"|{'-' * ((column_lengths[3]) + 2)}|" \
                                f"{'-' * ((column_lengths[2]) + 2)}|" \
                                f"{'-' * ((column_lengths[1]) + 2)}|\n"
        embed_header = embed_title_text + embed_title_underline

        # now generate the string for each entry. To separate entries into pages, we need to find the number of pages
        # required.
        embed_pages = math.ceil(len(database) / 10)
        table_string_pages = []
        # iterate through each page. because loop indices initiate at 0, we remove a 1 from the number of pages.
        for page in range(embed_pages):
            # on each page, we only want 10 entries except for on the final page, so do a check for that.
            # if it's not the final page, we want to iterate from the 0th to the 9th element.
            table_string_page_content = ''
            if page != (embed_pages - 1):
                # we add 1 to page because for loops initialise the index at 1
                for i in range((page * 10), ((page + 1) * 10)):
                    table_string = f"| {str(database.iloc[i, 3]).rjust(column_lengths[3])} |" \
                                   f" {str(database.iloc[i, 2]).center(column_lengths[2])} |" \
                                   f" {str(database.iloc[i, 1]).ljust(column_lengths[1])} |\n"
                    table_string_page_content = table_string_page_content + table_string
            # if not, then we're on the final page.
            elif page == (embed_pages - 1):
                for i in range((page * 10), len(database)):
                    table_string = f"| {str(database.iloc[i, 3]).rjust(column_lengths[3])} |" \
                                   f" {str(database.iloc[i, 2]).center(column_lengths[2])} |" \
                                   f" {str(database.iloc[i, 1]).ljust(column_lengths[1])} |\n"
                    table_string_page_content = table_string_page_content + table_string
            table_string_pages.insert(page, embed_header + table_string_page_content)
        return table_string_pages

    worker_pages = workerInfoGenerator(database_user_cards)

    # read in the event database table to get the latest time.
    effort_update_event_database = pd.read_csv(filepath_or_buffer=r"workerUpdateEvent.csv",
                                               sep=',',
                                               index_col=False,
                                               dtype={'timeRequested': np.float64})
    # sort the update event in datetime
    effort_update_event_database.sort_values(by='timeRequested',
                                             ascending=False,
                                             inplace=True)

    if database_user_cards.empty:
        embed_message = await effort_message_request.channel.send("I couldn't find any worker info for you etc placeholder text xd, just hit the search emoji pls")

    else:
        # filter the database by the selected user:
        filtered_event_time_database = effort_update_event_database.where(
            effort_update_event_database['requestedBy'] == str(effort_message_request.author.id))

        # now remove all NaNs from the grid.
        filtered_event_time_database = filtered_event_time_database[
            filtered_event_time_database["requestedBy"].notnull()]

        # if the grid is empty, this means that we filtered by the selected user and all results were invalid.
        # in this scenario, we want to search for any entries that were done manually (by the bot)
        if filtered_event_time_database.empty:
            # filter database on Initialiser entries.
            effort_update_event_database = effort_update_event_database[effort_update_event_database['requestedBy'] == "Initialiser"]
            user_update_time = effort_update_event_database['timeRequested'].where(
                effort_update_event_database['requestedBy'] == "Initialiser").iloc[0]

            # convert this unix time to a string that front end users can understand
            user_update_time_text = datetime.utcfromtimestamp(user_update_time).strftime("%H:%M %d/%m/%y")
            user_updated_by = str("me, beep boop")

            # we can also define what message we would like to appear here
            search_prompt_header_text = f"The last search was run at {user_update_time_text} by {user_updated_by}.\n\n" \
                                        f"If you'd like me to update your worker list, please react with 🔍."
        # otherwise, we can filter normally:
        else:
            # filter for the selected user and get the most recent event for that user.
            user_update_time = filtered_event_time_database['timeRequested'].where(
                filtered_event_time_database['requestedBy'] == str(effort_message_request.author.id)).iloc[0]
            # convert this unix time to a string that front end users can understand
            user_update_time_text = datetime.utcfromtimestamp(user_update_time).strftime("%H:%M %d/%m/%y")

            search_prompt_header_text = f"You last updated your workers on {user_update_time_text}.\n \n"

        search_description_message = search_prompt_header_text + f"If you'd like me to update your worker list," \
                                                                 f" please react with 🔍."

        # now create an embed.
        # we also want a comment saying when the last search was run.
        worker_table_message = f'Workers owned by <@{requester_user_id}>, sorted by effort.\n' \
                               f'```python\n{worker_pages[0]}```\n'
        filteredEmbed = discord.Embed(title='Top Worker List',
                                      description=worker_table_message + f'{search_description_message}',
                                      footer='',
                                      colour=int('FFA500', 16)
                                      )
        # set a variable which determines the page number
        page_number = 1

        # define a function for the footer

        # we need to define a variable for the paging of the footer message.
        if len(database_user_cards) < 10:
            initial_page_upper_range = len(database_user_cards)
        else:
            initial_page_upper_range = page_number * 10

        filteredEmbed.set_footer(text=f"Showing workers "
                                      f"{((page_number - 1) * 10) + 1}-{initial_page_upper_range} of {len(database_user_cards)}",
                                 icon_url='https://www.nicepng.com/png/full/155-1552831_yay-for-the-transparent-diamond-pickaxe-im-bored.png')

        filteredEmbed.set_author(name="Top Worker List",
                                 icon_url='https://www.nicepng.com/png/full/155-1552831_yay-for-the-transparent-diamond-pickaxe-im-bored.png')

        embed_message = await effort_message_request.channel.send(embed=filteredEmbed)

    # this should be refactored into a for loop
    await embed_message.add_reaction('⬅️')
    time.sleep(0.5)
    await embed_message.add_reaction('➡️')
    time.sleep(0.5)
    await embed_message.add_reaction('❌')
    time.sleep(0.5)
    await embed_message.add_reaction('🔍')
    updated_embed = None
    # we want to timeout the message after a certain time
    embed_cutoff_time = embed_message.created_at.timestamp() + float(120)

    while float(time.time()) < embed_cutoff_time:
        try:
            payload = await bot.wait_for('raw_reaction_add', timeout=embed_cutoff_time)
        # we go down this route if there was no reaction added
        except asyncio.exceptions.TimeoutError:
            print('ending workflow')
            return
        # we only proceed with the code if the user reacted with the right emojis.
        if payload.member.id == requester_user_id:
            if payload.message_id == embed_message.id:
                if str(payload.emoji) in ['⬅️', '➡️', '🔍', '❌']:
                    # if this is met, then we say if its right, then increment the page number by 1
                    # update the content
                    # also update the footer
                    if str(payload.emoji) == '➡️':
                        # if the page number is equal to the max number of pages, we cannot go any further forward.
                        if page_number == len(worker_pages):
                            pass
                        # otherwise we should edit the message to display the previous page of results.
                        else:
                            page_number += 1

                            # to make message editing easier, we save the first two lines into a variable.
                            worker_table_message = f'Workers owned by <@{requester_user_id}>, sorted by effort.\n' \
                                                   f'```python\n{worker_pages[page_number - 1]}```\n'

                            # since we've stored this into an array, the Nth page actually corresponds to the (N-1)th index
                            updated_embed = discord.Embed(title='Top Worker List',
                                                          description=worker_table_message + f'{search_description_message}',
                                                          footer='',
                                                          colour=int('FFA500', 16))
                            # the footer needs to show the correct number of workers at the max limit.
                            if page_number == len(worker_pages):
                                updated_embed.set_footer(text=f"Showing workers "
                                                              f"{((page_number - 1) * 10) + 1}-{len(database_user_cards)} of {len(database_user_cards)}",
                                                         icon_url='https://www.nicepng.com/png/full/155-1552831_yay-for-the-transparent-diamond-pickaxe-im-bored.png')
                            else:
                                updated_embed.set_footer(text=f"Showing workers "
                                                              f"{((page_number - 1) * 10) + 1}-{page_number * 10} of {len(database_user_cards)}",
                                                         icon_url='https://www.nicepng.com/png/full/155-1552831_yay-for-the-transparent-diamond-pickaxe-im-bored.png')

                            await embed_message.edit(embed=updated_embed)

                    if str(payload.emoji) == '⬅️':
                        # if the page_number is 1, we cannot go any further back. this is invalid so we do nothing
                        if page_number == 1:
                            pass
                        # otherwise we should edit the message to display the previous page of results.
                        else:
                            # decrease the page_number by 1, then pull in the array corresponding to that page.
                            page_number -= 1
                            worker_table_message = f'Workers owned by <@{requester_user_id}>, sorted by effort.\n' \
                                                   f'```python\n{worker_pages[page_number - 1]}```\n'
                            # since we've stored this into an array, the Nth page actually corresponds to the (N-1)th index
                            updated_embed = discord.Embed(title='Top Worker List',
                                                          description=worker_table_message + f'{search_prompt_header_text}',
                                                          footer='',
                                                          colour=int('FFA500', 16)
                                                          )
                            updated_embed.set_footer(text=f"Showing workers "
                                                          f"{((page_number - 1) * 10) + 1}-{page_number * 10} of {len(database_user_cards)}",
                                                     icon_url='https://www.nicepng.com/png/full/155-1552831_yay-for-the-transparent-diamond-pickaxe-im-bored.png')
                        await embed_message.edit(embed=updated_embed)

                    if str(payload.emoji) == '❌':
                        break

                    if str(payload.emoji) == '🔍':
                        # get the description from before, and append the searching message.
                        current_embed_description = worker_table_message + f"Searching for your cards now... this might " \
                                                                           f"take me a while, so I'll send you a new " \
                                                                           f"message when I'm done."
                        search_embed = discord.Embed(title='Top Worker List',
                                                     description=current_embed_description,
                                                     footer='',
                                                     colour=int('ADD8E6', 16)
                                                     )
                        await embed_message.edit(embed=search_embed)

                        # now run a search for the kwi commands as usual.
                        character_name_data = []
                        card_code_data = []
                        card_effort_data = []
                        recovery_date_data = []

                        # get the new update time
                        new_user_update_time = time.time()

                        message_array = await effort_message_request.channel.history(
                            after=datetime.utcfromtimestamp(user_update_time),
                            limit=None).flatten()

                        message_array.reverse()
                        print(
                            f'MESSAGES FOUND: It has been {time.time() - new_user_update_time} seconds since code '
                            f'started. I found {len(message_array)} messages')
                        previous_message = ''
                        valid_bot_message_titles = ['Card Details', 'Card Collection']
                        for msg in message_array:
                            # first, we only want messages from the current user.
                            if msg.author.id == requester_user_id:
                                # for each message, look for all messages of format 'kwi <code>'. we can ignore anything with
                                # content that is empty, as these are bot messages.
                                if msg.content:
                                    # if there is a message, then the way to identify if it is a kwi is by splitting it
                                    # this should produce an array of ['kwi', <cardcode>]
                                    message_split = msg.content.split()
                                    if len(message_split) == 2:
                                        # we now want only messages that contain "kwi".
                                        if message_split[0] == 'kwi':
                                            # if we match a kwi, this means the message is of the form kwi <string>.
                                            # we now check to see if we've matched this code before. If we have, then we skip.
                                            if message_split[1] not in card_code_data:
                                                # now that we've matched a new card code, make sure that the previous message
                                                # contains an embed.
                                                if previous_message.embeds:
                                                    # just in case we get the message is incorrect, we will check to see if the embed
                                                    # content contains worker information.
                                                    if 'Effort modifiers' in previous_message.embeds[0].description:
                                                        # now run our parser to pull out the required data. we should refactor this fn to save
                                                        # on compute time.
                                                        parsed_message = workerInfoParser(previous_message)

                                                        # before creating the database entry, we generate the recovery date if applicable.
                                                        recovery_date = recoveryDateCalculator(
                                                            previous_message.created_at,
                                                            (parsed_message[3]))

                                                        # now add data to each of the list elements. we don't add to the user id column
                                                        # since anyone can run a kwi
                                                        character_name_data.append(parsed_message[0][1].strip())
                                                        card_code_data.append(message_split[1])
                                                        card_effort_data.append(int(parsed_message[1][1].strip()))
                                                        recovery_date_data.append(recovery_date)
                                # if the message does not have content, then it's a bot message and we want to note down the user info

                            # regardless of if it was matched, we now write the message to a variable.
                            # this allows us to compare previous messages to current ones.
                            previous_message = msg

                        print(
                            f'CODES FOUND: It has been {time.time() - new_user_update_time} seconds since code started. I found {len(card_code_data)} codes ')

                        # now, search through and verify the codes.
                        # first, define the array with empty data
                        user_id_data = [''] * len(character_name_data)
                        valid_bot_message_titles = ['Card Details', 'Card Collection']
                        for code in range(len(card_code_data)):
                            async for elem in effort_message_request.channel.history(limit=len(message_array)):
                                # only proceed if the message was from the bot
                                if elem.author.id == KARUTA_BOT:
                                    # only proceed if the message had embeds
                                    if elem.embeds:
                                        # only proceed if the title of the embed matches the ones that we want
                                        if elem.embeds[0].title in valid_bot_message_titles:
                                            # only proceed if the code was found in the embeds
                                            if card_code_data[code] in elem.embeds[0].description:
                                                text = elem.embeds[0].description
                                                # search for the first instance of a user id
                                                user_id = re.search('@(.+?)>', text)
                                                user_id_string = user_id.group(1)
                                                user_id_data[code] = int(user_id_string)
                                                # once we've made a match, we can break the for loop and move onto the next code.
                                                break

                        print(
                            f"VERIFIED CODES: {sum(x == requester_user_id for x in user_id_data)} out of {len(card_code_data)} codes were verified.")

                        data = {'userId': user_id_data,
                                'characterName': character_name_data,
                                'cardCode': card_code_data,
                                'cardEffort': card_effort_data,
                                'recoveryDate': recovery_date_data
                                }
                        # We now create the searched effort database which we can update the original database with.
                        searched_effort_database = pd.DataFrame(data=data,
                                                                columns=['userId', 'characterName', 'cardCode',
                                                                         'cardEffort', 'recoveryDate'])

                        # we save a copy of this with all the unapplicable values
                        unmatched_worker_database = searched_effort_database[~searched_effort_database.userId.isin([requester_user_id])]

                        unmatched_worker_database.sort_values(by='cardEffort',
                                                              ascending=False,
                                                              inplace=True)

                        # filter database by requested user
                        searched_effort_database = searched_effort_database[
                            searched_effort_database['userId'] == requester_user_id]

                        # sort the database by effort in descending order
                        searched_effort_database.sort_values(by='cardEffort',
                                                             ascending=False,
                                                             inplace=True)

                        for code in searched_effort_database.cardCode.values:
                            # search the database to see if the card is in there.
                            if code in database_cards.cardCode.values:
                                # if the code is present, then we want to append that value in the main database.
                                # we need to get the index of the card first.
                                matchIndex = database_cards[database_cards['cardCode'] == code].index[0]
                                print(f"MATCHED: updating DB entry")
                                # we now replace the row with the row from our seaarched and filtered database
                                database_cards.loc[matchIndex] = searched_effort_database.loc[
                                    searched_effort_database[
                                        searched_effort_database['cardCode'] == code].index[0]]

                            # if there is no match, then we need to append it to the database, rather than updating.
                            else:
                                database_cards.loc[database_cards.index.max() + 1] = \
                                    searched_effort_database.loc[searched_effort_database[
                                        searched_effort_database['cardCode'] == code].index[0]]
                                print(
                                    f"NO MATCH: adding new entry to DB")

                        # We want to display the data that has no userId.
                        unmatched_worker_pages = workerInfoGenerator(unmatched_worker_database)

                        # initialise the embed

                        # we now re-initialise our page_number variable for paging on this new message
                        page_number = 1

                        if unmatched_worker_pages:
                            if sum(x == requester_user_id for x in user_id_data) == 0:
                                embed_header_text = f"Hmm, looks like I couldn't actually find any cards that" \
                                                            f" belonged to you... \n" \
                                                            f"Take a look at these and if they're yours, please run" \
                                                            f" a kcharacterinfo command and a kworkerinfo command" \
                                                            f" for those cards, and run me again!"

                                search_embed = discord.Embed(title='Card Matching Failed',
                                                             description='',
                                                             footer='',
                                                             colour=int('800000', 16))

                            # if there were unmatched workers and we were able to match some of them, then we edit the
                            # description message and change the colour of the embed.
                            else:
                                embed_header_text = f"I've found all your cards! By the way, I found these codes but " \
                                                            f"weren't able to verify that they were yours. If they were, " \
                                                            f"please run a kcharacterinfo command and a kworkerinfo command" \
                                                            f" for those cards and run me again! "
                                search_embed = discord.Embed(title='Cards Updated',
                                                             description='',
                                                             footer='',
                                                             colour=int('00FF00', 16))

                            current_embed_description = embed_header_text + \
                                                        f"```python\n{unmatched_worker_pages[0]}```\n" \
                                                        f"Here's some stats:"

                            if len(unmatched_worker_database) < 10:
                                initial_page_upper_range = len(unmatched_worker_database)

                            else:
                                initial_page_upper_range = page_number * 10
                            search_embed.set_footer(
                                text=f"Showing workers {((page_number - 1) * 10) + 1}-{initial_page_upper_range} of "
                                     f"{len(unmatched_worker_database)}")
                        else:
                            current_embed_description = f"Lucky you, looks like I was able to verify that all of the " \
                                                        f"cards I found belonged to you! Have some stats anyway."
                            search_embed = discord.Embed(title='Cards Updated',
                                                         description='',
                                                         footer='',
                                                         colour=int('00FF00', 16))

                        # now we add our constant elements:
                        search_embed.description = current_embed_description

                        search_embed.add_field(name="Cards Found",
                                               value=len(card_code_data),
                                               inline=True)
                        search_embed.add_field(name="Cards Verified",
                                               value=sum(x == requester_user_id for x in user_id_data),
                                               inline=True)
                        search_embed.add_field(name="Cards Unverified",
                                               value=len(card_code_data) - sum(x == requester_user_id for x in user_id_data),
                                               inline=True)
                        
                        search_embed.add_field(name="Time Taken",
                                               value=f"{round(time.time() - new_user_update_time,2)} seconds ")

                        search_results_message = await effort_message_request.channel.send(
                            content=f"<@{requester_user_id}>",
                            embed=search_embed)

                        # write the update event data to a dataframe, then write it into the database.
                        update_event = pd.DataFrame({'requestedBy': [requester_user_id],
                                                     'timeRequested': [embed_message.created_at.timestamp()]})

                        update_event.to_csv('workerUpdateEvent.csv',
                                            float_format='%.5f',
                                            mode='a',
                                            index=False,
                                            header=False)

                        database_cards.to_csv('initialisedDatabase.csv',
                                              float_format='%.5f',
                                              index=False)

                        # initialise the page number variable for this message
                        search_embed_page_number = 1


                        if len(unmatched_worker_pages) >= 2:
                            # set a variable to the amount of time we want the user to be able to browse the pages
                            user_paging_duration = float(120)
                            await search_results_message.add_reaction('⬅️')
                            time.sleep(0.5)
                            await search_results_message.add_reaction('➡️')
                            while float(time.time()) < search_results_message.created_at.timestamp() + user_paging_duration:

                                try:
                                    payload = await bot.wait_for('raw_reaction_add', timeout=user_paging_duration)
                                # we go down this route if there was no reaction added
                                except asyncio.exceptions.TimeoutError:
                                    print('ending workflow')
                                    return
                                # we only proceed with the code if the user reacted with the right emojis.
                                print('found a payload')
                                if payload.member.id == requester_user_id:
                                    print(f'payload is from the requested user')
                                    if payload.message_id == search_results_message.id:
                                        if str(payload.emoji) in ['⬅️', '➡️']:
                                            # if this is met, then we say if its right, then increment the page number by 1
                                            # update the content
                                            # also update the footer
                                            if str(payload.emoji) == '➡️':
                                                # if the page number is equal to the max number of pages, we cannot go any further forward.
                                                if search_embed_page_number == len(unmatched_worker_pages):
                                                    pass
                                                # otherwise we should edit the message to display the previous page of results.
                                                else:
                                                    search_embed_page_number += 1

                                                    # to make message editing easier, we save the first two lines into a variable.
                                                    search_embed.description = embed_header_text + \
                                                        f"```python\n{unmatched_worker_pages[search_embed_page_number-1]}```\n" \
                                                        f"Here's some stats anyway..."

                                                    # the footer needs to show the correct number of workers at the max limit.
                                                    if search_embed_page_number == len(unmatched_worker_pages):
                                                        search_embed.set_footer(text=f"Showing workers "
                                                                                      f"{((search_embed_page_number - 1) * 10) + 1}-{len(unmatched_worker_database)} of {len(unmatched_worker_database)}",
                                                                                 icon_url='https://www.nicepng.com/png/full/155-1552831_yay-for-the-transparent-diamond-pickaxe-im-bored.png')
                                                    else:
                                                        search_embed.set_footer(text=f"Showing workers "
                                                                                      f"{((search_embed_page_number - 1) * 10) + 1}-{search_embed_page_number * 10} of {len(unmatched_worker_database)}",
                                                                                 icon_url='https://www.nicepng.com/png/full/155-1552831_yay-for-the-transparent-diamond-pickaxe-im-bored.png')

                                            if str(payload.emoji) == '⬅️':
                                                # if the page_number is 1, we cannot go any further back. this is invalid so we do nothing
                                                if search_embed_page_number == 1:
                                                    pass
                                                # otherwise we should edit the message to display the previous page of results.
                                                else:
                                                    # decrease the page_number by 1, then pull in the array corresponding to that page.
                                                    search_embed_page_number -= 1
                                                    search_embed.description = embed_header_text + \
                                                        f"```python\n{unmatched_worker_pages[search_embed_page_number-1]}```\n" \
                                                        f"Here's some stats anyway..."
                                                    search_embed.set_footer(text=f"Showing workers "
                                                                                  f"{((search_embed_page_number - 1) * 10) + 1}-{search_embed_page_number * 10} of {len(unmatched_worker_database)}",
                                                                             icon_url='https://www.nicepng.com/png/full/155-1552831_yay-for-the-transparent-diamond-pickaxe-im-bored.png')
                                            await search_results_message.edit(embed=search_embed)

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
                            j = []
                            if card_stats[i] == '':
                                pass
                            else:
                                card_stats[i] = card_stats[i].split('·')
                                # remove trailing spaces from the category names
                                card_stats[i][0] = card_stats[i][0].strip()
                                # we now want to remove the formatting on the data. For non-integers, we must
                                # specify the specific elements (character, series, claim time)
                                character_string_elements = [0, 1, 11]
                                if i in character_string_elements:
                                    card_stats[i][1] = re.sub('[*]', '', card_stats[i][1])
                                    # for the claim time, we must have a more tailored solution. this isn't exactly
                                    # the most elegant solution though.
                                    if i == 11:
                                        card_stats[11][1] = card_stats[11][1].strip()
                                        card_stats[11][1] = card_stats[11][1].split()[0]
                                # all other elements are required in integer form.
                                else:
                                    card_stats[i][1] = re.sub('\D', '', card_stats[i][1])
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

        try:
            data = lookupParser(message)
        except:
            if message.embeds:
                message_info = message.embeds[0].description
            else:
                message_info = message.content
            print(f'Lookup bot found an error, it probably received the wrong message. Here is the message:\n'
                  f'{message.info}\n\n')

        if data:
            responseText = baseValueResponse(data)
            response = await message.channel.send(responseText)
            # if the card has a second edition, then we wait to see if the user want to see the second edition.
            # this can be made more robust in the future. For now, we do a simple check on if the message has been edited.
            # wait for the message to be edited
            await bot.wait_for('message_edit')
            try:
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
            except:
                print('The message did not have any data for the 2nd edition.')

    await bot.process_commands(message)


@bot.command(name='effortInitialiser')
# this scans all messages for worker information. takes long to run!
async def on_message(message):
    # define a function that parses out a worker info message
    # 0     - character
    # 1     - effort
    # 2     - healthy | injured for x days
    # 6     - x, Base, Value
    # the following are in random order
    #       - x, <grade>, Wellness
    #       - x, <grade>, Purity
    #       - x, <grade>, Quickness
    #       - x, <grade>, Grabber
    #       - x, <grade>, Dropper
    #       - x, <grade>, Style
    #       - x, <grade>, Toughness
    def workerInfoParser(lookup_message):
        # first, check that the message is from the bot.
        if int(lookup_message.author.id) == KARUTA_BOT:
            # taking input as the lookup message, if the message does not contain embeds then it's not a lookup message.
            if lookup_message.embeds:
                # we now check if this is actually the lookup by searching on text that only appears in
                # the lookup message.
                # we assign a variable to the embed description due to python limitations
                message_text = lookup_message.embeds[0].description
                # once the message is confirmed to be a lookup message, parse the message by a new line
                if 'Effort modifiers' in message_text:
                    worker_stats = message_text.split("\n")
                    # worker_stats now contains the array of data. To parse out this info, we need different code for
                    # each line.
                    for i in range(len(worker_stats)):
                        # this takes in the first and second elements (character, effort)
                        if i <= 1:
                            worker_stats[i] = worker_stats[i].split('·')
                            # we now remove the asterisks.
                            worker_stats[i][1] = re.sub('[*]', '', worker_stats[i][1])
                        # this condition handles the status
                        if i == 3:
                            # strip all text except for digits.
                            # If it's healthy, we'll get a null.
                            # If it's injured, we'll have a number.
                            worker_stats[i] = re.sub('\D', '', worker_stats[i])
                        if i >= 6:
                            # everything past this value can be sorted on the basis of splitting, then turning the
                            # first index to an integer.
                            worker_stats[i] = worker_stats[i].split()
                            worker_stats[i][0] = (re.sub('\D', '', worker_stats[i][0]))
                        else:
                            pass
                        # all the required information is now contained within worker stats.

        return worker_stats

    # we also define a function which will take in a message date and a time period, then return the recovery date
    # the date is returned in unix time.
    def recoveryDateCalculator(message_time, injury_days):
        if injury_days:
            recovery_date = message_time + timedelta(days=int(injury_days))
            return recovery_date.replace(tzinfo=timezone.utc).timestamp()
        # if the variable passed in is null, then we return null too.
        else:
            return

    # sample test code
    # async for elem in message.channel.history(limit=5):
    #     # proceed if there is no message content
    #     if not elem.content:
    #         # define the string into a variable
    #         text = elem.embeds[0].description
    #         # search for the first instance of a user id
    #         m = re.search('@(.+?)>', text)
    #         if m:
    #             found = m.group(1)
    #             print(found)
    # exit()

    confirmation_message = await message.channel.send('This will scan the entire server for worker information. '
                                                      'This will take a looong time, are you sure you '
                                                      'want to continue?')
    await confirmation_message.add_reaction('❌')
    time.sleep(1)
    await confirmation_message.add_reaction('✅')

    payload = ''

    # define a function which only takes in emojis from the person requesting the search
    proceed_flag = False
    while proceed_flag == False:
        try:
            payload = await bot.wait_for('raw_reaction_add', timeout=10.0)
        except asyncio.exceptions.TimeoutError:
            proceed_flag = True
            print('ending workflow')
            return
        if payload.member.id == message.author.id:
            if payload.message_id == confirmation_message.id:
                if str(payload.emoji) in ['✅', '❌']:
                    proceed_flag = True
                    break

    if str(payload.emoji) == '✅':
        time.sleep(1)
        await confirmation_message.add_reaction('👍')
        proceed_flag = False
        while proceed_flag == False:
            try:
                payload = await bot.wait_for('raw_reaction_add', timeout=10.0)
            except asyncio.exceptions.TimeoutError:
                proceed_flag = True
                return
            if payload.member.id == message.author.id:
                if payload.message_id == confirmation_message.id:
                    if str(payload.emoji) == '👍':
                        proceed_flag = True
                        break
        if str(payload.emoji) == '👍':
            start_time = time.time()
            await confirmation_message.edit(content='Looking through all messages, this might take a while...')
            previous_message = ''

            # define the arrays that we will be writing to for the bot
            user_id_data = []
            character_name_data = []
            card_code_data = []
            card_effort_data = []
            recovery_date_data = []

            # define the message limit in a variable
            message_limit = None

            async for elem in message.channel.history(limit=message_limit):
                # for each message, look for all messages of format 'kwi <code>'. we can ignore anything with
                # content that is empty, as these are bot messages.
                if elem.content:
                    # if there is a message, then the way to identify if it is a kwi is by splitting it
                    # this should produce an array of ['kwi', <cardcode>]
                    message_split = elem.content.split()
                    if len(message_split) == 2:
                        # we now want only messages that contain "kwi".
                        if message_split[0] == 'kwi':
                            # if we match a kwi, this means the message is of the form kwi <string>.
                            # we now check to see if we've matched this code before. If we have, then we skip.
                            if message_split[1] not in card_code_data:
                                # now that we've matched a new card code, make sure that the previous message
                                # contains an embed.
                                if previous_message.embeds:
                                    # just in case we get the message is incorrect, we will check to see if the embed
                                    # content contains worker information.
                                    if 'Effort modifiers' in previous_message.embeds[0].description:
                                        # now run our parser to pull out the required data. we should refactor this fn to save
                                        # on compute time.
                                        parsed_message = workerInfoParser(previous_message)

                                        # before creating the database entry, we generate the recovery date if applicable.
                                        recovery_date = recoveryDateCalculator(previous_message.created_at,
                                                                               (parsed_message[3]))

                                        # now add data to each of the list elements. we don't add to the user id column
                                        # since anyone can run a kwi
                                        character_name_data.append(parsed_message[0][1].strip())
                                        card_code_data.append(message_split[1])
                                        card_effort_data.append(parsed_message[1][1].strip())
                                        recovery_date_data.append(recovery_date)

                # regardless of if it was matched, we now write the message to a variable.
                # this allows us to compare previous messages to current ones.
                previous_message = elem

            # once the list of workers has been generated, we need to run another check to make sure that the person
            # actually owns the card. We have assumed that the person doing the kwi command owns it, so we now do a
            # check for the first message that is:
            # - by the bot
            # - contains the card code
            # - contains the text "card details", or the text "cards carried by"

            await message.channel.send(
                f'Finished searching for codes, I found {len(card_code_data)} codes. Now matching for users...')

            # adding error handling:
            try:
                # define the array with empty data
                user_id_data = [None] * len(character_name_data)
                valid_bot_message_titles = ['Card Details', 'Card Collection']
                for code in range(len(card_code_data)):
                    print(f'Searching for card code: {card_code_data[code]}')
                    async for elem in message.channel.history(limit=message_limit):
                        # only proceed if the message was from the bot
                        if elem.author.id == KARUTA_BOT:
                            print('Found a message from the bot.')
                            # only proceed if the message had embeds
                            if elem.embeds:
                                print('Found a bot message with embeds.')
                                # only proceed if the title of the embed matches the ones that we want
                                if elem.embeds[0].title in valid_bot_message_titles:
                                    print('The bot message is a Card Details or a Card Collection message.')
                                    # only proceed if the code was found in the embeds
                                    if card_code_data[code] in elem.embeds[0].description:
                                        print('Found the card code in the embed content.')
                                        text = elem.embeds[0].description
                                        # search for the first instance of a user id
                                        user_id = re.search('@(.+?)>', text)
                                        user_id_string = user_id.group(1)
                                        user_id_data[code] = user_id_string
                                        print(f'ID found: {user_id_string}\n')
                                        # once we've made a match, we can break the for loop and move onto the next code.
                                        break
                                    else:
                                        print('Could not find the card code in the bot message\n')
                                else:
                                    print('Bot message was not a valid message.\n')
                            else:
                                print('The message did not have any embeds\n')
                        else:
                            print(f'The author of the message was not the bot\n')

            except:
                if elem.embeds:
                    print(f"Found an error. Here's some info: \n"
                          f"I was searching for card code = {card_code_data[code]}\n"
                          f"The message i matched had this text in it = {elem.content}\n"
                          f"The embed content was as follows = {elem.embeds[0].description}\n"
                          f"And the title of the embed was {elem.embed[0].title}\n, which I was checking against {valid_bot_message_titles}")
                else:
                    print(f"Found an error. Here's some info: \n"
                          f"I was searching for card code = {card_code_data[code]}\n"
                          f"The message i matched had this text in it = {elem.content}")
                await message.channel.send("I broke! There was an error, please let my bot master know.")

            finally:
                # turn our array into a database
                data = {'userId': user_id_data,
                        'characterName': character_name_data,
                        'cardCode': card_code_data,
                        'cardEffort': card_effort_data,
                        'recoveryDate': recovery_date_data}

                effort_database = pd.DataFrame(data=data)
                effort_database.to_csv('initialisedDatabase.csv',
                                       index=False,
                                       float_format='%.5f')

                # now write out an informational message
                finished_time = time.time()
                elapsed_time = finished_time - start_time
                await confirmation_message.channel.send(content=f"All done <@{message.author.id}> ! "
                                                                f"I've recorded {len(user_id_data)} codes, "
                                                                f"of which {len([x for x in user_id_data if x is not None])} were matched to users. "
                                                                f"This took me {str(round(elapsed_time, 2))} seconds.")

                # write the update event data to a dataframe, then write it into the database.
                update_event = pd.DataFrame({'requestedBy': ['Initialiser'],
                                             'timeRequested': [start_time]})
                update_event.to_csv('workerUpdateEvent.csv',
                                    float_format='%.5f',
                                    mode='a',
                                    index=False,
                                    header=False)

    if str(payload.emoji) == '❌':
        await confirmation_message.edit(content="Gotcha, I won't go snooping around.")

    # await bot.process_commands(message)


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
