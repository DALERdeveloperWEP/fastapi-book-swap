from telegram import KeyboardButton, ReplyKeyboardMarkup

first_start = """Assalomu alaykum, botimizga xush kelibsiz 📚

Bu bot orqali siz:
- kitob sotishingiz
- kitob olishingiz
- kitoblar ro‘yxatini ko‘rishingiz mumkin

Davom etish uchun telefon raqamingizni yuboring yoki yordam bo‘limini oching."""

guest_help = """Nima maqsad uchun yordam kerakligini yozib yuboring:"""

auth_keyboard = ReplyKeyboardMarkup(
    [
        [KeyboardButton("📱 Telefon raqam yuborish", request_contact=True)],
        [KeyboardButton("❓ Yordam")]
    ],
    resize_keyboard=True
)

phone_access = """Rahmat, telefon raqamingiz qabul qilindi ✅

Kerakli bo‘limni tanlang:"""

menu_keyboard = ReplyKeyboardMarkup(
    [
        [KeyboardButton("📚 Kitob olish"), KeyboardButton("💰 Kitob sotish")],
        [KeyboardButton("📖 Mening kitoblarim"), KeyboardButton("🛒 Mening buyurtmalarim")],
        [KeyboardButton("👤 Profil"), KeyboardButton("❓ Yordam")]
    ],
    resize_keyboard=True
)

user_help = """Yordam bo‘limi ℹ️

Botdan foydalanish tartibi:

1. Telefon raqamingizni yuboring
2. Menudan kerakli bo‘limni tanlang
3. Kitob olish yoki sotish bo‘limidan foydalaning

Asosiy bo‘limlar:
📚 Kitob olish — mavjud kitoblarni ko‘rish
💰 Kitob sotish — o‘z kitobingizni joylash
📖 Mening kitoblarim — siz qo‘shgan kitoblar
🛒 Mening buyurtmalarim — buyurtmalar holati
👤 Profil — foydalanuvchi ma’lumotlari"""