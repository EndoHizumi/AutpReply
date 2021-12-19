import json
import os
import requests
from time import sleep
from random import uniform, randint


def auto_reply(request):
    if request.method == 'GET':
        return "hello world"
    elif request.method == 'POST':
        request_json: dict = request.get_json()
        if request_json['type'] == 'url_verification':
            if os.environ['verification_token'] == request_json['token']:
                return (json.dumps({'challenge': request_json['challenge']}), 200, {})
            else:
                return (json.dumps(['']), 403, {})
        elif request_json['type'] == 'event_callback':
            # botとかblockがないので、スキップ。
            if not 'blocks' in request_json['event']:
                return '', 200
            # 返答処理
            mention_message(request_json['event']['blocks'][0]['elements']
                            [0]['elements'], request_json['event']['channel'],
                            request_json['event']['ts'],
                            request_json['event']['user'])
            return '', 200
        else:
            return '', 200
    else:
        return 'hello world'


def mention_message(blocks_elements: list, channel: str, time_stamp: str, user: str):
    mention_pattern = [
        '了解です！',
        '了解です',
        '了解でーす',
        '承知しました～',
        'わかりました！',
        'わかりました',
        'ピッカピカチュー！',
        'シャドーボール！',
        'わかりました。寿司が食いたいです。'
    ]
    # リプライじゃないときもスキップ
    if len(blocks_elements) < 2:
        return

    target_user = blocks_elements[0]['user_id']
    # 自分宛じゃないときは、飛ばす。
    if not os.environ['me'] == target_user:
        return '', 200
    
    
    sleep(uniform(1, 2))
    if not randint(1, 100) % 5: 
        payload = {'token': os.environ['token'],
               'channel': channel, 'name':'ok_hand', 'timestamp': time_stamp}
        res = requests.post('https://slack.com/api/reactions.add', data=payload)
    else:
        payload = {'token': os.environ['token'],
               'channel': channel, 'text': f'<@{user}> {mention_pattern[randint(0, len(mention_pattern)-1)]}'}
        requests.post('https://slack.com/api/chat.postMessage',
                        data=payload)
    return
