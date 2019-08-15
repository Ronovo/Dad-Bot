# Dad
import discord
import requests
import json
import random
from discord.ext import commands
import asyncio
from itertools import cycle

#---------------------------------------------------------------
#Object initialization
#--------------------------------------------------------------
players = {}
queues = {}
#Status that are cycled through
status = ['Hi you, I\'m Dad','~help for commands']

#List for ProudDad
proud = ['Thats My Boy!',
		'Atta Boy!',
		'I am glad to call you my Son.',
		'Oi, that there be my Boy!']
		
TOKEN = ''

client = discord.Client()
client = commands.Bot(command_prefix = '~')
client.remove_command('help')

extensions = ['common','onJoin']
#---------------------------------------------------------------
#Cog Setup
#--------------------------------------------------------------
'''
if __name__ == '__main__':
	for extension in extensions:
		try:
			client.load_extension(extension)
		except Exception as error:
			print('{} cannot be loaded.. [{}]'.format(extension, error)
'''
			
'''
@client.command()
async def load(extension):
	try:
		client.load_extension(extension)
		print('{} was loaded.'.format(extension)
	except Exception as error:
		print('{} cannot be loaded. [{}]'.format(extension, error)
		
@client.command()
async def unload(extension):
	try:
		client.unload_extension(extension)
		print('{} was unloaded.'.format(extension)
	except Exception as error:
		print('{} cannot be unloaded. [{}]'.format(extension, error)
'''
#---------------------------------------------------------------
#Helper Methods
#--------------------------------------------------------------
def check_queue(id):
	if queues[id] != []:
		player = queues[id].pop(0)
		players[id] = player
		player.start()

#---------------------------------------------------------------
#Background Tasks
#--------------------------------------------------------------	
#Cyles through every x minutes and changes the bot status
#Current x = 30
async def change_status():
	await client.wait_until_ready()
	msgs = cycle(status)

	while not client.is_closed:
		current_status = next(msgs)
		minutes = 30
		await client.change_presence(game=discord.Game(name=current_status))
		await asyncio.sleep(60 * minutes)

#---------------------------------------------------------------
#Bot Start
#--------------------------------------------------------------			
#Logs Ready and sets Status at start
@client.event
async def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('------')
	await client.change_presence(game=discord.Game(name='Hi you, I\'m Dad'))

#---------------------------------------------------------------
#On_Member_Join 
#--------------------------------------------------------------	
#Auto Assignes Role to new members
#Adds them to json for leveling up
@client.event
async def on_member_join(member):
	role = discord.utils.get(member.server.roles, name="Tater ToTs")
	await client.add_roles(member, role)
	#channel = discord.utils.get(member.server.getChannel('423653908552876043')
	#await client.send_message(channel, 'Hi {}, I\'m Dad!'.format(member.name))
	with open('users.json', 'r') as f:
		users = json.load(f)
		
	await update_data(users, member)
	
	with open('users.json', 'w') as f:
		json.dump(users,f)

#---------------------------------------------------------------
#Level System Code
#--------------------------------------------------------------	

@client.event	
async def on_message(message):
	with open('users.json', 'r') as f:
		users = json.load(f)
		
	await update_data(users, message.author)
	await add_experience(users, message.author, 1)
	await level_up(users, message.author, message.channel)
	
	with open('users.json', 'w') as f:
		json.dump(users,f)
	await client.process_commands(message)
	
async def update_data(users, user):
	if not user.id in users:
		users[user.id] = {}
		users[user.id]['experience'] = 0
		users[user.id]['level'] = 1
	
async def add_experience(users, user, exp):
	users[user.id]['experience'] += exp

async def level_up(users,user,channel):
	experience = users[user.id]['experience']
	lvl_start = users[user.id]['level']
	lvl_tater = 250
	lvl_baby = 1000
	
	if experience > lvl_tater and lvl_start == 1:
		users[user.id]['level'] = 2
		users[user.id]['experience'] = 0
		await client.send_message(channel, '{} has become a Buff Baby!'.format(user.mention))
		role = discord.utils.get(user.server.roles, name="Buff Babies")
		await client.add_roles(user, role)
		
	if experience > lvl_tater and lvl_start == 2:
		users[user.id]['level'] = 3
		users[user.id]['experience'] = 0
		await client.send_message(channel, '{} has become a Teammate! Welcome to the team!'.format(user.mention))

#---------------------------------------------------------------
#Reaction Logging for voting
#Really Spammy in current form
#--------------------------------------------------------------	

@client.event
async def on_reaction_add(reaction, user):
	channel = reaction.message.channel
	with open('users.json', 'r') as f:
		users = json.load(f)
		
	await update_data(users, message.author)
	await add_experience(users, message.author, 1)
	await level_up(users, message.author, message.channel)
	
	with open('users.json', 'w') as f:
		json.dump(users,f)
	await client.process_commands(message)
'''	
@client.event
async def on_reaction_remove(reaction, user):
	channel = reaction.message.channel
	print(channel)
	await client.send_message(channel,'{} has removed {} to the message: {}'.format(user.name, reaction.emoji, reaction.message.content))
'''

#---------------------------------------------------------------
#Original Dad Bot Commands
#--------------------------------------------------------------	

#Test Ping Command. Simplest Command in the bot
@client.command()
async def ping():
	await client.say('Pong!')

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

#---------------------------------------------------------------
#FOAAS(Fuck Off As A Service) Commands
#--------------------------------------------------------------
#Says goodbye to me	
@client.command(pass_context=True)
async def byeme(ctx):
	r = requests.get('https://foaas.com/bye/from', headers={"Accept":"application/json"})
	fuck = r.json();
	msg = fuck['message']
	author = ctx.message.author
	msg = msg + ', {}'.format(author)
	msg = msg[:-5]
	await client.say(msg)

#Says bye to whoever you pass in
@client.command(pass_context=True)
async def bye(ctx,args):
	r = requests.get('https://foaas.com/bye/from', headers={"Accept":"application/json"})
	fuck = r.json();
	msg = fuck['message']
	author = ctx.message.author
	msg = msg + ', {}'.format(args)
	await client.say(msg)

@client.command(pass_context=True)
async def horse(ctx):
	r = requests.get('https://foaas.com/horse/from', headers={"Accept":"application/json"})
	fuck = r.json();
	msg = fuck['message']
	await client.say(msg)

@client.command(pass_context=True)
async def fascinating(ctx):
	r = requests.get('https://foaas.com/fascinating/from', headers={"Accept":"application/json"})
	fuck = r.json();
	msg = fuck['message']
	await client.say(msg)
	
#---------------------------------------------------------------
#Chuck Norris Quote Commands
#--------------------------------------------------------------
@client.command(pass_context=True)
async def chuck(ctx):
	r = requests.get('https://api.chucknorris.io/jokes/random', headers={"Accept":"application/json"})
	fuck = r.json();
	msg = fuck['value']
	await client.say(msg)

@client.command(pass_context=True)
async def chuckEmbed(ctx):
	r = requests.get('https://api.chucknorris.io/jokes/random', headers={"Accept":"application/json"})
	fuck = r.json();
	msg = fuck['value']
	
	embed = discord.Embed(
		title = 'TEAM OF TEAMS',
		description = 'Now Sponsered by 7-UP',
		colour = discord.Colour.blue()
	)

	embed.set_image(url=fuck['icon_url'])
	x = random.randint(57,556)
	embed.add_field(name='Chuck Norris Fact #{}'.format(x), value=msg)
	await client.say(embed=embed)

#---------------------------------------------------------------
#International Space Station Command
#--------------------------------------------------------------
@client.command(pass_context=True)
async def iss(ctx):
	r = requests.get('http://api.open-notify.org/iss-now.json', headers={"Accept":"application/json"})
	iss = r.json();
	issPosition = iss['iss_position']
	lat = issPosition['latitude']
	long = issPosition['longitude']
	msg = 'Currently, the ISS is at {} latitude and {} longitude'.format(lat,long)
	await client.say(msg)
	
@client.command(pass_context=True)
async def issEmbed(ctx):
	r = requests.get('http://api.open-notify.org/iss-now.json', headers={"Accept":"application/json"})
	iss = r.json();
	issPosition = iss['iss_position']
	lat = issPosition['latitude']
	long = issPosition['longitude']
	msg = 'Currently, the ISS is at {} latitude and {} longitude'.format(lat,long)
	embed = discord.Embed(
		title = 'TEAM OF TEAMS',
		description = 'Now Sponsered by 7-UP',
		colour = discord.Colour.green()
	)
	embed.add_field(name='ISS Locator', value=msg)
	embed.set_image(url='https://www.popsci.com/sites/popsci.com/files/styles/1000_1x_/public/images/2017/03/sts-116_spacewalk_1.jpg?itok=Z9nxaRrK&fc=50,50')
	await client.say(embed=embed)
	
#---------------------------------------------------------------
#Cat Commands
#--------------------------------------------------------------

@client.command(pass_context=True)
async def catFact(ctx):
	r = requests.get('https://cat-fact.herokuapp.com/facts/random?animal=cat', headers={"Accept":"application/json"})
	cat = r.json();
	msg = cat['text']
	await client.say(msg)
	
@client.command(pass_context=True)
async def catEmbed(ctx):
	r = requests.get('https://cat-fact.herokuapp.com/facts/random?animal=cat', headers={"Accept":"application/json"})
	cat = r.json();
	msg = cat['text']
	embed = discord.Embed(
		title = 'TEAM OF TEAMS',
		description = 'Now Sponsered by 7-UP',
		colour = discord.Colour.green()
	)
	x = random.randint(57,556)
	embed.add_field(name='Cat Fact #{}'.format(x), value=msg)
	
	#Get Cat Image
	r = requests.get('https://api.thecatapi.com/v1/images/search?size=1&mime_types=jpg,png,gif&format=json&order=RANDOM&page=0&limit=1&category_ids&breed_ids', headers={"Accept":"application/json","x-api-key":"026516ab-e9d2-426c-8117-f738d9c25061"})
	cat = r.json();
	img = cat[0]['url']
	
	await client.say(embed=embed)

@client.command(pass_context=True)
async def catPic(ctx):	
	#Get Cat Image
	r = requests.get('https://api.thecatapi.com/v1/images/search?size=1&mime_types=jpg,png,gif&format=json&order=RANDOM&page=0&limit=1&category_ids&breed_ids', headers={"Accept":"application/json","x-api-key":"026516ab-e9d2-426c-8117-f738d9c25061"})
	cat = r.json();
	img = cat[0]['url']
	
	await client.say(img)

#---------------------------------------------------------------
#Dice Command
#--------------------------------------------------------------
#Rolls Dice
@client.command(pass_context=True)
async def roll(ctx,sides):
	x = random.randint(1,int(sides))
	await client.say('You rolled a {} sided die. Your result was {}'.format(sides,x))

@client.command(pass_context=True)
async def rolld3(ctx,number=1):
	count = 0
	total = 0
	while count < number:
		x = random.randint(1,3)
		total += x
		count += 1
		await client.say('Roll {}: {}'.format(count,x))
	await client.say('You rolled {} d3. Your result was {}'.format(number,total))
	
@client.command(pass_context=True)
async def rolld4(ctx,number=1):
	count = 0
	total = 0
	while count < number:
		x = random.randint(1,4)
		total += x
		count += 1
		await client.say('Roll {}: {}'.format(count,x))
	await client.say('You rolled {} d4. Your result was {}'.format(number,total))
	
@client.command(pass_context=True)
async def rolld6(ctx,number=1):
	count = 0
	total = 0
	while count < number:
		x = random.randint(1,6)
		total += x
		count += 1
		await client.say('Roll {}: {}'.format(count,x))
	await client.say('You rolled {} d6. Your result was {}'.format(number,total))
	
@client.command(pass_context=True)
async def rolld8(ctx,number=1):
	count = 0
	total = 0
	while count < number:
		x = random.randint(1,8)
		total += x
		count += 1
		await client.say('Roll {}: {}'.format(count,x))
	await client.say('You rolled {} d8. Your result was {}'.format(number,total))
	
@client.command(pass_context=True)
async def rolld10(ctx,number=1):
	count = 0
	total = 0
	while count < number:
		x = random.randint(1,10)
		total += x
		count += 1
		await client.say('Roll {}: {}'.format(count,x))
	await client.say('You rolled {} d10. Your result was {}'.format(number,total))
	
@client.command(pass_context=True)
async def rolld20(ctx,number=1):
	count = 0
	total = 0
	while count < number:
		x = random.randint(1,10)
		total += x
		count += 1
		await client.say('Roll {}:{}'.format(count,x))
	await client.say('You rolled {} d20. Your result was {}'.format(number,total))
	
#---------------------------------------------------------------
#Embeds
#--------------------------------------------------------------
@client.command()
async def team():
	embed = discord.Embed(
		title = 'TEAM OF TEAMS',
		description = 'Now Sponsered by 7-UP',
		colour = discord.Colour.blue()
	)
	
	#embed.set_footer(text='           foot                    foot')
	embed.set_image(url='https://cdn.discordapp.com/attachments/498656146513592320/501144634148257793/unknown.png')
	#embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/424990916261183489/512323690084433940/vpqbe5d3jxjz.jpg')
	embed.set_author(name='Ronovo', icon_url ='https://cdn.discordapp.com/attachments/498656146513592320/512419060886142988/unknown.png')
	embed.add_field(name='You\'ve given up', value='Now try 7-Up')
	embed.add_field(name='https://discord.gg/BYbFyct', value='Join Us!')
	
	await client.say(embed=embed)
	
@client.command(pass_context=True)
async def help(ctx):
	
	author = ctx.message.author
	
	embed = discord.Embed(
		colour = discord.Colour.orange()
	)
	embed.set_author(name='Help(1/2)')
	embed.add_field(name='~ping', value='Returns pong', inline=False)
	embed.add_field(name='~hi', value='Personalized Hello', inline=False)
	embed.add_field(name='~hello', value='Regular Hello', inline=False)
	embed.add_field(name='~prouddad', value='Hear Me Be Proud of You!', inline=False)
	embed.add_field(name='~joke', value='I\'ll tell you a joke', inline=False)
	embed.add_field(name='~help', value='Hi help, I\'m Dad', inline=False)
	embed.add_field(name='~prune x', value='removes x messages in channel. Default 10', inline=False)
	
	embed.add_field(name='FOAAS(Fuck Off As A Service) Commands', value='-------------', inline=False)
	embed.add_field(name='~bye (name)', value='Bye to whoever you want. Ex. ~bye Ronovo', inline=False)
	embed.add_field(name='~fascinating', value='N/A', inline=False)
	embed.add_field(name='~horse', value='N/A', inline=False)
	embed.add_field(name='~horse1', value='N/A', inline=False)
	
	embed.add_field(name='Chuck Norris Commands', value='-------------', inline=False)
	embed.add_field(name='~chuck', value='Random Chuck Fact', inline=False)
	embed.add_field(name='~chuckEmbed)', value='Random Chuck Fact Embeded', inline=False)
	
	embed.add_field(name='International Space Station Commands', value='-------------', inline=False)
	embed.add_field(name='~iss', value='Lat and Long of ISS', inline=False)
	embed.add_field(name='~issEmbed', value='Embeded with Picture', inline=False)	
	
	embed.add_field(name='Cat Commands', value='-------------', inline=False)
	embed.add_field(name='~catFact', value='Lat and Long of ISS', inline=False)
	embed.add_field(name='~catEmbed', value='Cat Fact with Random Cat Pic', inline=False)	
	embed.add_field(name='~catPic', value='Random Cat Pic', inline=False)
	
	embed1 = discord.Embed(
		colour = discord.Colour.orange()
	)
	embed1.set_author(name='Help(2/2)')
	embed1.add_field(name='Dice Roll Commands', value='-------------', inline=False)
	embed1.add_field(name='~roll (numberOfSides)', value='rolls one die with any number of sides', inline=False)
	embed1.add_field(name='~roll{dieType} (numberOfDice=1(default))', value='Rolls a number of dice that pass into the command.', inline=False)	
	embed1.add_field(name='Supported Die Types', value='d4,d6,d8,d10,d20', inline=False)
	embed1.add_field(name=' Example Call', value='~rolld6 4', inline=False)
	embed1.add_field(name='Voice Channel Commands', value='-----------', inline=False)
	embed1.add_field(name='~join', value='Joins current voice channel', inline=False)
	embed1.add_field(name='~leave', value='Leaves current voice channel', inline=False)
	
	embed1.add_field(name='Music Commands', value='-----------', inline=False)
	embed1.add_field(name='~play (url)', value='Strats Playing song. DO NOT use after music has started. Use Queue', inline=False)
	embed1.add_field(name='~pause', value='Pauses Music', inline=False)
	embed1.add_field(name='~resume', value='Starts playing music again (if paused)', inline=False)
	embed1.add_field(name='~queue (url)', value='Add a song after you have used play', inline=False)
	
	await client.say('Help has been sent to your DMs.')
	await client.send_message(author,embed=embed)
	await client.send_message(author,embed=embed1)

#---------------------------------------------------------------
#General Voice Commands
#--------------------------------------------------------------
#Joins The Channel
@client.command(pass_context=True)
async def join(ctx):
	channel = ctx.message.author.voice.voice_channel
	await client.join_voice_channel(channel)

#Leaves the Channel
@client.command(pass_context=True)
async def leave(ctx):
	server = ctx.message.server
	voice_client = client.voice_client_in(server)
	await voice_client.disconnect()

#---------------------------------------------------------------
#Music Bot Commands
#--------------------------------------------------------------
#Plays a song given a URL.
#Only Supports Youtube currently
@client.command(pass_context=True)
async def play(ctx, url):
	server = ctx.message.server
	voice_client = client.voice_client_in(server)
	if voice_client is None:
		channel = ctx.message.author.voice.voice_channel
		await client.join_voice_channel(channel)
		server = ctx.message.server
		voice_client = client.voice_client_in(server)
	player = await voice_client.create_ytdl_player(url, after=lambda: check_queue(server.id))
	players[server.id] = player
	player.start()
	
#Pauses Player
@client.command(pass_context=True)
async def pause(ctx):
	id = ctx.message.server.id
	players[id].pause()
	
#Resumes if paused
@client.command(pass_context=True)
async def resume(ctx):
	id = ctx.message.server.id
	players[id].resume()
	
#Queues a song
@client.command(pass_context=True)
async def queue(ctx, url):
	server = ctx.message.server
	voice_client = client.voice_client_in(server)
	player = await voice_client.create_ytdl_player(url, after=lambda: check_queue(server.id))
	
	if server.id in queues:
		queues[server.id].append(player)
	else:
		queues[server.id] = [player]
	await client.say('Video queued.')

#Plays "No Cock Like Horse Cock" by Pepper Coyote
@client.command(pass_context=True)
async def horse1(ctx):
	channel = ctx.message.author.voice.voice_channel
	await client.join_voice_channel(channel)
	server = ctx.message.server
	voice_client = client.voice_client_in(server)
	player = await voice_client.create_ytdl_player('https://www.youtube.com/watch?v=h2dJ-JUzhVs')
	players[server.id] = player
	player.start()
	await client.say('!play https://www.youtube.com/watch?v=h2dJ-JUzhVs')

#---------------------------------------------------------------
#Administration Commands
#--------------------------------------------------------------
#Closes the session	
@client.command()
async def close():
	await client.close()

#Pruning. Default set to 10	
@client.command(pass_context=True)
async def prune(ctx,amount=10):
	channel = ctx.message.channel
	messages = []
	async for message in client.logs_from(channel, limit=int(amount)):
		messages.append(message)
	await client.delete_messages(messages)
	
#Creates loop to cycle through statuses
client.loop.create_task(change_status())

client.run(TOKEN)

#Code that needs to be fixed
#Currently, I can't get commands to work when this runs
#I tried normal bot.process_commands, but it didn't work
'''
conversations = ['~We are only togeter because of the kids']
@client.event
async def on_message(message):
	#Conversation Commands
	if message.content.startswith(conversations[0]):
		msg = 'Can we please not have this fight tonight?'
		await client.send_message(message.channel, msg)
		await bot.process_commands(message)
'''