# Import Statements
from configs import Config
from .database import db
from pyrogram import Client
from pyrogram.types import Message

# Async Function
async def add_user_to_database(bot: Client, cmd: Message):
    try:
        # Check if the user already exists in the database
        if not await db.is_user_exist(cmd.from_user.id):
            # Add the user to the database
            await db.add_user(cmd.from_user.id)

            # Check if a log channel is configured
            if Config.LOG_CHANNEL is not None:
                # Log the new user information
                await bot.send_flooded_message(
                    int(Config.LOG_CHANNEL),
                    f"#NEW_USER: \n\nNew User [{cmd.from_user.first_name}](tg://user?id={cmd.from_user.id}) started @{(await bot.get_me()).username} !!"
                )

    except Exception as e:
        # Handle exceptions, log the error, and maybe notify the developer
        print(f"Error in add_user_to_database: {e}")
