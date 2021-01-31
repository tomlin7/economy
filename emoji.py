import discord
from discord.ext.commands import Bot

from constants import emoji_server_id, coin_emoji_id

emoji_server = None
coin_emoji = None


async def setup_emojis(client: Bot):
    global emoji_server
    global coin_emoji
    emoji_server = discord.utils.get(client.guilds, id=emoji_server_id)
    coin_emoji = await emoji_server.fetch_emoji(coin_emoji_id)


def get_coin():
    return coin_emoji
