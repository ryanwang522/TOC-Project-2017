# -*- coding: utf8 -*-
from transitions.extensions import GraphMachine
import random
import requests
from bs4 import BeautifulSoup 

url = None
more = False
animal = {'整體':' ', '事業':' ', '財富':' ', '感情':' '}
kidsTalk = {1:'為了保護我心愛的女人我會開槍', 2:'年輕人終究是年輕人 太衝動了', \
            3:'人不犯我，我不犯人。人如犯我，我變犯人', \
            4:'我是個愛情騙子\n看到我請不要回盼'}
def split_paragraph(src, front, end):
        tempList = src.split(front)
        tempList = tempList[1].split(end)
        return str(tempList[0]) 

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(
            model = self,
            **machine_configs
        )  

    def is_going_to_talk(self, update):
        if (update.message != None):
            text = update.message.text
            return text == '+1' or text == '一起狂'
        else:
            return False

    def is_going_to_sorry(self, update):
        if (update.message != None):
            text = update.message.text
            return text in u'這算什麼我更狂' or u'太狂了吧' in text
        else:
            return False

    def is_going_to_suck(self, update):
        if (update.message != None):
            text = update.message.text
            return u'我輸' in text
        else:
            return False

    def is_going_to_play(self, update):
        if (update.message != None):
            text = update.message.text
            return text == '+2' or text == '起乩'
        else:
            return False

    def is_going_to_east(self, update):
        if (update.message != None):
            text = update.message.text
            return text == '三太子'
        else:
            return False

    def is_going_to_animal(self, update):
        if (update.message != None):
            text = update.message.text
            return text in '鼠牛虎兔龍蛇馬羊猴雞狗豬'
        else:
            return False

    def is_going_to_animalDetail(self, update):
        if (update.message != None):
            text = update.message.text
            return text == '事業' or text == '財富' or text == '感情' 
        else:
            return False
            
    def is_going_out_animalDetail(self, update):
        if (update.message != None):
            text = update.message.text
            return text != '事業' and text != '財富' and text != '感情'
        else:
            return False

    def is_going_to_west(self, update):
        if (update.message != None):
            text = update.message.text
            return text == '薇薇安'
        else:
            return False

    def is_going_to_astro(self, update):
        if (update.message != None):
            text = update.message.text
            return u'座' in text
        else:
            return False

    def is_going_to_astroDetail(self, update):
        if (update.message != None):
            text = update.message.text
            return text == '整體' or text == '事業' or text == '財富' or text == '愛情' 
        else:
            return False

    def is_going_to_math(self, update):
        if (update.message != None):
            text = update.message.text
            return text == '+3' or text == '算數學'
        else:
            return False

    def is_going_to_matheq(self, update):
        if (update.message != None):
            text = update.message.text
            return text == '87' or u'不會' in text
        else:
            return False

    def is_going_to_mathneq(self, update):
        if (update.message != None):
            text = update.message.text
            return text != '87' and u'不會' not in text
        else:
            return False
            
    def on_enter_talk(self, update):
        reply = u'想跟我一起狂？有比接下來這個更狂再來找我，有的話就說「這算什麼我更狂」，沒有就說「我輸ㄌ」'
        update.message.reply_text(reply)
        reply = u'［驚］油漆工人松姓少年把自己也變成油漆刷竟遭警察先生帶走。'
        with open('img/brush.jpg', 'rb') as photo:
            update.message.reply_photo(photo)
        update.message.reply_text(reply)

    def on_exit_talk(self, update):
        print('Leaving talk')

    def on_enter_sorry(self, update):
        print('Entering sorry')
        update.message.reply_text(u'大哥大姐拍謝，不想再打打殺殺')
        self.go_back(update)

    def on_exit_sorry(self, update):
        print('Leaving sorry')

    def on_enter_suck(self,update):
        reply = u'唉，其實妳們並不壞只是長壞了\n懂我意思嗎？\n#懂不懂阿孩子們\n#請分享'
        update.message.reply_text(reply)
        self.go_back(update)

    def on_exit_suck(self, update):
        print('Leaving suck')

    def on_enter_play(self, update):
        print('Entering play')
        reply = u'有什麼煩惱是嗎... 想要請「三太子」還是「薇薇安」降駕呢？'
        update.message.reply_text(reply)

    def on_exit_play(self, update):
        print('Leaving play')

    def on_enter_east(self, update):
        print('Entering east')
        reply = u'!@#*(&%@~！告訴我你的生肖吧，讓我來幫你看看！*&^^%@!...'
        update.message.reply_text(reply)

    def on_exit_east(self, update):
        print('Leaving east')

    #test
    def on_enter_animal(self, update):
        print('Entering animal')
        global url
        info = update.message.text
        animalNum = {'鼠':'-20179528989', '牛':'-20179250649', '虎':'-20173085857', \
                     '兔':'-20176750047', '龍':'-20175930235', '蛇':'-20172111447', \
                     '馬':'-20171050671', '羊':'-20178191351', '猴':'-20175374913', \
                     '雞':'-2017', '狗':'-20177176821', '豬':'-20173896574'}
        url = 'http://www.go4134.com/26143242312133823458/' + animalNum[info]
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'lxml')
        result = soup.select('.paragraph')
        str = split_paragraph(result[1].get_text(), '各方面運勢', '是非：')
        global animal
        animal['整體'] = result[0].get_text()
        animal['事業'] = split_paragraph(str, '事業：', '。')
        animal['財富'] = split_paragraph(str, '財運：', '。')
        animal['感情'] = split_paragraph(str, '感情：', '。')
        update.message.reply_text(result[0].get_text())
        reply = u'想聽更詳細的嗎？請告訴我想聽「事業」、「財富」、「感情」，記得付錢阿！'
        update.message.reply_text(reply)
        
    def on_exit_animal(self, update):
        print('Leaving animal')    

    def on_enter_animalDetail(self, update):
        print('Entering animal detail')
        global animal, kidsTalk
        info = update.message.text
        update.message.reply_text(animal[info])
        reply = '出來混總是要還的...\n告訴神明還想聽什麼吧！沒事的話我就要退駕了！#$&*#^&'
        if (info == '感情'):
            update.message.reply_text(kidsTalk[random.randint(1, 2)*2])
        else:
            update.message.reply_text(kidsTalk[random.randint(1, 4)])
        update.message.reply_text(reply)

    def on_exit_animalDetail(self, update):
        print('Leaving animal detail')    

    def on_enter_west(self, update):
        print('Entering west')
        reply = u'有什麼煩惱？告訴我你的星座（e.g. 雙子座）讓神明來幫你算算吧！'
        update.message.reply_text(reply)

    def on_exit_west(self, update):
        print('Leaving west')

    def on_enter_astro(self, update):
        print('Entering astro')
        info = update.message.text
        astroNum = {'牡羊座':'1', '金牛座':'2', '雙子座':'3', '巨蟹座':'4', '獅子座':'5', '處女座':'6', \
                '天秤座':'7', '天蠍座':'8', '射手座':'9', '魔羯座':'10', '水瓶座':'11' ,'雙魚座':'12'}
        global url
        url = "http://m.click108.com.tw/astro/index.php?astroNum=" + str(astroNum[info])
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'lxml')
        result = soup.select('#astroDailyWording')
        update.message.reply_text(result[0].get_text())
        reply = u'還想知道什麼嗎？告訴我你想聽「整體」、「事業」、「財富」還是「愛情」'
        update.message.reply_text(reply)
        #self.go_back(update)
        
    def on_exit_astro(self, update):
        print('Leaving astro')

    def on_enter_astroDetail(self, update):
        print('Entering detail')
        info = update.message.text
        astroDtl = {'整體':'#astroDailyData_all', '事業':'#astroDailyData_career', \
                    '財富':'#astroDailyData_money' , '愛情':'#astroDailyData_love'}
        global url
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'lxml')
        result = soup.select(str(astroDtl[info]))
        update.message.reply_text(result[0].get_text())
        reply = '神明會保佑你的，加油了兄弟'
        update.message.reply_text(reply)
        self.go_back(update)

    def on_exit_astroDetail(self, update):
        print('Leaving detail')

    def on_enter_math(self, update):
        print("Entering math")
        update.message.reply_text("想跟我算數學嗎？可是我只會一條算式...")
        update.message.reply_text("88 - 1 = ?")
    
    def on_exit_math(self, update):
        print('Living math')

    def on_enter_matheq(self, update):
        print('entering matheq')
        update.message.reply_text("等於你")
        self.go_back(update)
    
    def on_exit_matheq(self, update):
        print('Leaving matheq')

    def on_enter_mathneq(self, update):
        print('entering mathneq')
        update.message.reply_text('這樣也不會，等於 87 阿！看來你真的4個87ㄏㄏ')
        self.go_back(update)

    def on_exit_mathneq(self, update):
        print('Leaving mathneq')

    def to_user(self,update):
        print('to user')
        self.to_user(update)

    def on_enter_user(self, update):
        text = u"安安，台南人15單，缺真心朋友\n一起狂+1\n起乩+2\n算數學+3\n"
        update.message.reply_text(text)