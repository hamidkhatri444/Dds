DEVELOPER = "This File Is Made By @Laxxyplayzz" #DON'T CHANGE THIS WARNA ERROR AYEGA 100%

import telebot
import random
import string
import os
import threading
import time
import hashlib
import sys
import re
from datetime import datetime, timedelta
from flask import Flask # Added for web server integration

TOKEN = "8813651105:AAGylBFfx5_JejGpwL7SJE8gu_5Wxklu0zg"  
ADMIN_IDS = ["990627221"]      

bot = telebot.TeleBot(TOKEN) 
SCRIPT_NAME = "laxxy.py" 
FOOTER = "@MPYT_09" 

keys_db = {}
users_db = {}
active_attacks = {}
IS_SYSTEM_VERIFIED = False
MASTER_SECURITY_KEY = "LAXXY-BHAI-OP"

# --- FLASK WEB SERVER FOR RENDER HEALTH CHECKS ---
app = Flask('')

@app.route('/')
def home():
    return "Bot Core Engine is Online!", 200

@app.route('/healthz')
def health_check():
    return "OK", 200

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
# --------------------------------------------------

def generate_random_key(prefix="MODSKING-", length=8):
    chars = string.ascii_uppercase + string.digits 
    return prefix + ''.join(random.choice(chars) for _ in range(length))

# --- FIXED SECURITY GATEKEEPER ---
@bot.message_handler(func=lambda message: not IS_SYSTEM_VERIFIED, content_types=['text'])
def security_gatekeeper(message):
    global IS_SYSTEM_VERIFIED
    input_text = message.text.strip()

    if input_text == MASTER_SECURITY_KEY:
        IS_SYSTEM_VERIFIED = True
        msg = (
            f"🔓 <b>SECURITY VERIFIED!</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"✅ Master key accept ho gayi hai.\n"
            f"🚀 All bot commands are now fully unlocked.\n\n"
            f"<i>💡 Ab aap /start ya /help use kar sakte hain.</i>"
        )
        bot.reply_to(message, msg, parse_mode="HTML")
    else:
        # If someone tries to use a command while locked, tell them to unlock it
        msg = (
            f"🔒 <b>SYSTEM LOCKED</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"⚠️ Verification Required!\n"
            f"📝 Please enter the correct Master Security Key to unlock the bot commands."
        )
        bot.reply_to(message, msg, parse_mode="HTML")
        
@bot.message_handler(commands=['start'])
def start_cmd(message):
    user_id = str(message.chat.id) 
    msg = (
        f"🔥 <b>WELCOME TO MODSKING BOT</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🚀 <b>Status:</b> 🟢 Online\n"
        f"👤 <b>Your ID:</b> <code>{user_id}</code>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"👑 <b>Owner:</b> {FOOTER}\n\n"
        f"💡 <i>Use /help to see all available commands.</i>"
    ) 
    bot.reply_to(message, msg, parse_mode="HTML") 

@bot.message_handler(commands=['help'])
def help_cmd(message):
    msg = (
        f"🛠️ <b>MODSKING BOT - HELP MENU</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"ℹ️ <b>User Commands:</b>\n"
        f"🔹 /start  - Start / Activate Bot\n"
        f"🔹 /help   - View this control menu\n"
        f"🔹 /rules  - Check terms & restrictions\n"
        f"🔹 /myinfo - Check your profile & validity\n"
        f"🔹 /redeem - Redeem your access key\n"
        f"🔹 /bgmi   - Launch processing engine\n"
        f"🔹 /status - Check active system slots\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"👑 <b>Admin Controls:</b>\n"
        f"🔹 /admin  - Access authorized owner panel\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"👑 <b>Owner:</b> {FOOTER}"
    ) 
    bot.reply_to(message, msg, parse_mode="HTML") 

@bot.message_handler(commands=['rules'])
def rules_cmd(message):
    msg = (
        f"📜 <b>MODSKING BOT - OFFICIAL RULES</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"1️⃣ <b>System Use:</b> System ka sahi tarike se istemal karein.\n"
        f"2️⃣ <b>No Abuse/Spam:</b> Bot ko abuse ya commands spam bilkul na karein.\n"
        f"3️⃣ <b>Admin Authority:</b> Admin ke banaye gaye niyam sabhi par lagu hote hain.\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"✅ <i>Follow the protocol to avoid Ban!</i>"
    ) 
    bot.reply_to(message, msg, parse_mode="HTML") 

def verify_creator_rights():
    current_hash = hashlib.sha256(DEVELOPER.encode()).hexdigest()
    if current_hash != ATTACK:
        print("❌ ERROR: TERI FILE H KYA DEVELOPER KA NAM CHANGE KAREGA")
        sys.exit(1)

@bot.message_handler(commands=['myinfo'])
def myinfo_cmd(message):
    user_id = str(message.chat.id) 
    username = message.from_user.username if message.from_user.username else "No Username" 
    first_name = message.from_user.first_name if message.from_user.first_name else "User" 
    
    if user_id in users_db: 
        expiry_status = users_db[user_id] 
        role = "Authorized User" 
    elif user_id in ADMIN_IDS: 
        expiry_status = "Lifetime (Admin)" 
        role = "System Administrator" 
    else:
        expiry_status = "No Active Session" 
        role = "Guest" 

    info_text = (
        f"👤 <b>USER ACCOUNT PROTOCOL</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🔹 <b>First Name:</b> {first_name}\n"
        f"🔹 <b>Username:</b> @{username}\n"
        f"🔹 <b>User ID:</b> <code>{user_id}</code>\n"
        f"🔹 <b>Access Role:</b> {role}\n"
        f"🔹 <b>Expiration:</b> {expiry_status}\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🛰️ <i>System integration status: Active</i>"
    ) 
    bot.reply_to(message, info_text, parse_mode="HTML") 

@bot.message_handler(commands=['redeem'])
def redeem_cmd(message):
    user_id = str(message.chat.id)
    username = message.from_user.username if message.from_user.username else "None"
    cmd_args = message.text.split()
    
    if len(cmd_args) < 2:
        bot.reply_to(message, "💡 <b>Usage:</b> /redeem [YOUR_KEY]", parse_mode="HTML")
        return

    input_key = cmd_args[1]
    
    if input_key in keys_db:
        if keys_db[input_key]["status"] == "used":
            bot.reply_to(message, "❌ <b>Error:</b> Yeh key pehle hi redeem ho chuki hai.")
            return
            
        duration = keys_db[input_key]["duration"]
        
        if duration == 'all':
            expiry_time_str = "Lifetime Access"
        else:
            val = int(re.search(r'\d+', duration).group())
            unit = duration[-1]
            
            if unit == 'm': expiry_delta = timedelta(minutes=val)
            elif unit == 'h': expiry_delta = timedelta(hours=val)
            elif unit == 'd': expiry_delta = timedelta(days=val)
            elif unit == 'w': expiry_delta = timedelta(weeks=val)
            elif unit == 'y': expiry_delta = timedelta(days=val*365)
            
            expiry_time_str = (datetime.now() + expiry_delta).strftime('%Y-%m-%d %H:%M:%S')

        keys_db[input_key]["status"] = "used"
        keys_db[input_key]["used_by"] = user_id
        keys_db[input_key]["username"] = username
        users_db[user_id] = expiry_time_str
        
        msg = (
            f"✅ <b>KEY REDEEMED SUCCESSFULLY!</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🎫 <b>Key:</b> {input_key}\n"
            f"⏳ <b>Validity:</b> {expiry_time_str}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🚀 Aapka access instantly grant kar diya gaya hai."
        )
        bot.reply_to(message, msg, parse_mode="HTML")
    else:
        bot.reply_to(message, "❌ <b><i> Galat key mat dal </i></b>")

def simulation_worker(bot, chat_id, duration):
    time.sleep(duration)
    if chat_id in active_attacks:
        del active_attacks[chat_id]
        try:
            bot.send_message(chat_id, "✅ <b>Processing Session Completed!</b>\nYour background thread slot is now empty.", parse_mode="HTML")
        except Exception:
            pass

@bot.message_handler(commands=['bgmi'])
def bgmi_cmd(message):
    user_id = str(message.chat.id) 
    
    if (user_id not in users_db) and (user_id not in ADMIN_IDS): 
        bot.reply_to(message, "❌ <b>Access Denied!</b>\nAapke paas active subscription nahi hai. Please key /redeem karein.", parse_mode="HTML") 
        return

    cmd_args = message.text.split() 
    if len(cmd_args) < 4: 
        bot.reply_to(message, "💡 <b>Usage:</b> /bgmi [Target] [Port] [Time]\n📝 <i>Example: /bgmi 1.1.1.1 80 60</i>", parse_mode="HTML") 
        return

    target = cmd_args[1] 
    port = cmd_args[2] 
    
    try:
        duration = int(cmd_args[3]) 
        if duration > 180: 
            bot.reply_to(message, "⚠️ <b>Limit Exceeded!</b> Maximum duration 180 seconds allowed hai.") 
            return
    except ValueError:
        bot.reply_to(message, "❌ Duration hamesha ek number hona chahiye.") 
        return

    end_timestamp = time.time() + duration
    active_attacks[user_id] = {
        "target": target,
        "port": port,
        "end_time": end_timestamp,
        "total": duration
    }

    msg_text = (
        f"🚀 <b>SIMULATION ENGINE LAUNCHED</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🎯 <b>Target Host:</b> {target}\n"
        f"🔌 <b>Target Port:</b> {port}\n"
        f"⏳ <b>Time Limit:</b> {duration} Seconds\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🛰️ <i>Status: Processing simulation in background...</i>"
    ) 
    bot.reply_to(message, msg_text, parse_mode="HTML") 

    threading.Thread(target=simulation_worker, args=(bot, user_id, duration)).start()

ATTACK = "5e84b0c692c1e2630b6a3560ba746e46c01517fe7b9e4765bf88af638f2c6cff"
verify_creator_rights()

@bot.message_handler(commands=['admin'])
def admin_cmd(message):
    user_id = str(message.chat.id) 
    
    if user_id in ADMIN_IDS: 
        msg = (
            f"👑 <b>MODSKING MASTER - ADMIN PANEL</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🛠️ <b>Admin Commands List:</b>\n\n"
            f"🔹 /add_users [ID] [Days] - Add new user\n"
            f"🔹 /rm_users [ID] - Remove user access\n"
            f"🔹 /genkey [Duration] - Generate new key\n"
            f"🔹 /allkey - Show all generated keys\n"
            f"🔹 /delete_key [KEY] - Delete a key\n"
            f"🔹 /status - Monitor system instances\n"
            f"🔹 /details [KEY] - Check key redeemer info\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"⚙️ <i>Select a command above to manage the system.</i>"
        ) 
    else:
        msg = (
            f"❌ <b>ACCESS DENIED!</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"⚠️ This terminal is restricted to authorized owners only.\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"👤 <b>Your ID:</b> <code>{user_id}</code>"
        ) 
    bot.reply_to(message, msg, parse_mode="HTML") 

@bot.message_handler(commands=['add_users'])
def add_user_cmd(message):
    user_id = str(message.chat.id) 
    if user_id not in ADMIN_IDS: return 
    
    cmd_args = message.text.split() 
    if len(cmd_args) < 3: 
        bot.reply_to(message, "💡 <b>Usage:</b> /add_users [User_ID] [Days]", parse_mode="HTML") 
        return
    
    target_id = cmd_args[1] 
    try:
        days = int(cmd_args[2]) 
    except ValueError:
        bot.reply_to(message, "❌ Days ek number (digits) hona chahiye.") 
        return
        
    expiry_time = datetime.now() + timedelta(days=days) 
    users_db[target_id] = expiry_time.strftime('%Y-%m-%d %H:%M:%S') 
    bot.reply_to(message, f"✅ <b>User Authorized!</b>\n🆔 ID: {target_id}\n📅 Validity: {days} Days", parse_mode="HTML") 

@bot.message_handler(commands=['rm_users'])
def rm_user_cmd(message):
    user_id = str(message.chat.id) 
    if user_id not in ADMIN_IDS: return 

    cmd_args = message.text.split() 
    if len(cmd_args) < 2: 
        bot.reply_to(message, "💡 <b>Usage:</b> /rm_users [User_ID]", parse_mode="HTML") 
        return

    target_id = cmd_args[1] 
    if target_id in users_db: 
        del users_db[target_id] 
        bot.reply_to(message, f"🗑️ User {target_id} access removed successfully.", parse_mode="HTML") 
    else:
        bot.reply_to(message, "❌ Yeh user access database mein nahi mila.") 

@bot.message_handler(commands=['genkey'])
def genkey_cmd(message):
    user_id = str(message.chat.id) 
    if user_id not in ADMIN_IDS: return 

    cmd_args = message.text.split() 
    if len(cmd_args) < 2: 
        bot.reply_to(message, "💡 <b>Usage:</b> /genkey [time+unit / all]\n📝 <i>Examples: /genkey 5h, /genkey 30m, /genkey 15d, /genkey all</i>", parse_mode="HTML") 
        return

    duration = cmd_args[1].lower() 
    
    if duration != 'all': 
        if not re.match(r"^\d+[mhdwy]$", duration): 
            bot.reply_to(message, "❌ <b>Invalid format!</b>\nUse digits followed by m, h, d, w, y (e.g., 5h, 45m, 7d) or use all for lifetime.", parse_mode="HTML") 
            return

    new_key = generate_random_key() 
    keys_db[new_key] = {
        "duration": duration, 
        "status": "unused", 
        "used_by": None, 
        "username": None 
    }

    msg = (
        f"🔑 <b>KEY GENERATED SUCCESSFULLY</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"⏳ <b>Duration:</b> {duration.upper()}\n"
        f"🎫 <b>Key:</b> <code>{new_key}</code>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"📋 <i>Tap on the key above to copy it instantly.</i>"
    ) 
    bot.reply_to(message, msg, parse_mode="HTML") 

CREATOR = "This File Is Made By @Laxxyplayzz" #DON'T CHANGE THIS WARNA ERROR AYEGA 100%

@bot.message_handler(commands=['allkey'])
def allkey_cmd(message):
    user_id = str(message.chat.id) 
    if user_id not in ADMIN_IDS: return 

    if not keys_db: 
        bot.reply_to(message, "📋 Database me koi key records available nahi hain.") 
        return

    msg = "📋 <b>ALL GENERATED KEYS LIST</b>\n━━━━━━━━━━━━━━━━━━━━━━\n" 
    for key, data in keys_db.items(): 
        status_emoji = "🟢" if data['status'] == "unused" else "🔴" 
        msg += f"{status_emoji} <code>{key}</code> | <b>Time:</b> {data['duration'].upper()} | <b>Status:</b> {data['status']}\n" 
    
    bot.reply_to(message, msg, parse_mode="HTML") 

@bot.message_handler(commands=['delete_key'])
def delete_key_cmd(message):
    user_id = str(message.chat.id) 
    if user_id not in ADMIN_IDS: return 

    cmd_args = message.text.split() 
    if len(cmd_args) < 2: 
        bot.reply_to(message, "💡 <b>Usage:</b> /delete_key [KEY]", parse_mode="HTML") 
        return

    target_key = cmd_args[1] 
    if target_key in keys_db: 
        del keys_db[target_key] 
        bot.reply_to(message, f"🗑️ Key <code>{target_key}</code> permanently deleted from database.", parse_mode="HTML") 
    else:
        bot.reply_to(message, "❌ Yeh key records me nahi mili.") 

@bot.message_handler(commands=['status'])
def status_cmd(message):
    user_id = str(message.chat.id)
    if user_id not in ADMIN_IDS: return

    total_active = len(active_attacks)
    current_time = time.time()
    
    msg = (
        f"📊 <b>LIVE SYSTEM MONITOR PANEL</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🛰️ <b>Active Slots:</b> [{total_active}/10]\n"
        f"🟢 <b>Core Engine:</b> Operational\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
    )
    
    if total_active == 0:
        msg += "<i>✨ All slots are empty. System load is 0%.</i>\n"
    else:
        msg += "⚡ <b>Active Instances Load:</b>\n\n"
        for idx, (chat_id, data) in enumerate(active_attacks.items(), 1):
            remaining = int(data["end_time"] - current_time)
            if remaining <= 0:
                continue
                
            total = data["total"]
            elapsed = total - remaining
            percentage = int((elapsed / total) * 100)
            if percentage > 100: percentage = 100
            if percentage < 0: percentage = 0
            
            filled_blocks = int(percentage / 10)
            empty_blocks = 10 - filled_blocks
            progress_bar = "■" * filled_blocks + "□" * empty_blocks
            
            msg += (
                f"🔹 <b>SLOT [{idx}] DETAILS</b>\n"
                f"🎯 <b>Target:</b> {data['target']} : {data['port']}\n"
                f"⏳ <b>Time Left:</b> {remaining}s / {total}s\n"
                f"📈 <b>Progress:</b> [{progress_bar}] <b>{percentage}%</b>\n"
                f"━━━━━━━━━━━━━━━━━━━━━━\n"
            )
            
    msg += f"👑 <b>Console:</b> {FOOTER}"
    bot.reply_to(message, msg, parse_mode="HTML")

@bot.message_handler(commands=['details'])
def details_cmd(message):
    user_id = str(message.chat.id) 
    if user_id not in ADMIN_IDS: return 

    cmd_args = message.text.split() 
    if len(cmd_args) < 2: 
        bot.reply_to(message, "💡 <b>Usage:</b> /details [KEY]", parse_mode="HTML") 
        return

    target_key = cmd_args[1] 
    if target_key in keys_db: 
        data = keys_db[target_key] 
        if data['status'] == "used": 
            msg = (
                f"👤 <b>REDEEMED KEY DETAILS</b>\n"
                f"━━━━━━━━━━━━━━━━━━━━━━\n"
                f"🎫 <b>Key:</b> <code>{target_key}</code>\n"
                f"⏳ <b>Plan Type:</b> {data['duration'].upper()}\n"
                f"🆔 <b>User ID:</b> <code>{data['used_by']}</code>\n"
                f"👤 <b>Username:</b> @{data['username'] if data['username'] else 'None'}\n"
                f"━━━━━━━━━━━━━━━━━━━━━━"
            ) 
        else:
            msg = f"ℹ️ Key <code>{target_key}</code> abhi tak kisi ne <b>Redeem nahi ki hai</b> (🟢 Unused)." 
    else:
        msg = "❌ Records me yeh key nahi mili." 

    bot.reply_to(message, msg, parse_mode="HTML") 

CREATOR = "This File Is Made By @Laxxyplayzz" #DON'T CHANGE THIS WARNA ERROR AYEGA 100%

if __name__ == "__main__":
    print(f"🚀 Starting {SCRIPT_NAME} framework...") 
    
    print("[+] Launching background web proxy for Render health checks...")
    threading.Thread(target=run_web_server, daemon=True).start()
    
    while True:
        try:
            bot_info = bot.get_me() 
            print(f"[+] Bot started successfully! Username: @{bot_info.username}") 
            bot.polling(none_stop=True, interval=0, timeout=20) 
        except Exception as e:
            print(f"[!] Error: {e}. Reconnecting system in 5 seconds...") 
            time.sleep(5)
