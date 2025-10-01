import os
import sys
import asyncio
import random
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.errors import FloodWaitError
from telethon.tl.functions.channels import CreateChannelRequest
from telethon.tl.functions.messages import ExportChatInviteRequest

# 🔹 Ambil ENV
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION = os.getenv("SESSION")
OWNER_ID = os.getenv("OWNER_ID")
if OWNER_ID and OWNER_ID.isdigit():
    OWNER_ID = int(OWNER_ID)
else:
    OWNER_ID = None

# 🔹 Buat client
client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)

# 🔹 Variabel status spam
spam_status = {"kena": False, "sisa": 0}

# 🔹 Pesan acak anti spam
pesan_random = [
    "🎉 Grup berhasil dibuat!",
    "✅ Grup sudah siap digunakan.",
    "🔥 Selesai, grup kamu aktif!",
    "📢 Grup berhasil aktif sekarang."
]

# 🔹 Animasi progress bar
async def progress_anim(event, total):
    for i in range(1, total + 1):
        bar = "▓" * i + "░" * (total - i)
        text = f"⏳ Membuat grup ...\n[{bar}] {i}/{total}\nEstimasi: {total - i} detik lagi"
        await event.edit(text)
        await asyncio.sleep(1)

# 🔹 Command cek status spam
@client.on(events.NewMessage(pattern=r"\.cek"))
async def cek_status(event):
    if spam_status["kena"]:
        await event.reply(f"🚨 Saat ini kena spamwait!\n⏳ Tunggu {spam_status['sisa']} detik lagi.")
    else:
        await event.reply("✅ Aman, bot bisa jalan tanpa spamwait.")

# 🔹 Command buat grup
@client.on(events.NewMessage(pattern=r"\.buat g(?: (\d+))? (.+)"))
async def handler_buat(event):
    if OWNER_ID and event.sender_id != OWNER_ID:
        return await event.reply("❌ Kamu tidak punya akses.")

    try:
        jumlah = int(event.pattern_match.group(1) or 1)
        nama = event.pattern_match.group(2)

        await event.reply(f"⏳ Proses membuat {jumlah} grup dengan nama: **{nama}**")

        for i in range(1, jumlah + 1):
            # 🔹 Animasi progress
            anim_msg = await event.respond("⏳ Membuat grup ...")
            await progress_anim(anim_msg, 10)

            # 🔹 Bikin grup
            try:
                result = await client(CreateChannelRequest(
                    title=f"{nama} {i}",
                    about="Grup otomatis by bot",
                    megagroup=True
                ))
                chat = result.chats[0]

                # 🔹 Ambil link grup
                invite = await client(ExportChatInviteRequest(chat.id))

                # 🔹 Kirim pesan random biar anti spam
                msg = random.choice(pesan_random)
                await event.respond(f"{msg}\n\n🔗 {invite.link}")

            except FloodWaitError as e:
                spam_status["kena"] = True
                spam_status["sisa"] = e.seconds
                await event.respond(f"🚨 Kena spamwait {e.seconds} detik, stop dulu.")
                break

    except Exception as e:
        await event.reply(f"⚠️ Error: {str(e)}")

# 🔹 Jalankan client
print("✅ Bot jalan...")
client.start()
client.run_until_disconnected()
