# karuta-bot-tracker

The purpose of this bot is to provide some quality of life improvements to the Karuta Bot game on Discord, link https://karuta.xyz/. First, some FAQs:

## Isn't this against ToS?

This is a bit of a grey area. The two and only rules that Karuta gives are as follows:

> 1. Do not use any form of automation ("botting"), such as a macro or selfbot, in the presence of the bot.
> 2. Do not use more than one account ("alting") in the presence of the bot.

What is defined as automation here? From the examples given, it seems to be anything that allows you to automate playing with Karuta Bot itself (so, creating code that automatically grabs cards, having the bot run on your own account, etc).

Furthermore, I've asked whether a feature that returns the users worker informations (the effort database functionality, which will be described later) is allowed and I've received the following responses:

From a Support member of the Karuta Hub Discord:
>Q. " I was going to make a bot for personal use which would pull worker information from my server's history, then return it in effort order. However, I know that one of the rules says that botting is forbidden. I just wanted to confirm what the rules say on this? 
Technically, it's interacting with the bot to get information (e.g. doing k!collection <user>, k!workerinfo <card code>, reacting to Karuta Bot's messages to go through collections, etc) but from my perspective, it's not actually playing the game and it's simply doing some QoL stuff that we'd have to manage externally (keeping external spreadsheets for effort and stuff)."
> A. "not allowed, if it were passively collecting data without interacting with the bot, then sure [it's allowed]...

From the owner of Karuta Bot, Craig:
> Q. "...so if it was just running in the background and registering all instances of k!workerinfo, then that would be fine?"
> A. "yes, your bot won't even be able to interact with karuta starting march 1st so i would suggest not coding it in any way other than being able to passively read from the bot"

In conclusion, bots are allowed so long as the code doesn't involve them directly interacting with Karuta Bot itself, regardless of whether it's done by the bot, or through your own account using a selfbot.

However, do not take this as approval for whether botting is allowed. Craig has not explicitly confirmed the legality of this bot, so you are using this at your own risk.
