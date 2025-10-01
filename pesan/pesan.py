import random

# Kumpulan pesan otomatis (50+ variasi)
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
✅ Jangan ganti judul MC.""",

    """:: Uang sudah masuk di saya. Silahkan kalian serah terima data ::

━━━━PENTING!!━━━━
⚠️Harap Tanyakan dulu masalah Garansi.
⚠️Jgn coba2 ada drama jika tidak mau saya mintain ident via VC. Karena drama=ripper.
⚠️Jangan Berikan Hal2 yg rawan seperti OTP tele WA OTP email di luar transaksi
⚠️Jika Pembeli tidak ada kabar selama 8 jam maka dana akan di cairkan dan jika penjual tidak ada kabar selama 5 jam uang di transfer balik ke pembeli
━━━━━━━━━━━━━""",

    "👋 Hallo, grup berhasil dibuat!",
    "✅ Jangan lupa screenshot bukti transaksi untuk keamanan.",
    "⚠️ Admin hanya mediator, semua resiko tetap ada pada buyer & seller.",
    "📌 Ingat! Jangan pernah memberikan OTP kepada siapapun!",
    "💡 Transaksi di luar grup tidak akan dilayani admin.",
    "🔒 Semua data transaksi akan diamankan oleh admin.",
    "🚀 Transaksi cepat = reputasi bagus. Jangan menunda transaksi.",
    "🛑 Dilarang melakukan spam di grup.",
    "📢 Gunakan format transaksi agar tidak membingungkan.",
    "❌ Jangan coba-coba scam, admin langsung banned permanen.",
    "📊 Reputasi penjual/pembeli bisa dicek melalui admin.",
    "🕑 Transaksi hanya diproses pada jam kerja normal, harap sabar.",
    "📌 Jika ada masalah, segera tag admin agar cepat ditangani.",
    "✅ Selesai transaksi? Jangan lupa beri feedback.",
    "⚠️ Seller wajib menjelaskan garansi sebelum transaksi.",
    "💸 Refund hanya berlaku sesuai aturan yang disepakati.",
    "📱 Hati-hati terhadap akun palsu yang menyerupai admin.",
    "🔎 Buyer wajib cek barang/data sebelum transaksi diselesaikan.",
    "📝 Semua transaksi tercatat untuk menghindari perselisihan.",
    "⚡ Jangan melakukan transaksi pribadi tanpa mediator jika belum percaya.",
    "🎯 Tujuan grup ini adalah keamanan bersama dalam transaksi.",
    "🤝 Kepercayaan adalah modal utama dalam jual beli.",
    "📜 Baca aturan grup sebelum transaksi.",
    "📌 Simpan ID transaksi untuk bukti di kemudian hari.",
    "🔔 Jika ada update, admin akan mengumumkan di grup.",
    "🛡️ Jangan bagikan data pribadi sembarangan.",
    "✍️ Format transaksi wajib dipakai agar jelas.",
    "🚫 Jangan melakukan transaksi fiktif.",
    "📥 Pastikan pembayaran dikonfirmasi admin.",
    "✅ Buyer & Seller wajib setuju aturan sebelum mulai.",
    "🗣️ Komunikasi yang jelas = transaksi lancar.",
    "⏳ Jangan membuat transaksi berlarut-larut.",
    "📦 Untuk transaksi barang, minta resi pengiriman.",
    "🔑 Password/akun jangan dishare di luar transaksi.",
    "🧾 Setiap transaksi punya bukti, jangan dihapus.",
    "📣 Admin tidak ikut campur selain mediator.",
    "🎫 Nomor transaksi dicatat otomatis.",
    "🛒 Belanja aman = transaksi via grup.",
    "📂 Data transaksi disimpan maksimal 30 hari.",
    "📍 Seller wajib jujur dengan kondisi barang.",
    "🙅 Jangan janji palsu, trust itu mahal.",
    "🧑‍⚖️ Perselisihan diselesaikan dengan adil.",
    "🚧 Jangan buat lebih dari 1 transaksi di 1 thread.",
    "📢 Admin tidak bertanggung jawab jika transaksi di luar grup.",
    "💬 Sopan santun wajib dijaga dalam grup.",
    "🔔 Notifikasi transaksi akan dikirim otomatis.",
    "👮 Penipu akan dilaporkan & dibanned.",
    "📈 Semakin cepat transaksi selesai, semakin baik reputasi.",
    "🔒 Semua transaksi dilindungi aturan grup.",
    "🛑 Jangan pernah mengirim bukti kosong.",
    "📧 Email/akun hanya diberikan lewat jalur aman.",
    "📲 Semua komunikasi wajib tercatat di grup."
]
pesan_startup = [
    "🤖 Bot berhasil online! Siap digunakan 🚀",
    "✅ Bot aktif sekarang, semua sistem berjalan normal.",
    "📡 Koneksi ke server berhasil, bot sudah hidup!",
    "⚡ Bot berjalan lancar, selamat menggunakan!",
    "🔔 Bot sudah siap melayani perintah Anda!",
    "🚀 Startup sukses, bot siap dipakai.",
    "💡 Bot online. Jangan lupa gunakan format transaksi.",
    "📢 Bot berhasil aktif. Silakan gunakan dengan bijak.",
    "✅ Semua sistem OK. Bot sekarang aktif.",
    "🔒 Bot hidup. Siap menjaga transaksi Anda."
]

# Fungsi untuk ambil pesan random
def get_random_pesan():
    return random.choice(pesan_otomatis)
