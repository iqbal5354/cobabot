import os
import sys
from dotenv import load_dotenv
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.functions.messages import CreateChatRequest, ExportChatInviteRequest
from telethon.tl.functions.channels import CreateChannelRequest

# Load .env
load_dotenv()

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
string_session = os.getenv("SESSION")
owner_id = int(os.getenv("OWNER_ID", "0"))

client = TelegramClient(StringSession(string_session), api_id, api_hash)

# =====================================================================
# COMMAND .buat
# =====================================================================
@client.on(events.NewMessage(pattern=r"\.buat (b|g|c)(?: |$)(.*)"))
async def handler(event):
    tipe = event.pattern_match.group(1).strip()
    teks = event.pattern_match.group(2).strip()

    await event.delete()  # hapus pesan perintah

    jumlah = 1
    nama = teks

    parts = teks.split(maxsplit=1)
    if parts and parts[0].isdigit():
        jumlah = int(parts[0])
        nama = parts[1] if len(parts) > 1 else "Tanpa Nama"

    # Kirim pesan awal "loading"
    msg = await event.respond(f"⏳ Mohon tunggu sebentar...\nSedang membuat {jumlah} {'grup' if tipe=='g' else 'channel'}")

    try:
        hasil = []
        for i in range(1, jumlah + 1):
            judul = f"{nama} {i}" if jumlah > 1 else nama

            if tipe == "b":
                result = await client(CreateChatRequest(users=[], title=judul))
                chat_id = result.chats[0].id
                link = (await client(ExportChatInviteRequest(chat_id))).link
                hasil.append(f"✅ Grup **{judul}** → {link}")

            elif tipe in ["g", "c"]:
                result = await client(
                    CreateChannelRequest(
                        title=judul,
                        about="Dibuat otomatis oleh userbot",
                        megagroup=(tipe == "g"),
                    )
                )
                chat_id = result.chats[0].id
                link = (await client(ExportChatInviteRequest(chat_id))).link

                tipe_str = "Supergroup" if tipe == "g" else "Channel"
                hasil.append(f"✅ {tipe_str} **{judul}** → {link}")

        # Edit pesan jadi hasil akhir
        await msg.edit("\n".join(hasil), link_preview=False)

    except Exception as e:
        await msg.edit(f"❌ Error: `{e}`")


# =====================================================================
# COMMAND .id
# =====================================================================
@client.on(events.NewMessage(pattern=r"\.id"))
async def get_id(event):
    try:
        await event.delete()  # hapus pesan perintah

        if event.is_group or event.is_channel:
            chat = await event.get_chat()
            chat_id = chat.id

            # konsisten: supergroup/channel pakai -100 prefix
            if not str(chat_id).startswith("-100") and event.is_channel:
                chat_id = f"-100{chat_id}"

            await event.respond(f"🆔 Chat ID: `{chat_id}`")

        elif event.is_private:
            user = await event.get_sender()
            await event.respond(f"🆔 User ID: `{user.id}`")

    except Exception as e:
        await event.respond(f"❌ Error: `{e}`")

# =====================================================================
# COMMAND .restart
# =====================================================================
@client.on(events.NewMessage(pattern=r"\.restart"))
async def restart_bot(event):
    await event.delete()  # hapus pesan perintah
    await event.respond("♻️ Restarting bot...")
    python = sys.executable
    os.execl(python, python, __file__)

# =====================================================================
# MAIN PROGRAM
# =====================================================================
async def main():
    await client.start()
    if owner_id:
        try:
            await client.send_message(owner_id, "✅ Bot berhasil dijalankan dan siap menerima perintah.")
        except Exception as e:
            print(f"Gagal kirim notif ke owner: {e}")
    print("🚀 Userbot berjalan... kirim perintah di Telegram")
    await client.run_until_disconnected()

if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(main())
