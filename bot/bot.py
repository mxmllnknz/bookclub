from dotenv import load_dotenv
import discord
from discord.ext import commands
from os import getenv

import requests
from database import util as database

from models import user as u
from models import book as b
from models import user_book as ub

load_dotenv()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='$',intents=intents)

@bot.command(name='reading', help='Ask the bot what a user is currently reading')
async def reading(ctx, username=""):
    if not username:
        username = ctx.message.author
        
    reader, _ = u.createOrGetUser(username)
    
    titles = ub.getCurrentReadingTitles(reader)
    if not titles:
        await ctx.send(f'{reader.formatted_name} isn\'t reading any books at the moment.')
    else:
        # TODO: Use a numbered list 
        await ctx.send(f'{reader.formatted_name} is reading {", ".join(titles)}')
    
@bot.command(name='set', help='Update the reading status of a book in your reading/read list')
async def setBookStatus(ctx, title, status):
    r = requests.get(url = f'https://www.googleapis.com/books/v1/volumes?q={title}')
 
    data = r.json()
    result = data['items'][0]['volumeInfo']
    book, _ = b.createOrGetBook(title=result["title"], num_pages=result["pageCount"], author=result["authors"][0], year=result["publishedDate"][0:4], publisher=result["publisher"], api_id=data['items'][0]['id'])
    user, _ = u.createOrGetUser(name=ctx.message.author)
    
    formatted_status = status.lower().strip()
    if formatted_status == ub.User_Book_Status.WANT_TO_READ.value or formatted_status == ub.User_Book_Status.READING.value or formatted_status == ub.User_Book_Status.READ.value:
        ub.createOrGetUserBook(user=user, book=book)
        ub.User_Book.update(status=formatted_status).where((ub.User_Book.user == user) and (ub.User_Book.book == book)).execute()
        await ctx.send(f'Set \"{book.title}\" to {formatted_status.upper()} for {user.formatted_name}')
    else:
        await ctx.send(f'{formatted_status} is not a valid status. Please enter either "want to read", "reading", or "read".')
    
    
    return None

@bot.command(name='pages', help='Ask the bot how many pages you\'ve read in total')
async def pages(ctx, username=""):
    if not username:
        username = ctx.message.author
    user, _ = u.createOrGetUser(username)
    return ub.getPagesRead(user)

@bot.command(name='search')
async def search(ctx, name):
    r = requests.get(url = f'https://www.googleapis.com/books/v1/volumes?q={name}')
 
    data = r.json()
    result = data['items'][0]['volumeInfo']
    book, _ = b.createOrGetBook(title=result["title"], num_pages=result["pageCount"], author=result["authors"][0], year=result["publishedDate"][0:4], publisher=result["publisher"], api_id=data['items'][0]['id'])
    message = f'{repr(book)}\n\n{result["description"]}'[:2000]
    if len(f'{repr(book)}\n\n{result["description"]}') > 2000:
        message = f'{repr(book)}\n\n{result["description"]}'[:1997] + '...'
    await ctx.send(message)

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
   
if __name__ == "__main__":
    token = getenv('DISCORD_TOKEN')
    db = database.get_db()
    if token:
        bot.run(token=token)
    