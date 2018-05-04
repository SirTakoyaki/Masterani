# -*- coding: utf-8 -*-

'''
    Phoenix Add-on

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

import sys
import urlparse

params = dict(urlparse.parse_qsl(sys.argv[2].replace('?', '')))
print "params", params

try: action = params['action']
except: action = None

try: anime_id = params['anime_id']
except: anime_id = None

try: episode_id = params['episode_id']
except: episode_id = None

try: genre_id = params['genre_id']
except: genre_id = None

try: sort = params['sort']
except: sort = None

try: status = params['status']
except: status = None

try: stype = params['stype']
except: stype = []

try: genre = params['genre']
except: genre = []

try: offset = params['offset']
except: offset = 0

try: query = params['query']
except: query = None

try: unmark = params['unmark']
except: unmark = None

if action is None:
    from resources.lib.indexers import root
    root.main_menu()

elif action == 'recent':
    from resources.lib.indexers import recent
    recent.Indexer().get()

elif action == 'list':
    from resources.lib.indexers import animeshows
    animeshows.Indexer().selectdialog()

elif action == 'animelist':
    from resources.lib.indexers import animeshows
    animeshows.Indexer().get(anime_id)

elif action == 'get_episodes':
    from resources.lib.indexers import animeepisodes
    animeepisodes.Indexer().get(anime_id)

elif action == "get_by_select":
    from resources.lib.indexers import animeshows
    animeshows.Indexer().get_by_select(stype, sort, status, genre, offset)

elif action == 'play':
    from resources.lib.modules.player import play
    play(anime_id, episode_id)

elif action == 'search':
    from resources.lib.indexers import animeshows
    animeshows.Indexer().search(query)

elif action == 'clearCache':
    from resources.lib.modules import cache
    cache.clear()

elif action == "watched":
    from resources.lib.modules import watched
    watched.Watched().mark(anime_id, episode_id, unmark)

elif action == "add_favorite":
    from resources.lib.modules import favorites
    favorites.Favorites().add(anime_id)

elif action == "remove_favorite":
    from resources.lib.modules import favorites
    favorites.Favorites().delete(anime_id)

elif action == "favorites":
    from resources.lib.indexers import animeshows
    animeshows.Indexer().get_favorites()

elif action == 'authTrakt':
    from resources.lib.modules import trakt
    trakt.authTrakt()
