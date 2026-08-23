# FastBots Python - Music Bot Maker

صانع بوتات ميوزك بـ Python - No Redis, No TDLib, No Lua.

## المتطلبات
- Python 3.8+
- `requests` فقط

## التشغيل
```bash
pip install requests
python3 Fast.py
```

أول مرة هتطلب منك:
1. توكن البوت
2. معرف المطور
3. ايدي المطور

## الملفات
- `Fast.py` - الكود الرئيسي
- `td.py` - Telegram Bot API wrapper (بدل TDLib)
- `storage.py` - تخزين JSON (بدل Redis)
- `start` - سكريبت التشغيل
- `requirements.txt` - المتطلبات

## المميزات
- ✅ تلوين الأزرار (primary/danger/success)
- ✅ إيموجي مخصص للأزرار
- ✅ Pure Python - لا اعتماد على Redis أو TDLib أو Lua
- ✅ تخزين JSON بدل Redis
