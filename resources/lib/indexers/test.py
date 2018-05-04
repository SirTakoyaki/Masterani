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

from resources.lib.modules import selectdialog


class List:
    def __init__(self):
        self.listitems = []

    def createlist(self):
        self.type = ['TV', 'Movie', 'OVA', 'Special']
        self.sort = ['Score +', 'Score -', 'Title +', 'Title -']
        self.status = ['All', 'Completed', 'Ongoing', 'Not yet Aired']
        self.genre = ['Action', 'Adventure', 'Cars', 'Comedy', 'Dementia', 'Demons', 'Drama', 'Ecchi', 'Fantasy',
                      'Game', 'Harem', 'Historical', 'Horror', 'Josei', 'Kids', 'Magic', 'Martial Arts', 'Mecha',
                      'Military', 'Music', 'Mystery', 'Parody', 'Police', 'Psychological', 'Romance', 'Samurai',
                      'School', 'Sci-Fi', 'Seinen', 'Shoujo', 'Shoujo Ai', 'Shounen', 'Shounen Ai', 'Slice of Life',
                      'Space', 'Sports', 'Super Power', 'Supernatural', 'Thriller', 'Vampire', 'Yuri']
        genres = {57: u'Action', 58: u'Adventure', 59: u'Comedy', 60: u'Drama', 61: u'Sci-Fi', 62: u'Space',
                  63: u'Mystery', 64: u'Shounen', 65: u'Sports', 66: u'Josei', 67: u'Romance', 68: u'Slice of Life',
                  69: u'Cars', 70: u'Seinen', 71: u'Horror', 72: u'Police', 73: u'Psychological', 74: u'Thriller',
                  75: u'Martial Arts', 76: u'Super Power', 77: u'Fantasy', 78: u'School', 79: u'Ecchi',
                  80: u'Supernatural', 81: u'Vampire', 82: u'Historical', 83: u'Military', 84: u'Dementia',
                  85: u'Mecha', 86: u'Demons', 87: u'Samurai', 88: u'Magic', 89: u'Harem', 90: u'Music', 91: u'Shoujo',
                  92: u'Shoujo Ai', 93: u'Game', 94: u'Parody', 95: u'Kids', 96: u'Shounen Ai', 97: u'Yuri'}

        dialog = selectdialog.SelectDialog(title="Select", stype=self.type, sort=self.sort, status=self.status,
                                           genre=genres, callback=self.testfunc)
        dialog.doModal()
        # dialog = control.dialog.multiselect("bob", self.genre)

    def testfunc(self, stype=[], sort=[], status=[], genre=[]):
        print stype, sort, status, genre
