# 🔹 Command .buat g → buat grup otomatis dengan progress bar
@client.on(events.NewMessage(pattern=r"\.buat g(?: (\d+))? (.+)"))
async def handler_buat(event):
    if OWNER_ID and event.sender_id != OWNER_ID:
        return

    jumlah = int(event.pattern_match.group(1) or 1)  # default = 1
    nama = event.pattern_match.group(2)

    await event.delete()
    msg = await event.respond("⏳ Membuat grup...")

    hasil = []
    start_time = asyncio.get_event_loop().time()

    for i in range(jumlah):
        try:
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

            # kirim pesan otomatis acak
            pesan = random.choice(pesan_otomatis)
            await client.send_message(chat_id, pesan)

            hasil.append(f"✅ [{nama} {i+1}]({link})")

            # hitung progress
            selesai = i + 1
            persen = int((selesai / jumlah) * 10)  # progress bar dari 10 blok
            bar = "▓" * persen + "░" * (10 - persen)

            # estimasi sisa waktu (kasar, 2 detik per grup)
            elapsed = asyncio.get_event_loop().time() - start_time
            avg_per_group = elapsed / selesai
            sisa = int((jumlah - selesai) * avg_per_group)

            await msg.edit(
                f"⏳ Membuat grup ...\n[{bar}] {selesai}/{jumlah}\nEstimasi: {sisa} detik lagi"
            )

            await asyncio.sleep(2)

        except FloodWaitError as e:
            await msg.edit(f"⚠️ Kena FloodWait! Tunggu {e.seconds//3600} jam {(e.seconds%3600)//60} menit lagi.")
            return
        except Exception as er:
            await msg.edit(f"❌ Error saat membuat grup: {er}")
            return

    await msg.edit("🎉 Grup berhasil dibuat:\n\n" + "\n".join(hasil), link_preview=False)
