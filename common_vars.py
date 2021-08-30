import imports

bot = commands.Bot(command_prefix='s!', owner_id='AnbjoWYA') 
snipe_messages = {} # "channel.id": ["author.id", "message.id", "datetime"]
snipe_channels = [] # a list with the channels currently available for `snipe`
editsnipe_messages = {} # "channel.id": ["author.id", "message.id", "datetime"]
editsnipe_channels = [] # a list with the channels currently available for `editsnipe`
money = {} # in the format: user.id : cash
claimed_daily = [] # contains id's of people who have already claimed their daily
token_for_gist = os.environ.get("token_for_gist")
database_id = "a7bd641039a0deb6601f9aacf9b662b3"
headers_for_db = {'Authorization': f'token {token_for_gist}'}

def get_money():
	r = requests.get('https://api.github.com/gists', headers=headers_for_db) 
	pairs = r.json()[0]
	print(pairs)
	return pairs.get("files").get("money.txt").get("raw_url")

def push_money():
	r = requests.patch('https://api.github.com/gists/' + database_id data=json.dumps({'files':{"money.txt":{"content":str(money).replace("'", "\"")}}}),headers=headers_for_db) 

def get_daily():
	r = requests.get('https://api.github.com/gists', headers=headers) 
	pairs = r.json()[0]
	print(pairs)
	return pairs.get("files").get("claimed_daily.txt").get("raw_url")

def push_daily():
	r = requests.patch('https://api.github.com/gists/' + database_id, data=json.dumps({'files':{"claimed_daily.txt":{"content":str(claimed_daily).replace("[", " ").replace("]", " ").replace(",", " ").replace("\'", " ").replace("\"", " ")}}}),headers=headers_for_db)
	
def convert_time(time):
	if int(time[:2]) >= 12:
		a = len(time)
		return f"{str(int(time[:2]) - 12)}:{time[3:-(a-5)]} PM"
	else:
		return f"{time} AM"
	
async def register_in_money_db(memberid):
	money[memberid] = 100
	push_money()
