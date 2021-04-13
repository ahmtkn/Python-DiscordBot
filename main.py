import discord
from utils import *
from functions import *
from discord.ext import commands
import safygiphy
import youtube_dl
import os
import random


intents = discord.Intents(messages=True, guilds=True, reactions=True, members=True, presences=True)
Bot = commands.Bot(command_prefix='!')
game = Game()


@Bot.event
async def on_ready():
    await Bot.change_presence(activity=discord.Game(name="Buraya oyun yazılır"))
    print('Ben Hazırım!')


@Bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name="hos-geldiniz")
    await channel.send(f"{member.mention} aramıza katıldı.Hoş geldin!")
    print(f"{member} aramıza katıldı.Hoş geldi!")


@Bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name="gidenler")
    await channel.send(f"{member.mention} Giiitmeee Kaaaall :(")
    print(f"{member} aramızdan ayrıldı :(")


@Bot.command()
async def gurkan(ctx):
    await ctx.send('My Best')


@Bot.command()
async def oyun(ctx):
    await ctx.send(game.roll_dice())


@Bot.command()
@commands.has_role("admin")
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)


@Bot.command(aliases=["copy"])
async def clone_channel(ctx, amount=1):
    for i in range(amount):
        await ctx.channel.clone()


@Bot.command()
@commands.has_role("admin")
async def kick(ctx, member: discord.Member, *, reason="Yok"):
    await member.kick(reason=reason)


@Bot.command()
@commands.has_role("admin")
async def ban(ctx, member: discord.Member, *, reason="Yok"):
    await member.ban(reason=reason)


@Bot.command()
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')
    for bans in banned_users:
        user = bans.user
        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned user{user.mention}')
            return


@Bot.command()
async def gif(ctx, gif: str):
    g = safygiphy.Giphy()
    rgif = g.random(tag=gif)
    embed = discord.Embed(color=0x00ff00)
    embed.set_image(url=str(rgif.get("data", {}).get('image_original_url')))
    await ctx.send(embed=embed)




player1 = ""
player2 = ""
turn = ""
gameOver = True

board = []

winningConditions = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]

@Bot.command()
async def tictactoe(ctx, p1: discord.Member, p2: discord.Member):
    global count
    global player1
    global player2
    global turn
    global gameOver

    if gameOver:
        global board
        board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:"]
        turn = ""
        gameOver = False
        count = 0

        player1 = p1
        player2 = p2

        # print the board
        line = ""
        for x in range(len(board)):
            if x == 2 or x == 5 or x == 8:
                line += " " + board[x]
                await ctx.send(line)
                line = ""
            else:
                line += " " + board[x]

        # determine who goes first
        num = random.randint(1, 2)
        if num == 1:
            turn = player1
            await ctx.send("It is <@" + str(player1.id) + ">'s turn.")
        elif num == 2:
            turn = player2
            await ctx.send("It is <@" + str(player2.id) + ">'s turn.")
    else:
        await ctx.send("Bir oyun zaten devam ediyor! Yenisine başlamadan önce oyunu bitirin.")

@Bot.command()
async def place(ctx, pos: int):
    global turn
    global player1
    global player2
    global board
    global count
    global gameOver

    if not gameOver:
        mark = ""
        if turn == ctx.author:
            if turn == player1:
                mark = ":regional_indicator_x:"
            elif turn == player2:
                mark = ":o2:"
            if 0 < pos < 10 and board[pos - 1] == ":white_large_square:" :
                board[pos - 1] = mark
                count += 1

                # print the board
                line = ""
                for x in range(len(board)):
                    if x == 2 or x == 5 or x == 8:
                        line += " " + board[x]
                        await ctx.send(line)
                        line = ""
                    else:
                        line += " " + board[x]

                checkWinner(winningConditions, mark)
                print(count)
                if gameOver == True:
                    await ctx.send(mark + " wins!")
                elif count >= 9:
                    gameOver = True
                    await ctx.send("It's a tie!")

                # switch turns
                if turn == player1:
                    turn = player2
                elif turn == player2:
                    turn = player1
            else:
                await ctx.send("1 ile 9 (dahil) arasında bir tam sayı ve işaretlenmemiş bir döşeme seçtiğinizden emin olun.")
        else:
            await ctx.send("Senin sıran değil.")
    else:
        await ctx.send("Lütfen !tictactoe komutunu kullanarak yeni bir oyuna başlayın.")


def checkWinner(winningConditions, mark):
    global gameOver
    for condition in winningConditions:
        if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
            gameOver = True

@tictactoe.error
async def tictactoe_error(ctx, error):
    print(error)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please mention 2 players for this command.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure to mention/ping players (ie. <@688534433879556134>).")

@place.error
async def place_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please enter a position you would like to mark.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure to enter an integer.")


Bot.run(TOKEN)
