#!/usr/bin/env python3

#import logging

import discord
from discord.ext import commands

from NHentai.nhentai_async import NHentaiAsync
from NHentai.entities.doujin import Doujin

client = commands.Bot(description="Fetch the names of various sauces!",
                      command_prefix=[],
                      case_insensitive=True,
                      help_command=None)

nhentai = NHentaiAsync()

config = None


async def start(_config: dict) -> None:
    global config

    config = _config
    client.command_prefix = config["command_prefix"]

    await client.start(config["bot_key"])


@client.event
async def on_ready() -> None:
    """
    Connects/logs in the bot to discord. Also outputs to the console that the
    connection was successful.
    """
    # logging.info("DISCORD: Logged in as %s (ID: %s)" %
    #       (client.user.name, client.user.id))
    # logging.info("DISCORD: Connected to %d servers, and %d users" %
    #       (len(client.guilds), len(set(client.get_all_members()))))
    # logging.info(("DISCORD: Invite link: "
    #        "https://discordapp.com/oauth2/authorize?client_id="
    #        "%d&scope=bot&permissions=19456" % client.user.id))
    print("Logged in!")
    print("Invite:  https://discordapp.com/oauth2/authorize?client_id=%d&scope=bot&permissions=19456" % client.user.id)
    activity = discord.Game(name="!help | Slurping up some yummy sauce!")
    return await client.change_presence(activity=activity)

@client.command()
async def sauce(context: commands.Context, id: str) -> None:

    if len(id) != 6 or id.isdecimal() != True:
        await context.send("Invalid sauce code. A valid code is a 6 digit number")
        return

    doujin: Doujin = await nhentai.get_doujin(id=id)

    if doujin is None:
        await context.send(f"There is no sauce {id}. Sorry :/")
        return
    
    await context.send(f"Sauce {id} is {doujin.title}")

@client.command()
async def help(context: commands.Context) -> None:    
    await context.send("Use !sauce with a 6 digit sauce code to locate it and it's title!")
