import discord
from discord.ext import commands

from dotenv import load_dotenv
from os import getenv

import requests

from database import util as database
from utils import utils

from models import user as u
from models import book as b
from models import user_book as ub

load_dotenv()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='$',intents=intents)

@bot.command(name='reading', help='Ask the bot what a user is currently reading')
async def reading(ctx, username=""):
    """
    The `reading` function retrieves the current reading titles of a user and sends a message indicating
    the books they are currently reading.
    
    :param ctx: The `ctx` parameter is an object that represents the context of the command being
    executed. It contains information about the message, the author, the server, and other relevant
    details
    :param username: The `username` parameter is an optional parameter that represents the username of
    the user whose reading list we want to retrieve. If no `username` is provided, it defaults to the
    author of the message (`ctx.message.author`)
    """
    if not username:
        username = ctx.message.author
        
    reader, _ = u.createOrGetUser(username)
    
    titles = ub.getCurrentReadingTitles(reader)
    if not titles:
        await ctx.send(f'{reader.formatted_name} isn\'t reading any books at the moment.')
    else:
        await ctx.send(f'{reader.formatted_name} is reading:\n{utils.numberedStrIterable(titles)}')
    
@bot.command(name='set', help='Update the reading status of a book in your reading/read list')
async def setBookStatus(ctx, title, status):
    """
    The function `setBookStatus` retrieves book information from the Google Books API, creates or
    retrieves a book and user in the database, and updates the status of the user's book.
    
    :param ctx: The `ctx` parameter is the context object, which contains information about the current
    invocation of the command. It includes attributes such as the message that triggered the command,
    the channel it was sent in, the author of the message, etc
    :param title: The `title` parameter is the title of the book that you want to set the status for
    :param status: The `status` parameter in the `setBookStatus` function is used to specify the status
    of a book for a user. It can have one of the following values: `want to read`, `reading`, `read`
    """
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

@bot.command(name='pages', help='Ask the bot how many pages you\'ve read in total')
async def pages(ctx, username=""):
    """
    The `pages` function retrieves the number of pages read by a user and sends a message with the
    user's formatted name and the number of pages read.
    
    :param ctx: The `ctx` parameter is an object that represents the context of the command being
    executed. It contains information about the message, the channel, the server, and the user who
    triggered the command
    :param username: The `username` parameter is an optional parameter that allows you to specify a
    specific username. If no username is provided, it defaults to the author of the message
    (`ctx.message.author`)
    """
    if not username:
        username = ctx.message.author
    user, _ = u.createOrGetUser(username)
    await ctx.send(f'{user.formatted_name} has read {ub.getPagesRead(user)} pages')

@bot.command(name='search')
async def search(ctx, name):
    """
    The `search` function takes a name as input, makes a request to the Google Books API to search for
    books with that name, retrieves the information of the first book in the search results, creates or
    gets a book object using that information, and sends a message with the book details and description
    (limited to 2000 characters) to the specified context.
    
    :param ctx: ctx is the context object, which contains information about the current state of the bot
    and the message that triggered the command. It includes attributes such as the message content, the
    channel the message was sent in, the author of the message, etc
    :param name: The `name` parameter is the name of the book that you want to search for. It is used to
    make a request to the Google Books API to retrieve information about the book
    """
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
    