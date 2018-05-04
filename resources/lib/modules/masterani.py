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
import os
import re
import sqlite3
import urllib
import urllib2

from resources.lib.modules import net
from resources.lib.modules import client
from resources.lib.modules import control


def get_anime_details(anime_id):
    # print "Getting anime details: %s" % url
    try:
        result = client.request("http://www.masterani.me/api/anime/%s/detailed" % anime_id, timeout=60)
        result = json.loads(result)

        info = result['info']


        anime_id = info['id']
        title = info['title']
        type = info['type']
        plot = info['synopsis'] if 'synopsis' in info else ''
        premiered = info['started_airing_date'] if 'started_airing_date' in info else ''
        rating = info['score'] if 'score' in info else 0
        episode_count = info['episode_count'] if 'episode_count' in info else 0
        age_rating = info['age_rating'] if 'age_rating' in info else ''
        tvdb = info['tvdb_id'] if 'tvdb_id' in info else 0
        genre = [g['name'] for g in result['genres']]
        genre = ' / '.join(genre)

        status = info['status'] if 'status' in info else 0
        duration = info['episode_length'] if 'episode_length' in info else 24
        if duration is None or duration is 0: duration = 24

        episodes = result['episodes']
        fanart = [f['file'] for f in result['wallpapers']]
        poster = result['poster'] if 'poster' in result else None
        episodes2 = dict()

        for episode in episodes:
            episodes2[episode['info']['id']] = episode

        return (
            {'title': title, 'anime_id': anime_id, 'plot': plot, 'poster': poster, 'premiered': premiered,
             'rating': rating, 'type': type, 'episode_count': episode_count, 'age_rating': age_rating, 'tvdb': tvdb,
             'genre': genre, 'status': status, 'duration': duration, 'episodes': episodes2, 'fanart': fanart})

    except:
        pass

def extract_data_from_filter_list(data):
    mlist = []
    for e in data['data']:
        anime_id = e['id']
        title = e['title']
        type = e['type']
        plot = e['synopsis'] if 'synopsis' in e else ''
        premiered = e['started_airing_date'] if 'started_airing_date' in e else ''
        rating = e['score'] if 'score' in e else 0
        episode_count = e['episode_count'] if 'episode_count' in e else 0
        age_rating = e['age_rating'] if 'age_rating' in e else ''
        tvdb = e['tvdb_id'] if 'tvdb_id' in e else 0
        genre = [g['name'] for g in e['genres']]
        genre = ' / '.join(genre)

        status = e['status'] if 'status' in e else 0
        duration = e['episode_length'] if 'episode_length' in e else 24
        if duration is None or duration is 0: duration = 24

        fanart = [f['file'] for f in e['wallpapers']]

        poster = e['poster'] if 'poster' in e else None
        poster = poster['file']

        mlist.append({'title': title, 'anime_id': anime_id, 'plot': plot, 'poster': poster, 'premiered': premiered,
             'rating': rating, 'type': type, 'episode_count': episode_count, 'age_rating': age_rating, 'tvdb': tvdb,
             'genre': genre, 'status': status, 'duration': duration, 'fanart': fanart})

    return mlist



# def get_by_genre_id(genre_id, anime_offset=0, limit=100, lsort=True, asc=True):
#     path = os.path.join(control.addonPath + "/resources/resources.db")
#     dbconn = sqlite3.connect(path)
#     sortby = "title" if 'True' in lsort else "score"
#     asc = "ASC" if 'True' in asc else "DESC"
#     print "%s, %s, %s" % (sortby, lsort, asc)
#     dbcur = dbconn.execute(
#         "SELECT anime_id,status FROM anime WHERE anime_id IN(SELECT anime_id FROM genremapping WHERE genre_id = '%s') ORDER BY %s %s LIMIT '%d'" % (
#             genre_id, sortby, asc, limit))
#     match = dbcur.fetchall()
#     # match = [tuple(g)[0] for g in match]
#     dbconn.close()
#     return match
#
#
# def get_by_select(genre=[], limit=5000, sort=0, status=0, stype=[]):
#     try:
#         sort = eval(sort)
#     except:
#         pass
#     try:
#         status = eval(status)
#     except:
#         pass
#     try:
#         genre = eval(genre)
#     except:
#         pass
#     try:
#         stype = eval(stype)
#     except:
#         pass
#
#     mainsql = "SELECT anime_id, status FROM anime WHERE "
#
#     genresql = ''
#     if len(genre) > 0:
#         genresql = " anime_id IN(SELECT anime_id FROM genremapping WHERE %s)" % ' OR '.join(
#             ["genre_id = %s" % str(x) for x in genre])
#
#     statussql = "status != 2 "
#     if status is not None:
#         statussql = "status = '%s' " % status
#
#     typesql = ""
#     if len(stype) > 0:
#         typesql += "type IN(%s)" % ",".join(str(x) for x in stype)
#
#     sortsql = ""
#     if sort is 0:
#         sortsql = " ORDER BY score ASC"
#     if sort is 1:
#         sortsql = " ORDER BY score DESC"
#     if sort is 2:
#         sortsql = " ORDER BY title ASC"
#     if sort is 3:
#         sortsql = " ORDER BY title DESC"
#
#     if len(genresql) > 0:
#         genresql += " AND "
#
#     if len(typesql) > 0:
#         typesql = " AND " + typesql
#
#     sql = mainsql + genresql + statussql + typesql + sortsql
#     print sql
#     path = os.path.join(control.addonPath + "/resources/resources.db")
#     dbconn = sqlite3.connect(path)
#     dbcur = dbconn.execute(sql + " LIMIT '%d'" % limit)
#     match = dbcur.fetchall()
#     # match = [tuple(g)[0] for g in match]
#     dbconn.close()
#     print "Matches found: %s" % len(match)
#     return match
#
#
# def get_by_search(search):
#     path = os.path.join(control.addonPath + "/resources/resources.db")
#     dbconn = sqlite3.connect(path)
#     dbcur = dbconn.execute("SELECT anime_id,status FROM anime WHERE title LIKE '%" + str(search) + "%'")
#     match = dbcur.fetchall()
#     # match = [tuple(g)[0] for g in match]
#     dbconn.close()
#     return match

def get_google_link(url, quality):
    # html = client.request(url)
    response = net.Net().http_GET(url)
    html = response.content
    links = _parse_gdocs(html)
    links = sorted(links, reverse=True)

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0'}
    if response is not None:
        res_headers = response.get_headers(as_dict=True)
        if 'Set-Cookie' in res_headers:
            headers['Cookie'] = res_headers['Set-Cookie']

    for l in links:
        if str(quality) in l[0]:
            return l[1] + append_headers(headers)

    return links[0][1] + append_headers(headers)


def _parse_gdocs(html):
    urls = []
    for match in re.finditer('\[\s*"([^"]+)"\s*,\s*"([^"]+)"\s*\]', html):
        key, value = match.groups()

        if key == 'fmt_stream_map':
            items = value.split(',')
            for item in items:
                _source_itag, source_url = item.split('|')
                if isinstance(source_url, unicode):
                    source_url = source_url.encode('utf-8')

                source_url = source_url.decode('unicode_escape')
                quality = itag_map.get(_source_itag, 'Unknown Quality [%s]' % _source_itag)
                source_url = urllib2.unquote(source_url)
                urls.append((quality, source_url))
            return urls

    return urls

itag_map = {'5': '240', '6': '270', '17': '144', '18': '360', '22': '720', '34': '360', '35': '480',
            '36': '240', '37': '1080', '38': '3072', '43': '360', '44': '480', '45': '720', '46': '1080',
            '82': '360 [3D]', '83': '480 [3D]', '84': '720 [3D]', '85': '1080p [3D]', '100': '360 [3D]',
            '101': '480 [3D]', '102': '720 [3D]', '92': '240', '93': '360', '94': '480', '95': '720',
            '96': '1080', '132': '240', '151': '72', '133': '240', '134': '360', '135': '480',
            '136': '720', '137': '1080', '138': '2160', '160': '144', '264': '1440',
            '298': '720', '299': '1080', '266': '2160', '167': '360', '168': '480', '169': '720',
            '170': '1080', '218': '480', '219': '480', '242': '240', '243': '360', '244': '480',
            '245': '480', '246': '480', '247': '720', '248': '1080', '271': '1440', '272': '2160',
            '302': '2160', '303': '1080', '308': '1440', '313': '2160', '315': '2160', '59': '480'}

def append_headers(headers):
    return '|%s' % '&'.join(['%s=%s' % (key, urllib.quote_plus(headers[key])) for key in headers])

    # get_anime_details(1)


def base36encode(integer):
    chars, encoded = '0123456789abcdefghijklmnopqrstuvwxyz', ''

    while integer > 0:
        integer, remainder = divmod(integer, 36)
        encoded = chars[remainder] + encoded

    return encoded

def MP4UploadJSFix(p,a,c,k):
    while c > 0:
        c=c-1
        if k[int(c)]:
            p = re.sub('\\b' + str(base36encode(c) + '\\b'), k[int(c)], p)

    return p
