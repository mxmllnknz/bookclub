from dotenv import load_dotenv
import discord
from discord.ext import commands
from os import getenv
import sqlite3
from user import User

load_dotenv()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='$',intents=intents)

# TODO: Replace this with persistant storage
users = [
    {
        'name': 'maxthebadger',
        'reading_list': [
            {
                'title': 'Across the Universe',
                'author': 'Jim Henderson',
                'year' : '1960',
                'num_pages': '543'
            },
            {
                'title': 'Across the Foundation',
                'author': 'Isaac Asimov',
                'year' : '1956',
                'num_pages': '324'
            }
        ],
        'read_list': [],
    },
    {
        'name': 'bookclub',
        'reading_list': [],
        'read_list': [],
    }
]

@bot.command(name='reading', help='Ask the bot what you\'re currently reading')
async def reading(ctx, user=""):
    author = ""
    if not user:
        author = str(ctx.message.author).split('#')[0]
    else:
        author = user
        
    reader = getUserByName(author)

    await ctx.send(f'{author} is reading {reader["reading_list"]}')
    
@bot.command(name='finished', help='Tell the bot you\'ve finished reading a book')
async def finished(ctx, title):
    message = ""
    if not title:
        message = 'You must provide a title matching one of your current reading titles'
    else:
        # TODO: Print list of finished titles
        # TODO: Paginate responses
        return None

@bot.command(name='pages', help='Ask the bot how many pages you\'ve read in total')
async def pages(ctx):
    # TODO: Write this function
    return None

@bot.command(name='ping', help='Pings the bot server to check status')
async def ping(ctx):
    """
    This is an asynchronous Python function that sends a message "I'm alive!". It is used as a debugging
    tool to check the status of the bot.
    
    :param ctx: ctx stands for "context" and is a parameter commonly used in Discord.py commands. It
    represents the context in which the command was invoked, including information such as the message,
    the channel, the author, and the server. In this specific code snippet, ctx is used to send a
    message back to
    """
    await ctx.send("I'm alive!")
    
def getUserByName(name: str) -> User:
    for user in users:
        if user['name'] == name:
            return user
    return None
   
if __name__ == "__main__":
    conn = sqlite3.connect('club.db')
    #TODO: Get this database working
    
    bot.run(getenv('DISCORD_TOKEN'))
    