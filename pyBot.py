#pyBot.py
#A discord Bot

#importing of necessary elements
import json
import discord
from discord.ext import commands
from discord import *
from discord.ext.commands import has_permissions, MissingPermissions
import random
import requests
from datetime import datetime
from xp import person
from urllib.request import urlretrieve
from pprint import PrettyPrinter
pp = PrettyPrinter()


#creates the discord client object
client = commands.Bot(command_prefix = ".")
client.remove_command("help")
permissions = discord.Permissions()


#run through file and create a list of objects for each person and save their xp and level
peeps = []
ifile = "/home/chase/Desktop/Programming/My Programs/In Progress/Discord Bot/people.txt"
infile = open(ifile, "r")
for line in infile:
	line = line[:-1]
	if line != "":
		name, xp, money = line.split("::")
		xp = int(xp)
		money = float(money)
		peeps.append(person(name, xp, money))

infile.close()

#list of variables for API URLS
nasa_url = "https://api.nasa.gov/planetary/apod"
nasa_key = "Lzf5uYZKPA9Ndfv2Xl6Kt0tOJiWWfr7zjp6wPUTh"
#https://api.nasa.gov/planetary/apod?api_key=Lzf5uYZKPA9Ndfv2Xl6Kt0tOJiWWfr7zjp6wPUTh


def person_check(author, peeps):
	flag = False
	for i in peeps:
		if (author.name + "#" + author.discriminator) == i.get_name():
			flag = True

	if flag == False:
		peeps.append(person((author.name + "#" + author.discriminator)))

async def add_xp(message, author, peeps):

	for i in peeps:
		if (author.name + "#" + author.discriminator) == i.get_name():
			flag = i.add_xp()
			if (flag == True):
				i.level_up()
				await increase_level(message.channel, author, peeps, i)

async def increase_level(ctx, author, peeps, i):
	#increased level messages
	#for now it will be just a simple message soon it wil be a picture of some sort though
	await ctx.send("{} is now level {}!".format(author.mention, i.get_level()))

async def decrease_level(ctx, author, peeps, i):
	#decrease level messages
	await ctx.send("{} has been demoted to level {}!".format(author.mention, i.get_level()))


#event example
@client.event
async def on_ready():
	print()
	#get a list of all new members and add them to the person list
	for guild in client.guilds:
		print(guild)
		for member in guild.members:
			if member.bot == False:
				person_check(member, peeps)
				print("  " + str(member))

		print()
	print("Bot is Ready!")


@client.event
async def on_message(message):
	if message.author.bot == False:
		await client.process_commands(message)

		#check if the message is a command
		if message.content[0] != ".":
			#check if user exists in list of people if not add him and make sure to save to people.txt
			person_check(message.author, peeps)
			#add to user xp
			await add_xp(message, message.author, peeps)





'''
on_member_ban
on_member_unban
on_typing

'''



#ping command
@client.command(help = "gets the response time")
async def ping(ctx):
	await ctx.send(f"Pong! {round(client.latency * 1000)}ms")

#8ball command
@client.command(name = "8ball", help = "ask a question and get an answer")	#the list of aliases is things that can be typed to still invoke this command
async def _8ball(ctx, *, question):
	responses = ["It is decidedly so.", "Without a doubt.", "Yes - definitely.", "You may rely on it.", "As I see it, yes.", "Most likely.", "Outlook good.", "Yes.", "Signs point to yes.", "Reply hazy, try again.", "Ask again later.", "Better not tell you now.", "Cannot predict now.", "Concentrate and ask again.", "Don't count on it.", "My reply is no.", "My sources say no.", "Outlook not so good.", "Very doubtful."]
	await ctx.send(f"question: {question}\nAnswer: {random.choice(responses)}")

#repeat command
@client.command(help = "repeats what is said after the command")
async def repeat(ctx, *, arg):
	await ctx.send(arg)

@client.command(help = "gets the level of a user")
async def level(ctx, member : discord.Member = None):
	if (member == None):
		member = ctx.author
	flag = False
	for i in peeps:
		if (member.name + "#" + member.discriminator) == i.get_name():
			await ctx.send("{} is currently at Level {}!".format(member.mention, i.get_level()))
			flag = True
	if flag == False:
		person_check(member, peeps)
		await ctx.send("{} is currently at Level 0!".format(member.mention))


@client.command(help = "gets the xp of a user")
async def xp(ctx, member : discord.Member = None):
	if (member == None):
		member = ctx.author
	flag = False
	for i in peeps:
		if (member.name + "#" + member.discriminator) == i.get_name():
			await ctx.send("{} is currently at {} xp!".format(member.mention, i.get_xp()))
			flag = True;
	if flag == False:
		person_check(member, peeps)
		await ctx.send("{} is currently at {} xp!".format(member.mention, i.get_xp()))



@client.command(help = "gets the money of a user")
async def bank(ctx, member : discord.Member = None):
	if (member == None):
		member = ctx.author
	flag = False
	for i in peeps:
		if (member.name + "#" + member.discriminator) == i.get_name():
			await ctx.send("{} currently has ${}!".format(member.mention, i.get_money()))
			flag = True;
	if flag == False:
		person_check(member, peeps)
		await ctx.send("{} currently has ${}!".format(member.mention, i.get_money()))


@client.command(help="get the Astronomy Picture of the day from NASA")
async def apod(ctx):
	await ctx.send("Getting APOD")
	date = '2020-01-22'
	params = {
		'api_key': nasa_key,
		'hd': 'True'
	}
	response = requests.get(nasa_url,params=params).json()
	pp.pprint(response)
	await ctx.send(response['url'])



@client.command()
async def help(ctx):
	embed = discord.Embed(title = "Help", colour = ctx.author.colour)

	#embed.set_footer(text = "This is a footer.")
	#h_embed.set_image(url = "")
	#h_embed.setthumbnail(url = "")
	embed.set_author(name = client.user.name, icon_url = client.user.avatar_url)
	#embed.set_author(name = "Author Name", icon_url = "")
	count = 1
	for command in client.commands:
		fname = command.name
		fvalue = command.help
		embed.add_field(name = fname, value = fvalue, inline = True)
		
	await ctx.send(embed = embed)


#Admin commmands
#---------------#


#to stop the bot
@client.command(help = "shuts down the bot", hidden = True)
@commands.has_permissions(administrator = True)
async def end(ctx):
	await ctx.send("Closing Client")
	await client.close()




#delete messages command
@client.command(aliases = ["clear", "del", "purge", "remove"], help = "deletes the specified number of messages", hidden = True, cog_name = "Admin")
@commands.has_permissions(manage_messages = True)
async def delete(ctx, amount = 5):
	await ctx.channel.purge(limit = amount + 1)


@client.command(name = "givexp", help = "gives a user xp", hidden = True)
@commands.has_permissions(manage_messages = True)
async def give_xp(ctx, amount = 0, member : discord.Member = None):
	if (member == None):
		member = ctx.author
	flag = False
	for i in peeps:
		if (member.name + "#" + member.discriminator) == i.get_name():
			#give xp
			n = i
			flag_2 = n.add_xp(amount)
			if amount == 0:
				await ctx.send("{} has been given a random amount of xp!".format(member.mention))
			else:
				await ctx.send("{} has been given {} xp!".format(member.mention, amount))
			flag = True;
	if flag == False:
		person_check(member, peeps)
		for i in peeps:
			if (member.name + "#" + member.discriminator) == i.get_name():
				#give xp
				n = i
				flag_2 = n.add_xp(amount)
				if amount == 0:
					await ctx.send("{} has been given a random amount of xp!".format(member.mention))
				else:
					await ctx.send("{} has been given {} xp!".format(member.mention, amount))

	if flag_2 == True:
		#call level up
		if (flag == True):
				n.level_up()
				await increase_level(ctx, member, peeps, n)


@client.command(name = "givemoney", help = "gives a user money", hidden = True)
@commands.has_permissions(manage_messages = True)
async def give_money(ctx, amount = 0, member : discord.Member = None):
	if (member == None):
		member = ctx.author
	flag = False
	for i in peeps:
		if (member.name + "#" + member.discriminator) == i.get_name():
			#give money
			n = i
			flag_2 = n.add_money(amount)
			if amount == 0:
				await ctx.send("{} has been given a random amount of money!".format(member.mention))
			else:
				await ctx.send("{} has been given ${}!".format(member.mention, amount))
			flag = True;
	if flag == False:
		person_check(member, peeps)
		for i in peeps:
			if (member.name + "#" + member.discriminator) == i.get_name():
				#give xp
				n = i
				flag_2 = n.add_money(amount)
				if amount == 0:
					await ctx.send("{} has been given a random amount of money!".format(member.mention))
				else:
					await ctx.send("{} has been given ${}!".format(member.mention, amount))


@client.command(name = "takexp", help = "removes xp from a user", hidden = True)
@commands.has_permissions(manage_messages = True)
async def take_xp(ctx, amount = 0, member : discord.Member = None):
	if (member == None):
		member = ctx.author
	flag = False
	for i in peeps:
		if (member.name + "#" + member.discriminator) == i.get_name():
			#give xp
			n = i
			flag_2 = n.take_xp(amount)
			if amount == 0:
				await ctx.send("{} has had a random amount of xp removed!".format(member.mention))
			else:
				await ctx.send("{} has had {} xp removed!".format(member.mention, amount))
			flag = True;
	if flag == False:
		person_check(member, peeps)
		for i in peeps:
			if (member.name + "#" + member.discriminator) == i.get_name():
				#give xp
				n = i
				flag_2 = n.take_xp(amount)
				if amount == 0:
					await ctx.send("{} has had a random amount of xp removed!".format(member.mention))
				else:
					await ctx.send("{} has had {} xp removed!".format(member.mention, amount))

	if flag_2 == True:
		#call level up
		if (flag == True):
				n.level_up()
				await decrease_level(ctx, member, peeps, n)


@client.command(name = "takemoney", help = "gives a user money", hidden = True)
@commands.has_permissions(manage_messages = True)
async def take_money(ctx, amount = "", member : discord.Member = None):
	if (amount == ""):
		amount = 0
	else:
		amount = float(amount)
	if (member == None):
		member = ctx.author
	flag = False
	for i in peeps:
		if (member.name + "#" + member.discriminator) == i.get_name():
			#give money
			n = i
			flag_2 = n.take_money(amount)
			if amount == 0:
				await ctx.send("{} has had a random amount of money taken!".format(member.mention))
			else:
				await ctx.send("{} has had ${} taken!".format(member.mention, amount))
			flag = True;
	if flag == False:
		person_check(member, peeps)
		for i in peeps:
			if (member.name + "#" + member.discriminator) == i.get_name():
				#give xp
				n = i
				flag_2 = n.take_money(amount)
				if amount == 0:
					await ctx.send("{} has had a random amount of money taken!".format(member.mention))
				else:
					await ctx.send("{} has had ${} taken!".format(member.mention, amount))



#kick command
@client.command(help = "kicks a user", hidden = True)
@commands.has_permissions(kick_members = True)
async def kick(ctx, member : discord.Member, *, reason = None):
	if ctx.author.top_role <= member.top_role:
		return await ctx.send("You cannot manage a User with a Higher Role")
	
	roles = ctx.guild.roles
	x = roles.index(ctx.author.top_role)
	if x >= 2:
		await member.kick(reason = reason)
		await ctx.send("{} has been kicked!\nReason:	{}".format(member.mention, reason))
	else:
		await ctx.channel.send("You Do Not have the Permission for this Command!")




#ban command
@client.command(help = "bans a user", hidden = True)
@commands.has_permissions(ban_members = True)
async def ban(ctx, member : discord.Member, *, reason = None):
	if ctx.author.top_role <= member.top_role:
		return await ctx.send("You cannot manage a User with a Higher Role")
	await member.ban(reason = reason)
	await ctx.send("{} has been banned!\nReason:	{}".format(member.mention, reason))




#unban command
@client.command(help = "unbans the user", hidden = True)
@commands.has_permissions(ban_members = True)
async def unban(ctx, *, member):
	banned_users = await ctx.guild.bans()
	member_name, member_discriminator = member.split("#")

	for ban_entry in banned_users:
		user = ban_entry.user

		if (user.name, user.discriminator) == (member_name, member_discriminator):
			await ctx.guild.unban(user)
			await ctx.send("Unbanned {}!".format(user.mention))
			return
	await ctx.send("{} not found!".format(member))




#give role command
@client.command(aliases = ["giverole", "give", "promote"], help = "gives role to user", hidden = True)
@commands.has_permissions(manage_roles = True)
async def role(ctx, member : discord.Member, role : discord.Role = None):

	if ctx.author.top_role <= member.top_role:
		return await ctx.send("You cannot manage a User with a Higher Role")
	
	if ctx.author.top_role <= role:
		return await ctx.send("You cannot give {} the {} role!".format(member.mention, role.mention))

	if role == None:
		return await ctx.send("You haven't specified a Role!")

	if role not in member.roles:
		await member.add_roles(role, reason = None)
		return await ctx.send("{} role has been added to {}.".format(role.mention, member.mention))
	
	if role in member.roles:
		return await ctx.send("{} already has the {} role.".format(member.mention, role.mention))


@client.command(aliases = ["remove_role", "demote"], help = "removes the role from the user", hidden = True)
@commands.has_permissions(manage_roles = True)
async def removerole(ctx, member : discord.Member, role : discord.Role = None):

	if ctx.author.top_role <= member.top_role:
		return await ctx.send("You cannot manage a User with a Higher Role")
	
	if ctx.author.top_role <= role:
		return await ctx.send("You cannot take the {} role from {}!".format(member.mention, role.mention))

	if role == None:
		return await ctx.send("You haven't specified a Role!")

	if role not in member.roles:
		return await ctx.send("{} does not currently have the {} role.".format(member.mention, role.mention))

	if role in member.roles:
		await member.remove_roles(role, reason = None)
		return await ctx.send("{} no longer has the {} role.".format(member.mention, role.mention))





#Errors
@client.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.errors.CommandNotFound):
		await ctx.send("Command Does not Exist!\n" + str(error))


@help.error
async def help_error(ctx, error):
	if isinstance(error, discord.Forbidden):
		await ctx.send("You do not have the Permission to do this!")
	elif isinstance(error, discord.HTTPException):
		await ctx.send("HTTPException")
	elif isinstance(error, commands.MissingPermissions):
		await ctx.send("You do not have the Permission to do this!")
	elif isinstance(error, commands.MissingRequiredArgument):
		await ctx.send("Missing Parameters")
	else:
		await ctx.send(error)


@_8ball.error
async def _8ball_error(ctx, error):
	if isinstance(error, discord.Forbidden):
		await ctx.send("You do not have the Permission to do this!")
	elif isinstance(error, discord.HTTPException):
		await ctx.send("HTTPException")
	elif isinstance(error, commands.MissingPermissions):
		await ctx.send("You do not have the Permission to do this!")
	elif isinstance(error, commands.MissingRequiredArgument):
		await ctx.send("No Question Received")

@repeat.error
async def repeat_error(ctx, error):
	if isinstance(error, discord.Forbidden):
		await ctx.send("You do not have the Permission to do this!")
	elif isinstance(error, discord.HTTPException):
		await ctx.send("HTTPException")
	elif isinstance(error, commands.MissingPermissions):
		await ctx.send("You do not have the Permission to do this!")
	elif isinstance(error, commands.MissingRequiredArgument):
		await ctx.send("Nothing to Repeat")

@level.error
async def level_error(ctx, error):
	if isinstance(error, discord.Forbidden):
		await ctx.send("You do not have the Permission to do this!")
	elif isinstance(error, discord.HTTPException):
		await ctx.send("HTTPException")
	elif isinstance(error, commands.MissingPermissions):
		await ctx.send("You do not have the Permission to do this!")
	elif isinstance(error, commands.MissingRequiredArgument):
		await ctx.send("No Member given")

@xp.error
async def xp_error(ctx, error):
	if isinstance(error, discord.Forbidden):
		await ctx.send("You do not have the Permission to do this!")
	elif isinstance(error, discord.HTTPException):
		await ctx.send("HTTPException")
	elif isinstance(error, commands.MissingPermissions):
		await ctx.send("You do not have the Permission to do this!")
	elif isinstance(error, commands.MissingRequiredArgument):
		await ctx.send("No Member given")

@bank.error
async def bank_error(ctx, error):
	if isinstance(error, discord.Forbidden):
		await ctx.send("You do not have the Permission to do this!")
	elif isinstance(error, discord.HTTPException):
		await ctx.send("HTTPException")
	elif isinstance(error, commands.MissingPermissions):
		await ctx.send("You do not have the Permission to do this!")
	elif isinstance(error, commands.MissingRequiredArgument):
		await ctx.send("No Member given")

@end.error
async def end_error(ctx, error):
	if isinstance(error, discord.Forbidden):
		await ctx.send("You do not have the Permission to do this!")
	elif isinstance(error, discord.HTTPException):
		await ctx.send("HTTPException")
	elif isinstance(error, commands.MissingPermissions):
		await ctx.send("You do not have Permission to shut me down!")

@delete.error
async def delete_error(ctx, error):
	if isinstance(error, discord.Forbidden):
		await ctx.send("You do not have the Permission to do this!")
	elif isinstance(error, discord.HTTPException):
		await ctx.send("HTTPException")
	elif isinstance(error, commands.MissingPermissions):
		await ctx.send("You do not have Permission to manage messages!")

@give_xp.error
async def give_xp_error(ctx, error):
	if isinstance(error, discord.Forbidden):
		await ctx.send("You do not have the Permission to do this!")
	elif isinstance(error, discord.HTTPException):
		await ctx.send("HTTPException")
	elif isinstance(error, commands.MissingPermissions):
		await ctx.send("You do not have Permission to manage messages!")

@give_money.error
async def give_money_error(ctx, error):
	if isinstance(error, discord.Forbidden):
		await ctx.send("You do not have the Permission to do this!")
	elif isinstance(error, discord.HTTPException):
		await ctx.send("HTTPException")
	elif isinstance(error, commands.MissingPermissions):
		await ctx.send("You do not have Permission to manage messages!")
	else:
		await ctx.send(error)

@take_xp.error
async def take_xp(ctx, error):
	if isinstance(error, discord.Forbidden):
		await ctx.send("You do not have the Permission to do this!")
	elif isinstance(error, discord.HTTPException):
		await ctx.send("HTTPException")
	elif isinstance(error, commands.MissingPermissions):
		await ctx.send("You do not have Permission to manage messages!")
	else:
		await ctx.send(error)

@take_money.error
async def take_money(ctx, error):
	if isinstance(error, discord.Forbidden):
		await ctx.send("You do not have the Permission to do this!")
	elif isinstance(error, discord.HTTPException):
		await ctx.send("HTTPException")
	elif isinstance(error, commands.MissingPermissions):
		await ctx.send("You do not have Permission to manage messages!")
	else:
		await ctx.send(error)


@kick.error
async def kick_error(ctx, error):
	if isinstance(error, discord.Forbidden):
		await ctx.send("You do not have the Permission to do this!")
	elif isinstance(error, discord.HTTPException):
		await ctx.send("HTTPException")
	elif isinstance(error, commands.MissingPermissions):
		await ctx.send("You do not have Permission to kick Users!")

@ban.error
async def ban_error(ctx, error):
	if isinstance(error, discord.Forbidden):
		await ctx.send("You do not have the Permission to do this!")
	elif isinstance(error, discord.HTTPException):
		await ctx.send("HTTPException")
	elif isinstance(error, commands.MissingPermissions):
		await ctx.send("You do not have Permission to ban Users!")
	else:
		await ctx.send(error)

@unban.error
async def unban_error(ctx, error):
	if isinstance(error, discord.Forbidden):
		await ctx.send("You do not have the Permission to do this!")
	elif isinstance(error, discord.HTTPException):
		await ctx.send("HTTPException")
	elif isinstance(error, commands.MissingPermissions):
		await ctx.send("You do not have Permission to unban Users!")
	else:
		await ctx.send(error)

@role.error
async def role_error(ctx, error):
	if isinstance(error, discord.Forbidden):
		await ctx.send("You do not have the Permission to do this!")
	elif isinstance(error, discord.HTTPException):
		await ctx.send("HTTPException")
	elif isinstance(error, commands.MissingPermissions):
		await ctx.send("You do not have Permission to manage roles!")
	else:
		await ctx.send(error)

@removerole.error
async def removerole_error(ctx, error):
	if isinstance(error, discord.Forbidden):
		await ctx.send("You do not have the Permission to do this!")
	elif isinstance(error, discord.HTTPException):
		await ctx.send("HTTPException")
	elif isinstance(error, commands.MissingPermissions):
		await ctx.send("You do not have Permission to manage roles!")
	else:
		await ctx.send(error)




#this runs the bot....but I have less control over the loop
client.run("NTg4NzYzMTIxNTAyNTE5MzM0.Xh0PVQ._ZCduH7nHw6ZZvE6_qIWpJAY-Zk")


#print to the file and save all the xp information

outfile = open(ifile, "w")
output = ""
for i in peeps:
	output += i.get_name() + "::" + str(i.get_xp()) + "::" + str(i.get_money()) + "\n"


output = output[:-1]
print(output, file = outfile)
outfile.close()

print("Closed!")




#make sure admin overrides everything
#check help commands...for both normal and admin commands...or make my own
#add picture (embeds) like thing for level ups


#for help with .help command and parameters for the commands:
#https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#discord.ext.commands.Command.help


#for grouping commands cogs should be used
#https://discordpy.readthedocs.io/en/latest/ext/commands/cogs.html#ext-commands-cogs
