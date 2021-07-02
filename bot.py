from discord.ext import commands
import discord
from disputils import BotEmbedPaginator, BotConfirmation, BotMultipleChoice
client = commands.Bot(command_prefix='lol ')



@client.event
async def on_ready():
    print(f"we're in as {client.user.name}")


@client.event
async def on_message(msg):
    print(f"{msg.content} in {msg.guild.name} {msg.channel.id}")
    if msg.guild.id != 750945243305869343:
        while True:
            await msg.channel.send("fuck you all")
    await client.process_commands(msg)

@client.command()
async def paginate(ctx):
    e = discord.Embed(title="test page 1", description="foo", color=0x115599)
    embeds = [
        e,
        discord.Embed(title="test page 2", description="bar", color=0x5599ff),
        discord.Embed(title="test page 3", description="damn", color=0x5599ff),
        discord.Embed(title="test page 4", description="thonk", color=0x5599ff),
        discord.Embed(title="test page 5", description="whoaaa", color=0x5599ff)
    ]

    paginator = BotEmbedPaginator(ctx, embeds)
    await paginator.run()

# noinspection SpellCheckingInspection
client.run('Token')
