import os
import discord
from discord import app_commands
from discord.ext import commands
import json
import re
import urllib
import requests
from server import keep_alive

intents = discord.Intents.default()
intents.messages = True
intents.reactions = True
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

#citycodesは47都道府県のも対応
citycodes = {
  "北海道": "016010",
  "青森": "020010",
  "岩手": "030010",
  "宮城": "040010",
  "秋田": "050010",
  "山形": "060010",
  "福島": "070010",
  "茨城": "080010",
  "栃木": "090010",
  "群馬": "100010",
  "埼玉": "110010",
  "千葉": "120010",
  "東京": "130010",
  "神奈川": "140010",
  "新潟": "150010",
  "富山": "160010",
  "石川": "170010",
  "福井": "180010",
  "山形": "190010",
  "長野": "200010",
  "岐阜": "210010",
  "静岡": "220010",
  "愛知": "230010",
  "三重": "240010",
  "滋賀": "250010",
  "京都": "260010",
  "大阪": "270000",
  "兵庫": "280010",
  "奈良": "290010",
  "和歌山": "300010",
  "鳥取": "310010",
  "島根": "320010",
  "岡山": "330010",
  "広島": "340010",
  "山口": "350010",
  "徳島": "360010",
  "香川": "370000",
  "愛媛": "380010",
  "高知": "390010",
  "福島": "400010",
  "佐賀": "410010",
  "長崎": "420010",
  "熊本": "430010",
  "大分": "440010",
  "宮崎": "450010",
  "鹿児島": "460010",
  "沖縄": "471010",
}


@client.event
async def on_ready():
  print(
    "<<---------------------------------------Boot Completed--------------------------------------->>"
  )
  await tree.sync()

@tree.command(name="test", description="テストコマンドです。")
async def test_command(interaction: discord.Interaction):
  await interaction.response.send_message(
    "てすと！", ephemeral=True)  #ephemeral=True→「これらはあなただけに表示されています」

@tree.command(name="ping", description="pongを返します。")
async def ping_command(interaction: discord.Interaction):
  await interaction.response.send_message(
    "Pong!", ephemeral=True)

@tree.command(name="about", description="aiyueBOTについての説明です。")
async def about_command(interaction: discord.Interaction):
  await interaction.response.send_message(
    "`お天気BOTだよ～、今日明日明後日の各地の天気を教えてくれるよ！ \n 試しに「●●の天気は？」を入力してみてね！（●●に入る文字は県名が入るよ～）`",
    ephemeral=True)

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  reg_res = re.compile(u"(.+)の天気は？").search(message.content)
  if reg_res:
    if reg_res.group(1) in citycodes.keys():
      citycode = citycodes[reg_res.group(1)]
      try:
        resp = requests.get(
          f"https://weather.tsukumijima.net/api/forecast/city/{citycode}")
        if resp.status_code != 200:
          await message.channel.send(f"天気情報の取得に失敗しました: HTTP {resp.status_code}"
                                     )
          return
        resp = resp.json()
      except Exception as e:
        await message.channel.send(f"天気情報の取得に失敗しました: {e}")
        return
      msg = "__【お天気情報：**" + resp["location"]["city"] + "**】__\n"
      for f in resp["forecasts"]:
        msg += f["dateLabel"] + "：**" + f["telop"] + "**\n"
      msg += "```" + resp["description"]["bodyText"] + "```"
      await message.channel.send(msg)
    else:
      await message.channel.send("そこの天気はわかりません...")

keep_alive()
TOKEN = os.getenv("DISCORD_TOKEN")
try:
  client.run(TOKEN)
except:
  os.system("kill 1")