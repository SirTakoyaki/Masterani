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
import json
import random
import sys

import xbmc
from resources.lib.modules import cache
from resources.lib.modules import client
from resources.lib.modules import control
from resources.lib.modules import masterani
from resources.lib.modules import views
from resources.lib.modules import watched
from resources.lib.modules import workers
from resources.lib.modules.watched import Watched


class Indexer:
    def __init__(self):
        self.list = []
        self.posterurl = "http://cdn.masterani.me/poster/%s"
        self.fanarturl = "http://cdn.masterani.me/wallpaper/0/%s"

    def get(self):
        try:
            self.list = cache.get(self.get_recent, 2)
            self.add_directory(self.list)
            return self.list
        except:
            pass

    def worker(self):
        total = len(self.list)

        threads = []
        for r in range(0, total, 30):
            for i in range(r, r + 30):
                if i <= total: threads.append(workers.Thread(self.get_fanart, i))
        [i.start() for i in threads]

        timeout = 60
        progress = control.progressDialog
        progress.create(control.addonInfo('name'), '')
        progress.update(0, line1="%s episodes found." % total, line2="Loading recent information.")

        for i in range(timeout * 10):
            if xbmc.abortRequested is True: return sys.exit()

            progress.update(int((100 / float(len(threads))) * len([x for x in threads if x.is_alive() is False])),
                            line3="%s animes remaining." % len([x for x in threads if x.is_alive() is True]))
            if progress.iscanceled(): break

            is_alive = [x.is_alive() for x in threads]
            if all(x is False for x in is_alive): break
            xbmc.sleep(100)

    def get_recent(self):
        try:
            result = client.request("http://www.masterani.me/api/releases/detailed")
        except:
            return

        result = json.loads(result)
        for i in result:
            a = i['anime']
            anime_id = a['id']
            anime_title = a['title']
            poster = a['poster']
            fanart = a['wallpaper']
            genres = a['genres']

            e = i['episode']
            episode_id = e['id']
            episode = e['episode']
            episode_title = e['title']
            episode_duration = e['duration']
            premiered = e['official_air_date']
            plot = e['description']
            self.list.append(
                {'action': 'get_episodes', 'anime_id': anime_id, 'tvshowtitle': anime_title, 'title': episode_title,
                 'duration': episode_duration, 'premiered': premiered, 'plot': plot, 'poster': poster, 'fanart': fanart,
                 'episode': episode, 'episode_id': episode_id, 'genre': genres})
        return self.list

    def add_directory(self, items, mode=True):
        if items is None or len(items) == 0:
            return

        sysaddon = sys.argv[0]
        addon_poster = addon_banner = control.addonInfo('icon')
        addon_fanart = control.addonInfo('fanart')

        mode = 'episodes'
        for i in items:
            try:
                tvshowtitle = i['tvshowtitle']
                anime_id = i['anime_id']
                episode_id = i['episode_id'] if 'episode_id' in i else 0
                if episode_id is 0: continue

                duration = i['duration'] if 'duration' in i else 0
                if duration is 0 or duration is None:
                    duration = 24 * 60
                else:
                    duration = duration * 60


                url = '%s?action=play' % sysaddon
                try:
                    url += '&anime_id=%s&episode_id=%s' % (anime_id, episode_id)
                except:
                    pass

                episodetitle = i['title']
                plot = i['plot']
                if plot is u'' or plot is None: plot = "No overview of episode available at this time."

                season = 1
                episode = i['episode']
                if i['poster'] is not None: poster = self.posterurl % i['poster']
                else: poster = addon_poster
                if i['fanart'] is not None: fanart = self.fanarturl % i['fanart']
                else: fanart = addon_fanart
                premiered = i['premiered']

                genre = [g['name'] for g in i['genre']]
                genre = ' / '.join(genre)

                iswatched = Watched().watched(anime_id, episode_id)
                if iswatched:
                    overlay = 7
                    playcount = 1
                else:
                    overlay = 6
                    playcount = 0

                if episodetitle is not None:
                    label = "%s - %sx%s - %s" % (tvshowtitle, int(season), int(episode), episodetitle)
                else:
                    label = "%s - %sx%s" % (tvshowtitle, int(season), int(episode))

                item = control.item(label=label)

                try:
                    item.setArt({'poster': poster, 'fanart': fanart})
                    item.setInfo(type='Video', infoLabels={
                        'Plot': plot, 'Year': premiered, 'premiered': premiered, 'overlay': overlay,
                        'playcount': playcount, 'episode': episode, 'duration': duration, 'genre': genre,
                    })
                except:
                    pass

                item.setProperty('Fanart_Image', fanart)
                # item.setProperty('Video', 'true')
                # item.setProperty('IsPlayable', 'true')

                item.setProperty('startoffset', '0')
                item.setProperty('resumetime', '0')
                item.setProperty('totaltime', '1')

                item.addStreamInfo('video', {'codec': 'h264', 'width': 1280, 'height': 720, 'aspect': round(128 / 720)})
                item.addStreamInfo('audio', {'codec': 'aac', 'language': 'en', 'channels': 2})

                cm = []
                cm.append(
                    ('Browse anime', 'Container.Update(%s?action=get_episodes&anime_id=%s)' % (sysaddon, anime_id)))

                if iswatched:
                    cm.append(
                        ('Unmark as Watched', 'RunPlugin(%s?action=watched&anime_id=%s&episode_id=%s&unmark=True)' % (
                            sysaddon, anime_id, episode_id)))
                else:
                    cm.append(('Mark as Watched', 'RunPlugin(%s?action=watched&anime_id=%s&episode_id=%s)' % (
                        sysaddon, anime_id, episode_id)))
                item.addContextMenuItems(cm)

                control.addItem(handle=int(sys.argv[1]), url=url, listitem=item, isFolder=False)
            except:
                pass
        control.directory(int(sys.argv[1]), cacheToDisc=True)
        control.content(int(sys.argv[1]), mode)
        views.setView('episodes', {'skin.confluence': 504})
