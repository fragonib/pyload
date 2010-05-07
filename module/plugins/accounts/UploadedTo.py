# -*- coding: utf-8 -*-

"""
    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 3 of the License,
    or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
    See the GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, see <http://www.gnu.org/licenses/>.
    
    @author: mkaay
"""

from module.plugins.Account import Account
import re
from time import strptime, mktime

class UploadedTo(Account):
    __name__ = "UploadedTo"
    __version__ = "0.1"
    __type__ = "account"
    __description__ = """ul.to account plugin"""
    __author_name__ = ("mkaay")
    __author_mail__ = ("mkaay@mkaay.de")
    
    def getAccountInfo(self, name):
        req = self.core.requestFactory.getRequest(self.__name__, name)
        data = None
        for account in self.accounts:
            if account[0] == name:
                data = account
        if not data:
            return
        html = req.load("http://uploaded.to/", cookies=True)
        raw_traffic = re.search(r"Traffic left: </span><span class=.*?>(.*?)</span>", html).group(1)
        raw_valid = re.search(r"Valid until: </span> <span class=.*?>(.*?)</span>", html).group(1)
        traffic = int(self.parseTraffic(raw_traffic))
        validuntil = int(mktime(strptime(raw_valid.strip(), "%d-%m-%Y %H:%M")))
        return {"login":name, "validuntil":validuntil, "trafficleft":traffic}
    
    def login(self):
        for account in self.accounts:
            req = self.core.requestFactory.getRequest(self.__name__, account[0])
            req.load("http://uploaded.to/login", None, { "email" : account[0], "password" : account[1]}, cookies=True)