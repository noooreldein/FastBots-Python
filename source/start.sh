#!/bin/bash
# start.sh - Bot startup with auto-restart and error reporting
# This file gets copied with the source to each bot directory

LOG_FILE="/tmp/$(basename "$(pwd)")_bot.log"

# Read admin info from environment or arguments
ADMIN_TOKEN="$1"
ADMIN_ID="$2"
MAX_RETRIES=2

send_admin() {
    if [ -n "$ADMIN_TOKEN" ] && [ -n "$ADMIN_ID" ]; then
        curl -s -X POST "https://api.telegram.org/bot${ADMIN_TOKEN}/sendMessage" \
            -d chat_id="$ADMIN_ID" \
            --data-urlencode "text=$1" > /dev/null 2>&1
    fi
}

for attempt in $(seq 1 $((MAX_RETRIES + 1))); do
    echo "[start] Attempt $attempt/$((MAX_RETRIES + 1))..."
    python3 -m YukkiMusic > "$LOG_FILE" 2>&1
    EXIT_CODE=$?

    if [ $EXIT_CODE -eq 0 ]; then
        echo "[start] Bot exited normally."
        break
    fi

    ERROR=$(tail -15 "$LOG_FILE" 2>/dev/null | head -800)

    if [ $attempt -le $MAX_RETRIES ]; then
        send_admin "⚠️ البوت وقع (محاولة $attempt/$((MAX_RETRIES + 1)))
كود الخروج: $EXIT_CODE

الخطأ:
$ERROR

جاري إعادة التشغيل..."
        echo "[start] Retrying in 5 seconds..."
        sleep 5
    else
        send_admin "❌ البوت فشل يشغل بعد $((MAX_RETRIES + 1)) محاولات

آخر خطأ:
$ERROR

⚠️ محتاج تدخل تشغله يدوياً"
        echo "[start] Failed after all retries."
    fi
done
