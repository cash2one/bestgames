#encoding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import shutil
from utils import make_image
import os
from django.template.loader import render_to_string

current_file_dir = os.path.split(os.path.realpath(__file__))[0]

class WeixinMessageItem(object):
    def __init__(self, image, title, digest, content):
        self.image = image
        self.title = title
        self.digest = digest
        self.content = content
        self.image_id = -1

class WeixinMessage(object):
    def __init__(self, entity_id, title, items):
        self.entity_id = entity_id
        self.title = title
        self.items = items

def _build_game_image(game):
    content = str(render_to_string('screenshots_weixin.tpl', {
        'screenshot_path_1' : game.screenshot_path_1.path,
        'screenshot_path_2' : game.screenshot_path_2.path,
        'screenshot_path_3' : game.screenshot_path_3.path,
        'screenshot_path_4' : game.screenshot_path_4.path
        }))
    return make_image(game.id, content)

def _normalize_content(content):
    url_pos = content.find('http://')
    normalized_content = content
    if url_pos != -1:
        normalized_content = normalized_content[5][:url_pos]
    return normalized_content + u'<br><br><font color="gray">回复游戏名获得该游戏的下载地址</font>'

def build_weixin_message(weixin):
    items = []
    index = 0
    message_title = ''
    if weixin.cover._file is not None and weixin.title is not None and weixin.recommended_reason is not None:
        message_title = weixin.title
        items.append(WeixinMessageItem(image=weixin.cover.path, title=weixin.title, digest=weixin.title, content=weixin.recommended_reason))
        index += 1
    for news in weixin.news.all():
        title = u'游戏情报站  -  %s' % news.brief_comment
        if index == 0:
            message_title = title
        items.append(WeixinMessageItem(image=news.image_url.path, title=title, digest=title, content=news.recommended_reason))
        index += 1
    for game in weixin.games.all():
        title = u'%s  -  %s' % (game.name, game.brief_comment)
        if index == 0:
            message_title = title
        if index > 0:
            items.append(WeixinMessageItem(image=game.icon.path, title=title, digest=title, content=_normalize_content(game.recommended_reason)))
        else:
            items.append(WeixinMessageItem(image=_build_game_image(game), title=title, digest=title, content=_normalize_content(game.recommended_reason)))
        index += 1
    for player in weixin.players.all():
        title = u'我是玩家  -  %s' % player.brief_comment
        if index == 0:
            message_title = title
        items.append(WeixinMessageItem(image=player.image_url.path, title=title, digest=title, content=player.recommended_reason))
        index += 1
    for puzzle in weixin.puzzles.all():
        title = u'趣题  -  %s' % puzzle.title
        if index == 0:
            message_title = title
        content = puzzle.description + '\n'
        content += 'A.' + puzzle.option1 + '\n'
        content += 'B.' + puzzle.option2 + '\n'
        content += 'C.' + puzzle.option3 + '\n'
        content += 'D.' + puzzle.option4 + '\n'
        content += u'回复"%d#你的答案"，参与答题得积分换礼品的活动吧\n' % puzzle.id
        items.append(WeixinMessageItem(image=image_url.path, title=title, digest=title, content=content))
        index += 1
    return WeixinMessage(weixin.id, message_title, items)
