from dotenv import load_dotenv
import discord
from discord.ext import commands
from os import getenv
from user import User
from book import Book
from user_book import User_Book, User_Book_Status
import requests
import db

load_dotenv()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='$',intents=intents)

@bot.command(name='reading', help='Ask the bot what a user is currently reading')
async def reading(ctx, user=""):
    author = ""
    if not user:
        user = ctx.message.author
        
    reader = User(user)
    titles = reader.getUserReadingTitles()
    if not titles:
        await ctx.send(f'{reader.formatted_name} isn\'t reading any books at the moment.')
    else:
        # Use a numbered list 
        await ctx.send(f'{reader.formatted_name} is reading {", ".join(titles)}')
    
@bot.command(name='set', help='Update the reading status of a book in your reading/read list')
async def setBookStatus(ctx, title, status):
    r = requests.get(url = f'https://www.googleapis.com/books/v1/volumes?q={title}')
 
    # extracting data in json format
    data = r.json()
    #print(data['items'][0])
    result = data['items'][0]['volumeInfo']
    book = Book(result["title"], result["pageCount"], result["authors"][0], result["publishedDate"][0:4], result["publisher"], api_id=data['items'][0]['id'])
    user = User(name=ctx.message.author)
    
    formatted_status = status.lower().strip()
    if formatted_status == User_Book_Status.WANT_TO_READ.value or formatted_status == User_Book_Status.READING.value or formatted_status == User_Book_Status.READ.value:
        user_book=User_Book(user_id=user.id, book_id=book.id)
        user_book.update(formatted_status)
        await ctx.send(f'Set \"{book.title}\" to {formatted_status.upper()} for {user.formatted_name}')
    else:
        await ctx.send(f'{formatted_status} is not a valid status. Please enter either "want to read", "reading", or "read".')
    
    
    return None

@bot.command(name='pages', help='Ask the bot how many pages you\'ve read in total')
async def pages(ctx):
    # TODO: Write this function
    return None

@bot.command(name='search')
async def search(ctx, name):
    reader = User(ctx.message.author)
    # sending get request and saving the response as response object
    r = requests.get(url = f'https://www.googleapis.com/books/v1/volumes?q={name}')
 
    # extracting data in json format
    data = r.json()
    #print(data['items'][0])
    result = data['items'][0]['volumeInfo']
    book = Book(result["title"], result["pageCount"], result["authors"][0], result["publishedDate"][0:4], result["publisher"], api_id=data['items'][0]['id'])
    message = f'{book}\n\n{result["description"]}'[:2000]
    if len(f'{book}\n\n{result["description"]}') > 2000:
        message = f'{book}\n\n{result["description"]}'[:1997] + '...'
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
    db.init_db()
    token = getenv('DISCORD_TOKEN')
    if token:
        bot.run(token=token)
    