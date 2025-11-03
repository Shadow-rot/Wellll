from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import os
import asyncio

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

# Store user session generation states
user_states = {}


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
        f"/info - Get chat info\n"
        f"/generate - Generate Pyrogram session string\n"
        f"/cancel - Cancel current operation"
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
        "/info - Get detailed chat information\n"
        "/generate - Generate Pyrogram session string\n"
        "/cancel - Cancel current operation\n\n"
        "**Session Generator:**\n"
        "Use /generate to create a Pyrogram session string for your userbot.\n\n"
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


@bot.on_message(filters.command("generate"))
async def generate_session_command(client: Client, message: Message):
    """Start session string generation process"""
    user_id = message.from_user.id
    
    # Send warning message
    warning_text = (
        "**🔐 PYROGRAM SESSION STRING GENERATOR**\n\n"
        "⚠️ **SECURITY WARNING:**\n"
        "• Your session string is like a PASSWORD to your Telegram account\n"
        "• NEVER share it with anyone\n"
        "• Keep it private and secure\n"
        "• Anyone with this string can access your account\n\n"
        "**📝 What you'll need:**\n"
        "• Your Telegram phone number (with country code)\n"
        "• Access to your Telegram app (to receive verification code)\n"
        "• Your 2FA password (if enabled)\n\n"
        "**Ready to continue?**\n"
        "Send your **API_ID** or use /cancel to stop."
    )
    
    await message.reply_text(warning_text)
    
    # Set user state
    user_states[user_id] = {"step": "waiting_api_id"}


@bot.on_message(filters.command("cancel"))
async def cancel_command(client: Client, message: Message):
    """Cancel current operation"""
    user_id = message.from_user.id
    
    if user_id in user_states:
        del user_states[user_id]
        await message.reply_text("✅ Operation cancelled.\n\nUse /generate to start again.")
    else:
        await message.reply_text("ℹ️ No active operation to cancel.")


@bot.on_message(filters.text & filters.private & ~filters.command(["start", "help", "ping", "id", "info", "generate", "cancel"]))
async def handle_user_input(client: Client, message: Message):
    """Handle user inputs for session generation"""
    user_id = message.from_user.id
    
    # Check if user is in session generation process
    if user_id not in user_states:
        # Echo handler for normal messages
        await message.reply_text(
            f"You said: {message.text}\n\n"
            f"Use /help to see available commands."
        )
        return
    
    state = user_states[user_id]
    step = state.get("step")
    
    try:
        if step == "waiting_api_id":
            # Validate and store API_ID
            try:
                api_id = int(message.text.strip())
                state["api_id"] = api_id
                state["step"] = "waiting_api_hash"
                await message.reply_text(
                    f"✅ API_ID saved: `{api_id}`\n\n"
                    f"Now send your **API_HASH**"
                )
            except ValueError:
                await message.reply_text(
                    "❌ Invalid API_ID. It must be a number.\n\n"
                    "Please send a valid API_ID or /cancel"
                )
        
        elif step == "waiting_api_hash":
            # Store API_HASH
            api_hash = message.text.strip()
            if len(api_hash) < 32:
                await message.reply_text(
                    "⚠️ API_HASH seems too short. Are you sure it's correct?\n\n"
                    "Send it again or use /cancel"
                )
                return
            
            state["api_hash"] = api_hash
            state["step"] = "waiting_phone"
            await message.reply_text(
                f"✅ API_HASH saved\n\n"
                f"Now send your **phone number** with country code\n"
                f"Example: `+1234567890`"
            )
        
        elif step == "waiting_phone":
            # Store phone and request code
            phone = message.text.strip()
            if not phone.startswith("+"):
                await message.reply_text(
                    "❌ Phone number must start with + and country code\n\n"
                    "Example: `+1234567890`\n"
                    "Try again or use /cancel"
                )
                return
            
            state["phone"] = phone
            
            # Create temporary client
            status_msg = await message.reply_text("🔄 Sending verification code...")
            
            try:
                temp_client = Client(
                    f"session_{user_id}",
                    api_id=state["api_id"],
                    api_hash=state["api_hash"],
                    phone_number=phone,
                    in_memory=True
                )
                
                state["temp_client"] = temp_client
                
                await temp_client.connect()
                sent_code = await temp_client.send_code(phone)
                state["phone_code_hash"] = sent_code.phone_code_hash
                state["step"] = "waiting_code"
                
                await status_msg.edit_text(
                    "✅ Verification code sent to your Telegram app!\n\n"
                    "📱 Check your Telegram and send the code here\n"
                    "Format: `12345` (just the numbers)"
                )
                
            except Exception as e:
                await status_msg.edit_text(
                    f"❌ Error sending code: {str(e)}\n\n"
                    "Please check your phone number and try again.\n"
                    "Use /generate to start over."
                )
                del user_states[user_id]
        
        elif step == "waiting_code":
            # Verify code
            code = message.text.strip().replace("-", "").replace(" ", "")
            status_msg = await message.reply_text("🔄 Verifying code...")
            
            try:
                temp_client = state["temp_client"]
                
                try:
                    await temp_client.sign_in(
                        state["phone"],
                        state["phone_code_hash"],
                        code
                    )
                    
                    # Generate session string
                    session_string = await temp_client.export_session_string()
                    me = await temp_client.get_me()
                    
                    await temp_client.disconnect()
                    
                    # Success message
                    success_text = (
                        "✅ **SESSION STRING GENERATED SUCCESSFULLY!**\n\n"
                        f"**📱 Account:** {me.first_name}\n"
                        f"**👤 Username:** @{me.username or 'None'}\n"
                        f"**🆔 User ID:** `{me.id}`\n\n"
                        "**🔐 Your Session String:**\n"
                        f"`{session_string}`\n\n"
                        "⚠️ **IMPORTANT:**\n"
                        "• Copy this string immediately\n"
                        "• Delete this message after copying\n"
                        "• Never share it with anyone\n"
                        "• Store it securely (Heroku Config Vars)\n\n"
                        "Use /generate to create another session."
                    )
                    
                    await status_msg.delete()
                    await message.reply_text(success_text)
                    
                    # Clean up
                    del user_states[user_id]
                    
                except Exception as signin_error:
                    error_str = str(signin_error)
                    
                    # Check if 2FA is required
                    if "password" in error_str.lower() or "two" in error_str.lower():
                        state["step"] = "waiting_2fa"
                        await status_msg.edit_text(
                            "🔐 **2FA Password Required**\n\n"
                            "Your account has Two-Factor Authentication enabled.\n"
                            "Send your **cloud password** now."
                        )
                    else:
                        await status_msg.edit_text(
                            f"❌ Verification failed: {error_str}\n\n"
                            "Common issues:\n"
                            "• Wrong code\n"
                            "• Code expired (try again with /generate)\n"
                            "• Too many attempts\n\n"
                            "Use /generate to try again."
                        )
                        del user_states[user_id]
                
            except Exception as e:
                await status_msg.edit_text(
                    f"❌ Error: {str(e)}\n\n"
                    "Use /generate to try again."
                )
                del user_states[user_id]
        
        elif step == "waiting_2fa":
            # Handle 2FA password
            password = message.text
            status_msg = await message.reply_text("🔄 Checking password...")
            
            try:
                temp_client = state["temp_client"]
                
                await temp_client.check_password(password)
                
                # Generate session string
                session_string = await temp_client.export_session_string()
                me = await temp_client.get_me()
                
                await temp_client.disconnect()
                
                # Success message
                success_text = (
                    "✅ **SESSION STRING GENERATED SUCCESSFULLY!**\n\n"
                    f"**📱 Account:** {me.first_name}\n"
                    f"**👤 Username:** @{me.username or 'None'}\n"
                    f"**🆔 User ID:** `{me.id}`\n\n"
                    "**🔐 Your Session String:**\n"
                    f"`{session_string}`\n\n"
                    "⚠️ **IMPORTANT:**\n"
                    "• Copy this string immediately\n"
                    "• Delete this message after copying\n"
                    "• Never share it with anyone\n"
                    "• Store it securely (Heroku Config Vars)\n\n"
                    "Use /generate to create another session."
                )
                
                await status_msg.delete()
                await message.reply_text(success_text)
                
                # Clean up
                del user_states[user_id]
                
            except Exception as e:
                await status_msg.edit_text(
                    f"❌ Wrong password: {str(e)}\n\n"
                    "Use /generate to try again."
                )
                del user_states[user_id]
    
    except Exception as e:
        await message.reply_text(
            f"❌ Unexpected error: {str(e)}\n\n"
            "Use /generate to start over."
        )
        if user_id in user_states:
            del user_states[user_id]


print("🚀 Starting bot...")
bot.run()
print("✅ Bot started successfully!")