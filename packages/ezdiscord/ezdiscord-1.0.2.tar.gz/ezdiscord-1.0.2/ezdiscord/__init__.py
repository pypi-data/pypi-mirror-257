import discord
from discord.ext import commands

class EasyDiscord():
    def __init__(self):
        self.client = commands.Bot(command_prefix='!')

    def addstock(self):
        @self.client.command()
        async def add(ctx, name, *args):
            server_name = ctx.guild.name

            # Open the file in 'a+' mode to append instead of overwrite
            with open(f"{server_name}_{name}.txt", 'a+') as file:
                # Join the arguments to form a single string with each argument on a new line
                content = '\n'.join(args)
                file.write(f"{content}\n")

            await ctx.reply("Done!")

    def run_bot(self, token):
        self.client.run(token)

# Example usage
# easy_discord = EasyDiscord()
# easy_discord.addstock()
# easy_discord.run_bot("YOUR_BOT_TOKEN")
