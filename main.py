"""
the main economy-management file.
"""
import discord
from discord.ext import commands
from discord.ext.commands import Bot, BucketType

import functions
import constants
from constants import Url
from constants import rank_emotes

from emoji import setup_emojis

from data import sync_data
from data import data

client: Bot = commands.Bot(command_prefix="lol ")
sync_data()


@client.event
async def on_ready():
    """
    Gets triggered when the bot is logged in.
    """
    sync_data()
    await setup_emojis(client)
    print(f"We're in as {client.user.name} \nLatency {client.latency}")


@client.command(name="top", aliases=['leaderboard', 'rich'])
async def leaderboard(ctx):
    """
    shows the leaderboard based on amount of wallet money.
    """
    await functions.leaderboard(ctx=ctx)


# noinspection SpellCheckingInspection
@client.command(name="work")
@commands.cooldown(1, 3600, BucketType.user)
async def work(ctx):
    """
    The main work category
    """
    await functions.work(ctx=ctx)


# noinspection SpellCheckingInspection
@client.command(name="worklist", aliases=["jobs", "work_list"])
async def work_list(ctx):
    """
    shows the list of available jobs and their respected salary
    """
    await functions.work_list(ctx)


@client.command(name="apply", aliases=['workas', 'apply for', 'workapply', 'join', 'work_as', 'work_apply'])
async def apply(ctx, *, job=None):
    """
    apply for a job, which is in work list.
    :param ctx:
    :param job:
    """
    await functions.apply(ctx, job)


@client.command(name="beg", aliases=["Beg"])
async def beg(ctx):
    """
    check for donations.
    """
    await functions.beg(ctx=ctx)


@client.command(name="balance", aliases=['bal', 'Balance'])
async def balance(ctx, _member: discord.Member = None):
    """
    check the balance of the specified user, or the context author.
    :param _member:
    """
    await functions.balance(ctx=ctx, _member=_member)


@work.error
async def work_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        cool_down_message = "You need to wait **1 hour** until you can work again!"
        await ctx.send(cool_down_message)
    else:
        pass


# TODO: make a rob command
# TODO: make deposit command
# TODO: make withdraw

@client.command(name="steal", aliases=["rob", "Rob", "Steal"])
async def steal(ctx, _member: discord.Member = None):
    """
    steal from other users.
    :param _member:
    :param ctx:
    """
    await functions.steal(ctx, _member)


@client.command(name="deposit", aliases=["dep", "Dep", "Deposit"])
async def deposit(ctx, amount: int = None, part: str = None):
    """
    deposit money to bank account.
    :param ctx:
    :param amount:
    :param part:
    """
    await functions.deposit(ctx=ctx)




















# noinspection SpellCheckingInspection
client.run('Nzc3MDIwODg2NDU1ODEyMTA2.X69XFw.xIFobbieghH4M7a0XvmB2JMBUQs')
