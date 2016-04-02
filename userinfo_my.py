#!/usr/bin/env python
# -*- coding: utf-8 -*-


import requests
import json
import pdb

class UserInfo:
    '''
    This class try to take some user info (following, followers, etc.)
    '''
    user_agent = ("Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/48.0.2564.103 Safari/537.36")

    url_list = {
                "ink361":
                     {
                      "main": "http://ink361.com/",
                      "user": "http://ink361.com/app/users/%s",
                      "search_name": "https://data.ink361.com/v1/users/search?q=%s",
                      "search_id": "https://data.ink361.com/v1/users/ig-%s",
                      "followers": "https://data.ink361.com/v1/users/ig-%s/followed-by",
                      "following": "https://data.ink361.com/v1/users/ig-%s/follows",
                      "stat": "http://ink361.com/app/users/ig-%s/%s/stats"
                     }
               }

    def __init__(self, info_aggregator="ink361"):
        self.i_a = info_aggregator
        self.unfollowing_list_id = []
        self.hello()

    def hello(self):
        self.s = requests.Session()
        self.s.headers.update({'User-Agent' : self.user_agent})
        main = self.s.get(self.url_list[self.i_a]["main"])
        if main.status_code == 200:
            return True
        return False

    def search_user(self, user_id=None, user_name=None):
        '''
        Search user_id or user_name, if you don't have it.
        '''
        
        self.user_id = user_id or False
        self.user_name = user_name or False

        if not self.user_id and not self.user_name:
            # you have nothing
            return False
        elif self.user_id:
            # you have just id
            search_url = self.url_list[self.i_a]["search_id"] % self.user_id
        elif self.user_name:
            # you have just name
            search_url = self.url_list[self.i_a]["search_name"] % self.user_name
        else:
            # you have id and name
            return True

        #print(search_url)
        search = self.s.get(search_url)

        if search.status_code == 200:
            r = json.loads(search.text)

            if self.user_id:
                # you have just id
                self.user_name = r["data"]["username"]
            else:
                for u in r["data"]:
                    if (u["username"] == self.user_name):
                        t = u["id"].split("-")
                        self.user_id = t[1]
                # you have just name
            return True
        return False

    def get_followers(self, limit=-1):
        self.followers = None
        self.followers = {}
        self.followers_list = []
        if self.user_id:
            next_url = self.url_list[self.i_a]["followers"] % self.user_id
            while True:
                followers = self.s.get(next_url)
                r = json.loads(followers.text)
                for u in r["data"]:
                    if  limit > 0 or limit < 0:
                        self.followers_list.append(u["username"])
                        self.followers[u["username"]] = u["id"].split("-")[1]
                                        #[u["profile_picture"] = u["profile_picture"],
                                        #[u"full_name"]= u["full_name"]
                                              
                        limit -= 1
                    else:
                        return True
                if r["pagination"]["next_url"]:
                    # have more data
                    next_url = r["pagination"]["next_url"]
                else:
                    # end of data
                    return True
        return False

    def get_following(self, limit=-1):
        self.following = None
        self.following = {}
        self.following_list = []
        if self.user_id:
            next_url = self.url_list[self.i_a]["following"] % self.user_id
            while True:
                
                #pdb.set_trace()
                following = self.s.get(next_url)
                r = json.loads(following.text)
                for u in r["data"]:
                    if limit > 0 or limit < 0:
                        self.following_list.append(u["username"])
                        self.following[u["username"]] = u["id"].split("-")[1]
                                        #[u["profile_picture"] = u["profile_picture"],
                                        #[u"full_name"]= u["full_name"]
                                              
                        limit -= 1
                    else:
                        return True
                if r["pagination"]["next_url"]:
                    # have more data
                    next_url = r["pagination"]["next_url"]
                else:
                    # end of data
                    self.following_list.sort()
                    return True
        return False

    def get_stat(self):
        # Print statistic of Following, Followers and Unfollowing list
        print('-'*144)
        print ('Following: ' + str(len(self.following_list)) + '; Followers: ' + str(len(self.followers_list)))
        print('-'*144)
        # Check if follower not in your following list. If True unfollowing him. 
        self.unfollowing_list_name = list(set(self.following_list).difference(self.followers_list))
        print("Unfollowing list: " + str (len(self.unfollowing_list_name)) + "-->>" + str(self.unfollowing_list_name))
        # Make unfollowing id list with special data for Instagram Bot
        for i in self.unfollowing_list_name:
            self.unfollowing_list_id.append([self.following[i], 0])
        print('-'*144)
        print("List of unfollowing id: " + str(self.unfollowing_list_id))
        print('-'*144)

        return self.unfollowing_list_id
if __name__ == '__main__':
    # example
    ui = UserInfo()
    # search by user_name:
    ui.search_user(user_name = raw_input("Please enter your USER_NAME: "))
    # or if you know user_id ui.search_user(user_id="50417061")
    print('It is your login: ' + ui.user_name + ' and ID: ' + ui.user_id)
    
    # get following list with no limit
    ui.get_following()
    print ('-'*144)
    print('Following list: ' + str(ui.following))
    print ('-'*144)
    
    # get followers list with no limit
    ui.get_followers()
    print("Followers_list: " + str(ui.followers))
    print('-'*144)
    
    ui.get_stat()

