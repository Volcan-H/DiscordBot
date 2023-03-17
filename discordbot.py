import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='!')

token = input("Enter your Discord bot token: ")
bot_token = token.strip()

text_channel_name = input("Enter the name for the text channel: ")
voice_channel_name = input("Enter the name for the voice channel: ")

async def create_text_channel(guild):
    try:
        channel = await guild.create_text_channel(text_channel_name)
        return channel
    except discord.Forbidden:
        print(f"Bot doesn't have permission to create a text channel in {guild.name}")
    except discord.HTTPException as e:
        print(f"Failed to create a text channel in {guild.name}: {e}")
    return None

async def create_voice_channel(guild):
    try:
        channel = await guild.create_voice_channel(voice_channel_name)
        return channel
    except discord.Forbidden:
        print(f"Bot doesn't have permission to create a voice channel in {guild.name}")
    except discord.HTTPException as e:
        print(f"Failed to create a voice channel in {guild.name}: {e}")
    return None

@bot.command()
async def create_server(ctx, server_name=None, text_channels=1, voice_channels=1, *channel_names):
    if not server_name:
        await ctx.send('Please specify a name for the server.')
        return

    if text_channels < 1 or voice_channels < 1:
        await ctx.send('Please specify at least 1 text channel and 1 voice channel.')
        return

    if len(channel_names) > (text_channels + voice_channels):
        await ctx.send('Too many channel names specified.')
        return


    try:
        guild = await bot.create_guild(name=server_name)
    except discord.Forbidden:
        await ctx.send("Bot doesn't have permission to create a server.")
        return
    except discord.HTTPException as e:
        await ctx.send(f"Failed to create a server: {e}")
        return

    await ctx.send(f'Successfully created server {guild.name}!')

    for i in range(text_channels):
        if i < len(channel_names):
            text_channel_name = channel_names[i]
        await create_text_channel(guild)

    for i in range(voice_channels):
        if i < len(channel_names) - text_channels:
            voice_channel_name = channel_names[text_channels + i]
        await create_voice_channel(guild)

    await ctx.send(f'Successfully created {text_channels} text channel(s) and {voice_channels} voice channel(s)!')

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="with code"))

bot.run(bot_token)
