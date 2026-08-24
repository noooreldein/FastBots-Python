#!/bin/bash
# bot_watchdog.sh - Auto-restart and error reporting for music bots
# Usage: bot_watchdog.sh <bot_name> <bot_dir> <admin_token> <admin_id>

BOT_NAME="$1"
BOT_DIR="$2"
ADMIN_TOKEN="$3"
ADMIN_ID="$4"
MAX_RETRIES=2
LOG_FILE="/tmp/${BOT_NAME}_bot.log"

cd "$BOT_DIR" || exit 1

send_admin() {
    local msg="$1"
    curl -s -X POST "https://api.telegram.org/bot${ADMIN_TOKEN}/sendMessage" \
        -d chat_id="$ADMIN_ID" \
        --data-urlencode "text=$msg" > /dev/null 2>&1
}

for attempt in $(seq 1 $((MAX_RETRIES + 1))); do
    echo "[Watchdog] Starting $BOT_NAME (attempt $attempt/$((MAX_RETRIES + 1)))..."
    python3 -m YukkiMusic > "$LOG_FILE" 2>&1
    EXIT_CODE=$?

    if [ $EXIT_CODE -eq 0 ]; then
        echo "[Watchdog] $BOT_NAME exited normally."
        break
    fi

    # Bot crashed - get last 15 lines of error
    ERROR=$(tail -15 "$LOG_FILE" 2>/dev/null | head -800)

    if [ $attempt -le $MAX_RETRIES ]; then
        send_admin "⚠️ البوت @$BOT_NAME وقع (محاولة $attempt من $((MAX_RETRIES + 1)))
كود الخروج: $EXIT_CODE

الخطأ:
$ERROR

جاري إعادة التشغيل..."
        echo "[Watchdog] Retrying in 5 seconds..."
        sleep 5
    else
        send_admin "❌ البوت @$BOT_NAME فشل يشغل بعد $((MAX_RETRIES + 1)) محاولات

آخر خطأ:
$ERROR

⚠️ محتاج تدخل تشغله يدوياً"
        echo "[Watchdog] $BOT_NAME failed after all retries."
    fi
done
