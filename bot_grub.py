import os
import sys
import re
import asyncio
import time
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.functions.channels import CreateChannelRequest
from telethon.tl.functions.messages import ExportChatInviteRequest

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

# 🔹 Pesan otomatis
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

# 🔹 Command .id
@client.on(events.NewMessage(pattern=r"\.id"))
async def handler_id(event):
    chat = await event.get_chat()
    await event.delete()

    chat_id = chat.id
    if not str(chat_id).startswith("-100") and (event.is_group or event.is_channel):
        chat_id = f"-100{abs(chat_id)}"

    msg = await event.respond("🔍 Mencari ID chat...")
    await msg.edit(f"🆔 Chat ID: `{chat_id}`")

# 🔹 Command .buat g → buat grup otomatis
@client.on(events.NewMessage(pattern=r"\.buat g(?: (\d+))? (.+)"))
async def handler_buat(event):
    if OWNER_ID and event.sender_id != OWNER_ID:
        return

    await event.delete()

    match = re.match(r"\.buat g(?: (\d+))? (.+)", event.raw_text)
    jumlah = int(match.group(1)) if match.group(1) else 1
    nama = match.group(2)

    msg = await event.respond("⏳ Membuat grup .")

    animasi = [".", "..", "...", "...."]
    hasil = []
    start_time = time.time()

    for i in range(jumlah):
        # progress bar
        total_bar = 10
        filled = int((i+1) / jumlah * total_bar)
        bar = "▓" * filled + "░" * (total_bar - filled)

        # estimasi waktu sisa
        elapsed = time.time() - start_time
        avg_per_item = elapsed / (i+1)
        remaining = int(avg_per_item * (jumlah - (i+1)))

        await msg.edit(
            f"⏳ Membuat grup {animasi[i % len(animasi)]}\n"
            f"[{bar}] {i+1}/{jumlah}\n"
            f"Estimasi: {remaining} detik lagi"
        )
        await asyncio.sleep(0.5)

        # buat grup
        nama_group = f"{nama} {i+1}" if jumlah > 1 else nama
        grup = await client(CreateChannelRequest(
            title=nama_group,
            about="GRUB BY @WARUNGBULLOVE",
            megagroup=True
        ))
        chat_id = grup.chats[0].id

        # link undangan
        try:
            result = await client(ExportChatInviteRequest(peer=chat_id))
            link = result.link
        except Exception as e:
            link = f"(gagal ambil link: {e})"

        # pesan otomatis
        await client.send_message(chat_id, "👋 Hallo, grup berhasil dibuat!")
        await client.send_message(chat_id, pesan1)
        await client.send_message(chat_id, pesan2)
        await client.send_message(chat_id, pesan3)

        hasil.append(f"✅ [{nama_group}]({link})")

    # selesai
    await msg.edit("🎉 Grup berhasil dibuat:\n\n" + "\n".join(hasil), link_preview=False)

# 🔹 Command .restart
@client.on(events.NewMessage(pattern=r"\.restart"))
async def handler_restart(event):
    await event.delete()
    await event.respond("♻️ Bot sedang restart...")
    args = [sys.executable] + sys.argv
    os.execv(sys.executable, args)

# === MAIN ===
async def main():
    print("🤖 Bot berjalan...")
    if OWNER_ID:
        try:
            await client.send_message(OWNER_ID, "✅ Bot berhasil dijalankan dan siap dipakai.")
        except Exception:
            pass
    await client.run_until_disconnected()

if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(main())
