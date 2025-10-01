import os
import sys
import asyncio
import random
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.functions.channels import CreateChannelRequest

# Import dari file animasi & pesan
from animasi.animasi import tampilkan_progress
from pesan.pesan import get_random_pesan

# Ambil API dari ENV
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
session_string = os.getenv("SESSION")  # string session biar ga input manual

# 🔹 OWNER ID langsung fix (tidak perlu ENV)
OWNER_ID = -1002271009889  

client = TelegramClient(StringSession(session_string), api_id, api_hash)


# 🔹 Command: buat grup otomatis
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

            # tampilkan progress
            await tampilkan_progress(msg, jumlah, i)

            # kirim pesan random (4 pesan)
            for _ in range(4):
                await client.send_message(chat_id, get_random_pesan())
                await asyncio.sleep(1)

            hasil.append(f"✅ [{nama} {i+1}]({link})")

        except Exception as e:
            hasil.append(f"❌ Gagal buat {nama} {i+1} → {e}")

    await msg.edit("🎉 Grup berhasil dibuat:\n\n" + "\n".join(hasil), link_preview=False)


# 🔹 Command: cek id
@client.on(events.NewMessage(pattern=r"\.id"))
async def handler_id(event):
    await event.reply(f"🆔 Chat ID: `{event.chat_id}`")


# 🔹 Command: restart bot
@client.on(events.NewMessage(pattern=r"\.restart"))
async def handler_restart(event):
    if event.sender_id != OWNER_ID:
        return
    await event.respond("♻️ Restarting bot...")
    os.execv(sys.executable, ['python'] + sys.argv)


print("🚀 Bot berjalan...")
client.start()
client.run_until_disconnected()
