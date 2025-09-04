import threading
import time
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, Filters
from telegram.error import NetworkError, TelegramError

# ============================ CONFIGURATION ============================

BOT_TOKENS = [
    "8173936619:AAGVx9jkEyxEGCzrmr5m2hRhhmoj1Igco_U",
    "8007675359:AAHndiJx_jy7Tj1AeKEoxCc38REFs8G7WKE",
    "8030922476:AAGUYae1baYED_nWj3dm1suBNCKEGrHCCUQ",
    "7947504375:AAHwvqubAO5mzGvXhdHcx7aaTIo7eNyHlAs",
    "8191691060:AAHGXI0ocqF4EPAZENJUmHS_mf_W46KiJ4k",
    "7934919219:AAHQunBTgAS0vTlrBIZSQJpKieeTCUrp2qk",
    "7598149868:AAFvkquuktXnbwaaxZ4C7iIlDP_WRX9V7TU",
    "7992504514:AAHCj0rhv07bncffiPcPQeKu3_AaKuOSrew",
    "8007983719:AAGqzBL5aOPDzUIABDReXsQTL7jklZOARfA",
    "7601863461:AAH-wZA45dU0o6P5IQXAypu4PKn88HVIYns",
    "7610897425:AAELqiLON_l8hYTI0GBpAzircwPFTR4ClA8",
    "7572039526:AAHhjL6qx_bYBCXngu47zMShySNgWqyw7X8",
    "7718053527:AAFQv-2lKHH_c5cO9KNyK2j9tAiDNMpWYWY",
    "8129855131:AAFilQgT_snSwapmLuAujSJ7DM-F89Ef2eY",
    "7907433370:AAEsGjsZmBchzG95VTezZCgVPkSoTxYz-LI",
    "7816732190:AAG40fAsduIWo1ofUN-c8OGwRbdBjZk2mDA",
    "7673246895:AAEn8fO3HlNJVwuvlDNO-P_veNGUfiy8uMY",
    "7808395585:AAEnNvuWRnZ-8mbtVw0OZ8Vz_McX2gNsBlw",
    "7638234020:AAEJG-V0GuGNInW3OLrVWK776onipCJa3tI",
    "7954855566:AAHMyiUB9J9IxGmPcx9g0FXqCoKHGK_1P80",
    "7764816416:AAFFqY25mpkJSoNHmxyGzx3agplIf8ayByc",
    "7474291094:AAGnz3QR0XQ9E-zTatlpEKEP0e4YPDT-5sw",
    "7889553659:AAFDzAsuC9ZFmrMXLILEILKCI1TO1Sr6xGg",
    "7982229981:AAGxK3_Zv-sol3lC5_ipQoGQ16vImGdyKzs",
    "8202240444:AAF9uUn6MMb7t9YudeQ-eAAtn_TTYwGrrgg",
    "8387978489:AAFMDDPareNBGag-63MNVUn6qu59iBJRF_U",
    "7777206379:AAGnCsL7hFDylg95j3aS6MJqme9--nq7ihU",
    "8147937098:AAE3Pw0pXm84hWA4xmonT2rpgBSYrrgCnG8",
    "7180804858:AAGaOm0bAw824sn34omtliFvLTolexzb2lE",
    "8413043844:AAH816ZIcNaldXftyE38Y7fhZjmOeWxmxfs",
    "8290160515:AAH-KES9qx3kBPvenC9dEwouNitZpFeN3H0",
    "8260434371:AAFfGjkUAqH-KsDTd6lGk8I65K-xKypBy3Y",
    "8257045931:AAHLNjtVXOBgR_zX15y_DinUMfetb1unC5g",
    "7768337024:AAGWE_IIKhMpLzxQk1zxcMHO--ShLDSpkZU",
    "7960285927:AAFYCBKL6VcxjDY6f-MzhjMuqALCbzOoINM",
    "8227148265:AAE0o0sDBYVVeoOiMrgDDjhgC8HODilNk9I",
    "8441058079:AAFgxFchhVkl9OjkYuKiGCjYnCXhDf9Rmcw",
    "8399467946:AAG305AHFc_MitsvVJ0f59QCS7W8br9yke0",
    "8458594855:AAEMxQzgYZptn_2H9W7lqu2Zmc7QI0KejlA",
    "8491333577:AAF5EfxhEwUTOVPLYslimT_tER9rk8bEgMk",
    "8352484447:AAHWDGCf0mavEkEzV4-sUm3UjyRQNp3j5dw",
    "8240050440:AAGb9AferoVyY86UVAbCMGOkUHIni6AWir4",
    "7607025521:AAHcjh2Xii7HdjltSWlo65OpIyYeer9W0N0",
    "7219197593:AAHbFGjRgMowyIduqYdXZ8tgccrACJZnJ90",
    "7558117642:AAHVm51c3yP4Oo4olh4EEspym03bjqqMi1o",
    "8128689581:AAGa-Pq1j-kbdzGI1mOrFH7IDQBt3uOg1mU",
    "7991652207:AAE6w_HHQdqowMj1rgwQ4JOu_NliHxDeogE",
    "8347439584:AAEeIKnPwxek938pMdc-RRzeZBkbIzdur5c",
    "7586031319:AAHKDyzsW06JbIRIuKivlAL7wmbouc-2aFY",
    "8128906295:AAFKneahabzIiWdhNY1F2BFh_95_2iutTos",
    "8386622456:AAHB-_c5inOtKLbEkrWW7tmjW-iJSBgGL4s",
    "8326036553:AAGt0nPxttn3_t_CvzLRZibHRsGRDDeVg6o",
    "8493131165:AAH3go2zhG5J3Nk5L5h0xUMs_6AqHCYPFKY",
    "8323082269:AAGF-Gg5DvNWialVJdjhndSJDAkuPEd-m1g",
    "7242166594:AAFi7UCO7VqALf-YGPcPbPy4SJayMvuHg64",
    "8394014266:AAGJdup7Zo36EYH2VYDFllCRf-eEDy_NzCI",
    "8398379160:AAEwbJDzz3uhA81BC_KFk0fqnPm2Jl4Kvg0",
    "8231414735:AAF69oAx1vGZbtG6K5B8CIRyMV6h-pUMHvM",
    "8307816433:AAHd5e3vVMYMopnA2mmKffLmJjjxugIqCDM",
    "8364623417:AAEX3Xq7hfvSKZSjLN-2LsF8lxrEAc3qA64"
]

CHANNELS = [
    ("🔗 Channel 1", "https://t.me/+mhC8UwL8vz9kYzdl"),
    ("🔗 Channel 2", "https://t.me/+NacjClJwpOA3ODI1"),
    ("🔗 Channel 3", "https://t.me/+f-cuPnEQOW5iZGM1"),
    ("🔗 Channel 4", "https://t.me/+-Mbvy-yDiC9iZTg1")
]

# Store user data
user_data = {}
total_users = set()

# ============================ BOT HANDLERS ============================

logging.basicConfig(format='[%(levelname)s] %(message)s', filename='bot.log', level=logging.INFO)

def start(update: Update, context: CallbackContext):
    user = update.effective_user
    user_id = user.id
    total_users.add(user_id)
    user_data[user_id] = {
        'amount': None,
        'clicked_channels': set(),
        'verify_attempts': 0,
        'step': 'select_promocode'
    }
    name = user.first_name or "User"
    keyboard = [
        [InlineKeyboardButton("💸 ₹500", callback_data='500')],
        [InlineKeyboardButton("🏅 ₹100", callback_data='100')],
        [InlineKeyboardButton("❤️ ₹50", callback_data='50')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        f"*👋 Hello {name}!*\n\n"
        "*Welcome to the PromoCode & GiftCode Bot!* 🎁\n\n"
        "*नीचे से अपनी Promocode राशि चुने* 👇\n\n"
        "*Please join all the channels below to get your promocode:*",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

def promocode_selected(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = query.from_user.id
    query.answer()
    if user_id not in user_data:
        query.message.reply_text("*❌ Please start the bot with /start.*", parse_mode='Markdown')
        return
    context.user_data['amount'] = query.data
    user_data[user_id]['amount'] = query.data
    user_data[user_id]['step'] = 'join_channels'
    keyboard = [
        [InlineKeyboardButton(f"🔗 Join {title}", url=link, callback_data=f'click_{i}')]
        for i, (title, link) in enumerate(CHANNELS)
    ]
    keyboard.append([InlineKeyboardButton("✅ I Joined", callback_data='joined')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.message.reply_text(
        f"*Great!* You selected *₹{query.data}* 💸\n"
        "*Now please join all the channels to continue:* 👇",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

def track_channel_click(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = query.from_user.id
    query.answer()
    if user_id not in user_data:
        query.message.reply_text("*❌ Please start the bot with /start.*", parse_mode='Markdown')
        return
    channel_index = int(query.data.split('_')[1])
    channel_name = CHANNELS[channel_index][0]
    if channel_index not in user_data[user_id]['clicked_channels']:
        user_data[user_id]['clicked_channels'].add(channel_index)
        logging.info(f"User {user_id} clicked {channel_name} (Index: {channel_index})")
    query.message.reply_text(f"*✅ You clicked {channel_name}!* Please click all channels and then press *'I Joined'*.", parse_mode='Markdown')

def joined_check(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = query.from_user.id
    query.answer()
    if user_id not in user_data or user_data[user_id]['step'] != 'join_channels':
        query.message.reply_text("*❌ Please complete the previous steps first.*", parse_mode='Markdown')
        return
    user_data[user_id]['verify_attempts'] += 1
    logging.info(f"User {user_id} attempted verification (Attempt: {user_data[user_id]['verify_attempts']})")
    if user_data[user_id]['verify_attempts'] == 1:
        query.message.reply_text(
            "*❌ Verification Failed!*\nकृपया सभी चैनलों को पहले जॉइn करें, फिर *✅ I Joined* पर क्लिक करें। 🙏",
            parse_mode='Markdown'
        )
        return
    if user_data[user_id]['verify_attempts'] == 2:
        user_data[user_id]['step'] = 'share'
        keyboard = [[InlineKeyboardButton("📤 Share Now", switch_inline_query="🎁 *500 Rs Promocode Bot जल्दी आओ!* 🎉\n🔥 *Instant 500 Promocode* 🔥")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text(
            "*✅ Thanks for joining!*\n\n"
            "*🔄 Almost done!* Now share this with your friends to claim the promocode.",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
        def send_final():
            context.bot.send_message(
                chat_id=user_id,
                text="*✅ Thanks for sharing!*\n*Please wait 24 hours* ⏳.\n\n"
                     "*🔎 Your promocode will be verified and sent manually.*\n\n"
                     "*⚠️ अगर आपने सभी चैनल जॉइn नहीं किए हैं, तो आपको प्रमोकोड नहीं दिया जाएगा।*",
                parse_mode='Markdown'
            )
        threading.Timer(20.0, send_final).start()
    else:
        query.message.reply_text(
            "*❌ Verification Failed!*\nकृपया सभी चैनलों को पहले जॉइn करें, फिर *✅ I Joined* पर क्लिक करें। 🙏",
            parse_mode='Markdown'
        )

def run_bot(token, delay_seconds):
    time.sleep(delay_seconds)
    try:
        updater = Updater(token, use_context=True)
        dp = updater.dispatcher
        dp.add_handler(CommandHandler('start', start))
        dp.add_handler(CallbackQueryHandler(promocode_selected, pattern='^(500|100|50)$'))
        dp.add_handler(CallbackQueryHandler(track_channel_click, pattern='click_.*'))
        dp.add_handler(CallbackQueryHandler(joined_check, pattern='^joined$'))
        dp.add_handler(MessageHandler(Filters.text & ~Filters.command, lambda x, y: None))  # Empty handler
        updater.start_polling()
        logging.info(f"*✅ Bot started:* {token}")
        updater.idle()
    except (NetworkError, TelegramError) as e:
        logging.error(f"*❌ Bot failed:* {token} | *Reason:* {e}")
        time.sleep(10)
        run_bot(token, delay_seconds)

# Start all bots
for index, token in enumerate(BOT_TOKENS):
    delay = index * 3
    threading.Thread(target=run_bot, args=(token, delay)).start()
