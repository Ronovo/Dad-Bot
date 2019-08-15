import discord
from discord.ext import commands

class common:
	def __init__(self, client):
		self.client = client
		
	#Test Ping Command. Simplest Command in the bot
	@commands.command()
	async def ping(self):
		await self.client.say('Pong!')

	#Presonalized Hello Command.
	#Added because of Cap'n Nova
	@client.command(pass_context=True)
	async def hi(ctx):
		author = ctx.message.author
		msg = 'Howdy, {}, my favorite son!'.format(author)
		await client.say(msg)
	
	#First hello command
	@client.command()
	async def hello():
		await client.say('Hello, son')

	#Dad Joke pulled from Dad Joke API
	@client.command()
	async def joke():
		r = requests.get('https://icanhazdadjoke.com', headers={"Accept":"application/json"})
		joke = r.json();
		msg = joke['joke']
		await client.say(msg)

	#Calls from the proud object at the top
	@client.command()
	async def prouddad():
		x = random.randint(0,3)
		msg = proud[x]
		await client.say(msg)