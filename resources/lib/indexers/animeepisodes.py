# -*- coding: utf-8 -*-

'''
    MasterAni Add-on

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''
import random
import sys

from resources.lib.modules import cache
from resources.lib.modules import control
from resources.lib.modules import masterani
from resources.lib.modules import views
from resources.lib.modules import watched
from resources.lib.modules.watched import Watched


class Indexer:
    def __init__(self):
        self.list = []
        self.duration = 0
        self.posterurl = "http://cdn.masterani.me/poster/%s"
        self.fanarturl = "http://cdn.masterani.me/wallpaper/0/%s"
        self.thumbnailurl = "http://cdn.masterani.me/episodes/%s"
        self.fanart = ''

    def get(self, url):
        self.list = self.get_episodes(url)
        self.episode_directory(self.list)
        return self.list

    def get_episodes(self, anime_id):
        animedata = cache.get(masterani.get_anime_details, 8, anime_id)

        episodes = animedata['episodes']
        self.duration = animedata['duration']
        if self.duration is None or self.duration is 0: self.duration = 24

        for episode in episodes:
            #print episode
            animedata['episodes'][episode]['info']['episode'] = animedata['episodes'][episode]['info']['episode'].split("-")[0]

        episodes = sorted(episodes, key=lambda k: float(episodes[k]['info']['episode']))

        for episode in episodes:
            e = animedata['episodes'][episode]['info']
            anime_id = animedata['anime_id']
            label = "Episode " + e['episode']
            episode_id = e['id']
            duration = e['duration']
            if duration is None or duration is 0:
                duration = self.duration * 60
            else:
                duration = duration * 60

            premiered = e['aired'] if 'aired' in e else 0
            title = e['title'] if 'title' in e else None
            episode_number = e['episode'] if 'episode' in e else ''
            season = e['season'] if 'season' in e else 1
            plot = e['description'] if 'description' in e else ''

            poster = animedata['episodes'][episode]['thumbnail']

            fanart = ''
            if len(animedata['fanart']) > 0:
                fanart = animedata['fanart'][random.randint(0, len(animedata['fanart']) - 1)]

            self.list.append(
                {'label': label, 'episode_id': episode_id, 'action': 'play', 'poster': poster, 'premiered': premiered,
                 'title': title,
                 'episode': episode_number, 'plot': plot, 'duration': duration, 'season': season, 'fanart': fanart,
                 'anime_id': anime_id})

        return self.list

    def episode_directory(self, items):
        if items is None or len(items) == 0:
            return
        sysaddon = sys.argv[0]
        addon_poster = addon_banner = control.addonInfo('icon')
        addon_fanart = control.addonInfo('fanart')

        if self.fanart is None:
            self.fanart = addon_fanart

        mode = 'episodes'
        j = 0
        for i in items:
            # try:
                j += 1
                tvshowtitle = i['title']
                if tvshowtitle is None: tvshowtitle = i['label']
                tvshowtitle = str(j) + ". " + tvshowtitle
                episode_id = i['episode_id']
                anime_id = i['anime_id']
                duration = i['duration']
                if duration is 0 or duration is None: duration = 24

                url = '%s?action=play' % sysaddon
                try:
                    url += '&anime_id=%s&episode_id=%s' % (anime_id, episode_id)
                except:
                    pass

                plot = i['plot']
                if plot is u'' or plot is None: plot = "No overview of episode available at this time."

                season = i['season']
                if season is 0 or season is None: season = 1

                episode = i['episode']
                if i['fanart'] is not None:
                    fanart = self.fanarturl % i['fanart']
                else:
                    fanart = addon_fanart

                if i['poster'] is not None:
                    poster = self.thumbnailurl % i['poster']
                else:
                    poster = addon_poster
                premiered = i['premiered']

                iswatched = Watched().watched(anime_id, episode_id)

                if iswatched:
                    overlay = 7
                    playcount = 1
                else:
                    overlay = 6
                    playcount = 0

                item = control.item(label=tvshowtitle)

                try:
                    item.setArt({'poster': poster})
                except:
                    pass
                try:
                    item.setInfo(type='Video', infoLabels={
                        'Plot': plot, 'plot': plot, 'Year': premiered, 'premiered': premiered, 'overlay': overlay,
                        'playcount': playcount, 'episode': episode, 'duration': duration, 'season': season,
                        'title': tvshowtitle, 'mediatype': 'episode'
                    })
                except:
                    pass

                item.setProperty('Fanart_Image', fanart)
                # item.setProperty('IsPlayable', 'true')

                item.setProperty('startoffset', '0')
                item.setProperty('resumetime', '0')
                item.setProperty('totaltime', '1')

                item.addStreamInfo('video', {'codec': 'h264', 'width': 1280, 'height': 720, 'aspect': round(128 / 720)})
                item.addStreamInfo('audio', {'codec': 'aac', 'language': 'en', 'channels': 2})

                cm = []
                if iswatched:
                    cm.append(('Unmark as Watched', 'RunPlugin(%s?action=watched&anime_id=%s&episode_id=%s&unmark=True)' % (
                        sysaddon, anime_id, episode_id)))
                else:
                    cm.append(('Mark as Watched', 'RunPlugin(%s?action=watched&anime_id=%s&episode_id=%s)' % (
                        sysaddon, anime_id, episode_id)))
                item.addContextMenuItems(cm)
                control.addItem(handle=int(sys.argv[1]), url=url, listitem=item, isFolder=False)
            # except:
            #     pass
        control.content(int(sys.argv[1]), mode)
        control.directory(int(sys.argv[1]), cacheToDisc=True)
        #views.setView('episodes', {'skin.confluence': 504})
