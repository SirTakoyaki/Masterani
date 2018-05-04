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

from resources.lib.modules import control


class Favorites:
    def __init__(self):
        try:
            control.makeFile(control.dataPath)
            self.dbcon = database.connect(control.favoriteFile)
            self.dbcur = self.dbcon.cursor()
            self.dbcur.execute("CREATE TABLE IF NOT EXISTS favorites (""anime_id INTEGER, UNIQUE(anime_id) "");")
        except:
            pass

    def add(self, anime_id):
        try:
            self.dbcur.execute("INSERT OR IGNORE INTO favorites VALUES (%s)" % anime_id)
            self.dbcon.commit()
            control.refresh()
        except:
            pass

    def delete(self, anime_id):
        try:
            self.dbcur.execute("DELETE FROM favorites WHERE (anime_id = '%s')" % anime_id)
            self.dbcon.commit()
            control.refresh()
        except:
            pass

    def is_favorite(self, anime_id):
        try:
            self.dbcur.execute("SELECT COUNT(*) FROM favorites WHERE (anime_id = '%s')" % anime_id)
            match = self.dbcur.fetchone()[0]
            if int(match) is 0:
                return False
            else:
                return True
        except:
            pass

    def list(self):
        try:
            self.dbcur.execute("SELECT * FROM favorites")
            return self.dbcur.fetchall()
        except:
            pass
