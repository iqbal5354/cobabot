import os
import sys
import asyncio
import random
from datetime import datetime, timedelta
from telethon import TelegramClient, events, functions
from telethon.sessions import StringSession
from telethon.tl.functions.channels import CreateChannelRequest

# Import animasi & pesan
from animasi.animasi import tampilkan_progress
from pesan.pesan import get_random_pesan, get_startup_pesan

# 🔹 API dari ENV
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
session_string = os.getenv("SESSION")

# 🔹 OWNER ID langsung fix
OWNER_ID = -1002271009889  

client = TelegramClient(StringSession(session_string), api_id, api_hash)

# ===============================
# 🔹 Command: buat grup otomatis
# ===============================
@client.on(events.NewMessage(pattern=r"\.buat g(?: (\d+))? (.+)"))
async def handler_buat(event):
    if event.sender_id != OWNER_ID:
        return

    jumlah = int(event.pattern_match.group(1)) if event.pattern_match.group(1) else 1
    nama = event.pattern_match.group(2)

    await event.delete()
    msg = await event.respond("⏳ Membuat grup...")

    hasil = []
    for i in range(jumlah):
        try:
            grup = await client(CreateChannelRequest(
                title=f"{nama} {i+1}",
                about="Grub by @WARUNGBULLOVE",
                megagroup=True
            ))
            chat_id = grup.chats[0].id

            # bikin link undangan
            try:
                link = await client.export_chat_invite_link(chat_id)
            except Exception as e:
                link = f"(gagal ambil link: {e})"

            # tampilkan progress animasi
            await tampilkan_progress(msg, jumlah, i)

            # kirim pesan random (4 pesan)
            for _ in range(4):
                await client.send_message(chat_id, get_random_pesan())
                await asyncio.sleep(1)

            hasil.append(f"✅ [{nama} {i+1}]({link})")

        except Exception as e:
            hasil.append(f"❌ Gagal buat {nama} {i+1} → {e}")

    await msg.edit("🎉 Grup berhasil dibuat:\n\n" + "\n".join(hasil), link_preview=False)


# ===============================
# 🔹 Command: cek id
# ===============================
@client.on(events.NewMessage(pattern=r"\.id"))
async def handler_id(event):
    await event.reply(f"🆔 Chat ID: `{event.chat_id}`")


# ===============================
# 🔹 Command: restart bot
# ===============================
@client.on(events.NewMessage(pattern=r"\.restart"))
async def handler_restart(event):
    if event.sender_id != OWNER_ID:
        return
    await event.respond("♻️ Restarting bot...")
    os.execv(sys.executable, ['python'] + sys.argv)


# ===============================
# 🔹 Command: cek spam/limit
# ===============================
@client.on(events.NewMessage(pattern=r"\.cek"))
async def handler_cek(event):
    if event.sender_id != OWNER_ID:
        return

    try:
        result = await client(functions.account.GetNotifySettingsRequest(peer="me"))
        await event.respond("✅ Akun aman, tidak terkena spam/limit.")
    except Exception as e:
        if "FloodWaitError" in str(type(e)):
            detik = int(str(e).split("Seconds: ")[1].split(" ")[0])
            selesai = datetime.now() + timedelta(seconds=detik)
            await event.respond(
                f"⚠️ Akun terkena limit/spam!\n\n"
                f"⏳ Waktu tersisa: {detik//86400} hari {detik%86400//3600} jam {detik%3600//60} menit {detik%60} detik\n"
                f"📅 Bisa digunakan lagi pada: {selesai.strftime('%A, %d %B %Y %H:%M:%S')}"
            )
        else:
            await event.respond(f"❌ Gagal cek status: {e}")


# ===============================
# 🔹 Auto kirim pesan saat start
# ===============================
async def kirim_start_message():
    try:
        pesan = get_startup_pesan()
        await client.send_message(OWNER_ID, pesan)
    except Exception as e:
        print(f"Gagal kirim pesan startup: {e}")


# ===============================
# 🔹 Start bot
# ===============================
async def main():
    await client.start()
    await kirim_start_message()
    print("🚀 Bot berjalan...")
    await client.run_until_disconnected()

with client:
    client.loop.run_until_complete(main())
