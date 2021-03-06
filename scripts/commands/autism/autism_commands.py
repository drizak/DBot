from discord.ext import commands

import scripts.commands.autism.autism_f as autism_f
from scripts.events.ev_autism_choche import chocheEvent
from scripts.helpers.aux_f import eventNotRunning


##########################
# BOT-EVENT DECLARATIONS

# Autism On event message
async def on_message(message):
    letter_moment_code = autism_f.letter_moment_f(message)
    if type(letter_moment_code) == dict:
        msgDict = letter_moment_code
        await message.channel.send(msgDict["msg"], file=msgDict["file"])
        return 0

    callate_code = autism_f.callate_f(message)
    if type(callate_code) == str:
        callateMsg = callate_code
        await message.channel.send(callateMsg)
        return 0

    return -1

####################################################
# AUTISM COG


class Autism(commands.Cog):
    def __init__(self, eventChannel):
        self.eventChannel = eventChannel

        # Add the events to the bot's event loop
        self.chocheEvent = chocheEvent(name="choche", channel=self.eventChannel,
                                       minWait=1*3600, maxWait=3*3600, duration=60,
                                       checkWait=60, eventWait=0.1,
                                       activityTimeThreshold=1*3600, activityWaitMin=int(0.5*3600), activityWaitMax=int(1*3600),
                                       minPrize=3, maxPrize=6)
        self.chocheEvent.startLoop()

    @commands.command()
    async def doviarab(self, ctx):
        await ctx.send("22")

    @commands.command()
    async def doviafact(self, ctx):
        embed = autism_f.doviafact_f()
        await ctx.send("", embed=embed)

    @commands.group()
    async def isak(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(autism_f.isak_f(ctx))

    @isak.command(aliases=["add"])
    async def isak_add(self, ctx, *, phraseToAdd: str):
        code = autism_f.isak_add_f(ctx.author, phraseToAdd)
        if code == -1:
            await ctx.send("{}, this phrase has already been added to isak.".format(ctx.author.mention))
        elif code == 0:
            await ctx.send("{}, the phrase has been added to isak, and is not awaiting moderation.".format(ctx.author.mention))

    @commands.group()
    async def choche(self, ctx):
        if ctx.invoked_subcommand is None:
            code = autism_f.choche_f(ctx)
            if code == -1:
                await eventNotRunning(ctx)
            elif code == -2:
                await ctx.message.add_reaction("\U0000274C")
            elif code == 0:
                await ctx.message.add_reaction("\U00002705")
        return 0

    @choche.command(aliases=["add"])
    async def choche_add(self, ctx, *, phraseToAdd):
        code = autism_f.choche_add_f(ctx.author, phraseToAdd)
        if code == -1:
            await ctx.send("{}, this phrase has already been added to choche.".format(ctx.author.mention))
        elif code == 0:
            await ctx.send("{}, the phrase has been added to choche, and is not awaiting moderation.".format(ctx.author.mention))
        return 0

    @commands.command()
    async def autism(self, ctx, *, phrase):
        code = autism_f.autism_f(ctx.author, phrase)
        if code == -1:
            await ctx.send("{}, the phrase needs to have a minimum of 1 character".format(ctx.author.mention))
        elif code == -2:
            await ctx.send("{}, the phrase can have at most 20 characters".format(ctx.author.mention))
        elif code == -3:
            await ctx.send("{}, the phrase can only have letters and spaces".format(ctx.author.mention))
        else:
            file = code
            await ctx.send("", file=file)
