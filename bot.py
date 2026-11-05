import telebot
import requests

BOT_TOKEN = "8661409339:AAELN6QYZHcP4MPWlL9Ctm1Bc72W2ailPkk" # Put your BotFather token here
API_BASE = "https://ff-player-backend-five.vercel.app/api" # Put your Vercel URL here

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    text = (
        "🤖 Welcome To Free Fire Info Bot\n\n"
        "Available Commands:\n\n"
        "├── Player Commands\n"
        "│   ├── /get [uid] – Full Player Information\n"
        "│   └── /search [name] – Search Players By Nickname\n"
        "│\n"
        "└── Token Commands\n"
        "    ├── /token [uid] [password] – Generate Guest Token\n"
        "    └── /decode [token] – Decode JWT Token\n"
    )
    bot.reply_to(message, text)

@bot.message_handler(commands=['get'])
def get_player(message):
    args = message.text.split()
    if len(args) != 2:
        bot.reply_to(message, "Usage: /get [uid]")
        return
    
    uid = args[1]
    
    try:
        res = requests.get(f"{API_BASE}/player/{uid}")
        
        if res.status_code == 200:
            d = res.json()
            text = (
                f"Player Information:\n"
                f"├── Basic Information:\n"
                f"│   ├── Name: {d['basic']['name']}\n"
                f"│   ├── Uid: {d['basic']['uid']}\n"
                f"│   ├── Region: {d['basic']['region']}\n"
                f"│   ├── Level: {d['basic']['level']} (Exp: {d['basic']['exp']})\n"
                f"│   └── Title: {d['basic']['title']}\n"
                f"│\n"
                f"├── Activity Information:\n"
                f"│   ├── Gender: {d['activity']['gender']}\n"
                f"│   ├── Br Rank: {d['activity']['br_rank']}\n"
                f"│   ├── Cs Rank: {d['activity']['cs_rank']}\n"
                f"│   └── Last Login: {d['activity']['last_login']}\n"
                f"│\n"
                f"└── Guild Information:\n"
                f"    ├── Guild ID: {d['guild']['id']}\n"
                f"    ├── Guild Name: {d['guild']['name']}\n"
                f"    ├── Guild Level: {d['guild']['level']}\n"
                f"    └── Live Members: {d['guild']['members']}\n"
            )
            bot.reply_to(message, text)
        else:
            bot.reply_to(message, "❌ Player not found or API error.")
            
    except Exception as e:
        bot.reply_to(message, f"❌ Error: {e}")

print("Bot is running...")
bot.infinity_polling()