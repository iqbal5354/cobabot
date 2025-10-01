import os
import sys
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.functions.channels import CreateChannelRequest

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

# 🔹 Init client pakai StringSession
client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)


# 🔹 Pesan otomatis untuk grup baru
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


# 🔹 Command .id → cek chat id
@client.on(events.NewMessage(pattern=r"\.id"))
async def handler_id(event):
    chat = await event.get_chat()
    await event.delete()

    chat_id = chat.id
    if not str(chat_id).startswith("-100") and (event.is_group or event.is_channel):
        chat_id = f"-100{abs(chat_id)}"

    msg = await event.respond("🔍 Mencari ID chat...")
    await msg.edit(f"🆔 Chat ID: `{chat_id}`")


# 🔹 Command .restart → restart bot
@client.on(events.NewMessage(pattern=r"\.restart"))
async def handler_restart(event):
    if OWNER_ID and event.sender_id != OWNER_ID:
        return
    await event.delete()
    await event.respond("♻️ Bot sedang restart...")
    os.execv(sys.executable, [sys.executable] + sys.argv)


# 🔹 Command .buat g → buat grup otomatis
# 🔹 Command .buat g → buat grup otomatis
@client.on(events.NewMessage(pattern=r"\.buat g (\d+) (.+)"))
async def handler_buat(event):
    if OWNER_ID and event.sender_id != OWNER_ID:
        return

    jumlah = int(event.pattern_match.group(1))
    nama = event.pattern_match.group(2)

    await event.delete()
    msg = await event.respond("⏳ Mohon tunggu sebentar, sedang membuat grup...")

    hasil = []
    for i in range(jumlah):
        grup = await client(CreateChannelRequest(
            title=f"{nama} {i+1}",
            about="GRUB BY @WARUNGBULLOVE",
            megagroup=True
        ))
        chat_id = grup.chats[0].id

        # bikin link undangan
        try:
            link = await client.export_chat_invite_link(chat_id)
        except Exception as e:
            link = f"(gagal ambil link: {e})"

        # kirim pesan otomatis ke grup
        await client.send_message(chat_id, "👋 Hallo, grup berhasil dibuat!")
        await client.send_message(chat_id, pesan1)
        await client.send_message(chat_id, pesan2)
        await client.send_message(chat_id, pesan3)

        # tambahkan ke hasil, format nama + link
        hasil.append(f"✅ [{nama} {i+1}]({link})")

    await msg.edit("🎉 Grup berhasil dibuat:\n\n" + "\n".join(hasil), link_preview=False)

# 🔹 Notif saat bot berhasil jalan
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


