"""
td.py - Telegram Bot API wrapper (NO TDLib, NO Lua, pure Python)
Uses Telegram Bot API directly via HTTP requests.
Supports button styling (primary/danger/success) and custom emoji.
"""

import json
import os
import re
import time
import base64
import requests
import threading
import traceback
from typing import Any, Optional, List, Dict, Callable

# ------------------------------------------------------------------
# Color codes
# ------------------------------------------------------------------
COLORS_KEY = {
    'reset': 0, 'bright': 1, 'dim': 2, 'underline': 4, 'blink': 5,
    'reverse': 7, 'hidden': 8,
    'black': 30, 'red': 31, 'green': 32, 'yellow': 33, 'blue': 34,
    'magenta': 35, 'cyan': 36, 'white': 37,
}

def colors(buffer):
    for key in re.findall(r'%\{(.*?)\}', buffer):
        if key in COLORS_KEY:
            buffer = buffer.replace(f'%{{{key}}}', f'\033[{COLORS_KEY[key]}m')
    return buffer + '\033[0m'

def print_error(err):
    print(colors('%{red}Error: ' + str(err)))


# ------------------------------------------------------------------
# Button Style - Telegram's new button coloring
# ------------------------------------------------------------------
def _style_color(style):
    """Map style names to Telegram API style values."""
    if style == 'primary':
        return 'primary'
    elif style == 'danger':
        return 'danger'
    elif style == 'success':
        return 'success'
    return None


def reply_markup(input_data):
    """
    Build Telegram Bot API reply_markup from simplified input.
    Supports inline keyboards and reply keyboards.
    Preserves button styles and icon_custom_emoji_id.
    """
    if not isinstance(input_data, dict) or not isinstance(input_data.get('type'), str):
        return None

    markup_type = input_data['type'].lower()

    if markup_type == 'inline':
        inline_keyboard = []
        for row in input_data.get('data', []):
            kb_row = []
            for value in row:
                if not isinstance(value, dict):
                    continue
                text = value.get('text', '')
                btn = {'text': text}

                # Add style if present
                style = _style_color(value.get('style'))
                if style:
                    btn['style'] = style

                # Add custom emoji if present
                emoji_id = value.get('icon_custom_emoji_id')
                if emoji_id:
                    btn['icon_custom_emoji_id'] = str(emoji_id)

                if value.get('url'):
                    btn['url'] = value['url']
                elif value.get('data'):
                    btn['callback_data'] = str(value['data'])
                elif value.get('query'):
                    btn['switch_inline_query'] = value['query']

                kb_row.append(btn)
            inline_keyboard.append(kb_row)
        return {'inline_keyboard': inline_keyboard}

    elif markup_type == 'keyboard':
        keyboard = []
        for row in input_data.get('data', []):
            kb_row = []
            for value in row:
                if not isinstance(value, dict):
                    continue
                btn_type = value.get('type', 'text')
                if isinstance(btn_type, str):
                    btn_type = btn_type.lower()
                text = value.get('text', '')
                btn = {'text': text}

                # Add style if present
                style = _style_color(value.get('style'))
                if style:
                    btn['style'] = style

                # Add custom emoji if present
                emoji_id = value.get('icon_custom_emoji_id')
                if emoji_id:
                    btn['icon_custom_emoji_id'] = str(emoji_id)

                if btn_type == 'requestlocation':
                    btn['request_location'] = True
                elif btn_type == 'requestphone':
                    btn['request_contact'] = True
                elif btn_type == 'requestpoll':
                    btn['request_poll'] = {}
                # 'text' type: just text button (default)

                kb_row.append(btn)
            keyboard.append(kb_row)

        result = {'keyboard': keyboard, 'resize_keyboard': input_data.get('resize', True)}
        if input_data.get('one_time'):
            result['one_time_keyboard'] = True
        if input_data.get('is_personal'):
            result['is_persistent'] = True
        return result

    elif markup_type == 'forcereply':
        return {'force_reply': True, 'selective': input_data.get('is_personal', False)}

    elif markup_type == 'remove':
        return {'remove_keyboard': True, 'selective': input_data.get('is_personal', False)}

    return None


# ------------------------------------------------------------------
# FastBots - Main class using Telegram Bot API directly
# ------------------------------------------------------------------
class FastBots:
    """
    Telegram Bot API wrapper - no TDLib needed.
    Uses HTTP requests to api.telegram.org directly.
    Supports button styling and custom emoji.
    """

    def __init__(self):
        self.token = None
        self.api_id = None
        self.api_hash = None
        self.session_name = None
        self.base_url = None
        self.get_update = True
        self._update_functions = []
        self._timers = []
        self._offset = 0

    def set_config(self, api_id=None, api_hash=None, session_name=None, token=None, **kwargs):
        self.api_id = api_id
        self.api_hash = api_hash
        self.session_name = session_name
        self.token = token
        self.base_url = f"https://api.telegram.org/bot{token}"
        return self

    def set_bot(self, api_hash=None, api_id=None, session_name=None, token=None, **kwargs):
        return self.set_config(api_id=api_id, api_hash=api_hash, session_name=session_name, token=token, **kwargs)

    def replyMarkup(self, input_data):
        return reply_markup(input_data)

    def base64_encode(self, data):
        if isinstance(data, str):
            data = data.encode('utf-8')
        return base64.b64encode(data).decode('utf-8')

    def base64_decode(self, data):
        if isinstance(data, str):
            data = data.encode('utf-8')
        return base64.b64decode(data).decode('utf-8')

    # --- Core API call ---
    def _api_call(self, method, **params):
        """Make a Telegram Bot API call."""
        url = f"{self.base_url}/{method}"
        # Remove None values
        clean = {k: v for k, v in params.items() if v is not None}
        # Serialize dicts/lists as JSON
        for k, v in clean.items():
            if isinstance(v, (dict, list)):
                clean[k] = json.dumps(v)
        try:
            res = requests.post(url, data=clean, timeout=30)
            if res.status_code != 200:
                try:
                    err = res.json()
                    print(f"API error ({method}): {err.get('description', res.text[:200])}")
                except Exception:
                    print(f"API error ({method}): HTTP {res.status_code}")
                return None
            return res.json()
        except Exception as e:
            print(f"API call error ({method}): {e}")
            return None

    # --- Send methods ---
    def sendText(self, chat_id, reply_to_message_id=0, text='', parse_mode=None,
                 disable_web_page_preview=None, clear_draft=None,
                 disable_notification=None, from_background=None, reply_markup=None):
        params = {
            'chat_id': chat_id,
            'text': text,
        }
        if reply_to_message_id:
            params['reply_to_message_id'] = reply_to_message_id
        if parse_mode:
            pm = parse_mode.lower()
            if pm in ('md', 'markdown'):
                params['parse_mode'] = 'Markdown'
            elif pm in ('html', 'lg'):
                params['parse_mode'] = 'HTML'
        if disable_web_page_preview:
            params['disable_web_page_preview'] = True
        if disable_notification:
            params['disable_notification'] = True
        if reply_markup:
            params['reply_markup'] = reply_markup
        return self._api_call('sendMessage', **params)

    def sendMessage(self, chat_id, reply_to_message_id=0, input_message_content=None, parse_mode=None,
                    disable_notification=0, from_background=1, reply_markup=None):
        """Send message with input_message_content dict (TDLib-style compat)."""
        text = ''
        if isinstance(input_message_content, dict):
            text = input_message_content.get('text', {}).get('text', '') if isinstance(input_message_content.get('text'), dict) else input_message_content.get('text', '')
            if not text and input_message_content.get('caption'):
                text = input_message_content['caption'].get('text', '') if isinstance(input_message_content['caption'], dict) else input_message_content['caption']
        return self.sendText(chat_id, reply_to_message_id, text, parse_mode, None, None, disable_notification, None, reply_markup)

    def sendPhoto(self, chat_id, reply_to_message_id=0, photo=None, caption='', parse_mode=None, **kwargs):
        params = {'chat_id': chat_id, 'photo': photo}
        if reply_to_message_id: params['reply_to_message_id'] = reply_to_message_id
        if caption: params['caption'] = caption
        if parse_mode:
            pm = parse_mode.lower()
            params['parse_mode'] = 'Markdown' if pm in ('md', 'markdown') else 'HTML' if pm in ('html', 'lg') else None
        if kwargs.get('reply_markup'): params['reply_markup'] = kwargs['reply_markup']
        return self._api_call('sendPhoto', **params)

    def sendVideo(self, chat_id, reply_to_message_id=0, video=None, caption='', parse_mode=None, **kwargs):
        params = {'chat_id': chat_id, 'video': video}
        if reply_to_message_id: params['reply_to_message_id'] = reply_to_message_id
        if caption: params['caption'] = caption
        if parse_mode:
            pm = parse_mode.lower()
            params['parse_mode'] = 'Markdown' if pm in ('md', 'markdown') else 'HTML' if pm in ('html', 'lg') else None
        if kwargs.get('reply_markup'): params['reply_markup'] = kwargs['reply_markup']
        return self._api_call('sendVideo', **params)

    def sendVideoNote(self, chat_id, reply_to_message_id=0, video_note=None, **kwargs):
        params = {'chat_id': chat_id, 'video_note': video_note}
        if reply_to_message_id: params['reply_to_message_id'] = reply_to_message_id
        if kwargs.get('reply_markup'): params['reply_markup'] = kwargs['reply_markup']
        return self._api_call('sendVideoNote', **params)

    def sendVoiceNote(self, chat_id, reply_to_message_id=0, voice_note=None, caption='', parse_mode=None, **kwargs):
        params = {'chat_id': chat_id, 'voice': voice_note}
        if reply_to_message_id: params['reply_to_message_id'] = reply_to_message_id
        if caption: params['caption'] = caption
        if parse_mode:
            pm = parse_mode.lower()
            params['parse_mode'] = 'Markdown' if pm in ('md', 'markdown') else 'HTML' if pm in ('html', 'lg') else None
        if kwargs.get('reply_markup'): params['reply_markup'] = kwargs['reply_markup']
        return self._api_call('sendVoice', **params)

    def sendAnimation(self, chat_id, reply_to_message_id=0, animation=None, caption='', parse_mode=None, **kwargs):
        params = {'chat_id': chat_id, 'animation': animation}
        if reply_to_message_id: params['reply_to_message_id'] = reply_to_message_id
        if caption: params['caption'] = caption
        if parse_mode:
            pm = parse_mode.lower()
            params['parse_mode'] = 'Markdown' if pm in ('md', 'markdown') else 'HTML' if pm in ('html', 'lg') else None
        if kwargs.get('reply_markup'): params['reply_markup'] = kwargs['reply_markup']
        return self._api_call('sendAnimation', **params)

    def sendAudio(self, chat_id, reply_to_message_id=0, audio=None, caption='', parse_mode=None, **kwargs):
        params = {'chat_id': chat_id, 'audio': audio}
        if reply_to_message_id: params['reply_to_message_id'] = reply_to_message_id
        if caption: params['caption'] = caption
        if parse_mode:
            pm = parse_mode.lower()
            params['parse_mode'] = 'Markdown' if pm in ('md', 'markdown') else 'HTML' if pm in ('html', 'lg') else None
        if kwargs.get('reply_markup'): params['reply_markup'] = kwargs['reply_markup']
        return self._api_call('sendAudio', **params)

    def sendDocument(self, chat_id, reply_to_message_id=0, document=None, caption='', parse_mode=None, **kwargs):
        params = {'chat_id': chat_id, 'document': document}
        if reply_to_message_id: params['reply_to_message_id'] = reply_to_message_id
        if caption: params['caption'] = caption
        if parse_mode:
            pm = parse_mode.lower()
            params['parse_mode'] = 'Markdown' if pm in ('md', 'markdown') else 'HTML' if pm in ('html', 'lg') else None
        if kwargs.get('reply_markup'): params['reply_markup'] = kwargs['reply_markup']
        return self._api_call('sendDocument', **params)

    def sendSticker(self, chat_id, reply_to_message_id=0, sticker=None, **kwargs):
        params = {'chat_id': chat_id, 'sticker': sticker}
        if reply_to_message_id: params['reply_to_message_id'] = reply_to_message_id
        if kwargs.get('reply_markup'): params['reply_markup'] = kwargs['reply_markup']
        return self._api_call('sendSticker', **params)

    def sendLocation(self, chat_id, reply_to_message_id=0, latitude=None, longitude=None, **kwargs):
        params = {'chat_id': chat_id, 'latitude': latitude, 'longitude': longitude}
        if reply_to_message_id: params['reply_to_message_id'] = reply_to_message_id
        return self._api_call('sendLocation', **params)

    def sendContact(self, chat_id, reply_to_message_id=0, phone_number='', first_name='', last_name='', **kwargs):
        params = {'chat_id': chat_id, 'phone_number': str(phone_number), 'first_name': str(first_name)}
        if last_name: params['last_name'] = str(last_name)
        if reply_to_message_id: params['reply_to_message_id'] = reply_to_message_id
        return self._api_call('sendContact', **params)

    def sendVenue(self, chat_id, reply_to_message_id=0, latitude=None, longitude=None, title='', address='', **kwargs):
        params = {'chat_id': chat_id, 'latitude': latitude, 'longitude': longitude, 'title': str(title), 'address': str(address)}
        if reply_to_message_id: params['reply_to_message_id'] = reply_to_message_id
        return self._api_call('sendVenue', **params)

    def sendForwarded(self, chat_id, reply_to_message_id=0, from_chat_id=None, message_id=None, **kwargs):
        return self.forwardMessages(chat_id, from_chat_id, [message_id])

    # --- Forward ---
    def forwardMessages(self, chat_id, from_chat_id, message_ids, send_copy=0, disable_notification=0, from_background=True, as_album=False, server_oid=0, **kwargs):
        """Forward messages. Accepts TDLib-style 9-arg calls for compatibility."""
        if isinstance(message_ids, list):
            for mid in message_ids:
                self._api_call('forwardMessage', chat_id=chat_id, from_chat_id=from_chat_id, message_id=mid)
        else:
            self._api_call('forwardMessage', chat_id=chat_id, from_chat_id=from_chat_id, message_id=message_ids)
        return {'ok': True}

    # --- Edit ---
    def editMessageText(self, chat_id, message_id, text='', parse_mode=None, **kwargs):
        params = {'chat_id': chat_id, 'message_id': message_id, 'text': text}
        if parse_mode:
            pm = parse_mode.lower()
            params['parse_mode'] = 'Markdown' if pm in ('md', 'markdown') else 'HTML' if pm in ('html', 'lg') else None
        if kwargs.get('reply_markup'): params['reply_markup'] = kwargs['reply_markup']
        return self._api_call('editMessageText', **params)

    def editMessageCaption(self, chat_id, message_id, caption='', parse_mode=None, **kwargs):
        params = {'chat_id': chat_id, 'message_id': message_id, 'caption': caption}
        if parse_mode:
            pm = parse_mode.lower()
            params['parse_mode'] = 'Markdown' if pm in ('md', 'markdown') else 'HTML' if pm in ('html', 'lg') else None
        return self._api_call('editMessageCaption', **params)

    def editInlineMessageText(self, inline_message_id, input_message_content=None, **kwargs):
        text = ''
        if isinstance(input_message_content, dict):
            text = input_message_content.get('text', '')
        params = {'inline_message_id': inline_message_id, 'text': text}
        if kwargs.get('reply_markup'): params['reply_markup'] = kwargs['reply_markup']
        return self._api_call('editMessageText', **params)

    # --- Chat actions ---
    def sendChatAction(self, chat_id, action, progress=100):
        action_map = {
            'Typing': 'typing', 'UploadingPhoto': 'upload_photo', 'UploadingVideo': 'upload_video',
            'UploadingDocument': 'upload_document', 'RecordingAudio': 'record_voice',
            'UploadingAudio': 'upload_voice', 'UploadingVideoNote': 'upload_video_note',
            'FindingLocation': 'find_location'
        }
        api_action = action_map.get(action, action.lower() if isinstance(action, str) else 'typing')
        return self._api_call('sendChatAction', chat_id=chat_id, action=api_action)

    # --- Callback ---
    def answerCallbackQuery(self, callback_query_id, text='', show_alert=None, url=None, cache_time=None):
        params = {'callback_query_id': callback_query_id}
        if text: params['text'] = text
        if show_alert: params['show_alert'] = True
        if url: params['url'] = url
        if cache_time: params['cache_time'] = cache_time
        return self._api_call('answerCallbackQuery', **params)

    # --- Inline ---
    def answerInlineQuery(self, inline_query_id, results, **kwargs):
        return self._api_call('answerInlineQuery', inline_query_id=inline_query_id, results=json.dumps(results))

    # --- Get info ---
    def getMe(self):
        return self._api_call('getMe')

    def getUser(self, user_id):
        return self._api_call('getChatMember', chat_id=user_id, user_id=user_id)

    def getChat(self, chat_id):
        return self._api_call('getChat', chat_id=chat_id)

    def getMessage(self, chat_id, message_id):
        return self._api_call('forwardMessage', chat_id=chat_id, from_chat_id=chat_id, message_id=message_id)

    def searchPublicChat(self, username):
        """Search for a public chat/channel by username."""
        try:
            uname = username.lstrip('@')
            res = requests.get(f"https://api.telegram.org/bot{self.token}/getChat?chat_id=@{uname}", timeout=10)
            if res.status_code == 200:
                data = res.json()
                if data.get('ok'):
                    result = data['result']
                    # Return in TDLib-like format for compatibility
                    chat_id = result.get('id')
                    chat_type = result.get('type', '')
                    if chat_type == 'supergroup':
                        return {
                            'id': chat_id,
                            'type': {'@type': 'chatTypeSupergroup', 'supergroup_id': str(abs(int(chat_id)) - 1000000000000),
                                     'is_channel': result.get('is_channel', False)}
                        }
                    elif chat_type == 'channel':
                        return {
                            'id': chat_id,
                            'type': {'@type': 'chatTypeSupergroup', 'supergroup_id': str(abs(int(chat_id)) - 1000000000000),
                                     'is_channel': True}
                        }
                    else:
                        return {'id': chat_id, 'type': {'@type': 'chatTypePrivate', 'user_id': chat_id}}
        except Exception as e:
            print(f"searchPublicChat error: {e}")
        return None

    def getChatMember(self, chat_id, user_id):
        return self._api_call('getChatMember', chat_id=chat_id, user_id=user_id)

    def getChatAdministrators(self, chat_id):
        return self._api_call('getChatAdministrators', chat_id=chat_id)

    def getFile(self, file_id):
        return self._api_call('getFile', file_id=file_id)

    # --- Chat management ---
    def setChatTitle(self, chat_id, title):
        return self._api_call('setChatTitle', chat_id=chat_id, title=str(title))

    def setChatDescription(self, chat_id, description):
        return self._api_call('setChatDescription', chat_id=chat_id, description=str(description))

    def setChatPhoto(self, chat_id, photo):
        return self._api_call('setChatPhoto', chat_id=chat_id, photo=photo)

    def pinChatMessage(self, chat_id, message_id, disable_notification=None):
        return self._api_call('pinChatMessage', chat_id=chat_id, message_id=message_id, disable_notification=disable_notification)

    def unpinChatMessage(self, chat_id):
        return self._api_call('unpinChatMessage', chat_id=chat_id)

    def unpinAllChatMessages(self, chat_id):
        return self._api_call('unpinAllChatMessages', chat_id=chat_id)

    def deleteChatHistory(self, chat_id, **kwargs):
        return self._api_call('deleteChat', chat_id=chat_id)

    def leaveChat(self, chat_id):
        return self._api_call('leaveChat', chat_id=chat_id)

    def exportChatInviteLink(self, chat_id):
        return self._api_call('exportChatInviteLink', chat_id=chat_id)

    # --- Profile ---
    def setUsername(self, username):
        return None  # Bot API doesn't support this directly

    def setName(self, first_name, last_name=''):
        return None

    def setBio(self, bio):
        return None

    # --- Polling ---
    def run(self, callback):
        """Start long-polling for updates."""
        print(colors('%{yellow}FastBots v2.0 - Pure Python (No TDLib, No Redis) starting...\n'))

        while self.get_update:
            try:
                url = f"{self.base_url}/getUpdates"
                params = {'offset': self._offset, 'timeout': 30}
                res = requests.post(url, data=params, timeout=35)

                if res.status_code == 200:
                    data = res.json()
                    if data.get('ok') and data.get('result'):
                        for update in data['result']:
                            self._offset = update['update_id'] + 1

                            # Convert to TDLib-like format for compatibility
                            converted = self._convert_update(update)
                            if converted:
                                try:
                                    callback(converted)
                                except Exception as e:
                                    print(f"Callback error: {e}")
                                    traceback.print_exc()
                else:
                    time.sleep(1)

            except requests.exceptions.Timeout:
                continue
            except Exception as e:
                print(f"Polling error: {e}")
                time.sleep(2)

            # Check timers
            now = time.time()
            for timer in self._timers[:]:
                if timer['run_in'] <= now:
                    try:
                        timer['def'](timer['argv'])
                    except Exception as e:
                        print_error(str(e))
                    self._timers.remove(timer)

    def _convert_update(self, update):
        """Convert Telegram Bot API update to TDLib-like format for Fast.py compatibility."""
        import traceback

        msg = update.get('message') or update.get('edited_message') or update.get('channel_post') or update.get('edited_channel_post')

        if msg:
            chat_id = msg.get('chat', {}).get('id', 0)
            msg_id = msg.get('message_id', 0)
            from_user = msg.get('from', {})
            sender_id = from_user.get('id', 0)

            # Build TDLib-like message structure
            content = {}
            if msg.get('text'):
                content['text'] = {'text': msg['text']}
            if msg.get('photo'):
                content['photo'] = {'sizes': [{'photo': {'remote': {'id': p['file_id']}}, 'width': p.get('width'), 'height': p.get('height')} for p in msg['photo']]}
            if msg.get('video'):
                content['video'] = {'video': {'remote': {'id': msg['video']['file_id']}}}
            if msg.get('video_note'):
                content['video_note'] = {'video': {'remote': {'id': msg['video_note']['file_id']}}}
            if msg.get('voice'):
                content['voice_note'] = {'voice': {'remote': {'id': msg['voice']['file_id']}}}
            if msg.get('animation'):
                content['animation'] = {'animation': {'remote': {'id': msg['animation']['file_id']}}}
            if msg.get('document'):
                content['document'] = {'document': {'remote': {'id': msg['document']['file_id']}}}
            if msg.get('audio'):
                content['audio'] = {'audio': {'remote': {'id': msg['audio']['file_id']}}}
            if msg.get('sticker'):
                content['sticker'] = {'sticker': {'remote': {'id': msg['sticker']['file_id']}}}
            if msg.get('location'):
                content['location'] = {'latitude': msg['location']['latitude'], 'longitude': msg['location']['longitude']}
            if msg.get('contact'):
                content['contact'] = {'phone_number': msg['contact']['phone_number'], 'first_name': msg['contact']['first_name']}
            if msg.get('forward_origin') or msg.get('forward_from') or msg.get('forward_from_chat'):
                content['forward_info'] = True

            converted = {
                'Fastbots': 'updateNewMessage',
                'message': {
                    'id': msg_id,
                    'chat_id': chat_id,
                    'sender_id': {'user_id': sender_id},
                    'content': content,
                    'date': msg.get('date', 0),
                    'text': msg.get('text', ''),
                    'forward_info': content.get('forward_info'),
                    'reply_to_message_id': msg.get('reply_to_message', {}).get('message_id', 0) if msg.get('reply_to_message') else 0,
                },
                'chat_id': chat_id,
                'id': msg_id,
                'sender_id': {'user_id': sender_id},
                'content': content,
            }

            # Also flatten text for easy access
            if msg.get('text'):
                converted['text'] = msg['text']

            return converted

        elif update.get('callback_query'):
            cq = update['callback_query']
            return {
                'Fastbots': 'updateNewCallbackQuery',
                'sender_user_id': cq.get('from', {}).get('id', 0),
                'chat_id': cq.get('message', {}).get('chat', {}).get('id', 0),
                'message_id': cq.get('message', {}).get('message_id', 0),
                'payload': {'data': base64.b64encode(cq.get('data', '').encode()).decode() if cq.get('data') else ''},
                'id': cq.get('id', ''),
            }

        elif update.get('inline_query'):
            iq = update['inline_query']
            return {
                'Fastbots': 'updateNewInlineQuery',
                'sender_user_id': iq.get('from', {}).get('id', 0),
                'query': iq.get('query', ''),
                'offset': iq.get('offset', ''),
                'id': iq.get('id', ''),
            }

        return None

    @staticmethod
    def VERSION():
        print(colors('%{yellow}FastBots v2.0 - Pure Python Edition'))

    # --- Timers ---
    def set_timer(self, seconds, def_func, argv=None):
        if not isinstance(seconds, (int, float)) or not callable(def_func):
            return {'Fastbots': False}
        timer = {'def': def_func, 'argv': argv, 'run_in': time.time() + seconds}
        self._timers.append(timer)
        return {'Fastbots': True, 'run_in': timer['run_in'], 'timer_id': len(self._timers) - 1}

    def get_timer(self, timer_id):
        if 0 <= timer_id < len(self._timers):
            t = self._timers[timer_id]
            return {'Fastbots': True, 'run_in': t['run_in'], 'argv': t['argv']}
        return {'Fastbots': False}

    def cancel_timer(self, timer_id):
        if 0 <= timer_id < len(self._timers):
            del self._timers[timer_id]
            return {'Fastbots': True}
        return {'Fastbots': False}

    def add_events(self, def_func, filters):
        if not callable(def_func) or not isinstance(filters, list):
            return {'Fastbots': False}
        self._update_functions.append({'def': def_func, 'filters': filters})
        return {'Fastbots': True}
