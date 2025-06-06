import aiohttp
import asyncio
import discord
import os

from logger.logger import LogV1, LogV2

scale_dict = {
    10: '1', 20: '2', 30: '3', 40: '4',
    45: '5弱', 50: '5強', 55: '6弱', 60: '6強', 70: '7'
}

class Eqinfo:
    def __init__(self, code: int = 551, id_file: str = "last_id.txt"):
        self.code = code
        self.id_file = id_file
        self.last_earthquake_id = self.load_last_id()

    def load_last_id(self):
        if os.path.exists(self.id_file):
            with open(self.id_file, 'r') as f:
                return f.read().strip()
        return None

    def save_last_id(self, eq_id):
        with open(self.id_file, 'w') as f:
            f.write(str(eq_id))

    async def EqinfoLoop(self, callback):
        while True:
            url = f"https://api.p2pquake.net/v2/history?codes={self.code}&limit=1"
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as resp:
                        data = await resp.json()

                        if not data:
                            continue

                        earthquake = data[0]
                        earthquake_id = earthquake['id']

                        # ✅ 前回と同じIDならスキップ
                        if earthquake_id == self.last_earthquake_id:
                            await asyncio.sleep(60)
                            continue

                        # ✅ 新しいID → 保存＆通知
                        self.last_earthquake_id = earthquake_id
                        self.save_last_id(earthquake_id)

                        hypocenter_name = earthquake['earthquake']['hypocenter']['name']
                        magnitude = earthquake['earthquake']['hypocenter']['magnitude']
                        max_scale = earthquake['earthquake']['maxScale']
                        earthquake_time = earthquake['earthquake']['time']
                        max_scale_str = scale_dict.get(max_scale, '不明')

                        # Embed 色決定
                        if max_scale >= 55:
                            color = discord.Color.red()
                        elif max_scale >= 45:
                            color = discord.Color.gold()
                        else:
                            color = discord.Color.blue()

                        embed = discord.Embed(
                            title="📢 地震情報",
                            description=f"震源地: {hypocenter_name}",
                            color=color
                        )
                        embed.add_field(name="マグニチュード", value=str(magnitude), inline=True)
                        embed.add_field(name="最大震度", value=max_scale_str, inline=True)
                        embed.add_field(name="発生時刻", value=earthquake_time, inline=False)

                        await callback(embed)

            except Exception as e:
                LogV2(f"地震情報取得中にエラー: {e}")

            await asyncio.sleep(60)
