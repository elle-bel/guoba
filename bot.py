# bot.py
import os
import random
import discord
from discord.ext import commands
from discord.ext.commands import MissingPermissions
from dotenv import load_dotenv


# configuration
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='g!', help_command=None)

# ///////
# bot events


@bot.event  # lets terminal know bot is online
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    await bot.change_presence(activity=discord.Game(name="Use g!help"))


@bot.event  # responds to "guoba" in any text with random message
async def on_message(message):
    if message.author.bot:
        return
    elif "g!" in message.content.lower():
        await bot.process_commands(message)
        return
    elif "guoba" in message.content.lower():
        guoba_options = [
            "GUOBAAAAA!!!!",
            "**guoba**",
            "i believe in guoba supremacy",
            "guoba! guoba! guoba!",
            "hello :D",
            "hello :smirk:",
        ]
        response = random.choice(guoba_options)
        await message.channel.send(response)
    await bot.process_commands(message)


# ///////

# g!help commands


@bot.group(name='help', invoke_without_command=True)  # Parent command
async def help(ctx):
    embed = discord.Embed(title="List of all Guoba Bot commands",
                          description="Type `help <command>` for more info on each command", color=0xF9AD39)
    fields = [
        ("Commands", "- `picture`: Sends a random picture"
                     "\n- `phrase`: Sends a random phrase"
                     "\n- `panic`: Use when in voice channel panic (removes a user)"
                     "\n- `genshin-team`: Randomizes a Genshin Impact Team", False),
        ("Features", "- Whenever you say guoba, Guoba will get super excited and respond in kind!", False)
    ]
    for name, value, inline in fields:
        embed.add_field(name=name, value=value, inline=inline)
    await ctx.send(embed=embed)
    embed.set_footer(text="ping @erooo#8904 for suggestions and maintenance!")


@help.command(name='picture')
async def picture_help(ctx):
    embed = discord.Embed(title="The `picture` command", description="Sends a random picture, or adding a parameter "
                                                                     "sends a random picture from a specific category",
                          color=0xF9AD39)
    fields = [
        ("Parameters: `picture <parameter>`", "- `floyd`: Sends a random floyd picture"
                                             "\n- `genshin`: Sends a random genshin picture"
                                             "\n- `guoba`: Sends a random guoba picture"
                                             "\n- `idv`: Sends a random idv picture"
                                             "\n- `misc`: Sends a random miscellaneous picture", False),
        ("Details:", "Message @erooo#8904 to add to the photo library. Possible automation for this to come!", False),
        ("Credit", "Type `picture credit` for more information", False)
    ]
    for name, value, inline in fields:
        embed.add_field(name=name, value=value, inline=inline)
    await ctx.send(embed=embed)


@help.command(name='phrase')
async def phrase_help(ctx):
    embed = discord.Embed(title="The `phrase` command", description="Sends a random phrase, or adding a parameter "
                                                                     "sends a random phrase from a specific category",
                          color=0xF9AD39)
    fields = [
        ("Parameters: `phrase <parameter>`", "- `floyd`: Sends a random floyd phrase"
                                             "\n- `zhongli`: Sends a random zhongli phrase"
                                             "\n- `guoba`: Sends a random guoba phrase", False)
    ]
    for name, value, inline in fields:
        embed.add_field(name=name, value=value, inline=inline)
    await ctx.send(embed=embed)


@help.command(name='panic')
async def panic_help(ctx):
    embed = discord.Embed(title="The `panic` command", description="Removes a single user from voice call with "
                                                                   "`panic <@user>`. Requires permissions "
                                                                   "to move members", color=0xF9AD39)
    await ctx.send(embed=embed)


@help.command(name='genshin-team')
async def genshin_help(ctx):
    embed = discord.Embed(title="The `genshin-team` command", description="Gives a random Genshin "
                                                                          "Impact Team", color=0xF9AD39)
    fields = [
        ("Parameters: `genshin-team <parameter>`", "- Any name saved within the Guoba bot", False),
        ("Details:", "- Call `g!genshin-names` to see which names are saved and can be used as parameters"
                     "\n- Message @erooo#8904 with your desired name and usable characters to be added to the list",
         False)
    ]
    for name, value, inline in fields:
        embed.add_field(name=name, value=value, inline=inline)
    await ctx.send(embed=embed)


# ///////
# guoba functions


def picture_credit(title):  # Function returns string for picture()
    title = title[:-4]
    credit = ""
    if "-" in title:
        credit_lst = title.split("-", 1)
        credit = credit_lst[0] + " | " + credit_lst[1]
    else:
        credit_lst = title.split("_")
        length = len(credit_lst)
        for words in credit_lst:
            if words == credit_lst[length - 1]:
                credit = credit + words
            else:
                credit = credit + words + " "
    return credit


@bot.group(name='picture', invoke_without_command=True, help='sends a picture')  # picture function parent command
async def picture(ctx):
    chosen_filepath = random.choice(os.listdir("images"))
    chosen_image = random.choice(os.listdir("images/" + chosen_filepath))
    file = discord.File("images/" + chosen_filepath + "/" + chosen_image, filename=chosen_image)
    embed = discord.Embed(color=0xF9AD39)
    embed.set_image(url="attachment://" + chosen_image)
    img_credit = picture_credit(str(chosen_image))
    embed.set_footer(text=img_credit)

    await ctx.send(file=file, embed=embed)


@picture.command(name="credit", help='details on picture credit')  # help command for the credit of picture()
async def credit_help(ctx):
    embed = discord.Embed(title="Guoba Giving Credit", description="Credit is included for all artworks, fanart or "
                                                                   "original",
                          color=0xF9AD39)
    fields = [
        ("Credit Details", "- If a string of numbers follows a username, the source is from Twitter.com. "
                           "You can copy `/user/status/number` into Twitter to see the original post"
                           "\n- If there is only a string of numbers, the art is from pixiv.com. You can copy "
                           "`/users/number` into pixiv to see the original post"
                           "\n- If the credit is a proper noun, it is original artwork", False),
        ("Credit Feedback", "- Please message @erooo#8904 if the source has changed their name/is wrong"
                            "\n- If you are submitting a photo you must include credit", False)
    ]
    for name, value, inline in fields:
        embed.add_field(name=name, value=value, inline=inline)
    await ctx.send(embed=embed)


@picture.command(name='genshin', help='sends a genshin photo')
async def genshin_picture(ctx):
    chosen_image = random.choice(os.listdir("images/genshin/"))
    file = discord.File("images/genshin/" + chosen_image, filename=chosen_image)
    embed = discord.Embed(color=0xF9AD39)
    embed.set_image(url="attachment://" + chosen_image)
    img_credit = picture_credit(str(chosen_image))
    embed.set_footer(text=img_credit)

    await ctx.send(file=file, embed=embed)


@picture.command(name='floyd', help='sends a floyd photo')
async def floyd_picture(ctx):
    chosen_image = random.choice(os.listdir("images/floyd/"))
    file = discord.File("images/floyd/" + chosen_image, filename=chosen_image)
    embed = discord.Embed(color=0xF9AD39)
    embed.set_image(url="attachment://" + chosen_image)
    img_credit = picture_credit(str(chosen_image))
    embed.set_footer(text=img_credit)

    await ctx.send(file=file, embed=embed)


@picture.command(name='guoba', help='sends a guoba photo')
async def guoba_picture(ctx):
    chosen_image = random.choice(os.listdir("images/guoba/"))
    file = discord.File("images/guoba/" + chosen_image, filename=chosen_image)
    embed = discord.Embed(color=0xF9AD39)
    embed.set_image(url="attachment://" + chosen_image)
    img_credit = picture_credit(str(chosen_image))
    embed.set_footer(text=img_credit)

    await ctx.send(file=file, embed=embed)


@picture.command(name='idv', help='sends an idv photo')
async def idv_picture(ctx):
    chosen_image = random.choice(os.listdir("images/idv/"))
    file = discord.File("images/idv/" + chosen_image, filename=chosen_image)
    embed = discord.Embed(color=0xF9AD39)
    embed.set_image(url="attachment://" + chosen_image)
    img_credit = picture_credit(str(chosen_image))
    embed.set_footer(text=img_credit)

    await ctx.send(file=file, embed=embed)


@picture.command(name='misc', help='sends a miscellaneous photo')
async def misc_picture(ctx):
    chosen_image = random.choice(os.listdir("images/misc/"))
    file = discord.File("images/misc/" + chosen_image, filename=chosen_image)
    embed = discord.Embed(color=0xF9AD39)
    embed.set_image(url="attachment://" + chosen_image)
    img_credit = picture_credit(str(chosen_image))
    embed.set_footer(text=img_credit)

    await ctx.send(file=file, embed=embed)


@bot.command(name='panic', pass_context=True, help='use when in voice channel panic')  # removes single user from a vc
@commands.has_guild_permissions(move_members=True)
async def panic(ctx, member: discord.Member):
    await member.move_to(None)


@panic.error  # panic() error command
async def panic_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send("You do not have the permisssions to use this command")


@bot.group(name='phrase', invoke_without_command=True, help='displays a random phrase.')  # phrase() parent command
async def phrase(ctx):
    thirst2 = [
        'zhongli ass so phat',
        'zhongli archon skin WHEN bih',
        'GUOBA.....bot?',
        'GUOBAPOT GUOBAPOT GUOBAPOT',
        'floyd is hot ur all just cowards',
        'me when floyd: :weary:'
    ]

    response = random.choice(thirst2)
    await ctx.send(response)


@phrase.command(name='zhongli', help='sends a phrase about zhongli')
async def zhongli_phrase(ctx):
    thirst2 = [
        'zhongli ass so phat',
        'zhongli archon skin WHEN bih'
    ]

    response = random.choice(thirst2)
    await ctx.send(response)


@phrase.command(name='guoba', help='sends a phrase about guoba')
async def guoba_phrase(ctx):
    thirst2 = [
        'GUOBA.....bot?',
        'GUOBAPOT GUOBAPOT GUOBAPOT'
    ]

    response = random.choice(thirst2)
    await ctx.send(response)


@phrase.command(name='floyd', help='sends a phrase about floyd')
async def floyd_phrase(ctx):
    thirst2 = [
        'floyd is hot ur all just cowards',
        'me when floyd: :weary:'
    ]

    response = random.choice(thirst2)
    await ctx.send(response)



bot.run(TOKEN)
