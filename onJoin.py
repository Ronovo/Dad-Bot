import discord
from discord.ext import commands

class onJoin:
	def __init__(self, client):
		self.client = client
		
	#Auto Assignes Role to new members
	#Adds them to json for leveling up
	async def on_member_join(self, member):
		role = discord.utils.get(member.server.roles, name="ToTLER")
		await self.client.add_roles(member, role)
		#channel = discord.utils.get(member.server.getChannel('423653908552876043')
		#await self.client.send_message(channel, 'Hi {}, I\'m Dad!'.format(member.name))
		#with open('users.json', 'r') as f:
		#	users = json.load(f)
			
		#await update_data(users, member)
	
		#with open('users.json', 'w') as f:
		#	json.dump(users,f)

def setup(client):
	client.add_cog(Fun(client))