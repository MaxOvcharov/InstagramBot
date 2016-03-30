from instabot import InstaBot

bot = InstaBot(login="USER_LOGIN", password="PASSWORD",
               like_per_day=500,
               media_max_like=100,
               media_min_like=5,
               follow_per_day=10,
               follow_time=5*60*60,
               unfollow_per_day=10,
               max_like_for_one_tag=5,              
               tag_list=["photooftheday","beautiful","instadaily","follow","bestoftheday","followme","like","nature","repost","clouds","followback","likeforlike", "forest", "wood", "travel", "mountains", "mountain", "russia", "like4like", "follow4followback"],
               log_mod=0)

bot.new_auto_mod()
