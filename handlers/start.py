from time import time
from datetime import datetime
from config import BOT_USERNAME, BOT_NAME, ASSISTANT_NAME, OWNER_NAME, UPDATES_CHANNEL, GROUP_SUPPORT
from helpers.filters import command
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, Chat, CallbackQuery
from helpers.decorators import sudo_users_only


START_TIME = datetime.utcnow()
START_TIME_ISO = START_TIME.replace(microsecond=0).isoformat()
TIME_DURATION_UNITS = (
    ('week', 60 * 60 * 24 * 7),
    ('day', 60 * 60 * 24),
    ('hour', 60 * 60),
    ('min', 60),
    ('sec', 1)
)

async def _human_time_duration(seconds):
    if seconds == 0:
        return 'inf'
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append('{} {}{}'
                         .format(amount, unit, "" if amount == 1 else "s"))
    return ', '.join(parts)


@Client.on_message(command(["start", f"start@{BOT_USERNAME}"]) & filters.private & ~filters.edited)
async def start_(client: Client, message: Message):
    await message.reply_text(
        f"""<b>✨ **Halooo **{message.from_user.first_name}** Telaso** \n
💭 **[{BOT_NAME}](https://t.me/{BOT_USERNAME}) Bot ini dapat memutar musik di obrolan suara di gc lu, !!**

💡 **Cari perintah apa aja yg ada dalam bot di » PERINTAH!**

❓ **Bila ketololan lu muncul lu ketik aja /help**

🔔 **Perhatian, lu {message.from_user.first_name} klo dikasi gratis jgn mengeluh bego, klo lagu lu proses terus, berarti udah dri sananya error!**
</b>""",
        reply_markup=InlineKeyboardMarkup(
            [ 
                [
                    InlineKeyboardButton(
                        "➕ Tambahkan gua ke GC lu ➕", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")
                ],[
                    InlineKeyboardButton(
                        "❓ Bagaimana cara memakai", callback_data="cbhowtouse")
                ],[
                    InlineKeyboardButton(
                         "📚 Perintah", callback_data="cbcmds"
                    ),
                    InlineKeyboardButton(
                        "🤗Donasinya om/tante🤗", url="https://t.me/tummingrockers")
                ],[
                    InlineKeyboardButton(
                        "👥Join Grup Gua👥", url=f"https://t.me/{GROUP_SUPPORT}"
                    ),
                    InlineKeyboardButton(
                        "📣Official Channel📣", url=f"https://t.me/{UPDATES_CHANNEL}")
                ],[
                    InlineKeyboardButton(
                        "💕Terima Kasih Buat💕", url="https://t.me/tummingrockers")
                ],[
                    InlineKeyboardButton(
                        "🤤ASUPAN🤤", url="https://xnxx.com"
                    )
                ]
            ]
        ),
     disable_web_page_preview=True
    )


@Client.on_message(command(["start", f"start@{BOT_USERNAME}"]) & filters.group & ~filters.edited)
async def start(client: Client, message: Message):
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    await message.reply_text(
        f"""✅ **bot sedang berjalan**\n<b>💠 **berjalan:**</b> `{uptime}`""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "✨ Grupku", url=f"https://t.me/{GROUP_SUPPORT}"
                    ),
                    InlineKeyboardButton(
                        "📣 Channelku", url=f"https://t.me/{UPDATES_CHANNEL}"
                    )
                ]
            ]
        )
    )

@Client.on_message(command(["help", f"help@{BOT_USERNAME}"]) & filters.group & ~filters.edited)
async def help(client: Client, message: Message):
    await message.reply_text(
        f"""<b>👋🏻 **Haiii** {message.from_user.mention()} telaso</b>

**Please press the button below to read the explanation and see the list of available commands !**

⚡ __Powered by {BOT_NAME} A.I""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="❔ HOW TO USE ME", callback_data=f"cbguide"
                    )
                ]
            ]
        )
    )

@Client.on_message(command(["help", f"help@{BOT_USERNAME}"]) & filters.private & ~filters.edited)
async def help_(client: Client, message: Message):
    await message.reply_text(
        f"""<b>💡 Halo telaso {message.from_user.mention} welcome to the help menu !</b>

**in this menu you can open several available command menus, in each command menu there is also a brief explanation of each command**

⚡ __Powered by {BOT_NAME} A.I__""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "📚 Basic Cmd", callback_data="cbbasic"
                    ),
                    InlineKeyboardButton(
                        "📕 Advanced Cmd", callback_data="cbadvanced"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "📘 Admin Cmd", callback_data="cbadmin"
                    ),
                    InlineKeyboardButton(
                        "📗 Sudo Cmd", callback_data="cbsudo"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "📙 Owner Cmd", callback_data="cbowner"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "📔 Fun Cmd", callback_data="cbfun"
                    )
                ]
            ]
        )
    )


@Client.on_message(command(["ping", f"ping@{BOT_USERNAME}"]) & ~filters.edited)
async def ping_pong(client: Client, message: Message):
    start = time()
    m_reply = await message.reply_text("pinging...")
    delta_ping = time() - start
    await m_reply.edit_text(
        "🏓 `PONG!!`\n"
        f"⚡️ `{delta_ping * 1000:.3f} ms`"
    )


@Client.on_message(command(["uptime", f"uptime@{BOT_USERNAME}"]) & ~filters.edited)
@sudo_users_only
async def get_uptime(client: Client, message: Message):
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    await message.reply_text(
        "🤖 bot status:\n"
        f"• **berjalan:** `{uptime}`\n"
        f"• **dimulai sejak:** `{START_TIME_ISO}`"
    )
