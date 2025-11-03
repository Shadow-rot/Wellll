"""
Pyrogram Session String Generator
Users can run this to generate their own session strings
"""

from pyrogram import Client
import os

print("="*60)
print("🔐 PYROGRAM SESSION STRING GENERATOR")
print("="*60)
print("\nThis will generate a session string for your Telegram account.")
print("You'll need this to create a userbot.\n")

# Default API credentials (you can change these)
DEFAULT_API_ID = "23664800"
DEFAULT_API_HASH = "1effa1d4d80a7b994dca61b1159834c9"

print(f"Using API_ID: {DEFAULT_API_ID}")
print(f"Using API_HASH: {DEFAULT_API_HASH}\n")

# Ask if user wants to use different credentials
use_custom = input("Do you want to use different API credentials? (y/n): ").lower()

if use_custom == 'y':
    API_ID = input("Enter your API_ID: ")
    API_HASH = input("Enter your API_HASH: ")
else:
    API_ID = DEFAULT_API_ID
    API_HASH = DEFAULT_API_HASH

print("\n" + "="*60)
print("📱 LOGIN TO YOUR TELEGRAM ACCOUNT")
print("="*60)

# Create temporary client
app = Client(
    "temp_session",
    api_id=int(API_ID),
    api_hash=API_HASH,
    in_memory=True
)

async def main():
    """Generate session string"""
    async with app:
        session_string = await app.export_session_string()
        me = await app.get_me()
        
        print("\n" + "="*60)
        print("✅ SESSION STRING GENERATED SUCCESSFULLY!")
        print("="*60)
        
        print(f"\n📱 Account: {me.first_name} (@{me.username})")
        print(f"🆔 User ID: {me.id}\n")
        
        print("🔐 YOUR SESSION STRING:")
        print("-"*60)
        print(f"{session_string}")
        print("-"*60)
        
        print("\n⚠️  IMPORTANT SECURITY WARNINGS:")
        print("1. Keep this session string SECRET!")
        print("2. Anyone with this string can access your account")
        print("3. Don't share it with anyone")
        print("4. Store it safely")
        print("5. Use it only for your own userbot")
        
        print("\n📝 NEXT STEPS:")
        print("1. Copy the session string above")
        print("2. Add it to your Heroku Config Vars as 'SESSION_STRING'")
        print("3. Deploy your userbot")
        
        print("\n" + "="*60)
        
        # Save to file option
        save = input("\nDo you want to save to a file? (y/n): ").lower()
        if save == 'y':
            with open("session_string.txt", "w") as f:
                f.write(session_string)
            print("✅ Saved to 'session_string.txt'")
            print("⚠️  Remember to delete this file after use!")

try:
    app.run(main())
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\nCommon issues:")
    print("1. Invalid phone number format (use +1234567890)")
    print("2. Wrong verification code")
    print("3. API credentials are incorrect")
    print("4. Account has restrictions")
