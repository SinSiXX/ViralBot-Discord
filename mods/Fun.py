from random import randint,sample
import asyncio
from discord.ext import commands
import io
import discord.utils
import json
from discord.errors import *
import time
import aiohttp
import sys
from PIL import Image, ImageDraw, ImageFont
from pyfiglet import figlet_format
import wikipedia
import wikipedia.exceptions
import base64
import random
import os
from bs4 import BeautifulSoup as bs

with open("mods/utils/json/configs/config.json") as f:
	config = json.load(f)
with open("mods/utils/json/fun/hexnamestocode.json") as f:
	name = json.load(f)
with open("mods/utils/json/fun/hexcodestoname.json") as f:
	color = json.load(f)
with open("mods/utils/json/configs/credentials.json") as f:
	credentials = json.load(f)

wrap = "```py\n{}\n```"

async def download(link:str,path:str):
	with aiohttp.ClientSession() as session:
		async with session.get(link) as resp:
			data = await resp.read()
			with open(path,"wb") as f:
				f.write(data)

async def tempsay(self,message:str,time:int):
	x = await self.bot.say(message)
	await asyncio.sleep(time)
	await self.bot.delete_message(x)

class Fun():
	def __init__(self,bot):
		self.bot = bot

	@commands.command(pass_context=True)
	async def scramble(self,ctx):
		"""Allows the user to play a word scramble with the bot."""
		with open("mods/utils/text/5 letter words.txt", "r") as f:
			data = f.read()
		data = data.split("\n")
		i = randint(1, 5757)
		word = data[i-1]
		print(word)
		scrambled = sample(word, len(word))
		scrambled = ''.join(scrambled)
		await self.bot.say("The word scramble is: {}!".format(scrambled))
		await self.bot.wait_for_message(content=word)
		await self.bot.say("Nice job! You solved the scramble!")

	@commands.command(name="8ball",pass_context=True)
	async def cmd_8ball(self,ctx,*,msg:str):
		"""Allows the user to be bestowed the wisdom of the almighy Magic 8-Ball."""
		await self.bot.say('{} asked '.format(ctx.message.author.name) + '`' + msg.replace("```","'''") + '`' + ': ' + config["eight_ball_replies"][randint(0, 19)])

	@commands.command(pass_context=True)
	async def rr(self,ctx):
		"""Allows the user to take part in the famous Russian Pasttime."""
		rr_bullet = randint(1, 6)
		rr_count = 1
		await self.bot.say('You spin the cylinder of the revolver with 1 bullet in it...')
		await asyncio.sleep(1)
		await self.bot.say('...you place the muzzle against your head and pull the trigger...')
		await asyncio.sleep(2)
		if rr_bullet == rr_count:
			await self.bot.say('...your brain gets splattered all over the wall.')
			rr_bullet = randint(1, 6)
			rr_count = 1
		else:
			await self.bot.say('...you live to see another day.')
			rr_count = rr_count + 1

	@commands.command(pass_context=True)
	async def shoot(self,ctx,*users:discord.User):
		"""Allows the user to shoot a person of choice."""
		for user in users:
			if user.id == self.bot.user.id:
				await self.bot.say('You attempted to shoot me, {}, but I dodged it!\nhttp://45.media.tumblr.com/c1165e983042a9cd1f17028a1c78170b/tumblr_n9c38m14291s5f9ado1_500.gif'.format(ctx.message.author.name))
			elif user.id == ctx.message.author.id:
				await self.bot.say('{} commited suicide!\nhttps://media.giphy.com/media/5xaOcLAo1Gg0oRgBz0Y/giphy.gif'.format(ctx.message.author.name))
			else:
				if user:
					await self.bot.say('{1} was shot dead by the mighty {0}!\nhttps://s-media-cache-ak0.pinimg.com/originals/2d/fa/a9/2dfaa995a09d81a07cad24d3ce18e011.gif'.format(ctx.message.author.name, user.name))
				else:
					await self.bot.say('You gotta give me someone to work with here!')

	@commands.command(pass_context=True)
	async def roti(self,ctx,*,number=''):
		"""Bestows the user with the 102 Rules of the Internet."""
		if not number:                
			with open("mods/utils/text/RulesOTI.txt", "r") as f:
				data = f.read()
			data = data.split("\n")
			i = randint(1, 102)
			await self.bot.say(data[i-1])
		else:
			try:
				i = int(number)
				if i > 0 and i <= 102:
					with open("mods/utils/text/RulesOTI.txt", "r") as f:
						data = f.read()
					data = data.split("\n")
					await self.bot.say(data[i-1])
				elif i >= 102 or i <= 0:
					await self.bot.say("It has to be a number between 1 and 102!")
			except ValueError:
				await self.bot.say("You have to put a number!")

	@commands.command(pass_context=True)
	async def lmgtfy(self,ctx,*,query):
		"""Gives the user a 'Let Me Google That For You' link."""
		msg = query.replace(' ','+')
		msg = 'http://lmgtfy.com/?q=%s' % msg
		await self.bot.say(msg)

	@commands.command(pass_context=True)
	async def pybelike(self,ctx):
		"""Gives the user an accurate description of Python."""
		await self.bot.send_file(ctx.message.channel, "mods/utils/images/other/python.png")

	@commands.command(pass_context=True)
	async def lenny(self,ctx):
		"""Gives the user a lenny face."""
		i = randint(1, 98)
		with io.open('mods/utils/text/lenny.txt','r',encoding='utf8') as f:
			text = f.read()
		text = text.split("\n")
		await self.bot.say("`" + text[i-1] + "`")

	@commands.command(pass_context=True)
	async def meh(self,ctx):
		"""Gives the user the famous shrug face."""
		i = 7
		with io.open('mods/utils/text/lenny.txt','r',encoding='utf8') as f:
			text = f.read()
		text = text.split("\n")
		await self.bot.say("" + text[i-1] + "")

	@commands.command(pass_context=True)
	async def emoji(self,ctx,query=""):
		"""Gives the user emojis.

			Do `^emoji url` to get the link to the cheat sheet page, or put a number from 1 to 874 to get a random emoji!"""
		if not query:
			with open("mods/utils/text/emoji.txt", "r") as f:
				data = f.read()
			data = data.split("\n")
			emoji1 = randint(1, 874)
			emoji2 = randint(1, 874)
			emoji3 = randint(1, 874)
			emoji4 = randint(1, 874)
			await self.bot.say("Some useful emojis are `" + data[emoji1-1] + "` " + data[emoji1-1] + ", `" + data[emoji2-1] + "` " + data[emoji2-1] + ", `" + data[emoji3-1] + "` " + data[emoji3-1] + ", and `" + data[emoji4-1] + "` " + data[emoji4-1] + "!")
		else:
			if query == "url":
				await self.bot.say("http://www.emoji-cheat-sheet.com/")
			else:
				with io.open('mods/utils/text/emoji.txt','r') as f:
					text = f.read()
				text = text.split("\n")
				i = int(query)
				await self.bot.say(text[i-1])

	@commands.command(pass_context=True)
	async def copypasta(self,ctx,query=''):
		"""Gives the user a random copypasta.

		Do `^copypasta <number from 1-19>` for a specific copypasta!
		"""
		if not query:
			with io.open('mods/utils/text/copypasta.txt','r',encoding='utf8') as f:
				data = f.read()
			data = data.split("\n")
			i = randint(1,19)
			await self.bot.say(data[i-1])
		else:
			with io.open('mods/utils/text/copypasta.txt','r',encoding='utf8') as f:
				data = f.read()
			data = data.split("\n")
			i = int(query)
			await self.bot.say(data[i-1])

	@commands.command(pass_context=True)
	async def nope(self,ctx):
		"""Gives a user a 'nope' gif."""
		with open("mods/utils/text/nope.txt","r") as f:
			data = f.read()
		data = data.split("\n")
		i = randint(1,3)
		await self.bot.say(data[i-1])

	@commands.command(pass_context=True)
	async def say(self,ctx,*,message):
		"""Makes the bot say anything the user wants it to."""
		await self.bot.say(message)

	@commands.group(pass_context=True,invoke_without_command=True)
	async def colors(self,ctx):
		"""Gives a giant list of all hex colors and their values."""
		if ctx.invoked_subcommand is None:
			await self.bot.say("A *whole* list of hexidecimal color codes can be found here: http://xkcd.com/color/rgb.txt")

	@colors.command(name='lookup',pass_context=True)
	async def _lookup(self,ctx,type,query):
		"""Allows users to look up colors."""
		if type == "name":
			file = color
		if type == "value":
			file = name
		await self.bot.say(file[query.lower()].title())

	@colors.command(name='convert',pass_context=True)
	async def _convert(self,ctx,convert_to:str,*,input):
		if convert_to == "hex":
			input = str(input)
			rgb = []
			input = input.strip("()").split(",")
			for i in input:
				rgb.append(int(i.strip(" ")))
			r,g,b = rgb[0],rgb[1],rgb[2]
			if r > 255 or g > 255 or b > 255:
				await self.bot.say("Only numbers from 0 to 255, please!")
			else:
				await self.bot.say("HEX = " + "#%02X%02X%02X".lower() % (r,g,b))
		if convert_to == "rgb":
			input = input.lstrip("#")
			await self.bot.say('RGB = ' + str(tuple(int(input[i:i+2], 16) for i in (0, 2 ,4))))

	@colors.command(name='preview',pass_context=True)
	async def _preview(self,ctx,rgbcolor:str):
		rgb = []
		input = rgbcolor.strip("()").split(",")
		for i in input:
			rgb.append(int(i.strip(" ")))
		r,g,b = rgb[0],rgb[1],rgb[2]
		if r > 255 or g > 255 or b > 255:
			await self.bot.say("Only numbers from 0 to 255, please!")
		else:
			url = "http://dev.gatt.space/color_image_maker/100/{0}/{1}/{2}/image.png".format(r,g,b)
			await self.bot.say(url)

	@commands.command(pass_context=True)
	async def codeblock(self,ctx,language:str,*,code:str):
		"""Transforms the specified code into a code block with the coding language of choice."""
		if "```" in code:
			await self.bot.say("```{0}\n{1}\n```".format(language,code.replace("```","'''")))
		else:
			await self.bot.say("```{0}\n{1}\n```".format(language,code))

	@commands.command(pass_context=True)
	async def timer(self,ctx,seconds,*,remember=''):
		"""Sets a timer for a user with the option of setting a reminder text."""
		if not remember:
			endtimer = self.bot.say(ctx.message.author.mention + ', your timer for ' + seconds + ' seconds has expired!')
			await self.bot.say(ctx.message.author.name + ', you have set a timer for ' + seconds + ' seconds!')
			await asyncio.sleep(float(seconds))
			await endtimer
		else:
			endtimer = self.bot.say(ctx.message.author.mention + ", your timer for " + seconds + " seconds has expired! I was instructed to remind you about `" + remember + "`!")
			await self.bot.say(ctx.message.author.name + ", I will remind you about `" + remember + "` in " + seconds + " seconds!")
			await asyncio.sleep(float(seconds))
			await endtimer

	@commands.group(pass_context=True,invoke_without_command=True)
	async def meme(self,ctx,meme:str,line1:str,line2:str,style=""):
		"""Generates a meme."""
		if ctx.invoked_subcommand is None:
			i = random.randint(0,9999)
			path = "mods/utils/images/other/tempimg{}.jpg".format(i)
			rep = [["-","--"],["_","__"],["?","~q"],["%","~p"],[" ","%20"],["''","\""]]
			for i in rep:
				line1 = line1.replace(i[0],i[1])
				line2 = line2.replace(i[0],i[1])
			if not style:
				link = "http://memegen.link/{0}/{1}/{2}.jpg".format(meme,line1,line2)
			else:
				link = "http://memegen.link/{0}/{1}/{2}.jpg?alt={3}".format(meme,line1,line2,style)
			await download(link,path)
			await self.bot.send_file(ctx.message.channel,path)
			os.remove(path)

	@meme.command(name="custom",pass_context=True)
	async def _custom(self,ctx,pic:str,line1:str,line2:str):
		"""Generates a meme using a custom picture."""
		if not ".gif" in pic[-5:]:
			i = random.randint(0,9999)
			path = "mods/utils/images/other/tempimg{}.jpg".format(i)
			rep = [["-","--"],["_","__"],["?","~q"],["%","~p"],[" ","%20"],["''","\""]]
			for i in rep:
				line1 = line1.replace(i[0],i[1])
				line2 = line2.replace(i[0],i[1])
			link = "http://memegen.link/custom/{0}/{1}.jpg?alt={2}".format(line1,line2,pic)
			await download(link,path)
			await self.bot.send_file(ctx.message.channel,path)
			os.remove(path)
		else:
			await self.bot.say("You can't use gifs for memes!")

	@meme.command(name="user",pass_context=True)
	async def _user(self,ctx,user:discord.User,line1:str,line2:str):
		"""Generates a meme on a users avatar."""
		i = random.randint(0,9999)
		path = "mods/utils/images/other/tempimg{}.jpg".format(i)
		rep = [["-","--"],["_","__"],["?","~q"],["%","~p"],[" ","%20"],["''","\""]]
		for i in rep:
			line1 = line1.replace(i[0],i[1])
			line2 = line2.replace(i[0],i[1])
		link = "http://memegen.link/custom/{0}/{1}.jpg?alt={2}".format(line1,line2,user.avatar_url)
		await download(link,path)
		await self.bot.send_file(ctx.message.channel,path)
		os.remove(path)

	@meme.group(name="templates",pass_context=True,invoke_without_command=True)
	async def _templates(self,ctx):
		"""Gives users a list of meme templates."""
		await self.bot.say("All stock templates can be found here: <{}>".format("http://memegen.link/templates/"))

	@_templates.command(name="search",pass_context=True)
	async def __search(self,ctx,searchtype,*,query):
		"""Searches the current usable meme templates.

			Don't put in searchtype and query for a list of search types."""
		searchtype, query == None
		if not searchtype and not query:
			await self.bot.say("Search types include:\nName: Searches for the meme code of a meme.\nExample: Gives an example version of the given meme code.\nAliases: Lists the possible alias meme codes for a meme.\nStyles: Lists alternate styles for a meme.")
		if searchtype == "name":
			url = "http://memegen.link/templates/"
			query = query.title()
			query = query.replace("'A","'a").replace("'R","'r").replace("'S","'s").replace("'M","'m")
			with aiohttp.ClientSession() as session:
				async with session.get(url) as resp:
					resp = await resp.json()
			with open("mods/utils/json/fun/memenames.json","w") as f:
				f.seek(0)
				f.write(json.dumps(resp))
				f.truncate()
			with open("mods/utils/json/fun/memenames.json") as f:
				names = json.load(f)
			if query in names:
				q = names[query]
				await self.bot.say(q[30:])
			else:
				await self.bot.say("That isn't a real meme!")
		if searchtype == "example":
			i = random.randint(0,9999)
			path = "mods/utils/images/other/tempimg{}.jpg".format(i)
			link = "http://memegen.link/{0}/your-text/goes-here.jpg".format(query)
			await download(link,path)
			await self.bot.send_file(ctx.message.channel,path)
			os.remove(path)
		if searchtype == "aliases":
			url = "http://memegen.link/templates/{}".format(query)
			with aiohttp.ClientSession() as session:
				async with session.get(url) as resp:
					resp = await resp.json()
			if len(resp["aliases"]) > 1:
				await self.bot.say("Aliases for {0} are `".format(query) + ", ".join(map(str,resp["aliases"] + "`")))
			else:
				await self.bot.say("There are no aliases for this meme.")
		if searchtype == "styles":
			url = "http://memegen.link/templates/{}".format(query)
			with aiohttp.ClientSession() as session:
				async with session.get(url) as resp:
					resp = await resp.json()
			if len(resp["styles"]) > 0:
				await self.bot.say("Alternative styles for {0} are `".format(query) + ", ".join(map(str,resp["styles"])) + "`")
			else:
				await self.bot.say("There are no alternative styles for this meme.")

	@commands.group(pass_context=True,invoke_without_command=True)
	async def ascii(self,ctx,text:str,font:str,textcolor='',background=''):
		"""Creates ASCII text."""
		if ctx.invoked_subcommand is None:
			if not textcolor:
				textcolor = "white"
			if not background:
				background = "black"
			if font == "barbwire":
				text = text.replace(""," ")
			img = Image.new('RGB', (2000, 1000))
			d = ImageDraw.Draw(img)
			d.text((20, 20), figlet_format(text, font=font), fill=(255, 0, 0))
			text_width, text_height = d.textsize(figlet_format(text, font=font))
			img1 = Image.new('RGB', (text_width + 30, text_height + 30),background)
			d = ImageDraw.Draw(img1)
			d.text((20, 20), figlet_format(text, font=font), fill=textcolor, anchor="center")
			text_width, text_height = d.textsize(figlet_format(text, font=font))
			img1.save("mods/utils/images/other/ascii.png")
			await self.bot.send_file(ctx.message.channel,"mods/utils/images/other/ascii.png")

	@ascii.command(name="fonts",pass_context=True)
	async def _fonts(self,ctx):
		"""Lists available ASCII fonts."""
		await self.bot.say("All available fonts for the command can be found here: http://www.figlet.org/examples.html")
		
	@commands.command(pass_context=True)
	async def wiki(self,ctx,query:str):
		"""Searches wikipedia."""
		try:
			q = wikipedia.page(query)
			await self.bot.say("{}:\n```\n{}\n```\nFor more information, visit <{}>".format(q.title,wikipedia.summary(query, sentences=5),q.url))
		except wikipedia.exceptions.PageError:
			await self.bot.say("Either the page doesn't exist, or you typed it in wrong. Either way, please try again.")

	@commands.command(pass_context=True)
	async def whoosh(self,ctx):
		"""Whoosh!"""
		await self.bot.say("http://i2.kym-cdn.com/photos/images/newsfeed/000/992/402/c35.gif")

	@commands.command(pass_context=True)
	async def encode(self,ctx,encoder:int,*,message:str):
		"""Encodes messages."""
		if encoder not in {16,32,64}:
			await self.bot.say("You can only encode in 16, 32, and 64!")
		else:
			if encoder == 16:
				encode = base64.b16encode(message.encode())
			if encoder == 32:
				encode = base64.b32encode(message.encode())
			if encoder == 64:
				encode = base64.b64encode(message.encode())
			await self.bot.say(encode.decode())

	@commands.command(pass_context=True)
	async def decode(self,ctx,decoder:int,*,message:str):
		"""Decodes messages."""
		if decoder not in {16,32,64}:
			await self.bot.say("You can only decode in 16, 32, and 64!")
		else:
			if decoder == 16:
				decode = base64.b16decode(message.encode())
			if decoder == 32:
				decode = base64.b32decode(message.encode())
			if decoder == 64:
				decode = base64.b64decode(message.encode())
			await self.bot.say(decode.decode())

	@commands.command(pass_context=True)
	async def tried(self,ctx):
		"""At least you tried."""
		await self.bot.send_file(ctx.message.channel, "mods/utils/images/other/At least you tried.png")

	@commands.command(pass_context=True)
	async def goldstar(self,ctx):
		"""You get a gold star!"""
		await self.bot.send_file(ctx.message.channel, "mods/utils/images/other/goldstar.png", content="You get a gold star!")

	@commands.command(pass_context=True)
	async def out(self,ctx,num:int=randint(1,2)):
		"""Fuck this shit I'm out."""
		outlist = {1:"https://www.youtube.com/watch?v=5FjWe31S_0g",2:"https://cdn.discordapp.com/attachments/81402706320699392/184995277332152321/tumblr_inline_o52a1n6vy21s4jhgf_5001.gif"}
		await self.bot.say(outlist[num])

	@commands.command(pass_context=True)
	async def shame(self,ctx):
		"""Let the shame bells ring!"""
		await self.bot.say('🔔🔔🔔 ​ ​ ​ ​ ​ ​ ​🔔 ​ ​ ​ ​ ​ ​ ​🔔 ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​🔔 ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​🔔 ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​🔔 ​ ​ ​ ​ ​ ​🔔🔔🔔\n🔔 ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​🔔 ​ ​ ​ ​ ​ ​ ​🔔 ​ ​ ​ ​ ​ ​ ​🔔 ​ ​ ​ ​ ​ ​ ​🔔 ​ ​ ​ ​ ​ ​ ​🔔🔔🔔🔔 ​ ​ ​ ​ ​ ​🔔\n🔔🔔🔔 ​ ​ ​ ​ ​ ​ ​🔔🔔🔔 ​ ​ ​ ​ ​ ​ ​🔔🔔🔔 ​ ​ ​ ​ ​ ​ ​🔔 ​ ​🔔 ​ ​ ​ ​🔔 ​ ​ ​ ​ ​ ​ ​🔔🔔🔔\n ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​🔔 ​ ​ ​ ​ ​ ​ ​🔔 ​ ​ ​ ​ ​ ​ ​🔔 ​ ​ ​ ​ ​ ​ ​🔔 ​ ​ ​ ​ ​ ​ ​🔔 ​ ​ ​ ​ ​ ​ ​🔔 ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​🔔 ​ ​ ​ ​ ​ ​ ​🔔\n🔔🔔🔔 ​ ​ ​ ​ ​ ​ ​🔔 ​ ​ ​ ​ ​ ​ ​🔔 ​ ​ ​ ​ ​ ​ ​🔔 ​ ​ ​ ​ ​ ​ ​🔔 ​ ​ ​ ​ ​ ​ ​🔔 ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​ ​🔔 ​ ​ ​ ​ ​ ​ ​🔔🔔​🔔')

	@commands.command(pass_context=True)
	async def discrim(self,ctx,discrim:int=None):
		if discrim is not None:
			discrim = discrim
		else:
			discrim = int(ctx.message.author.discriminator)
		await self.bot.say(discrim)
		disc = []
		for server in self.bot.servers:
			for member in server.members:
				if int(member.discriminator) == discrim:
					if not member.name in disc:
						disc.append(member.name)
		await self.bot.say(wrap.format(", ".join(disc)))

def setup(bot):
	bot.add_cog(Fun(bot))