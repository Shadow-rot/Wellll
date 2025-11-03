from pyrogram import Client, filters
from pyrogram.types import Message
import os

# Bot credentials from environment variables
API_ID = int(os.getenv("API_ID", "23664800"))
API_HASH = os.getenv("API_HASH", "1effa1d4d80a7b994dca61b1159834c9")
BOT_TOKEN = os.getenv("BOT_TOKEN", "7871802860:AAETOV8HtWbskHbzTRvfCQBeHq47kTqV2eQ")

# Initialize bot
bot = Client(
    "my_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)


@bot.on_message(filters.command("start"))
async def start_command(client: Client, message: Message):
    """Start command handler"""
    await message.reply_text(
        f"👋 **Hello {message.from_user.first_name}!**\n\n"
        f"I'm a Telegram bot running on Heroku.\n\n"
        f"**Available Commands:**\n"
        f"/start - Start the bot\n"
        f"/help - Get help\n"
        f"/ping - Check if bot is alive\n"
        f"/id - Get your user ID\n"
        f"/info - Get chat info"
    )


@bot.on_message(filters.command("help"))
async def help_command(client: Client, message: Message):
    """Help command handler"""
    await message.reply_text(
        "**📚 Bot Commands:**\n\n"
        "/start - Start the bot\n"
        "/help - Show this help message\n"
        "/ping - Check bot status\n"
        "/id - Get your user/chat ID\n"
        "/info - Get detailed chat information\n\n"
        "**Need more help?**\n"
        "Contact the bot owner."
    )


@bot.on_message(filters.command("ping"))
async def ping_command(client: Client, message: Message):
    """Ping command to check if bot is alive"""
    await message.reply_text("🏓 **Pong!**\n\nBot is running on Heroku! ✅")


@bot.on_message(filters.command("id"))
async def id_command(client: Client, message: Message):
    """Get user/chat ID"""
    text = f"**🆔 ID Information:**\n\n"
    text += f"**Your ID:** `{message.from_user.id}`\n"
    text += f"**Chat ID:** `{message.chat.id}`\n"
    
    if message.reply_to_message:
        text += f"**Replied User ID:** `{message.reply_to_message.from_user.id}`\n"
    
    await message.reply_text(text)


@bot.on_message(filters.command("info"))
async def info_command(client: Client, message: Message):
    """Get detailed chat information"""
    user = message.from_user
    chat = message.chat
    
    text = "**📊 Information:**\n\n"
    text += f"**User Info:**\n"
    text += f"├ Name: {user.first_name}\n"
    text += f"├ Username: @{user.username if user.username else 'None'}\n"
    text += f"├ ID: `{user.id}`\n"
    text += f"└ Bot: {'Yes' if user.is_bot else 'No'}\n\n"
    
    text += f"**Chat Info:**\n"
    text += f"├ Type: {chat.type}\n"
    text += f"├ ID: `{chat.id}`\n"
    
    if chat.title:
        text += f"└ Title: {chat.title}\n"
    
    await message.reply_text(text)


# Echo handler - replies to all messages
@bot.on_message(filters.text & filters.private & ~filters.command(["start", "help", "ping", "id", "info"]))
async def echo_handler(client: Client, message: Message):
    """Echo back user messages"""
    await message.reply_text(
        f"You said: {message.text}\n\n"
        f"Use /help to see available commands."
    )


print("🚀 Starting bot...")
bot.run()
print("✅ Bot started successfully!")

