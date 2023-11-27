from pytgbot import Bot


from some import API_KEY, CHATfortest

bot = Bot(API_KEY)

# sending messages:
bot.send_message(CHATfortest, "Example Text!")

# getting events:
for x in bot.get_updates():
	print(x)
