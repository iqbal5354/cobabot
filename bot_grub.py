import os
import sys
import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.functions.channels import CreateChannelRequest, UpdateUsernameRequest
from telethon.tl.functions.messages import CreateChatRequest, ExportChatInviteRequest

# 🔹 Ambil ENV
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION = os.getenv("SESSION")

# 🔹 OWNER_ID opsional
OWNER_ID = os.getenv("OWNER_ID")
if OWNER_ID and OWNER_ID.isdigit():
    OWNER_ID = int(OWNER_ID)
else:
    OWNER_ID = None

client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)

# 🔹 Notif saat bot berhasil jalan
async def main():
    if OWNER_ID:
        try:
            await client.send_message(OWNER_ID, "✅ Bot berhasil dijalankan dan siap dipakai.")
        except Exception:
            pass

# 🔹 Command .buat
@client.on(events.NewMessage(pattern=r"\.buat (b|g|c) (\d+) (.+)"))
async def handler_buat(event):
    jenis = event.pattern_match.group(1)
    jumlah = int(event.pattern_match.group(2))
    nama = event.pattern_match.group(3)

    # Hapus command user
    await event.delete()

    # Kirim pesan tunggu
    msg = await event.respond("⏳ Mohon tunggu sebentar, sedang membuat group...")

    try:
        hasil = []
        for i in range(1, jumlah + 1):
            nama_group = f"{nama} {i}" if jumlah > 1 else nama

            if jenis == "b":
                r = await client(
                    CreateChatRequest(
                        users=[await client.get_me()],
                        title=nama_group,
                    )
                )
                chat_id = r.chats[0].id
                link = (await client(ExportChatInviteRequest(chat_id))).link
            else:
                r = await client(
                    CreateChannelRequest(
                        title=nama_group,
                        about="Grup/Channel otomatis dibuat oleh bot",
                        megagroup=(jenis == "g"),
                    )
                )
                chat_id = r.chats[0].id
                link = (await client(ExportChatInviteRequest(chat_id))).link

            hasil.append(f"✅ [{nama_group}]({link})")

        await msg.edit("🎉 Grup/Channel berhasil dibuat:\n\n" + "\n".join(hasil), link_preview=False)

    except Exception as e:
        await msg.edit(f"❌ Error: {str(e)}")

# 🔹 Command .id
# 🔹 Command .buat
@client.on(events.NewMessage(pattern=r"\.buatt (b|g|c) (\d+) (.+)"))
async def handler_buat(event):
    jenis = event.pattern_match.group(1)
    jumlah = int(event.pattern_match.group(2))
    nama = event.pattern_match.group(3)

    # Hapus command user
    await event.delete()

    # Kirim pesan tunggu
    msg = await event.respond("⏳ Mohon tunggu sebentar, sedang membuat group...")

    try:
        hasil = []
        for i in range(1, jumlah + 1):
            nama_group = f"{nama} {i}" if jumlah > 1 else nama

            if jenis == "b":
                r = await client(
                    CreateChatRequest(
                        users=[await client.get_me()],
                        title=nama_group,
                    )
                )
                chat_id = r.chats[0].id
                link = (await client(ExportChatInviteRequest(chat_id))).link
            else:
                r = await client(
                    CreateChannelRequest(
                        title=nama_group,
                        about="Grup/Channel otomatis dibuat oleh bot",
                        megagroup=(jenis == "g"),
                    )
                )
                chat_id = r.chats[0].id
                link = (await client(ExportChatInviteRequest(chat_id))).link

            # kirim pesan ke grup yang baru dibuat
            await client.send_message(chat_id, "👋 Hallo, grup berhasil dibuat!")

            hasil.append(f"✅ [{nama_group}]({link})")

        await msg.edit("🎉 Grup/Channel berhasil dibuat:\n\n" + "\n".join(hasil), link_preview=False)

    except Exception as e:
        await msg.edit(f"❌ Error: {str(e)}")

# 🔹 Command .id
@client.on(events.NewMessage(pattern=r"\.id"))
async def handler_id(event):
    chat = await event.get_chat()

    # hapus command user
    await event.delete()

    # paksa format -100 untuk group / channel
    chat_id = chat.id
    if not str(chat_id).startswith("-100") and (event.is_group or event.is_channel):
        chat_id = f"-100{abs(chat_id)}"

    # bikin pesan dummy lalu edit jadi hasil
    msg = await event.respond("🔍 Mencari ID chat...")
    await msg.edit(f"🆔 Chat ID: `{chat_id}`")


# 🔹 Command .restart
@client.on(events.NewMessage(pattern=r"\.restart"))
async def handler_restart(event):
    await event.delete()
    await event.respond("♻️ Bot sedang restart...")

    args = [sys.executable] + sys.argv
    os.execv(sys.executable, args)


if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(main())
        client.run_until_disconnected()


