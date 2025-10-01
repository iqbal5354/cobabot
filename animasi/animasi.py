import asyncio

async def tampilkan_progress(msg, total):
    """
    Animasi progress bar untuk pembuatan grup.
    """
    for i in range(total):
        progress = int(((i+1)/total)*10)
        bar = "▓" * progress + "░" * (10-progress)
        estimasi = (total - (i+1)) * 2  # misal 2 detik/grup
        await msg.edit(
            f"⏳ Membuat grup ...\n"
            f"[{bar}] {i+1}/{total}\n"
            f"Estimasi: {estimasi} detik lagi"
        )
        await asyncio.sleep(2)  # jeda per update
