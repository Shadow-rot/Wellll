from pyrogram import Client, filters
from pyrogram.types import Message
import os
import asyncio

# Get credentials from environment variables
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION_STRING = os.getenv("SESSION_STRING")

app = Client(
    "my_userbot",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING
)

@app.on_message(filters.command("ping", prefixes=".") & filters.me)
async def ping(client: Client, message: Message):
    await message.edit("🏓 **Pong!**\nUserbot is running on Heroku!")

@app.on_message(filters.command("alive", prefixes=".") & filters.me)
async def alive(client: Client, message: Message):
    await message.edit("✅ **Userbot is alive on Heroku!**")

@app.on_message(filters.command("info", prefixes=".") & filters.me)
async def info(client: Client, message: Message):
    me = await client.get_me()
    text = (
        f"**📱 Your Account**\n\n"
        f"Name: {me.first_name}\n"
        f"Username: @{me.username}\n"
        f"ID: `{me.id}`"
    )
    await message.edit(text)

print("🚀 Userbot started on Heroku!")
app.run()
