import asyncio

async def animasi_loading(event, total, delay=1):
    for i in range(1, total + 1):
        progress = "▓" * i + "░" * (total - i)
        estimasi = (total - i) * delay
        await event.edit(
            f"⏳ Membuat grup ...\n[{progress}] {i}/{total}\nEstimasi: {estimasi} detik lagi"
        )
        await asyncio.sleep(delay)
