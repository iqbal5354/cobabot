import random

pesan_otomatis = [
    """FORMAT TRANSAKSI

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
✅ Janggn ganti judul MC.""",

    """:: Uang sudah masuk di saya. Silahkan kalian serah terima data ::

━━━━PENTING!!━━━━
⚠️Harap Tanyakan dulu masalah Garansi.
⚠️Jgn coba2 ada drama jika tidak mau saya mintain ident via VC. Karena drama=ripper.
⚠️Jangan Berikan Hal2 yg rawan seperti OTP tele WA OTP email di luar transaksi
⚠️Jika Pembeli tidak ada kabar selama 8 jam maka dana akan di cairkan dan jika penjual tidak ada kabar selama 5 jam uang di transfer balik ke pembeli
━━━━━━━━━━━━━""",

    "👋 Hallo, grup berhasil dibuat!",

    # Tambahan 20 pesan random
    "📰 News hari ini: selalu cek harga pasar sebelum transaksi.",
    "💡 Tips: Jangan pernah bagikan OTP ke siapapun.",
    "⚠️ Waspada penipuan! Pastikan lawan transaksi terpercaya.",
    "📌 Gunakan escrow untuk transaksi aman.",
    "✅ Semua transaksi wajib sesuai format.",
    "📢 Ingat! Jangan ganti nama grup tanpa izin admin.",
    "🛑 Jika ada masalah segera hubungi admin.",
    "🔥 Promo hari ini: keamanan transaksi adalah prioritas.",
    "📊 Statistik: 90% masalah transaksi karena miskomunikasi.",
    "🔒 Keamanan akun penting, aktifkan 2FA.",
    "⚡ Fast info: fee cancel tetap terpotong.",
    "💬 Diskusi sehat, tanpa spam.",
    "🕒 Jika penjual diam >5 jam dana kembali ke pembeli.",
    "🕗 Jika pembeli diam >8 jam dana otomatis cair.",
    "🎯 Tujuan utama: transaksi aman & nyaman.",
    "🤝 Kepercayaan adalah kunci utama.",
    "📍 Selalu gunakan channel resmi.",
    "📝 Catat semua detail transaksi.",
    "🔎 Verifikasi identitas lawan transaksi.",
    "🌐 Gunakan bot ini untuk perlindungan transaksi."
]

def ambil_pesan_acak(jumlah=4):
    return random.sample(pesan_otomatis, jumlah)
