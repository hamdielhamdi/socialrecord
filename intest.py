from FacebookWebBot import *
bot=FacebookBot()
bot.set_page_load_timeout(10)
bot.login("","")

allpost=bot.getPostInProfile("https://mbasic.facebook.com/profilid")
print(allpost)
