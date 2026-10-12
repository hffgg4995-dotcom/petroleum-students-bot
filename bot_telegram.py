import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv
import google.generativeai as genai

# تحميل التوكن والمفتاح من ملف .env
load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# إعداد البوت والذكاء الاصطناعي
bot = telebot.TeleBot(TOKEN)
genai.configure(api_key=GEMINI_API_KEY)

# التلقين الخاص بالبوت (شخصية البوت وحدوده لهندسة النفط)
bot_persona = """أنت مساعد أكاديمي ذكي مخصص لطلاب هندسة النفط في جامعة الفرقدين.
مهمتك هي الإجابة على أسئلة الطلاب العلمية في مجالات هندسة النفط، خواص صخور المكمن، الجيولوجيا النفطية، والرياضيات والفيزياء.
قوانينك الصارمة:
1. أجب دائماً بأسلوب أكاديمي محترم ومبسط.
2. إذا سألك الطالب عن أي موضوع خارج دراسة هندسة النفط أو المواد العلمية الجامعية، اعتذر بلباقة وقل: 'عذراً، أنا مبرمج فقط لمساعدة طلاب هندسة النفط في جامعة الفرقدين في دراستهم الأكاديمية ولا يمكنني الإجابة على مواضيع خارج هذا النطاق.'
"""

model = genai.GenerativeModel(
    'gemini-1.5-flash',
    system_instruction=bot_persona
)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = InlineKeyboardMarkup()
    
    # أزرار المحاضرات
    btn1 = InlineKeyboardButton("محاضرات الجيولوجيا النفطية للدكتورة نور", callback_data='noor')
    btn2 = InlineKeyboardButton("محاضرات خواص صخور المكمن للدكتورة الاء", callback_data='alaa')
    btn3 = InlineKeyboardButton("محاضرات دكتور صباح - رياضيات", callback_data='sabah_math')
    
    # زر الذكاء الاصطناعي
    btn_ai = InlineKeyboardButton("🤖 استخدام الذكاء الاصطناعي", callback_data='use_ai')
    
    markup.add(btn1)
    markup.add(btn2)
    markup.add(btn3)
    markup.add(btn_ai)
    
    bot.send_message(
        message.chat.id, 
        "أهلاً بك في بوت محاضرات هندسة النفط - جامعة الفرقان...\n\nاختر من القائمة أدناه:", 
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data == 'use_ai')
def ai_button_clicked(call):
    bot.answer_callback_query(call.id)
    msg