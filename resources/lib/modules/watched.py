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
try:
    from sqlite3 import dbapi2 as database
except:
    from pysqlite2 import dbapi2 as database

from resources.lib.modules import cache
from resources.lib.modules import control
from resources.lib.modules import masterani


class Watched:
    def __init__(self):
        try:
            control.makeFile(control.dataPath)
            self.dbcon = database.connect(control.watchedFile)
            self.dbcur = self.dbcon.cursor()
            self.dbcur.execute(
                "CREATE TABLE IF NOT EXISTS watched (""anime_id INTEGER, ""episode_id INTEGER, UNIQUE(anime_id, episode_id) "");")
        except:
            pass

    def mark(self, anime_id, episode_id, unmark=None):
        try:
            if int(episode_id) == -999:
                if unmark is None:
                    result = cache.get(masterani.get_anime_details, 1, anime_id)
                    episodes = result['episodes'] if 'episodes' in result else ''
                    for e in episodes:
                        self.dbcur.execute("INSERT OR IGNORE INTO watched VALUES (?, ?)", (anime_id, e))
                else:
                    self.dbcur.execute("DELETE FROM watched WHERE (anime_id = '%s')" % anime_id)
            else:
                if unmark is None:
                    self.dbcur.execute("INSERT OR IGNORE INTO watched VALUES (?, ?)", (anime_id, episode_id))
                else:
                    self.dbcur.execute(
                        "DELETE FROM watched WHERE (anime_id = '%s' and episode_id = '%s')" % (anime_id, episode_id))

            self.dbcon.commit()
            control.refresh()
        except:
            pass

    def watched(self, anime_id, episode_id=None):
        try:
            if episode_id is None:
                self.dbcur.execute("SELECT COUNT(*) FROM watched WHERE (anime_id = '%s')" % anime_id)
                return self.dbcur.fetchone()[0]
            else:
                self.dbcur.execute("SELECT * FROM watched WHERE (anime_id = '%s' and episode_id = '%s')" % (anime_id, episode_id))
                return self.dbcur.fetchone()
        except:
            pass