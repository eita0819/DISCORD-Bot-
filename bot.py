import discord  # discord.py
import asyncio
import discord
import random
import asyncio
import sys
from discord.ext import commands
import youtube_dl
import random
import asyncio
import json
import os
import time
  # Botのインスタンスを作成します
intents = discord.Intents.all()

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():  # Botが起動したときに実行されるイベント
    print(f"Bot is ready! Logged in as {bot.user}")
    
    await bot.tree.sync()
    return

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="ZEEDS"))
@bot.slash_command()
async def ping(ctx):  # ユーザーが"/ping"と入力したときに実行されるコマンド
    bot_message = await ctx.send("Pong!")
    await asyncio.sleep(10)
    await bot_message.delete()
    return

@bot.slash_command(name="role",description="ロール権利")
@commands.has_permissions(administrator=True)
async def add_role(ctx, user: discord.Member, role: discord.Role):
    await user.add_roles(role)
    bot_message = await ctx.respond(f"{user.mention}に{role.name}ロールが付与されました。")
    await asyncio.sleep(10)
    await bot_message.delete()
    return

@bot.slash_command(name="aiueo", description="Ping.")
async def あ(ctx):
    bot_message = await ctx.respond("あいうえお、すみません。だるいです。")
    await asyncio.sleep(10)
    await bot_message.delete()

@bot.slash_command(description="誰でしょうかね")
async def あなたはだれ(ctx):
    bot_message = await ctx.respond("私は、あなたのお手伝いをするために作られたBotです作者uuid_toxic_pikaanimal")
    await asyncio.sleep(10)
    await bot_message.delete()
    return

@bot.slash_command(description="しね")
async def しね(ctx):
    bot_message = await ctx.respond("しね")
    await asyncio.sleep(10)
    await bot_message.delete()
    return
@bot.slash_command(description="おはよう")
async def おはよう(ctx):
    bot_message = await ctx.respond("おはようございます")
    await asyncio.sleep(10)
    await bot_message.delete()
    return


@bot.slash_command(description="こんにちは")
async def こんにちは(ctx):
    bot_message = await ctx.respond("こんにちは")
    await asyncio.sleep(10)
    await bot_message.delete()
    return

@bot.slash_command(description="こんばんは")
async def こんばんは(ctx):
    bot_message = await ctx.respond("こんばんは")
    await asyncio.sleep(10)
    await bot_message.delete()
    return
@bot.slash_command(description="おやすみ" )
async def おやすみ(ctx):
    bot_message = await ctx.respond("おやすみなさい")
    await asyncio.sleep(10)
    await bot_message.delete()
    return

# 投票の結果を保存する辞書
vote_results = {}

@bot.slash_command()
@commands.has_permissions(manage_messages=True)
async def deletems(ctx, amount: int):
    await ctx.channel.purge(limit=amount+1)

@bot.slash_command(name='投票')
async def vote(ctx, title: str, option1: str, option2: str, *, details: str):
    embed = Embed(title=title, description=details, color=0x00ff00)
    embed.add_field(name="選択肢1", value=option1, inline=False)
    embed.add_field(name="選択肢2", value=option2, inline=False)
    message = await ctx.send(embed=embed)
    await message.add_reaction('1️⃣')
    await message.add_reaction('2️⃣')

    # 投票の結果を初期化
    vote_results[message.id] = {option1: 0, option2: 0}

    # メッセージIDを含むメッセージを送信
    await ctx.send(f"投票のメッセージIDは {message.id} です。")
    return

# 以下のコードは元のコードと同じです...
@bot.event
async def on_raw_reaction_add(payload):
    if payload.member == bot.user:
        return

    if payload.message_id in vote_results:
        channel = bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        if str(payload.emoji) == '1️⃣':
            vote_results[payload.message_id][message.embeds[0].fields[0].value] += 1
        elif str(payload.emoji) == '2️⃣':
            vote_results[payload.message_id][message.embeds[0].fields[1].value] += 1
            return

@bot.event
async def on_raw_reaction_remove(payload):
    if payload.member == bot.user:
        return

    if payload.message_id in vote_results:
        channel = bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        if str(payload.emoji) == '1️⃣':
            vote_results[payload.message_id][message.embeds[0].fields[0].value] -= 1
        elif str(payload.emoji) == '2️⃣':
            vote_results[payload.message_id][message.embeds[0].fields[1].value] -= 1
            return

@bot.slash_command(name='集票')
async def 集票(ctx, message_id: str):
    message_id = int(message_id)
    if message_id in vote_results:
        results = vote_results[message_id]
        await ctx.send(f"投票結果：\n{results}")
    else:
        await ctx.send("そのメッセージIDの投票は存在しません。")
    return

@bot.slash_command()
@commands.has_permissions(administrator=True)
async def create_ticket(ctx):
    guild = ctx.guild
    ticket_channel = await guild.create_text_chasnnel(name="ticket")
    await ticket_channel.set_permissions(guild.get_role(guild.id), send_messages=False, read_messages=False)
    await ticket_channel.set_permissions(ctx.author, send_messages=True, read_messages=True)

    embed = discord.Embed(
        title="新しいチケットが作成されました",
        description=f"{ctx.author.mention} さん、チケットチャンネル {ticket_channel.mention} をご確認ください。",
        color=0x00ff00
    )
    await ctx.send(embed=embed)
    return

@bot.slash_command()
@commands.has_permissions(administrator=True)
async def close_ticket(ctx, channel: discord.TextChannel):
    await channel.delete()

    embed = discord.Embed(
        title="チケットが閉じられました",
        description=f"{ctx.author.mention} さんにより、チケットチャンネル {channel.name} が閉じられました。",
        color=0xff0000
    )
    await ctx.send(embed=embed)
    return

# ﾁﾝﾁﾝ大好き！
@bot.slash_command()
async def 詳細(ctx):
    bot_message = await ctx.send("作者uuid_toxic_pikaanimal")
    await asyncio.sleep(10)
    await bot_message.delete()
    return

from collections import defaultdict
from datetime import datetime, timedelta
spam_tracker = defaultdict(list)

from collections import defaultdict
from datetime import datetime, timedelta
spam_tracker = defaultdict(list)

from discord import Embed, Color

@bot.slash_command()
@commands.has_permissions(administrator=True)
async def 認証(ctx, role: discord.Role, *, description: str):
    embed = Embed(title="認証", description=description, color=Color.blue())
    message = await ctx.send(embed=embed)
    await message.add_reaction("✅")
    bot.verify_message_id = message.id
    bot.verify_role_id = role.id

    # メッセージIDとロールIDをファイルに保存します
    with open('verify_info.json', 'w') as f:
        json.dump({'message_id': bot.verify_message_id, 'role_id': bot.verify_role_id}, f)
    print(f"Saved message ID {bot.verify_message_id} and role ID {bot.verify_role_id} to file.")
    return

@bot.event
async def on_raw_reaction_add(payload):
    if payload.message_id == bot.verify_message_id and payload.emoji.name == "✅":
        guild = bot.get_guild(payload.guild_id)
        role = discord.utils.get(guild.roles, id=bot.verify_role_id)
        if role is not None:
            user = guild.get_member(payload.user_id)
            await user.add_roles(role)
    return

@bot.event
async def on_raw_reaction_remove(payload):
    if payload.message_id == bot.verify_message_id and payload.emoji.name == "✅":
        guild = bot.get_guild(payload.guild_id)
        role = discord.utils.get(guild.roles, id=bot.verify_role_id)
        if role is not None:
            user = guild.get_member(payload.user_id)
            await user.remove_roles(role)
    return

@bot.event
async def on_ready():
    print(f"Current working directory: {os.getcwd()}")
    try:
        with open('verify_info.json', 'r') as f:
            verify_info = json.load(f)
        bot.verify_message_id = verify_info['message_id']
        bot.verify_role_id = verify_info['role_id']
        print(f"Loaded message ID {bot.verify_message_id} and role ID {bot.verify_role_id} from file.")
    except FileNotFoundError:
        print("File not found.")
    return

#end
inappropriate_words = ["ちんこ", "まんこ", "セックス", ]  # 実際の下ネタをここにリストとして追加します




# スパムと下ネタの回数を追跡する辞書
spam_tracker = defaultdict(list)
inappropriate_tracker = defaultdict(int)

# スパム検知機能、下ネタ検知機能、URL検知機能の初期状態を設定
spam_detection = {}
inappropriate_detection = {}
url_detection = {}

@bot.slash_command()
@commands.has_permissions(administrator=True)
async def 下ネタ検知(ctx, arg):
    if arg.lower() == 'no':
        inappropriate_detection[str(ctx.guild.id)] = False
        await ctx.send('下ネタ検知機能をオフにしました。')
    elif arg.lower() == 'yes':
        inappropriate_detection[str(ctx.guild.id)] = True
        await ctx.send('下ネタ検知機能をオンにしました。')
    else:
        await ctx.send('無効な引数です。yesまたはnoを指定してください。')

    # 下ネタ検知設定をファイルに保存します
    with open('inappropriate_detection.json', 'w') as f:
        json.dump(inappropriate_detection, f)
    return

@bot.slash_command()
@commands.has_permissions(administrator=True)
async def スパム検知(ctx, arg):
    if arg.lower() == 'no':
        spam_detection[str(ctx.guild.id)] = False
        await ctx.send('スパム検知機能をオフにしました。')
    elif arg.lower() == 'yes':
        spam_detection[str(ctx.guild.id)] = True
        await ctx.send('スパム検知機能をオンにしました。')
    else:
        await ctx.send('無効な引数です。yesまたはnoを指定してください。')

    # スパム検知設定をファイルに保存します
    with open('spam_detection.json', 'w') as f:
        json.dump(spam_detection, f)
    return

@bot.slash_command()
@commands.has_permissions(administrator=True)
async def url(ctx, arg):
    if arg.lower() == 'no':
        url_detection[str(ctx.guild.id)] = False
        await ctx.send('URL検知機能をオフにしました。')
    elif arg.lower() == 'yes':
        url_detection[str(ctx.guild.id)] = True
        await ctx.send('URL検知機能をオンにしました。')
    else:
        await ctx.send('無効な引数です。yesまたはnoを指定してください.')

    # URL検知設定をファイルに保存します
    with open('url_detection.json', 'w') as f:
        json.dump(url_detection, f)
    return

@bot.event
async def on_ready():
    # 設定ファイルが存在する場合、設定を読み込みます
    if os.path.isfile('spam_detection.json'):
        with open('spam_detection.json', 'r') as f:
            spam_detection.update(json.load(f))
    if os.path.isfile('inappropriate_detection.json'):
        with open('inappropriate_detection.json', 'r') as f:
            inappropriate_detection.update(json.load(f))
    if os.path.isfile('url_detection.json'):
        with open('url_detection.json', 'r') as f:
            url_detection.update(json.load(f))
    return


# ユーザーの経験値とレベルを保存する辞書
levels = {}

# Botが起動したときにlevels.jsonファイルからデータを読み込む
@bot.event
async def on_ready():
    if os.path.exists('levels.json'):
        with open('levels.json', 'r') as f:
            levels.update(json.load(f))
    bot.loop.create_task(save_levels())
    return

async def save_levels():
    while True:
        with open('levels.json', 'w') as f:
            json.dump(levels, f)
        await asyncio.sleep(60 * 5)  # 5分ごとに保存
    return

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    user_id = str(message.author.id)
    if user_id not in levels:
        levels[user_id] = {"experience": 0, "level": 1}

    levels[user_id]["experience"] += 1
    if levels[user_id]["experience"] >= levels[user_id]["level"] * 10:
        levels[user_id]["level"] += 1
        await message.channel.send(f"{message.author.mention} has leveled up to level {levels[user_id]['level']}!")

    await bot.process_slash_commands(message)
    return

@bot.slash_command()
async def level(ctx, member: discord.Member = None):
    member = member or ctx.author
    user_id = str(member.id)
    if user_id not in levels:
        await ctx.send("OOPSレベルがありません！")
    else:
        await ctx.send(f"あなたのレベルは {levels[user_id]['level']} with {levels[user_id]['experience']} experience points.")
    return

@bot.slash_command()
async def じゃんけん(ctx, user_choice: str = None):
    if user_choice not in ['グー', 'チョキ', 'パー']:
        await ctx.send("Please provide a valid choice (グー, チョキ, パー).")
        return

    bot_choice = random.choice(['グー', 'チョキ', 'パー'])

    if user_choice == bot_choice:
        result = '引き分け！'
    elif (user_choice == 'グー' and bot_choice == 'チョキ') or (user_choice == 'チョキ' and bot_choice == 'パー') or (user_choice == 'パー' and bot_choice == 'グー'):
        result = 'あなたの勝ち！'
    else:
        result = 'あなたの負け！'

    await ctx.send(f'あなた: {user_choice}, Bot: {bot_choice} - {result}')
    return

import json
import discord

from discord import File


# ボットの起動時に設定を読み込む
@bot.event
async def on_ready():
    try:
        with open('welcome_channel_id.json', 'r') as f:
            bot.welcome_channel_id = json.load(f)
    except FileNotFoundError:
        bot.welcome_channel_id = {}
    return

@bot.slash_command()
@commands.has_permissions(administrator=True)
async def ようこそ(ctx, channel_id: int):
    bot.welcome_channel_id[str(ctx.guild.id)] = channel_id

    # チャンネルIDをファイルに保存します
    with open('welcome_channel_id.json', 'w') as f:
        json.dump(bot.welcome_channel_id, f)
    await ctx.send(f"歓迎メッセージを送信するチャンネルがID {channel_id} のチャンネルに設定されました。")
    return

@bot.event
async def on_member_join(member):
    channel_id = bot.welcome_channel_id.get(str(member.guild.id))
    if channel_id:
        channel = bot.get_channel(int(channel_id))
        if channel:
            await channel.send(f"ようこそ、{member.mention}さん！", file=File('ようこそ.png'))
        else:
            print(f"Error: Could not find channel with ID {channel_id}.")
    else:
        print(f"No welcome channel set for guild {member.guild.id}.")
    return


@bot.event
async def on_ready():
    try:
        with open('welcome_channel_id.json', 'r') as f:
            bot.welcome_channel_id = json.load(f)
    except FileNotFoundError:
        bot.welcome_channel_id = {}
    # Rest of your on_ready code...
    return



@bot.slash_command()
@commands.has_permissions(manage_messages=True)
async def giveaway(ctx, mins: int, *, prize: str):
    embed = discord.Embed(title="ギブアウェイ！", description=f"{prize}", color=ctx.author.color)

    end = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=mins*60) # "mins" should be in seconds

    embed.add_field(name="終了時間:", value=f"{end} UTC")
    embed.set_footer(text=f"終了まで: {mins}分")
    my_msg = await ctx.send(embed=embed)

    await my_msg.add_reaction("🎉")

    await asyncio.sleep(mins*60)

    new_msg = await ctx.channel.fetch_message(my_msg.id)

    users = [user async for user in new_msg.reactions[0].users() if user != bot.user]

    winner = random.choice(users)

    await ctx.send(f"おめでとうございます！ {winner.mention} さんが {prize} を獲得しました！")
    return

from discord import Embed, Color

@bot.slash_command(name="warn", description="警告を行います")
@commands.has_permissions(manage_messages=True)
async def warn(ctx: commands.Context, member: discord.Member, *, reason=None):
    if reason is None:
        await ctx.send("警告の理由を指定してください。")
        return

    embed = Embed(title="警告", description=f"{member.mention} さん、以下の理由で警告します: {reason}", color=Color.red())
    await ctx.send(embed=embed)
    return

todo_list = []

@bot.slash_command()
async def todo_add(ctx, *, task):
    todo_list.append(task)
    await ctx.send(f'Task "{task}" added to the list.')
    return

@bot.slash_command()
async def todo_show(ctx):
    if not todo_list:
        await ctx.send('The list is empty.')
        return
    msg = 'ToDo List:\n' + '\n'.join(f'- {task}' for task in todo_list)
    await ctx.send(msg)
    return

@bot.slash_command()
async def todo_remove(ctx, *, task):
    if task in todo_list:
        todo_list.remove(task)
        await ctx.send(f'Task "{task}" removed from the list.')
    else:
        await ctx.send(f'Task "{task}" not found in the list.')
    return



@bot.slash_command()
async def rule(ctx, creator: discord.Member, *, rule_message):
    embed = Embed(title="ルール", description=rule_message, color=0x00ff00)
    embed.set_footer(text=f"作成者: {creator.name}")
    await ctx.send(embed=embed)
    return


import subprocess

server_process = None

def agree_to_eula():
    eula_path = "C:\\Users\\eita0\\OneDrive\\Desktop\\bot\\eula.txt"
    if os.path.exists(eula_path):
        with open(eula_path, 'r') as file:
            lines = file.readlines()

        with open(eula_path, 'w') as file:
            for line in lines:
                if line.startswith('eula='):
                    file.write('eula=true\n')
                else:
                    file.write(line)
    else:
        with open(eula_path, 'w') as file:
            file.write('eula=true\n')
    return

@bot.slash_command()
async def start_server(ctx):
    global server_process
    agree_to_eula()
    time.sleep(2)  # Wait for 2 seconds to ensure eula.txt is updated
    server_process = subprocess.Popen(["C:\\Users\\eita0\\OneDrive\\Desktop\\bot\\Start.bat"], stdin=subprocess.PIPE)
    await ctx.send("サーバーを起動しました。")
    return

@bot.slash_command()
async def stop_server(ctx):
    global server_process
    if server_process is not None:
        server_process.communicate(input=b'stop\n')
        server_process = None
        await ctx.send("サーバーをシャットダウンしました。")
    else:
        await ctx.send("サーバーは起動していません。")
    return

@bot.slash_command()
async def report(ctx, user: discord.Member, *, reason: str):
    admin = discord.utils.get(ctx.guild.members, name="uuid_toxic_pikaanimal")  # Replace with the actual admin's username
    if admin is not None:
        await admin.send(f"{ctx.author} が レポートしました！ {user} に {reason}の理由 @here")
        await ctx.send(f"{user} has been reported to the admin.")
    else:
        await ctx.send("Admin not found.")
    return



economy = {}

def load_economy():
    global economy
    if os.path.exists('economy.json'):
        with open('economy.json', 'r') as f:
            economy = json.load(f)
    else:
        economy = {}
    return

def save_economy():
    with open('economy.json', 'w') as f:
        json.dump(economy, f)

@bot.slash_command()
async def work(ctx):
    global economy
    load_economy()
    user = str(ctx.author)
    if user in economy and economy[user]['work_timer'] > time.time():
        await ctx.send("You're tired. Please wait for a while.")
        return
    economy[user] = {
        'money': economy.get(user, {}).get('money', 0) + random.randint(100, 1000),
        'work_timer': time.time() + 20*60
    }
    save_economy()
    await ctx.send(f"You worked and earned some money. Now you have {economy[user]['money']} money.")
    return

@bot.slash_command(name="moneychange")
async def moneyChange(ctx, user: discord.Member, money: int):
    global economy
    load_economy()
    user = str(user)
    if user not in economy:
        economy[user] = {'money': 0, 'work_timer': 0}
    economy[user]['money'] = money
    save_economy()
    await ctx.send(f"{user}'s money has been set to {money}.")
    return

@bot.slash_command()
async def money(ctx):
    global economy
    load_economy()
    user = str(ctx.author)
    if user not in economy:
        await ctx.send("You have no money.")
    else:
        await ctx.send(f"You have {economy[user]['money']} money.")
        await ctx.message.delete()
    return

@bot.slash_command()
async def trade(ctx, user: discord.Member, money: int):
    global economy
    load_economy()
    sender = str(ctx.author)
    receiver = str(user)
    if sender not in economy or economy[sender]['money'] < money:
        await ctx.send("You don't have enough money to trade.")
        return
    if receiver not in economy:
        economy[receiver] = {'money': 0, 'work_timer': 0}
    economy[sender]['money'] -= money
    economy[receiver]['money'] += money
    save_economy()
    await ctx.send(f"You traded {money} money to {receiver}.")
    await ctx.message.delete()
    return

from discord.utils import get

role_shop = {}
role_emojis = ["🍎", "🍊", "🍇"]  # Add more if needed

def load_role_shop():
    global role_shop
    if os.path.exists('role_shop.json'):
        with open('role_shop.json', 'r') as f:
            role_shop = json.load(f)
    else:
        role_shop = {}
    return

def save_role_shop():
    with open('role_shop.json', 'w') as f:
        json.dump(role_shop, f)
    return

@bot.slash_command()
@commands.has_permissions(administrator=True)
async def tradepanelrole(ctx, cost: int, role: discord.Role):
    global role_shop
    load_role_shop()
    role_shop[str(role.id)] = {'cost': cost, 'emoji': role_emojis[len(role_shop) % len(role_emojis)]}
    save_role_shop()
    await ctx.send(f"The {role.name} role is now available for purchase for {cost} money.")
    await ctx.message.delete()
    return

@bot.slash_command()
async def shop(ctx):
    global role_shop
    embed = discord.Embed(title="Role Shop", description="React to buy a role!", color=0x00ff00)
    for role_id, role_info in role_shop.items():
        role = get(ctx.guild.roles, id=int(role_id))
        if role:
            embed.add_field(name=f"{role_info['emoji']} {role.name}", value=f"Cost: {role_info['cost']}", inline=False)
    message = await ctx.send(embed=embed)
    for role_info in role_shop.values():
        await message.add_reaction(role_info['emoji'])
    await ctx.message.delete()
    return

@bot.event
async def on_reaction_add(reaction, user):
    global economy, role_shop
    if user == bot.user:
        return
    for role_id, role_info in role_shop.items():
        if reaction.emoji == role_info['emoji']:
            await reaction.message.remove_reaction(role_info['emoji'], user)
            role = get(reaction.message.guild.roles, id=int(role_id))
            if role:
                await buyrole(user, role, role_info['cost'])
    return

async def buyrole(user, role, cost):
    global economy, role_shop
    load_economy()
    user_str = str(user)
    if user_str not in economy or economy[user_str]['money'] < cost:
        await user.interaction.response.send_message("おっと、、、お金が足りません。")
        return
    economy[user_str]['money'] -= cost
    save_economy()
    await user.add_roles(role)
    await user.interaction.response.send_message(f"You bought the {role.name} role for {cost} money.")
    return


bot = commands.Bot(command_prefix='!')

@bot.command()
async def play(ctx, url : str):
    # ユーザーが接続しているボイスチャンネルを取得
    channel = ctx.message.author.voice.channel
    voice_channel = await channel.connect()

    # YouTubeの動画をダウンロードし、音声を抽出
    ydl_opts = {'format': 'bestaudio'}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        url2 = info['formats'][0]['url']
        voice_channel.play(discord.FFmpegPCMAudio(url2))

bot.run('TOKEN')
