import os
import sys
import asyncio
from telethon import TelegramClient, events
from telethon.tl.functions.channels import CreateChannelRequest

# === Load dari environment (.env atau Railway Variables) ===
api_id = int(os.getenv("API_ID", "0"))
api_hash = os.getenv("API_HASH", "")
session = os.getenv("SESSION", "session")
owner_id_str = os.getenv("OWNER_ID", "0")

try:
    owner_id = int(owner_id_str)
except ValueError:
    owner_id = 0

# === Init client ===
client = TelegramClient("bot", api_id, api_hash).start()

# Pesan otomatis untuk grup baru
pesan1 = """FORMAT TRANSAKSI

┏━━━━━━━━━━━━━━━━
┣ Jual Beli Apa  : 
┣ Penjual Siapa  : 
┣ Pembeli Siapa  :
┣ Harga Berapa   :
┗━━━━━━━━━━━━━━━━ 
PENTING!!!
☑️ Harap pasikan Transaksi tidak ada miskom buyer dan seller. 
☑️ Jika Transaksi Cancel Fee tetap Terpotong, jika tdk mau Terpotong Silahkan cari penjual lain.
☑️ Jadikan Saya Sebagai admin grub ini
✅ Janggn ganti judul MC."""

pesan2 = """FORMAT TRANSAKSI

┏━━━━━━━━━━━━━━━━
┣ Jual Beli Apa  : 
┣ Penjual Siapa  : 
┣ Pembeli Siapa  :
┣ Harga Berapa   :
┗━━━━━━━━━━━━━━━━ 
PENTING!!!
☑️ Harap pasikan Transaksi tidak ada miskom buyer dan seller. 
☑️ Jika Transaksi Cancel Fee tetap Terpotong, jika tdk mau Terpotong Silahkan cari penjual lain.
☑️ Jadikan Saya Sebagai admin grub ini
✅ Janggn ganti judul MC."""

pesan3 = """:: Uang sudah masuk di saya. Silahkan kalian serah terima data ::

━━━━PENTING!!━━━━
⚠️Harap Tanyakan dulu masalah Garansi.
⚠️Jgn coba2 ada drama jika tidak mau saya mintain ident via VC. Karena drama=ripper.
⚠️Jangan Berikan Hal2 yg rawan seperti OTP tele WA OTP email di luar transaksi
⚠️jika Pembeli tidak ada kabar selama 8 jam maka dana akan di cairkan dan jika penjual tidak ada kabar selama 5 jam uang di transfer balik ke pembeli
━━━━━━━━━━━━━"""

# === COMMAND ===

# Cek ID
@client.on(events.NewMessage(pattern=r"\.id"))
async def handler_id(event):
    if event.sender_id == owner_id:
        await event.delete()
        chat = await event.get_chat()
        prefix = "-100" if getattr(chat, "megagroup", False) else ""
        await event.respond(f"🆔 ID: `{prefix}{chat.id}`")

# Restart bot
@client.on(events.NewMessage(pattern=r"\.restart"))
async def handler_restart(event):
    if event.sender_id == owner_id:
        await event.delete()
        await event.respond("♻️ Restarting...")
        os.execv(sys.executable, ['python'] + sys.argv)

# Buat grup
@client.on(events.NewMessage(pattern=r"\.buat g (\d+) (.+)"))
async def handler_buat(event):
    if event.sender_id != owner_id:
        return
    await event.delete()
    jumlah = int(event.pattern_match.group(1))
    nama = event.pattern_match.group(2)

    msg = await event.respond("⏳ Mohon tunggu sebentar, sedang membuat grup...")

    hasil = []
    for i in range(jumlah):
        grup = await client(CreateChannelRequest(
            title=f"{nama} {i+1}",
            about="Grub by @warungbullove.",
            megagroup=True
        ))
        chat_id = grup.chats[0].id

        # Kirim pesan otomatis
        await client.send_message(chat_id, "👋 Hallo, grup by @WARUNGBULLOVE!")
        await client.send_message(chat_id, pesan1)
        await client.send_message(chat_id, pesan2)
        await client.send_message(chat_id, pesan3)

        hasil.append(f"{i+1}. Grup **{nama} {i+1}** → `-100{abs(chat_id)}`")

    await msg.edit("✅ Grup berhasil dibuat:\n\n" + "\n".join(hasil))


# === MAIN ===
async def main():
    print("🤖 Bot berjalan...")
    await client.run_until_disconnected()

if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(main())
