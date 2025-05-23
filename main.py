import telebot
from pyexpat.errors import messages
from telebot import types
from telebot.types import (InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReactionTypeEmoji)
import time
import datetime
import platform
from datetime import datetime
import jdatetime
import os
from flask import Flask, request,Response
import random
import pytz


TOKEN = "7579645804:AAF-Cy5brD6ZJabsLJ4JFlvt-Q5FPssM-yE"
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

CHANNEL_USERNAME = "rap_family1"  

def is_user_member(user_id):
    try:
        member = bot.get_chat_member(chat_id=f"@{CHANNEL_USERNAME}", user_id=user_id)
        return member.status in ['member', 'administrator', 'creator']
    except Exception as e:
        print(f"خطا در بررسی عضویت: {e}")
        return False

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    if is_user_member(user_id):
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(KeyboardButton("لیست"))
        bot.send_message(
            message.chat.id,
            'سلام، من علی بات 🤖 هستم.\n\n'
            '✅ شما در کانال عضو هستید و می‌توانید از ربات استفاده کنید.\n\n'
            'برای مشاهده قابلیت‌ها، دکمه «لیست» را بزن یا تایپ کن.',
            parse_mode="HTML",
            reply_markup=keyboard
        )
    else:
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("عضویت در کانال", url=f"https://t.me/{CHANNEL_USERNAME}"))
        bot.send_message(
            message.chat.id,
            '❌ شما در کانال عضو نیستید.\n\n'
            'لطفاً ابتدا عضو شوید و سپس کلمه «لیست» را ارسال کنید.',
            parse_mode="HTML",
            reply_markup=markup
        )

@bot.message_handler(func=lambda message: message.text.strip().lower() == 'لیست')
def send_features(message):
    user_id = message.from_user.id
    if is_user_member(user_id):
        features = [
            'ارتباط با ما',
            'مدیریت گروه',
            'بیوگرافی',
            'جوک',
            'اصطلاحات انگلیسی',
        ]
        msg = "\n".join(f"- {f}" for f in features)
        bot.send_message(message.chat.id, "لیست قابلیت‌های ربات:\n\n" + msg)
    else:
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("عضویت در کانال", url=f"https://t.me/{CHANNEL_USERNAME}"))
        bot.send_message(
            message.chat.id,
            '❌ لطفاً ابتدا در کانال عضو شوید و سپس «لیست» را ارسال کنید.',
            parse_mode="HTML",
            reply_markup=markup
        )

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = telebot.types.Update.de_json(request.data.decode("utf-8"))
    bot.process_new_updates([update])
    return '', 200

@app.route("/")
def index():
    return "ربات فعال است"

# تنظیم وب‌هوک فقط یک‌بار دستی انجام بده یا با curl:
# https://api.telegram.org/bot<توکن>/setWebhook?url=https://your-app.onrender.com/<توکن>


    
weekday_names = {
    'Saturday': 'شنبه',
    'Sunday': 'یک‌شنبه',
    'Monday': 'دوشنبه',
    'Tuesday': 'سه‌شنبه',
    'Wednesday': 'چهارشنبه',
    'Thursday': 'پنج‌شنبه',
    'Friday': 'جمعه'
}

month_names = {
    'Farvardin': 'فروردین',
    'Ordibehesht': 'اردیبهشت',
    'Khordad': 'خرداد',
    'Tir': 'تیر',
    'Mordad': 'مرداد',
    'Shahrivar': 'شهریور',
    'Mehr': 'مهر',
    'Aban': 'آبان',
    'Azar': 'آذر',
    'Dey': 'دی',
    'Bahman': 'بهمن',
    'Esfand': 'اسفند'
}

@bot.message_handler(func=lambda message: message.text.strip().lower() == 'زمان')
def send_jalali_datetime(message):
    iran_time = datetime.now(pytz.timezone('Asia/Tehran'))
    shamsi_time = jdatetime.datetime.fromgregorian(datetime=iran_time)

    weekday_en = shamsi_time.strftime('%A')     # مثلاً Saturday
    month_en = shamsi_time.strftime('%B')       # مثلاً Farvardin

    weekday_fa = weekday_names.get(weekday_en, weekday_en)
    month_fa = month_names.get(month_en, month_en)

    date_str = f"{shamsi_time.day} {month_fa} {shamsi_time.year}"
    time_str = shamsi_time.strftime('%H:%M:%S')

    response = f'{weekday_fa} {date_str} \n\nزمان: {time_str}'
    bot.reply_to(message, f'تاریخ 📅 و زمان ⏰ فعلی:\n\n{response}')

CHANNEL_USERNAME = 'rap_family1'


reply_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
reply_keyboard.add('ارتباط با ما📞 ', 'مدیریت گروه🤵‍♂️', 'بیوگرافی🗨️', 'اصطلاحات انگلیسی🔠', 'جوک😄', 'زبان هخامنشی𐎠', 'فونت اسم♍', 'جرعت حقیقت❔', 'دانستنی⁉️')


@bot.message_handler(func=lambda message: message.text.strip().lower() == 'زمان')
def send_jalali_datetime(message):
    now = jdatetime.datetime.now()
    weekday_name = now.strftime('%A')  # نام روز هفته به فارسی
    date_str = now.strftime('%d %B %Y')  # تاریخ به‌صورت متنی
    time_str = now.strftime('%H:%M:%S')  # زمان فعلی
    response = f'{weekday_name} {date_str} \n\nزمان: {time_str}'
    bot.reply_to(message, f'  تاریخ 📅 و زمان ⏰ فعلی:\n\n{response}')


# حروف فارسی به حروف میخی
farsi_to_cuneiform = {
    'ا': '𐎠', 'آ': '𐎠', 'ب': '𐎲', 'پ': '𐎱', 'ت': '𐎫', 'ث': '𐎰', 'تو': '𐎬', 'طو': '𐎬', 'ج': '𐎢', 'جی': '𐎪', 'چ': '𐎨', 'ح': '𐏃', 'خ': '𐎧',
    'د': '𐎭', 'دی': '𐎮', 'دو': '𐎯', 'ذ': '𐏀', 'ر': '𐎼', 'رو': '𐎽', 'ز': '𐏀', 'س': '𐎿', 'ش': '𐎤', 'ص': '𐎿', 'ض': '𐏀', 'ط': '𐎫', 'ظ': '𐏀', 'ع': '𐎠', 'غ': '𐎥', 'ک': '𐎣',
    'کو': '𐎤', 'قو': '𐎦', 'گ': '𐎥', 'م': '𐎶', 'مو': '𐎸', 'می': '𐎷', 'ن': '𐎴', 'نو': '𐎵', 'و': '𐎺', 'وی': '𐎻', 'ه': '𐎱', 'ی': '𐎡',
    'ف': '𐎳', 'ق': '𐎨', 'ل': '𐎾'
}

# تابع تبدیل
def convert_to_cuneiform(text):
    return ''.join(farsi_to_cuneiform.get(ch, ch) for ch in text)

# شروع
@bot.message_handler(func= lambda m: m.text == 'زبان هخامنشی𐎠')
def hakhmaneshi(message):
    bot.send_message(message.chat.id, "یک متن فارسی بفرست تا برات به خط میخی هخامنشی تبدیل کنم")
    bot.register_next_step_handler(message, handle_text)
    
def handle_text(message):
    original = message.text
    converted = convert_to_cuneiform(original)
    bot.reply_to(message, f"متن میخی:\n{converted}")   
    bot.send_message(message.chat.id, 'برای اینکه متن جدیدی را وارد کنید\n\nمجددا کلمه <b>زبان هخامنشی𐎠</b>را ارسال کنید', parse_mode="HTML")

 
@bot.message_handler(content_types=['document', 'audio'])
def handle_docs_audio(message):
    if message.audio:
        bot.reply_to(message, 'این یک فایل صوتی🎛️ هست')
    elif message.document:
        bot.reply_to(message, 'این یک سند📄 هست')  

@bot.message_handler(content_types=['photo'])    
def handle_photo(message):
    if message.photo:
        bot.reply_to(message, 'این یک تصویر🖼️ هست')
        
@bot.message_handler(content_types=['video'])    
def handle_photo(message):
    if message.video:
        bot.reply_to(message, 'این یک ویدیو📽️ هست')



@bot.message_handler(content_types=['new_chat_members'])
def welcome_new_member(message):
    for new_member in message.new_chat_members:
        welcome_text = f'🎉 کاربر @{message.from_user.username}\n خوش اومدی به گروه! 🎉'
        bot.send_message(message.chat.id, text=welcome_text)


@bot.message_handler(content_types=['left_chat_member'])
def handle_left_member(message):
    bot.reply_to(message, "به سلامت👋")


@bot.chat_join_request_handler(func=lambda r: True)
def approve(r):
    bot.approve_chat_join_request(r.chat.id, r.from_user.id)
    bot.send_message(
        r.chat.id, f" کاربر {r.from_user.first_name}\nدر گروه پذیرفته شد")

def is_user_admin(chat_id, user_id):
    admins = bot.get_chat_administrators(chat_id)
    for admin in admins:
        if admin.user.id == user_id:
            return True
    return False



@bot.message_handler(func=lambda m: m.text == 'پین')
def pin(m):
 chat_id = m.chat.id
 user_id = m.from_user.id
 
 if is_user_admin(chat_id, user_id):
     if m.reply_to_message:
         bot.pin_chat_message(m.chat.id, m.reply_to_message.id)
         bot.reply_to(m, "پیام مورد نظر پین شد")
     else:
        bot.reply_to(m, "برای پین کردن لطفا روی آن پیام ریپلای بزنین")
 else:
        bot.reply_to(m, 'فقط ادمین و مالک گروه میتونه پیامی رو پین کنه!')

 
@bot.message_handler(func=lambda m: m.text == 'حذف پین')
def unpin(m):
    bot.unpin_chat_message(m.chat.id, m.reply_to_message.id)
    bot.reply_to(m, 'پین پیام موردنظر حذف شد ')


@bot.message_handler(func=lambda m: m.text == 'افزودن ادمین')
def promote(m):
    bot.promote_chat_member(
        m.chat.id,
        m.reply_to_message.json['from']['id'],
        can_change_info=True,
        can_delete_messages=True,
        can_edit_messages=True,
        can_invite_users=True,
        can_manage_chat=True,
        can_manage_topics=False,
        can_manage_video_chats=True,
        can_manage_voice_chats=True,
        can_pin_messages=True,
        can_post_messages=True,
        can_promote_members=True,
        can_restrict_members=True,
    )
    bot.reply_to(m, 'ادمین جدید اضافه شد')


@bot.message_handler(func=lambda m: m.text == 'حذف ادمین')
def demote(m):
    bot.promote_chat_member(
        m.chat.id,
        m.reply_to_message.json['from']['id'],
        can_change_info=False,
        can_delete_messages=False,
        can_edit_messages=False,
        can_invite_users=False,
        can_manage_chat=False,
        can_manage_topics=False,
        can_manage_video_chats=False,
        can_manage_voice_chats=False,
        can_pin_messages=False,
        can_post_messages=False,
        can_promote_members=False,
        can_restrict_members=False,
    )
    bot.reply_to(m, 'ادمین از مقام برکنار شد ')


@bot.message_handler(func=lambda m: m.text == 'بن')
def ban(m):
 chat_id = m.chat.id
 user_id = m.from_user.id
 if is_user_admin(chat_id, user_id):
     if m.reply_to_message:
         bot.ban_chat_member(m.chat.id, m.reply_to_message.from_user.id)
         bot.reply_to(m, f" کاربر {m.reply_to_message.from_user.first_name} بن شد ")
     else:
        bot.reply_to(m, "برای بن کردن کاربر لطفا روی پیام  ریپلای بزنین")
 else:
     bot.reply_to(m, 'فقط ادمین و مالک گروه میتونه کاربری رو بن کنه!')
    


@bot.message_handler(func=lambda m: m.text == 'حذف بن')
def unban(m):
    bot.unban_chat_member(m.chat.id, m.reply_to_message.from_user.id)
    bot.reply_to(
        m, f" کاربر {m.reply_to_message.from_user.first_name} از لیست بن خارج شد ")


@bot.message_handler(func=lambda m: m.text == 'سکوت')
def restrict(m):
 chat_id = m.chat.id
 user_id = m.from_user.id
 if is_user_admin(chat_id, user_id):
     if m.reply_to_message:
        bot.restrict_chat_member(m.chat.id, m.reply_to_message.from_user.id, can_add_web_page_previews=False, can_change_info=False, can_invite_users=False,
                             can_pin_messages=False, can_send_media_messages=False, can_send_messages=False, can_send_other_messages=False, can_send_polls=False)
        bot.reply_to(m, 'کاربر موردنظر سکوت شد')
     else:
        bot.reply_to(m, "برای سکوت کردن کاربر لطفا روی پیام آن ریپلای بزنین")
 else:
        bot.reply_to(m, 'فقط ادمین و مالک گروه میتونه کاربری رو سکوت کنه!')

@bot.message_handler(func=lambda m: m.text == 'حذف سکوت')
def derestrict(m):
    bot.restrict_chat_member(m.chat.id, m.reply_to_message.from_user.id, can_add_web_page_previews=True, can_change_info=True, can_invite_users=True,
                             can_pin_messages=True, can_send_media_messages=True, can_send_messages=True, can_send_other_messages=True, can_send_polls=True)
    bot.reply_to(m, 'سکوت کاربر موردنظر حذف شد')


@bot.message_handler(func=lambda m: m.text == 'فونت اسم♍')
def text_formatting(m):
    bot.send_message(m.chat.id, "اسم را وارد کنید")
    bot.register_next_step_handler(m, process_text)


def process_text(m):
    text = m.text
    text1 = f"<b>➷➷☠{text}☠➶➶</b>"
    text2 = f"<i>¯°•º¤ϟϞ҂ ♛{text}♛ ҂Ϟϟ¤º•°¯ </i>"
    text3 = f"<ins>ıllıllı ⦳⦳{text}⦳⦳ ıllıllı</ins>"
    text4 = f"<s>ஜ۩۞۩ஜ ♬{text}♬ ஜ۩۞۩ஜ</s>"
    text5 = f"<code>╔╝✞ ஜ☣{text}☣ஜ ✞╚╗</code>"
   

    bot.send_message(m.chat.id, text1, parse_mode="HTML")
    bot.send_message(m.chat.id, text2, parse_mode="HTML")
    bot.send_message(m.chat.id, text3, parse_mode="HTML")
    bot.send_message(m.chat.id, text4, parse_mode="HTML")
    bot.send_message(m.chat.id, text5, parse_mode="HTML")
   


@bot.message_handler(func=lambda m: m.text.startswith('سکوت تایمری'))
def mute_user(m):
    duration = int(m.text.split()[-1])

    date = datetime.datetime.now() + datetime.timedelta(minutes=duration)
    until_date = int(date.timestamp())

    bot.restrict_chat_member(
        m.chat.id, m.reply_to_message.from_user.id,
        until_date=until_date,
        can_send_media_messages=False,
        can_send_messages=False,
        can_send_other_messages=False,
        can_send_polls=False
    )
    bot.reply_to(m, f"  کاربر به مدت {duration} دقیقه سکوت شد ")


@bot.message_handler(func=lambda m: m.text.startswith('بن تایمری'))
def mute_user(m):
    duration = int(m.text.split()[-1])

    date = datetime.datetime.now() + datetime.timedelta(minutes=duration)
    until_date = int(date.timestamp())

    bot.ban_chat_member(
        m.chat.id, m.reply_to_message.from_user.id,
        until_date=until_date,

    )
    bot.reply_to(m, f"کاربر به مدت {duration} دقیقه بن شد ")


media = []




@bot.message_handler(func=lambda message: message.text == 'جوک😄')
def random1(message):
    jock = ["آش رشته تنها جایی بود که گیاهان موفق شدن بدون کمک گوشت و خودشون\n\n به تنهایی طعم مطبوعی تولید کنن بقیه تجربه هاشون به شکست مطلق منجر شد", "چوپان دروغگو میمیره توی قبر ازش میپرسن اسمت چیه\n\n میگه دهقان فداکار", "با دختری که میگه “میسیییی” به جای “مرسی” باید درجا قطع رابطه کرد\n\nچون تا بیای براش توضیح بدی که نگو “میسییی” بهت میگه “چلااااااا؟”", "استقاده از آسانسو در فیلم ها چه ایرانی چه خارجی!\n\n یارو باعجله میره سمت آسانسور و فقط دکمشو میزنه بعد از پله ها میره بالا!!", "غضنفر می ره عروسی ‌‌‌ تو عروسی\n\n برف شادی می زنن  سرما می خوره!!", "غضنفر با کلید گوشش رو تمیز می کرده گردنش قفل می کنه!!", "مردی در هوای سرد، اسبی را دید که از\n\n بینی اش بخار بیرون می آمد با خود گفت فهمیدم پس اسب بخار که می گن همینه", "الان یکی زنگ زد گفت: شما!!!!!؟!\n\n منم گفتم: ببخشید اشتباه برداشتم خودش مرد از خنده فردا تشییع جنازشه", "هر کی میگه پول خوشبختی نمیاره پیام بده\n\n شماره حسابمو بدم پولاشو بریزه تو حسابم", "غضنفر به دوستش می گه: می دونستی آب سه تا جن داره؟\n\n دوستش: نه اسمش چیه؟ غضنفر : یکی اکسی جن و دو تا هیدرو جن.!!", "برای یه گوسفند فرق نمی کنه قراره\n\n کباب سلطانی، کالباس یا حلیم بشه سعی میکنه از علف خوردنش لذت ببره.", "می‌دونین اگه یه ماهی تو بانک کار کنه بهش چی می‌گن؟\n\n بهش می‌گن: فیش بانکی.", "به پشهه می گن: چرا زمستون پیداتون نیست؟ می گه:\n\n نه اینکه تابستون ها خیلی برخوردتون خوبه!", "به مرغه می‌گن: می‌تونی روزی پونزده‌ تا\n\n تخم بذاری؟ می‌گه: اون کار رو فقط ج**ده‌های تلاونگ می‌کنن.", "گلبول سفید میره تو خون می‌بینه\n\n همه گولبول‌ها قرمزن می‌گه »ای بابا چرا منو در شریان نذاشتین»", "یک روز دوتا سیاره داشتن دعوا می‌کردن\n\n نپتون می‌گه «آقا ولش کن همیشه حق با مشتریه…»", "می‌دونی کیبوردها چرا هم روزها کار می‌کنن هم شب‌ها؟\n\n چون دوتا شیفت دارن.", "سه نفر رو میندازن جهنم بعد چند روز میان\n\n می‌بینن خاکی و درب و داغونن می‌پرسن\n\n داستان چیه؟ می‌گن: خدایی کار ۳نفر نبود ولی بالاخره خاموشش کردیم.", "خره داشته می‌رفته چشمش به یه\n\n اسب میفته با حسرت می‌گه: ای کاش تحصیلاتم رو ادامه می‌دادم.", "غضنفر هی نگاه به گوشیش میکرده و میخندیده بهش میگن اس ام اس اومده ؟\n\nمیگه آره ، میگن چیه ؟\n\nمیگه یکی هی اس ام اس میده \nLow Battery"]
    random_message = random.choice(jock)
    bot.reply_to(message, random_message)
    

@bot.message_handler(func= lambda message: message.text == 'دانستنی⁉️')
def random2(message):
    messages = [
    "آیا می دانید کهکشان راه شیری 100 میلیون ستاره و یا بیشتر دارد.", "آیا می دانید ستاره دریایی مغز ندارد",  "آیا می دانید مساحت کره زمین 515 میلیون کیلومتر می باشد",  "آیا می دانید چینی ها بیشتر از آمریکایی ها انگلیسی بلدند", "آیا می دانید سیاره زهره گرمترین سیاره است و درجه حرارت آن درجه462 می باشد", "آیا می دانید 33 میلیارد الکترون در هر قطره آب وجود دارد", "آیا می دانید حلزون قادر است سه سال بخوابد", "آیا می دانید کوتاهترین جمله کامل در زبان انگلیسی جمله I am است", "آیا می دانید حیوانی که چشمانش از مغزش بزرگ تر است شتر مرغ می باشد", "آیا می دانید عمر خورشید 5 میلیارد سال است", "آیا می دانید نقره می تواند 650 نوع میکروب را از بین ببرد ومواد ضد عفونی قوی است", "آیا می دانید زبان مقاوم ترین ماهیچه در بدن است", "آیا می دانید پخش موسیقی برای مرغ سبب می شود او بزرگترین تخم را بگذارد", "آیا می دانید عسل تنها غذایی فاسد نشدنی است", "آیا می دانید تمام رگ های خونی بدن 97 هزار کیلومتر است", "اسب های دریایی تنها حیواناتی هستند که در آن ها جنس نر باردار می شود", "آیا می دانید قلب میگو در سرش قرار گرفته است", "آیا می دانید یونانیان باستان از ادرار خود\n\n برای تمیز کردن و سفید کردن دندان های شان استفاده می کردند", "آیا می دانید هشت پا سه قلب در بدنش دارد", "آیا می دانید شیر اسب آبی صورتی رنگ است"]
    random_message = random.choice(messages)
    bot.reply_to(message, random_message)


@bot.message_handler(func=lambda message: message.text == 'بیوگرافی🗨️' )
def random3(message):
    bio = [" <code> میان تمام نداشته‌هایم هنوز «خودی» دارم که سرسختانه پای من ایستاده است.🫂🤍️ </code>", "<code> دِل مَن میگه بِمونو بِساز، غُرورَم میگه وِلِش کُن بِباز:)️ </code>", "<code> بهترین حس ..؟ وقتی که تنهایی و تو آهنگات غرق شدی... </code>", "<code> -عَـقلتو‌ دنبـال ‌کـن، قَـلبت‌ احمقـه.️   </code>", "<code> 𝒂 𝒎𝒊𝒏𝒅 𝒇𝒖𝒍𝒍 𝒐𝒇 𝒖𝒏𝒔𝒂𝒊𝒅 𝒕𝒉𝒊𝒏𝒈𝒔 یه ذهن پر از چیزای نگفته️   </code>", " <code> بی تفاوت به هر تفاوت🕸🕷</code>", " <code> معرفتاشون‌ وصله‌ به‌ منفعت‌‌‌‌؛ </code>", " <code> «بهش نگو رويا، بگو هدف!»‌</code>", " <code> جوری باش که حتی مغزتم منت فکر کردنشو گذاشت خیلی راحت درش بیاری😏️</code>", " <code> گمشده در جنگل متروکه افکار....  </code>", " <code> از لحظه لحظه زندگیت لذت ببر شاید فردایی نباشد..  </code>", " <code> بلاخره یه روزی یه جایی دفتر زندگی منم بسته میشه و راحت میخوابم....  </code>", " <code> گاهی وقتا کلمات مانند شیشه میشند: «اگه سکوت کنی درد داره » «اگه حرف بزنی خونریزی میکنه» </code>", " <code> اما چـہ باید گفتـ... انسان نمایانی ڪ ننگِ نام انسانند🙂  </code>", " <code>-جوانہ باور کرد،درخت شُد!🌱✨.  </code>", " <code> آرامش یعنی نگاه به گذشته و شـــــکر خـــــــدا ، نگاه به آینده و اعتمــــاد به خــــــــــــــدا </code>", " <code> برای کشف اقیانوس های جدید باید جرات ترک ساحل را داشت، این دنیا، دنیای تغییر است نه تقدیر </code>", " <code> خری کِه از پُل گذشتِه باشِه هار میشِه!🖤 </code>", " <code> موفقیت داده نمیشه، بدست میاد🤞🏻🕊 </code>", " <code> خسته ام مثل لاک پشتی که یک خیابان را اشتباه رفته است🐢:) </code> "]
    random_message = random.choice(bio)
    bot.reply_to(message, random_message, parse_mode="HTML")
    bot.send_message(message.chat.id, 'متن به صورت مونو هست و با زدن روی متن کپی میشود')
    

@bot.message_handler(func=lambda message: message.text == 'اصطلاحات انگلیسی🔠')
def random4(message):
    essential = [ "<code> After Blood\n\nخونخواهی و انتقام</code>", "<code> A Busy Body\n\nآدم فوضول </code>", "<code> A Proper Meal\n\nیه غذای درست و حسابی  </code> ", "<code> All In Stitches\n\nاز خنده روده بر شدن </code>", "<code>Appearances Are Deceptive\n\nظاهر افراد فریبنده هست </code>", "<code> A Ray of Sunshine\n\nکورسوی امید</code>", "<code> Are You Sulking?\n\nقهری؟ </code>", "<code> Are You Ticklish\n\nقلقلکی هستی؟ </code>", "<code> As They Say\n\nبه قول معروف... </code>", "<code> At The Eleventh Hour\n\nدقیقه نود (لحظه آخر) </code>", " <code> Beet Red\n\nسرخ شدن از خجالت </code>", " <code> Bend Over Backwards\n\nجون کندن </code>", " <code> Being Broke Hurts!\n\nبی پولی بد دردیه </code>", " <code> Better Late Than Never\n\nدیر رسیدن بهتر از هرگز نرسیدنه </code>", " <code> Blow Hot And Cold\n\nهر دفعه یه سازی میزنه </code>", "<code> Blue In The Face\n\nزبونم مو در آورد </code>", "<code> Bust Hump\n\nبرو گمشو </code>",  "<code> Buy The Farm\n\nنخود هر آشی شدن </code>", "<code> Catch Someone Red Handed\n\nمچ کسی رو گرفتن </code>", "<code> Cat Got Your Tongue?\n\nگربه زبونتو خورده؟ </code>" ]
    random_message = random.choice(essential)
    bot.reply_to(message, random_message, parse_mode="HTML")
    bot.send_message(message.chat.id, 'متن به صورت مونو هست و با زدن روی متن کپی میشود')
    


@bot.message_handler(func=lambda m: m.text == 'جرعت حقیقت❓')
def joraat_haghighat(m): 
    bot.send_message(m.chat.id,           
'1. اگر زندگی ات یک فیلم بود کدام فیلم می شد؟\n\n 2. آیا آلرژی خاصی داری؟\n\n 3. اگر میتوانستی به یک زمان خاص در تاریخ برگردی کدام زمان بود؟\n\n 4. اگر ابر قدرت بودی چه قدرتی داشتی؟\n\n 5. وقتی آلارم گوشیت زنگ میزند بلافاصله بیدار میشوید یا دکمه بعدا را فشار میدهد؟\n\n 6. اولین کاری که هر روز صبح انجام میدی چیه؟\n\n 7. آخرین کاری که هر شب انجام میدی چیه؟\n\n 8. آخرین باری که گریه کردی کی بوده و چرا؟\n\n 9. عجیب ترین کاری که در تنهایی هایت انجام دادی چه بوده؟\n\n 10. بدترین بحثی که در آن شرکت کرده ای چه بوده؟\n\n 11. مسخره ترین لباسی که تابحال پوشیده ای چه بوده؟\n\n 12. اگر می توانستی یک چیز را در خودت تغییر دهی چه چیزی را تغییر می دادی؟\n\n 13. بزرگ ترین رازت چیه؟\n\n 14. چه چیزی باعث خجالتت میشه؟\n\n 15. خجالت آورترین اتفاقی که تاحالا برات افتاده؟\n\n 16. بزرگترین اشتباهی که تاحالا مرتکب شدی؟\n\n 17. توی چه کاری اصلا خوب نیستی؟\n\n 18. بزرگ ترین دروغی که تا حالا گفتی؟\n\n 19. تا حالا توی بازی تقلب کردی؟\n\n 20. عجیب ترین عادتی که داری؟\n\n 21. عجیب ترین غذایی که عاشقشی؟\n\n 22. بزرگ ترین ترس دوران بچگیت؟\n\n 23. پایین ترین نمره ای که توی دانشگاه یا مدرسه گرفتی؟\n\n 24. تا حالا یه چیز گرون قیمت رو شکستی؟\n\n 25. اگه یه دفعه صد میلیون تومن به دست بیاری، چطوری خرجش می کنی؟\n\n 26. بدترین غذایی که تا حالا امتحان کردی؟\n\n 27. خجالت آورترین چیزی که تا حالا توی فضای مجازی پست کردی؟\n\n 28. تا حالا راز دوستت رو به کسی گفتی؟\n\n 29. دوست داری در آینده چندتا بچه داشته باشی؟\n\n 30. اگه قرار باشه تا آخر عمرت فقط یه غذا رو بخوری، چه غذاییه؟\n\n 31. آخرین پیامی که برای دوست صمیمیت ارسال کردی؟\n\n 32. بدترین درد فیزیکی که تا حالا داشتی؟\n\n 33. از لحاظ شخصیتی، بیشتر شبیه مامانتی یا بابات؟\n\n 34. آخرین باری که از کسی عذرخواهی کردی کی بود؟ بابت چه کاری؟\n\n 35. اگه خونت آتش بگیره و فقط بتونی 3 تا چیزو برداری (به غیر از افراد)، چه چیزهایی رو بر می داری؟\n\n 36. توی بچگیات دوست داشتی چه سرگرمی یا ورزشی رو تجربه کنی؟\n\n 37. عجیب ترین کاری که تا حالا توی مکان عمومی انجام دادی؟\n\n 38. آخرین بهانه ای که برای کنسل کردن برنامه هات آوردی؟\n\n 39. بدترین اشتباهی که توی مدرسه یا سر کارت انجام دادی؟\n\n 40. کدوم یکی از اعضای خانوادت خیلی رو اعصابته؟')
    bot.reply_to(m, 'لیست جرعت حقیقت ارسال شد')                                 
                                                                               

@bot.message_handler(commands=['bot'])
def welcome(message):
    bot.reply_to(message,"از منوی زیر در صفحه کلید گزینه ای را انتخاب نمایید:", reply_markup=reply_keyboard)


@bot.message_handler(func= lambda message: True)
def option_messages(message): 
    if message.text == 'ارتباط با ما📞':
       bot.reply_to(message, 'آیدی سازنده ربات برای ارتباط: @AliamA7931')
       
    elif message.text == 'مدیریت گروه🤵‍♂️':
        bot.reply_to(message, 'برای اینکه ربات بتواند گروه شما را مدیریت کند\n\nابتدا باید ربات را در گروه خود عضو و سپس ربات را ادمین کامل کنید و بعد میتوانید از ربات استفاده کنید')
     
    elif message.text == 'شروع':
        bot.reply_to(message, 'سلام من علی بات🤖هستم\n\n برای اطلاع از قابلیت من کلمه <b>(لیست)</b> رو ارسال کن', parse_mode="HTML")
    
    elif message.text == 'لیست':
        bot.send_message(message.chat.id,'1-<code> مدیریت گروه🤵‍♂️</code>\n\n2-<code>بیوگرافی🗨️</code>\n\n3-<code> اصطلاحات انگلیسی🔠</code>\n\n4-<code> جرعت حقیقت❓</code>\n\n5-<code> جوک😄</code>\n\n6-<code>فونت اسم♍</code>\n\n7-<code> زبان هخامنشی𐎠</code>\n\n8-<code> دانستنی⁉️</code>\n\n9-<code> ارتباط با ما📞</code>\n\n<b>متن ها به صورت مونو هستند روی متن بزنید کپی میشوند</b>', parse_mode="HTML")   
        bot.reply_to(message, 'لیست قابلیت ربات ارسال شد')   
    elif message.text == 'سلام':
        bot.reply_to(message, 'سلام بر شما')

    elif message.text == 'سلام خوبی':
        bot.reply_to(message, 'خوبم ممنون شما خوبی')
        
    elif message.text == 'خوبی':
        bot.reply_to(message, 'سپاس به خوبی شما') 

    elif message.text == 'خوب هستی':
        bot.reply_to(message, ' اره خودت خوبی')
        
    elif message.text == 'چه خبرا':
        bot.reply_to(message, 'خبر سلامتیت شما چه خبر')
           
    elif message.text == 'منم سلامتی خبری نیست':
        bot.reply_to(message, 'آها خداروشکر')
       
    elif message.text == 'خبر خیر سلامتی':
        bot.reply_to(message, 'همیشه سلامت باشی😊')
        
    elif message.text == 'فدات':
        bot.reply_to(message, 'قربون شما❤️')
        
    elif message.text == 'فدابشم':
        bot.reply_to(message, 'نشی بمونی ارزش داری عزیز☺️')
         
    elif message.text == 'خداحافظ':
        bot.reply_to(message, 'خدانگهدار👋')
        
    elif message.text == 'بای':
        bot.reply_to(message, 'گودبای')
                                 
    elif message.text == 'کجایی':
        bot.reply_to(message, 'کجا میتونستم باشم تو تلگرامم دیگه😐!')
        

    elif message.text == 'اهل کجایی':
        bot.reply_to(message, 'از سیاره ربات ها اینم شد سوال!')
        
    elif message.text == 'رباط':
        bot.reply_to(message, 'معلم ادبیاتت کی بودش زنده میخامش ')

    elif message.text == 'چیکار میکنی':
        bot.reply_to(message, 'بقیه رباتا چیکار میکنن منم دارم همونکارو میکنم!')

    elif message.text == ' کیر نداری؟':
        bot.reply_to(message, 'دارم از جنس آهن هست بدجوری دردت میارم😁')
       
    elif message.text == 'کونی':
        bot.reply_to(message, 'لاپات بستنی نونی')
       
    elif message.text == 'دندون بگیر':
        bot.reply_to(message, 'کون بده فاکتور بگیر')

    elif message.text == 'اسمت چیه':
        bot.reply_to(message, 'اسمم علی بات🤖 هست')

    elif message.text == 'چطوری':
        bot.reply_to(message, 'خوبم شکر خدا')
        
    elif message.text == 'کصخول':
        bot.reply_to(message, ' کص ندارم کیر دارم آهنیه میخای😉؟')   
        
    elif message.text == 'درود':
        bot.reply_to(message, 'درود بر تو گل🌹')         
        
    elif message.text == 'ربات': 
        Bot_Response = f'جانم @{message.from_user.username}  کارم داشتی؟\n\n🔸برای ارتباط با ربات کلمه <b>(شروع)</b> را ارسال کنید\n\n🔺و برای اطلاع از تاریخ و ساعت امروز کلمه<b> (زمان) </b>را ارسال کنید'
        bot.send_message(message.chat.id, text=Bot_Response, parse_mode="HTML")

               


####################### Mazani Language###################### 
        
    elif message.text == 'سلام خاری':
        bot.reply_to(message, 'خارمه ته خاری')
        
    elif message.text == 'خاری':
        bot.reply_to(message, ' اره ته چیتی هستی؟')

    elif message.text == 'اره خارمه':
        bot.reply_to(message, 'خداره شکر')

    elif message.text == 'بد نیمه':
        bot.reply_to(message, 'خار بووشی')

    elif message.text == 'چه خبر':
        bot.reply_to(message, 'سلامتی ته چه خبر')

    elif message.text == 'منم سلامتی خبری نیه':
        bot.reply_to(message, ' آها همیشه سلامت بوشی')

    elif message.text == 'گم بواش':
        bot.reply_to(message, 'گم نوومبه شه سره راه ره بلدمه')
        
    elif message.text == 'گیخار':
        bot.reply_to(message, 'برو مه گی ره بخار')
        
    elif message.text == 'چیکار کندی':
        bot.reply_to(message, 'چیکار خاستی هاکانم درمه ته جه گپ زمبه😑') 
           
    elif message.text == 'چیکار کاندی':
        bot.reply_to(message, 'چیکار خاستی هاکانم درمه ته جه گپ زمبه😑') 
        
    elif message.text == 'کجه دری':
        bot.reply_to(message, 'تلگرام دله درمه دیگه اینتا هم بییه سوال🙄')
        
    elif message.text == 'ته اسم چیچیه':
        bot.reply_to(message, 'من علی بات🤖هستمه شما مه ره نشناسنی😁')   
                
    elif message.text == 'ته اسم چیه':
        bot.reply_to(message, 'من علی بات🤖هستمه شما مه ره نشناسنی😁')           

    elif message.text == 'ربات ته ره دوست دارمه':
        bot.reply_to(message, 'منم ته ره خله دوست دارمه ولی از یه نظر دیگه🙂😊')
        
    elif message.text == 'ربات ته ره دوست دارمه':
        bot.reply_to(message, 'منم ته ره خله دوست دارمه ولی از یه نظر دیگه🙂😊')
         
    elif message.text == 'ربات مه جه رل زندی':
        bot.reply_to(message, 'اره ته فدابووشم ناز ره بخارم😁')
        
    elif message.text == 'کیر':
        bot.set_message_reaction(chat_id=message.chat.id, message_id=message.message_id,  reaction=[
                                 ReactionTypeEmoji(emoji='🖕')])
        bot.reply_to(message, 'بوره ته زیر شفتکص')

    elif message.text == 'کاص نار':
        bot.reply_to(message, 'گفتنی نییه کردنی هسته عزیز')

    elif message.text == 'بزن به چاک':
        bot.reply_to(message, 'چاکتو باز کن بزنم')

    elif message.text == 'شفتکص':
        bot.reply_to(message, 'ته عمه هسته')

    elif message.text == 'ای کیر':
        bot.reply_to(message, 'بوره ته موس')
        
    elif message.text == 'من بورم':
        bot.reply_to(message, 'به سلامت شه هوا ره دار')        
    
    elif message.text == 'روبات':
        Bot_Response = f'جان @{message.from_user.username} مه ره کار داشتی؟\n\n🔸 برای گپ بزوعن با ربات کلمه <b>(شروع)</b>  ره راهی هاکان\n\n🔺و برای اطلاع داشتن از تاریخ و ساعت امروز کلمه<b> (زمان) </b>ره راهی هاکان'
        bot.send_message(message.chat.id, text=Bot_Response, parse_mode= 'HTML') 
        

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url="https://bottelegram-3-evsk.onrender.com/" + TOKEN)
