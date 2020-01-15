from discord.ext import commands
from datetime import datetime
import aiohttp
import discord
import asyncio
import asyncpg
import json

with open('credentials.json') as f:
	credentials = json.load(f)

async def run():
	db = await asyncpg.create_pool(**credentials['Postgres'])
	bot = Bot(database=db)
	try:
		await bot.start(credentials['bot']['token'])
	except KeyboardInterrupt:
		await db.close()
		await bot.logout()	

class Bot(commands.Bot):
	def __init__(self, **kwargs):
		super().__init__(
			description    = "Football lookup bot by Painezor#8489",
			help_command = commands.DefaultHelpCommand(dm_help_threshold = 20),
			command_prefix = ".tb"
		)
		self.db = kwargs.pop("database")
		self.credentials = credentials	
		with open('config.json') as f:
			self.config = json.load(f)
		self.configlock = asyncio.Lock()
		self.timerlock = asyncio.Lock()

	async def on_ready(self):
		print(f'{self.user}: {datetime.now().strftime("%d-%m-%Y %H:%M:%S")}\n-----------------------------------------')
		if not hasattr(self, 'initialised_at'):
			self.initialised_at = datetime.utcnow()
		self.session = aiohttp.ClientSession(loop=self.loop)
		
		# Startup Modules
		load = [	
			'ext.admin','ext.fixtures','ext.fun','ext.images','ext.info',
			'ext.meta','ext.mod','ext.mtb','ext.nufc','ext.quotes',
			'ext.reactions','ext.scores', 'ext.sidebar','ext.timers','ext.twitter',
			'ext.transfers','ext.tv',
			
			'ext.notifications',
			'ext.aspg'
		]
		for c in load:
			try:
				self.load_extension(c)
			except Exception as e:
				print(f'Failed to load cog {c}\n{type(e).__name__}: {e}')		

loop = asyncio.get_event_loop()
loop.run_until_complete(run())	