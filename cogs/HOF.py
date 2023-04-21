import discord
from discord.ext import commands
import json
import asyncio

with open("config.json", "r") as f:
    config = json.load(f)

TOKEN = config["DISCORD_TOKEN"]
TARGET_GUILD_ID = config["DISCORD_GUILD_ID"]
TARGET_CHANNEL_ID = config["DISCORD_CHANNEL_ID"]
INITIAL_CHANNEL_ID = config["DISCORD_INITIAL_CHANNEL_ID"]


class HofCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def check_unique_reactions(self, payload):
        initial_channel_id = INITIAL_CHANNEL_ID
        if payload.channel_id == initial_channel_id:
            channel = self.bot.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            await asyncio.sleep(5)
            message = await channel.fetch_message(payload.message_id)

            unique_users = set()
            for reaction in message.reactions:
                async for user in reaction.users():
                    unique_users.add(user.id)

            if len(unique_users) >= 2:
                destination_channel_id = TARGET_CHANNEL_ID
                destination_channel = self.bot.get_channel(destination_channel_id)
                embed = discord.Embed(
                    title=f"{message.channel.name}",
                    description=f"[Original Post](https://discord.com/channels/{message.guild.id}/{message.channel.id}/{message.id})",
                    timestamp=message.created_at,
                    color=discord.Color.gold(),
                )
                embed.set_author(
                    name=f"{message.author}",
                    icon_url=message.author.avatar.url,
                )
                if message.attachments and message.attachments[0].url:
                    embed.set_image(url=message.attachments[0].url)

                await destination_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        await self.check_unique_reactions(payload)


async def setup(bot):
    await bot.add_cog(HofCog(bot))
