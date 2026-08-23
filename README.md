# 🎵 FastBots Python - صانع بوتات الميوزك

<div align="center">

# 🎵 FastBots Python 🎵

### صانع بوتات ميوزك احترافي - Pure Python 100%

**بدون Redis | بدون TDLib | بدون Lua | بدون أي اعتماديات معقدة**

</div>

---

## ✨ المميزات

### 🔧 صانع بوتات متكامل
- **صناعة بوتات ميوزك غير محدودة** - اعمل بوتات على أساس Yukki Music
- **حذف البوتات** بضغطة زر
- **تحديث المصنوعات** - حدث كل البوتات دفعة واحدة
- **عدد البوتات والإحصائيات** - تابع كل حاجة

### 🎨 أزرار ملوّنة (Telegram Keyboard Styles)
كل الأزرار تستخدم ميزة Telegram الجديدة لتلوين الأزرار:
- 🟢 **success** - للأزرار الإيجابية (تفعيل، صنع)
- 🔴 **danger** - للأزرار السلبية (حذف، تعطيل، إلغاء)
- 🔵 **primary** - للأزرار المحايدة (إحصائيات، تحديث، اذاعه)

### 😍 إيموجي مخصص
كل زرار ليه إيموجي مميز خاص بيه (icon_custom_emoji_id) - سيبناها زي ما هي.

### 📢 نظام الإذاعة
- **إذاعة نصية** - ابعت رسالة لكل المشتركين
- **إذاعة بالتوجيه** - حول أي رسالة لكل المشتركين
- يدعم: نص، صور، فيديو، صوت، ستيكر، أنيميشن، ملفات، voice note

### 🔗 الاشتراك الإجباري
- تفعيل/تعطيل الاشتراك الإجباري لقناة معينة
- البوت يتأكد تلقائياً لو العضو مشترك ولا لا

### 💬 نظام التواصل
- الأعضاء يقدروا يبعوا رسائل للمطور
- المطور يرد عليهم أو يحظرهم
- تفعيل/تعطيل التواصل في أي وقت

### 🆓 الوضع المجاني
- تفعيل/تعطيل الوضع المجاني للبوتات
- لما يكون معطل، الأعضاء الجداد ميسمحلهمش يصنعوا بوتات

### 👥 نظام المطورين
- **مطور أساسي (Sudo)** - تحكم كامل في الصانع
- **مطورين مساعدين** - ارفع و نزّل مطورين بأمر
- حماية كاملة - مفيش حد يقدر يتحكم غير المطورين

### 📊 الإحصائيات
- عدد المشتركين الكلي
- عدد البوتات المصنوعة
- الأسكرينات المفتوحة (screen sessions)

---

## 📁 هيكل المشروع

```
FastBots-Python/
├── Fast.py              # الكود الرئيسي - الصانع
├── td.py                # Telegram Bot API wrapper (بديل TDLib)
├── storage.py           # تخزين JSON (بديل Redis)
├── start                # سكريبت التشغيل
├── requirements.txt     # المتطلبات (requests بس)
├── README.md            # هذا الملف
└── source/              # ملفات YukkiMusic - السورس اللي المصنع بيصنعه
    ├── YukkiMusic/
    │   ├── core/        # ├── bot.py, call.py, userbot.py, mongo.py
    │   ├── platforms/   # ├── Youtube, Spotify, Apple, Soundcloud, Resso, Telegram
    │   ├── plugins/
    │   │   ├── admins/   # ├── auth, callback, loop, mute, pause, resume, seek, shuffle, skip, stop, unmute
    │   │   ├── bot/     # ├── help, inline, settings, start
    │   │   ├── play/    # ├── play, playlist, channel, filters, live, source
    │   │   ├── sudo/    # ├── autoend, blacklist, block, globalban, heroku, maintenance, sudoers
    │   │   ├── tools/   # ├── active, lyrics, ping, queue, reload, songs, speedtest, stats
    │   │   └── misc/    # ├── autoleave, cleanmode, seeker, suggestion
    │   └── utils/       # ├── database, decorators, inline, stream, formatters, thumbnails
    ├── assets/         # ├── صور البوت (thumbnails, fonts)
    ├── config/         # ├── config.py
    ├── strings/        # ├── languages, commands, filters
    └── requirements.txt
```

---

## 🚀 التشغيل على السيرفر

### المتطلبات
- Python 3.8+
- `requests` فقط
- `screen` (لتشغيل البوتات في خلفية)
- MongoDB (بيتم استخدام MongoDB Atlas تلقائياً)

### التثبيت السريع - أمر واحد بس

```bash
git clone https://github.com/noooreldein/FastBots-Python.git && cd FastBots-Python && pip install -r requirements.txt && python3 Fast.py
```

### التثبيت اليدوي خطوة بخطوة

```bash
# 1. تحميل الملفات
git clone https://github.com/noooreldein/FastBots-Python.git
cd FastBots-Python

# 2. تثبيت المتطلبات
pip install -r requirements.txt

# 3. تشغيل الصانع
python3 Fast.py
```

### أول تشغيل
أول ما تشغل البوت، هيطلب منك:
1. **توكن البوت** - توكن البوت من @BotFather
2. **معرف المطور** - يوزرك بدون @
3. **ايدي المطور** - ايدي رقمي بتاعك

بعدها البوت هيشتغل ويرحب بيك ✨

---

## 📋 أوامر الصانع

### أوامر المطور الأساسي (Sudo)

| الأمر | الوصف | اللون |
|-------|-------|-------|
| ✨ صنع بوت | يبدأ عملية صناعة بوت جديد | 🟢 success |
| ✨ حذف بوت | حذف بوت موجود | 🔴 danger |
| ✨ تفعيل الاشتراك الاجباري | تفعيل قناة إجبارية | 🟢 success |
| ✨ تعطيل الاشتراك الاجباري | إلغاء القناة الإجبارية | 🔴 danger |
| ✨ تفعيل الوضع المجاني | السماح للجميع بصناعة بوتات | 🟢 success |
| ✨ تعطيل الوضع المجاني | منع صناعة البوتات | 🔴 danger |
| ✨ تحديث المصنوعات | تحديث كل البوتات دفعة واحدة | 🔵 primary |
| ✨ عدد البوتات | عرض عدد البوتات المصنوعة | 🔵 primary |
| ✨ الاحصائيات | عرض عدد المشتركين | 🔵 primary |
| ✨ الاسكرينات المفتوحه | عرض الـ screen sessions | 🔵 primary |
| ✨ تفعيل التواصل | السماح للأعضاء بالتواصل | 🟢 success |
| ✨ تعطيل التواصل | منع التواصل | 🔴 danger |
| ✨ اذاعه | إذاعة رسالة لكل المشتركين | 🔵 primary |
| ✨ اذاعه بالتوجيه | توجيه رسالة لكل المشتركين | 🔵 primary |
| اعاده التشغيل ✨ | إعادة تشغيل الصانع | 🔵 primary |
| ✨ الغاء الامر | إلغاء أي أمر جاري | 🔴 danger |

### أوامر نصية
- `رفع مطور <id>` - رفع عضو مطور
- `تنزيل مطور <id>` - تنزيل مطور
- `حظر` (reply) - حظر عضو من التواصل
- `الغاء الحظر` (reply) - إلغاء الحظر
- `تحديث` / `اعاده التشغيل` - إعادة تشغيل

### أوامر الأعضاء

| الأمر | الوصف | اللون |
|-------|-------|-------|
| ✨ صنع بوت | صناعة بوت ميوزك جديد | 🟢 success |
| ✨ حذف البوت | حذف البوت بتاعك | 🔴 danger |
| ✨ الغاء | إلغاء أي أمر جاري | 🔴 danger |

### خطوات صناعة البوت
1. اضغط **✨ صنع بوت**
2. ابعت **توكن البوت** من @BotFather
3. ابعت **معرف المطور** (يوزر بدون @)
4. ابعت **جلسة البايروجرام** من @s_stbot
5. ابعت **ايدي الحساب المساعد**
6. ابعت **معرف قناة الاشتراك الاجباري**
7. ابعت **معرف جروب الدعم**
8. البوت يشتغل تلقائياً! 🎉

---

## 🔄 المقارنة: Lua vs Python

| الميزة | Lua (قديم) | Python (جديد) |
|--------|-----------|---------------|
| التخزين | Redis | JSON file (storage.py) |
| Telegram API | TDLib | Bot API (td.py) |
| JSON | dkjson.lua | Python json (built-in) |
| URL parsing | url.lua | urllib (built-in) |
| Pretty print | serpent.lua | pprint (built-in) |
| الاعتماديات | Redis + TDLib + Lua libs | requests بس |
| التشغيل | معقد | أمر واحد |

---

## 🛠️ التقنيات المستخدمة

- **Python 3.8+** - اللغة الأساسية
- **requests** - للتواصل مع Telegram Bot API
- **JSON** - للتخزين بدل Redis
- **screen** - لتشغيل البوتات في الخلفية
- **MongoDB Atlas** - قاعدة بيانات البوتات المصنوعة (تلقائي)
- **Pyrogram** - إطار عمل بوتات الميوزك (في source/)

---

## 📦 ملفات المشروع

| الملف | الحجم | الوصف |
|------|-------|-------|
| `Fast.py` | 52KB | الكود الرئيسي - كل منطق الصانع |
| `td.py` | 28KB | Telegram Bot API wrapper |
| `storage.py` | 6KB | تخزين JSON بدل Redis |
| `source/` | 194 ملف | ملفات YukkiMusic الكاملة |
| `requirements.txt` | 1 سطر | requests>=2.20.0 |
| `start` | 56 bytes | سكريبت تشغيل |

---

## 🔒 الأمان

- `Information.py` - بيانات حساسة (في .gitignore)
- `data_store.json` - قاعدة البيانات (في .gitignore)
- `.CallBack-Bot/` - بيانات البوتات (في .gitignore)
- لا يتم رفع أي توكنات أو بيانات حساسة على GitHub

---

## 👨‍💻 المطور

**المطور الأساسي:** noooreldein
**الـ Repo:** [FastBots-Python](https://github.com/noooreldein/FastBots-Python)

---

<div align="center">

### 🎵 FastBots Python - صانع بوتات الميوزك 🎵

**Pure Python | No Redis | No TDLib | No Lua**

</div>
