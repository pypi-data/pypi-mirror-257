from ezdiscord import EasyDiscord

# Create an instance of EasyDiscord
easy_discord_bot = EasyDiscord()

# Add a command using addstock method
easy_discord_bot.addstock()

# Run the bot with your Discord bot token
token = "MTIwMzAwNDYzNTQ3Mjk5NDM4Ng.G1WzZR.iaUSuVCvsDqfzUsKNEEeAotnxuI99_AhWOzHo0"
easy_discord_bot.run_bot(token)
