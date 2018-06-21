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
import xbmcgui
from resources.lib.indexers import root
from resources.lib.modules import cache
from resources.lib.modules import client
from resources.lib.modules import control
from resources.lib.modules import favorites
from resources.lib.modules import masterani
from resources.lib.modules import selectdialog
from resources.lib.modules import trakt
from resources.lib.modules import views
from resources.lib.modules import workers
from resources.lib.modules.favorites import Favorites
from resources.lib.modules.watched import Watched


class Indexer:
    def __init__(self):
        self.list = []
        self.current_page = 1
        self.last_page = 1
        self.next_page_url = ""
        self.posterurl = "http://cdn.masterani.me/poster/%s"
        self.fanarturl = "http://cdn.masterani.me/wallpaper/0/%s"
        self.filterurl = "http://www.masterani.me/api/anime/filter?"

    #""https://www.masterani.me/api/anime/filter?genres=&order=title&status=2&type=1"

    def get(self, url):
        try:
            self.list = self.get_list(url)
            self.worker()
            self.add_directory(self.list)
            return self.list
        except:
            pass

    def selectdialog(self):
        #self.type = {'TV': 0, 'Movie': 2, 'OVA': 1, 'Special': 3}
        self.type = {'All Types': None, 'TV': 0, 'Movie': 2, 'OVA': 1, 'Special': 3}
        self.sort = {'Score +': 0, 'Score -': 1, 'Title +': 2, 'Title -': 3}
        self.status = {'All': None, 'Completed': 0, 'Ongoing': 1}
        self.genre = {57: u'Action', 58: u'Adventure', 59: u'Comedy', 60: u'Drama', 61: u'Sci-Fi', 62: u'Space',
                      63: u'Mystery', 64: u'Shounen', 65: u'Sports', 66: u'Josei', 67: u'Romance', 68: u'Slice of Life',
                      69: u'Cars', 70: u'Seinen', 71: u'Horror', 72: u'Police', 73: u'Psychological', 74: u'Thriller',
                      75: u'Martial Arts', 76: u'Super Power', 77: u'Fantasy', 78: u'School', 79: u'Ecchi',
                      80: u'Supernatural', 81: u'Vampire', 82: u'Historical', 83: u'Military', 84: u'Dementia',
                      85: u'Mecha', 86: u'Demons', 87: u'Samurai', 88: u'Magic', 89: u'Harem', 90: u'Music',
                      91: u'Shoujo',
                      92: u'Shoujo Ai', 93: u'Game', 94: u'Parody', 95: u'Kids', 96: u'Shounen Ai', 97: u'Yuri'}
        dialog = selectdialog.SelectDialog(title="Select", stype=self.type, sort=self.sort, status=self.status,
                                           genre=self.genre, callback=self.get_by_select)
        dialog.doModal()

    def get_by_select(self, stype=0, sort=0, status=0, genre=[], offset=0):
        self.list = []

        offset_string = ""
        if offset > 1:
            offset_string = "&page=" + str(offset)

        sort_string = ""
        if sort is '0':
            sort_string = "score"
        if sort is '1':
            sort_string = "score_desc"
        if sort is '2':
            sort_string = "title"
        if sort is '3':
            sort_string = "title_desc"

        sort_string = "order="+sort_string

        try:
            genre = eval(genre)

        except:
            pass

        genre_string = ""
        if type(genre) is int:
            genre_string = "&genres=" + str(genre)

        if type(genre) is list:
            genre_string = "&genres=" + ','.join(str(x) for x in genre)

        try:
            status = eval(status)
        except:
            pass

        try:
            stype = eval(stype)
        except:
            pass

        if stype is None:
            type_string = ""
        else:
            type_string = "&type="+str(stype)

        if status is None:
            status_string = ""
        else:
            status_string = "&status="+str(status)


        url = self.filterurl + sort_string + status_string + type_string + genre_string + "&detailed=1" + offset_string
        print url
        result = client.request(url)
        result = json.loads(result)

        self.list = masterani.extract_data_from_filter_list(result)

        if len(self.list) is 0:
            xbmcgui.Dialog().ok("Masterani", "No anime found.", "Try other options.")
            return

        self.last_page = result['last_page']
        self.current_page = result['current_page']
        self.next_page_url = url + "?page=" + str(self.current_page + 1)

        # if offset > self.totalitems: glist = glist[offset: self.totalitems]
        # else: glist = glist[offset: offset + self.itemsperpage]
        #
        #
        # for i in glist: self.list.append({'anime_id': i[0], 'status': i[1]})
        #
        # self.worker()
        self.add_directory(self.list, stype=stype, sgenre=genre, status=status, sort=sort)

    def get_favorites(self):
        favorite = favorites.Favorites().list()
        favorite = [tuple(g)[0] for g in favorite]

        if len(favorite) > 0:
            for i in range(0, len(favorite)):
                self.list.append({'anime_id': favorite[i], 'status': 1})

            self.worker()
            self.add_directory(self.list)
        else:
            root.main_menu()

    def get_popular(self):
        result = client.request("https://www.masterani.me/api/anime/trending")
        result = json.loads(result)

        print result

        if len(result) is 0: return

        for i in result['popular_today']: self.list.append({'anime_id': i['slug'].split('-', 1)[0], 'status': 1})

        self.worker()
        self.add_directory(self.list)

    def search(self, query=None):
        if query is None:
            keydialog = control.keyboard('', "Enter Search")
            keydialog.doModal()
            self.query = keydialog.getText() if keydialog.isConfirmed() else None
        else:
            self.query = query

        if self.query is None or self.query is '': return

        if query is None:
            control.execute("Container.Update(%s?action=search&query=%s, false)" % (sys.argv[0], self.query))
            return

        result = client.request("http://www.masterani.me/api/anime/search?search=%s&sb=true" % self.query)
        result = json.loads(result)

        print result

        if len(result) is 0: return

        for i in result: self.list.append({'anime_id': i['id'], 'status': 1})

        self.worker()
        self.add_directory(self.list)

    def worker(self):
        try:
            total = len(self.list)

            threads = []
            for i in range(0, total):
                if i <= total: threads.append(workers.Thread(self.get_fanart, i))
            [i.start() for i in threads]

            timeout = 30
            progress = control.progressDialog
            progress.create(control.addonInfo('name'), '')
            progress.update(0, line1="%s shows found." % total, line2="Loading information.")

            print "Adding progress dialog with %s total shows" % total
            for i in range(timeout * 2):
                if xbmc.abortRequested == True: return sys.exit()

                progress.update(int((100 / float(len(threads))) * len([x for x in threads if x.is_alive() is False])),
                                line3="%s remaining." % len([x for x in threads if x.is_alive() is True]))
                if progress.iscanceled(): break

                is_alive = [x.is_alive() for x in threads]
                if all(x is False for x in is_alive): break
                xbmc.sleep(100)
            progress.close()
        except:
            pass

    def get_list(self, url, result=None):
        try:
            if result is None:
                result = client.request(url)
        except:
            return

        result = json.loads(result)

        for item in result:
            title = item['anime']['title']
            url = self.masterani_url + "api/anime/" + str(item['anime']['id']) + "/detailed"
            anime_id = item['anime']['id']
            self.list.append({'name': title, 'url': url, 'action': 'get_episodes', 'anime_id': anime_id})

        return self.list

    def get_fanart(self, i):
        try:
            if self.list[i]['status'] is 0:
                self.list[i].update(cache.get(masterani.get_anime_details, 150, self.list[i]['anime_id']))
            elif self.list[i]['status'] != 0 or 'title' not in self.list[i]:
                self.list[i].update(cache.get(masterani.get_anime_details, 0, self.list[i]['anime_id']))
            return self.list
        except:
            return None

    def add_directory(self, items, stype=0, sort=0, status=0, sgenre=[]):
        if items is None or len(items) == 0:
            return
        # print items

        sysaddon = sys.argv[0]
        addon_poster = addon_banner = control.addonInfo('icon')
        addon_fanart = control.addonInfo('fanart')

        # from resources.lib.modules import playcount
        # indicators = playcount.getTVShowIndicators(refresh=True)

        mode = 'tvshows'
        for i in items:
            # try:
                print i
                tvshowtitle = i['title']
                anime_id = i['anime_id']
                if anime_id is None: continue
                duration = i['duration']
                if duration is 0 or duration is None:
                    duration = 24 * 60
                else:
                    duration = duration * 60
                anime_id = i['anime_id']

                animetype = int(i['type'])

                # print "atype"
                # if animetype is 2:
                #     episode_id = 0
                #     try:
                #         episode_id = i['episodes'].keys()[0]
                #     except:
                #         pass
                #     if episode_id is 0: continue
                #
                #     url = '%s?action=play' % sysaddon
                #     try:
                #         url += '&anime_id=%s&episode_id=%s' % (anime_id, episode_id)
                #     except:
                #         pass
                # else:
                url = '%s?action=get_episodes' % sysaddon
                try:
                    url += '&anime_id=%s' % anime_id
                except:
                    pass

                plot = i['plot']
                if plot is u'' or plot is None: plot = "No overview of episode available at this time."

                episode = len(i['episodes']) if 'episodes' in i else 0
                try:
                    if 'episode_count' in i:
                        episode = int(i['episode_count'])
                except:
                    pass


                rating = i['rating']
                if rating is None or rating is 0: rating = 0.1
                genre = i['genre']

                if 'fanart' in i:
                    if len(i['fanart']) > 0:
                        fanart = i['fanart'][random.randint(0, len(i['fanart']) - 1)]
                        fanart = self.fanarturl % fanart
                    else:
                        fanart = addon_fanart
                else:
                    fanart = addon_fanart

                if i['poster'] is not None:
                    poster = self.posterurl % i['poster']
                else:
                    poster = addon_poster

                premiered = i['premiered']

                num_watched = Watched().watched(anime_id)
                # tvdb = i['tvdb']
                # if tvdb is not 0:
                # print playcount.getTVShowOverlay(indicators, str(tvdb))
                # print "%s, %s" % (tvdb, trakt.getTraktShowID(tvdb))
                # except: pass


                if num_watched is None: num_watched = 0
                if episode is None: episode = 0
                # print "%s, %s" % (episode, num_watched)
                iswatched = True if num_watched == episode else False
                if iswatched:
                    overlay = 7
                    pcount = 1
                else:
                    overlay = 6
                    pcount = 0

                item = control.item(label=tvshowtitle)

                try:
                    item.setArt({'poster': poster, 'thumb': poster})
                    item.setInfo(type='Video', infoLabels={
                        'Plot': plot, 'Year': premiered, 'premiered': premiered, 'episode': episode,
                        'duration': duration,
                        'genre': genre, 'rating': rating, 'overlay': overlay, 'playcount': pcount
                    })
                except:
                   pass

                if animetype is 2:
                    item.addStreamInfo('video',
                                       {'codec': 'h264', 'width': 1280, 'height': 720, 'aspect': round(128 / 720)})
                    item.addStreamInfo('audio', {'codec': 'aac', 'language': 'en', 'channels': 2})
                    item.setProperty('IsPlayable', 'true')

                item.setProperty('Fanart_Image', fanart)
                item.setProperty('WatchedEpisodes', str(num_watched))
                item.setProperty('UnWatchedEpisodes', str(episode - num_watched))

                cm = []
                cm.append(("Show Information", 'Action(Info)'))
                if iswatched:
                    cm.append(('Unmark Show as Watched',
                               'RunPlugin(%s?action=watched&anime_id=%s&episode_id=%s&unmark=True)' % (
                                   sysaddon, anime_id, -999)))
                else:
                    cm.append(('Mark Show as Watched',
                               'RunPlugin(%s?action=watched&anime_id=%s&episode_id=%s)' % (
                                   sysaddon, anime_id, -999)))

                if Favorites().is_favorite(anime_id):
                    cm.append(('Remove from Favorite Anime List',
                               'RunPlugin(%s?action=remove_favorite&anime_id=%s)' % (sysaddon, anime_id)))
                else:
                    cm.append(('Add to Favorite Anime List',
                               'RunPlugin(%s?action=add_favorite&anime_id=%s)' % (sysaddon, anime_id)))

                item.addContextMenuItems(cm)

                control.addItem(handle=int(sys.argv[1]), url=url, listitem=item, isFolder=True)
        # except:
            #     pass

        if self.current_page < self.last_page:
            item = control.item(label="Next Page")
            url = '%s?action=get_by_select' % sysaddon
            url += '&stype=%s&sort=%s&status=%s&genre=%s&offset=%s' % (
                stype, sort, status, sgenre, self.current_page + 1)

            item.setArt({'poster': addon_poster, 'fanart': addon_fanart})
            control.addItem(handle=int(sys.argv[1]), url=url, listitem=item, isFolder=True)

        control.directory(int(sys.argv[1]), cacheToDisc=True)
        #control.content(int(sys.argv[1]), mode)
        views.setView('tvshows', {'skin.confluence': 504})
