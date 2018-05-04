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

import base64
import json
import re

import xbmc
import xbmcgui
from resources.lib.modules import cache
from resources.lib.modules import client
from resources.lib.modules import control
from resources.lib.modules import masterani
from resources.lib.modules import streamangoFix
from resources.lib.modules.control import progressDialog
from resources.lib.modules.watched import Watched


def play(anime_id, episode_id):
    # try:
        # content = cache.get(masterani.get_anime_details(anime_id), 2)

        l1 = "Fetching video"
        progressDialog.create(heading="MasterAni", line1="Fetching video")
        progressDialog.update(0, line1=l1, line3="Loading hosts")
        hosts = client.request("http://www.masterani.me/api/hosts")

        if hosts is None:
            xbmcgui.Dialog().ok("Masterani", "Something went wrong.", "Please try again later")
            return
        else:
            hosts = json.loads(hosts)

        # Remove Drive.g from list as it is not supported
        for e in hosts:
            # if 'Drive.g' in e['name']:
            #     hosts.remove(e)
            if 'Aika' in e['name']:
                hosts.remove(e)

        progressDialog.update(25, line1=l1, line3="Loading episodes urls")

        videos = client.request("http://www.masterani.me/api/episode/%s?videos=1" % episode_id)
        #the episode id api show all hosts (id) and the embed id of each video; host id is used to identify which host to select later
        videos = json.loads(videos)['videos']
        progressDialog.update(50, line1=l1, line3="Picking nose")

        hostlist = []

        videos = sorted(videos, key=lambda k: (-int(k['type']), int(k['quality'])), reverse=True)
        print videos
        autoplay = control.setting("autoplay.enabled")
        maxq = control.setting("autoplay.maxquality")
        subdub = control.setting("autoplay.subdub")

        for video in videos:
            try: hostname = [x['name'] for x in hosts if int(x['id']) == int(video['host_id'])][0]
            #just sort the videos by quality
            except: continue


            subs = 'Sub' if video['type'] is 1 else 'Dub'
            quality = video['quality']
            if 'true' in autoplay:
                if subdub in subs and int(quality) <= int(maxq):
                    hostlist.append("%s | %s | %s" % (quality, subs, hostname))
            else:
                hostlist.append("%s | %s | %s" % (quality, subs, hostname))


        if len(hostlist) is 0:
            xbmcgui.Dialog().ok("Masterani", "No supported hosts found.")
            return



        if autoplay in 'false':
            hostdialog = control.dialog.select("Select host", hostlist)
        else:
            if len(hostlist) is 0:
                progressDialog.close()
                xbmcgui.Dialog().ok("Masterani", "No hosts found for autoplay.", "Change addon settings and try again.")
                hostdialog = -1
            else:
                hostdialog = 0

        if hostdialog == -1:
            progressDialog.close()
            control.execute('Dialog.Close(okdialog)')
            return
        #choosing video from host id and embed id
        host_id = videos[hostdialog]['host_id']
        embed_id = videos[hostdialog]['embed_id']
        vidQuality = int(videos[hostdialog]['quality'])
        if host_id is '':
            return

        prefix = ""
        suffix = ""
        #each host has a prefix and suffix that makes the URL work, taken from the hosts api
        for host in hosts:
            if str(host_id) in str(host['id']):
                prefix = host['embed_prefix']
                suffix = host['embed_suffix']
                break

        try:
            if suffix is not None:
                url = prefix + embed_id + suffix
            else:
                url = prefix + embed_id
        except:
            pass

        print url
        progressDialog.update(75, line1=l1, line3="Loading video")
        #finds direct mp4 file on site (different methods depending on host)
        if 'moe' in host['name']:
            content = base64.b64decode(re.compile("atob\('(.+?)'\)").findall(client.request(url))[0])
            mp4 = re.compile("source src=\"(.+?)\"").findall(content)[0]
        if 'MP4Upload' in host['name']:
            www = re.compile("\|www([0-9]+?)\|").findall(client.request(url))[0]
            content = re.compile("\|mp4\|video\|(.+?)\|282\|").findall(client.request(url))[0]
            mp4 = "https://www" + www + ".mp4upload.com:282/d/" + content + "/video.mp4"
        if 'Bakavideo' in host['name']:
            content = re.compile("go\((.+?)\)").findall(client.request(url))[0]
            content = content.replace("'", "").replace(", ", "/")
            content = "https://bakavideo.tv/" + content
            content = client.request(content)
            content = json.loads(content)
            content = content['content']
            content = base64.b64decode(content)
            mp4s = client.parseDOM(content, 'source', ret='src')

            mp4 = ""
            for link in mp4s:
                if str(vidQuality) in link:
                    mp4 = link

            if mp4 is "":
                mp4 = mp4s[0]

        if 'BETA' in host['name']:
            mp4 = embed_id
        #I think this has changed to Vidstreaming
        # if 'Vidstream' in host['name']:
        #     data = client.request(url)
        #     # mp4 = re.compile("source src='(.+?)'.+?" + str(quality) + "'/>").findall(data)[0]
        #     openload = re.compile("embedvideo\" src=\"(.+?)\"").findall(data)
        #
        #     if len(openload) > 0:
        #         openload = client.request(openload[0])
        #         try: import urlresolver
        #         except: pass
        #
        #         hmf = urlresolver.HostedMediaFile(openload[0])
        #         mp4 = hmf.resolve()
        #
        #         if mp4 is False:
        #             return
        #     else:
        #         mp4 = re.compile("source src='(.+?)'.+?" + str(quality) + "'/>").findall(data)
        #         if len(mp4) is 0:
        #             mp4 = re.compile("source src='(.+?)'").findall(data)[0]
        #         else:
        #             mp4 = mp4[0]
        #
        #     if 'googlevideo' in mp4:
        #         try: import urlresolver
        #         except: pass
        #         hmf = urlresolver.HostedMediaFile(mp4)
        #         mp4 = hmf.resolve()
        if 'Vidstreaming' in host['name']:
            mp4 = re.compile("file: '(.+?)',label").findall(client.request(url))[0]
        if 'Aniupload' in host['name']:
            mp4 = re.compile("\(\[\{src: \"(.+?)\"").findall(client.request(url))[0]

        if 'Openload' in host['name']:
            try: import urlresolver
            except: pass
            hmf = urlresolver.HostedMediaFile(url)
            mp4 = hmf.resolve()
        if 'Drive.g' in host['name']:
            mp4 = masterani.get_google_link(prefix + embed_id, vidQuality)
        if 'Rapidvideo' in host['name']:
            #Rapidvideo is a little weird in that there is only a single quality avavilble for selection
            #but in the player UI, there are a couple to choose from
            #it seems the code doesn't account for this and only allows the best quality available to be selected
            url = url + "&q=" + str(vidQuality) + "p"
            mp4 = re.compile("source src=\"(.+?)\"").findall(client.request(url))[0]
        if 'Tiwi.kiwi' in host['name']:
            #Tiwi kiwi only seems to work half the time
            #Some stream seem to have seperate audio and video sources, in which case I'm not sure how to handle
            #I can get either the audio or video working but not both
            #The method below works if there is a single source for the video (which works sometimes)
            content = re.compile("\|mp4\|(.+?)\|sources\|").findall(client.request(url))[0]
            mp4= "https://fs01.tiwicdn.net/" + content + "/v.mp4"
        if 'Streamango' in host['name']:
            #there's a different num and token for every request, so call once
            streamangoURL = client.request(url)
            #I had orginally thought that there was multiple links for different quality videos, but that doesb't seem to be the case
            numFinder = "',(.+?)\),height:"# + str(vidQuality)
            num = re.compile(numFinder).findall(streamangoURL)[0]
            #xbmc.log("num is: " + str(num))

            tokenFinder = "src:d\('(.+?)'," + str(num) + "\),height:" #+ str(vidQuality)
            #tokenFinder2 = "src:d\('(.+?)" + numFinder
            #xbmc.log("tokenFinder is: " + tokenFinder)
            #xbmc.log("tokenFinder2 is: " + tokenFinder2)

            #token2 = re.compile(tokenFinder2).findall(streamangoURL)[0]
            #xbmc.log("token2 is: " + str(token2))
            token = re.compile(tokenFinder).findall(streamangoURL)[0]
            #xbmc.log("token is: " + str(token))
            mp4 = "https:" + streamangoFix.d(token,int(num))
        progressDialog.close()
        MAPlayer().run(anime_id, episode_id, mp4)
    # except:
    #     pass


class MAPlayer(xbmc.Player):
    def __init__(self):
        xbmc.Player.__init__(self)
        self.anime_id = 0
        self.episode_id = 0

    def run(self, anime_id, episode_id, url):
        control.sleep(200)

        self.anime_id = int(anime_id)
        self.episode_id = int(episode_id)

        item = control.item(path=url)

        try:
            c = cache.get(masterani.get_anime_details, 3, self.anime_id)

            ctype = c['type']
            ctype = 'video' if int(ctype) is 2 else 'episode'

            tvshowtitle = c['title']
            poster = c['poster'][0]

            item.setArt({'thumb': poster, 'poster': poster, 'tvshow.poster': poster, 'season.poster': poster})

            e = c['episodes'][self.episode_id]
            title = e['info']['title']
            season = 1
            if season is None: season = 1
            episode = e['info']['episode']
            if ctype is 'video': title = c['title']
            if title is None: title = "Episode %s" % episode

            item.setInfo(type="video",
                         infoLabels={'tvshowtitle': tvshowtitle, 'title': title, 'episode': int(episode),
                                     'season': int(season), 'mediatype': ctype})
        except:
            pass

        item.setProperty('Video', 'true')
        item.setProperty('IsPlayable', 'true')

        self.play(url, item)

        self.playback_checker()

        pass

    def playback_checker(self):
        for i in range(0, 300):
            if self.isPlaying():
                break
            xbmc.sleep(100)

        while self.isPlaying():
            try:
                if (self.getTime() / self.getTotalTime()) >= .8:
                    Watched().mark(self.anime_id, self.episode_id)
            except:
                pass
            xbmc.sleep(1000)

    def onPlayBackStarted(self):
        control.execute('Dialog.Close(all,true)')
        control.setSetting("anime.lastvisited", str(self.anime_id))
        pass

    def onPlayBackEnded(self):
        self.onPlayBackStopped()
        pass

    def onPlayBackStopped(self):
        control.refresh()
        pass
