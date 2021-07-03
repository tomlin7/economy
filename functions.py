"""
All functions.
"""
import json
import random
from typing import Union

import discord

from data import sync_data
from data import data
from data import users

import constants
from constants import random_word
from constants import beg_results
from constants import chances
from constants import people
from emoji import get_coin


def has_job(user: str) -> bool:
    """
    check, whether the specified user has any job.
    :rtype: bool
    :return:
    """
    sync_data()
    return data['users'][user]['job'] != 0


def make_leaderboard() -> dict:
    """
    make a leaderboard from the data.
    :rtype: dict
    :return:
    """
    sync_data()
    # order function
    order = sorted(users.items(), key=lambda val: val[1]['wallet'], reverse=True)

    # ranks dict
    names = {
        'first': {'id': 0, 'name': "None", 'score': 0},
        'second': {'id': 0, 'name': "None", 'score': 0},
        'third': {'id': 0, 'name': "None", 'score': 0},
        'fourth': {'id': 0, 'name': "None", 'score': 0},
        'fifth': {'id': 0, 'name': "None", 'score': 0}
    }
    # assigning ranks
    for number, name in zip(range(5), names):
        # print(name)

        names[name]['id'] = str(order[number])[2:]

        x = 0
        while 1 == 1:
            if names[name]['id'][x] == "'":
                break
            x += 1
        names[name]['id'] = str(order[number])[2:x + 2]

        names[name]['name'] = users[names[name]['id']]['name']
        names[name]['score'] = users[names[name]['id']]['wallet']

        # print(names[name]['id'], names[name]['name'], names[name]['score'])
    return names


def decide_score(job: int) -> Union[str, int]:
    """
    Function to decide score(income) from job_id
    :rtype: Union[str, int]
    :param job:
    :return:
    """
    sync_data()
    switcher = {
        1: random.randint(1700, 2000),
        2: random.randint(1400, 1700),
        3: random.randint(1100, 1400),
        4: random.randint(800, 1100),
        5: random.randint(600, 800),
        6: random.randint(400, 600)
    }
    return switcher.get(job, "no job")


def find_job_with_name(job: str) -> int:
    """
    find a job with the given name
    :rtype: int
    :param job:
    :return:
    """
    sync_data()
    switcher = {
        "software engineer": 1,
        "product manager": 2,
        "data scientist": 3,
        "electrical engineer": 4,
        "network engineer": 5,
        "systems integrator": 6
    }
    return switcher.get(job, 0)


def find_job_with_id(job: int) -> str:
    """
    find job from the given job_id
    :rtype: str
    :param job:
    :return:
    """
    sync_data()
    switcher = {
        1: "Software Engineer",
        2: "Product Manager",
        3: "Data Scientist",
        4: "Electrical Engineer",
        5: "Network Engineer",
        6: "Systems Integrator"
    }
    return switcher.get(job, "no job")


def save_data() -> None:
    """
    save the data to json file.
    """
    sync_data()
    json.dump(data, open("money.json", "w"), indent=4)


# noinspection SpellCheckingInspection
async def return_no_job(ctx) -> None:
    """
    return a no-job-warning to the specified context author
    :param ctx:
    """
    sync_data()
    await ctx.send(
        "You don't currently have a job to work at. You can use "
        "`{0} work list` to see a list of the available jobs".format(ctx.prefix))


async def create_new_user_and_apply_for_job(ctx, userid, job_id) -> None:
    """
    create a new user in the database and give the specified job
    :param ctx:
    :param userid:
    :param job_id:
    """
    await create_new_user(ctx, userid)
    data['users'][userid]['job'] = job_id
    save_data()
    await applied_for_job(ctx, job_id)


async def create_new_user_with_no_job(ctx, userid) -> None:
    """
    create a new user in the database with a no_job_warning.
    :param ctx:
    :param userid:
    """
    await create_new_user(ctx, userid)
    await return_no_job(ctx)


async def create_new_user(ctx, userid) -> None:
    """
    create a user in the database.
    :param ctx:
    :param userid:
    """
    sync_data()
    wallet = 0
    bank = 0
    _new = {
        f'{userid}': {
            'name': ctx.author.name,
            'job': 0,
            'wallet': wallet,
            'bank': bank
        }
    }
    data['users'].update(_new)
    save_data()


async def applied_for_job(ctx, job_id) -> None:
    """
    return a message to the context author after applying to a job.
    :param ctx:
    :param job_id:
    """
    sync_data()
    if find_job_with_id(job_id) != "no job":
        msg1 = "<@{0}> Congratulations, you are now working as a **{1}**!" \
            .format(ctx.author.id, find_job_with_id(job_id))
        msg2 = "You start now, and your salary is **{0} coins per hour**." \
            .format(constants.salaries[job_id])
        await ctx.send(f"{msg1}\n{msg2}")
    else:
        await ctx.send("No job with that name.")


async def give_score(ctx, data_, userid, amount: int) -> None:
    """
    give score to the context author after work.
    :param amount:
    :param ctx:
    :param data_:
    :param userid:
    """
    sync_data()
    data_['users'][userid]['wallet'] += amount
    data_['users'][userid]['name'] = str(ctx.author)
    save_data()
    # following PEP 8: E501 (line length > 120 characters)
    await ctx.send(f"**Boss** Good stuff {ctx.author.name}, got the work done well."
                   f" You were given **{get_coin()} {amount}** coins for one hour of work.")
    print("{0} was given ⏣{1} for his/her work.".format(ctx.author.name, amount))


async def balance(ctx, _member: discord.Member = None):
    if _member is None:
        _member = ctx.author
    _balance = get_balance(f"{_member.id}")
    bank_balance = 0
    total = _balance + bank_balance
    embed = discord.Embed(title=f"{_member.display_name}'s balance",
                          description=f"**Wallet:** {_balance}\n"
                                      "**Bank:** no bank account\n"
                                      f"**Total:** {total}\n",
                          color=discord.Color.blue())
    await ctx.send(embed=embed)


def get_balance(userid) -> int:
    """
    check user's balance.
    :rtype: int
    :param userid:
    :return:
    """
    sync_data()
    return data['users'][userid]['wallet']


def get_random_word() -> str:
    """
    get a random word from the dictionary.
    :rtype: str
    :return:
    """
    return random_word.get_random_word()


async def beg(ctx) -> None:
    """
    beg command - main
    :param ctx:
    """
    _id = str(ctx.author.id)
    person = get_random_famous_person()
    if chance():
        amount = get_random_amount(100, 1000)
        await give_begged_coins(ctx, _id, amount, data)
        await ctx.send("**{0}** has donated **{1} {2}** to {3.author.mention}".format(person, get_coin(), amount, ctx))
    else:
        await ctx.send("**{0}**: {1}".format(person, no_money_for_you()))


async def give_begged_coins(ctx, _id, amount, data_) -> None:
    """
    add the amount of donation to the user's wallet.
    :param data_:
    :param ctx:
    :param _id:
    :param amount:
    """
    try:
        test = data['users'][_id]
        if not test:
            raise KeyError
        sync_data()
        data_['users'][_id]['wallet'] += amount
        data_['users'][_id]['name'] = str(ctx.author)

    except KeyError:
        await create_new_user(ctx, _id)
    # saving data to json file
    save_data()


def get_random_famous_person() -> str:
    """
    get a donor's name.
    :rtype: str
    :return:
    """
    return random.choice(people)


def chance() -> bool:
    """
    for beg chances.
    :rtype: bool
    :return:
    """
    return random.choice(chances)


def get_random_amount(a, b) -> int:
    """
    declare donation amount.
    :rtype: int
    :param a:
    :param b:
    :return:
    """
    return random.randint(a, b)


def no_money_for_you() -> str:
    """
    when there is no chance of getting donations.
    :rtype: str
    :return:
    """
    return random.choice(beg_results)


async def steal(ctx, _member: discord.Member = None):
    """
    steal money from other users.
    :param ctx:
    :param _member:
    """
    author_id = str(ctx.author.id)
    userid = str(_member.id)
    if _member is not None:
        if _member.id == ctx.author.id:
            await ctx.send("Ok, you robbed yourself, now go rob someone else")
            return
        stolen = get_random_amount(0, data['users'][userid]['wallet'])
        caught = get_random_amount(0, data['users'][author_id]['wallet'])
        if chance():
            data['users'][userid]['wallet'] -= stolen
            data['users'][author_id]['wallet'] += stolen
            await ctx.send(
                f"You stole a small portion! 💸\nYour payout was {get_coin()} {stolen} coins. {_member.nick}")
        else:
            data['users'][author_id]['wallet'] -= caught
            await ctx.send("You were caught **HAHAHA**\n"
                           f"You paid the person you stole from {get_coin()} **{caught}** coins.")
    else:
        if chance():
            await ctx.send("Whom do you want to rob, dumbass")
        else:
            await ctx.send("Whom do you want to rob, mention it")


async def deposit(ctx):
    """
    deposit money to bank account.
    :param ctx:
    """
    await ctx.send("deposited")


async def work(ctx):
    sync_data()
    _id = str(ctx.author.id)
    try:
        test = data['users'][_id]
        if not test:
            raise KeyError
        if not has_job(_id):
            await return_no_job(ctx)
            return
        _score = decide_score(data['users'][_id]['job'])
        await give_score(ctx, data, _id, _score)

    except KeyError:
        await create_new_user_with_no_job(ctx, _id)
    # saving data to json file
    save_data()


async def task(ctx):
    user_id = str(ctx.author.id)
    job_id = data['users'][user_id]['job']
    job = find_job_with_id(job_id)
    word = get_random_word()

    await ctx.send(f"**Work for {job}** - Retype - Retype the following phrase below.\nType `{word}`")
    try:
        pass
    except TimeoutError:
        pass


async def work_list(ctx):
    sync_data()
    embed = discord.Embed(title="Available Jobs",
                          description="You can select a job from the list, and work on that job hourly for a payout!",
                          color=discord.Color.blue())
    for job, salary in zip(constants.jobs, constants.salaries):
        embed.add_field(name=job, value="`{0}`".format(constants.salaries[salary]), inline=False)
    await ctx.send(embed=embed)
    save_data()


async def apply(ctx, job=None):
    if job is None:
        await ctx.send("what do you want to work as, `{0} work as [job]`".format(ctx.prefix))
        return
    sync_data()
    job = str(job).lower()
    job_id = find_job_with_name(job)
    _id = str(ctx.author.id)
    try:
        test = data['users'][_id]
        if not test:
            raise KeyError
        data['users'][_id]['job'] = job_id
        await applied_for_job(ctx, job_id)
    except KeyError:
        await create_new_user_and_apply_for_job(ctx, ctx.author.id, job_id)
    save_data()


async def leaderboard(ctx):
    sync_data()
    top = make_leaderboard()
    message = []
    for emoji, rank in zip(constants.rank_emotes, top):
        if top[rank]['name'] == "None":
            break
        pt1 = "\n{0} **{1}**".format(emoji, top[rank]['score'])
        pt2 = top[rank]['name']
        message.append(f"{pt1} - {pt2}")
    embed = discord.Embed(title=f"Richest Users in **{ctx.guild.name}**",
                          description="\n".join(message),
                          color=discord.Color.blue())
    await ctx.send(embed=embed)
    save_data()
