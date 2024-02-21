import pygame as pg
import webbrowser as wb
import random,time,os,sys,urllib.request,requests,json,struct
res = requests.get("https://livefile.xesimg.com/programme/python_assets/c5d01a9e5189fef514bc1cc4e856abb3.TTF")
with open("STXINWEI.TTF","wb") as f:
    f.write(res.content)
res = requests.get("https://livefile.xesimg.com/programme/python_assets/6078b506afa793576f8a93475aab95b8.ttf")
with open("simkai.ttf","wb") as f:
    f.write(res.content)
res = requests.get("https://livefile.xesimg.com/programme/python_assets/242a828d266472665bf6ad46819772eb.TTF")
with open("STXINGKA.TTF","wb") as f:
    f.write(res.content)
pg.init()
if os.path.exists('D:\\'):
    if not os.path.isfile('D:\\score'):
        with open("D:\\score","w") as f:
            f.write('0')
else:
    if not os.path.isfile("C:\\Users\\Public\\score"):
        with open("C:\\Users\\Public\\score","w") as f:
            f.write('0')
if os.path.exists('D:\\'):
    if not os.path.isfile('D:\\coin'):
        with open("D:\\coin","w") as f:
            f.write('0')
else:
    if not os.path.isfile("C:\\Users\\Public\\coin"):
        with open("C:\\Users\\Public\\coin","w") as f:
            f.write('0')
if os.path.exists('D:\\'):
    if not os.path.isfile('D:\\goumai'):
        with open("D:\\goumai","w") as f:
            f.write('0\n')
            f.write('0')
else:
    if not os.path.isfile("C:\\Users\\Public\\goumai"):
        with open("C:\\Users\\Public\\goumai","w") as f:
            f.write('0\n')
            f.write('0')
if os.path.exists('D:\\'):
    if not os.path.isfile('D:\\killtank'):
        with open("D:\\killtank","w") as f:
            f.write('0')
else:
    if not os.path.isfile("C:\\Users\\Public\\killtank"):
        with open("C:\\Users\\Public\\killtank","w") as f:
            f.write('0')
class Bullet(pg.sprite.Sprite):
    def __init__(self,ai):
        super().__init__()
        self.ai = ai
        self.c = pg.image.load("bullet1.png")#.convert_alpha()
        self.c1 = pg.image.load("water.png")#.convert_alpha()
        self.c2 = pg.image.load("bullet3.png")
        self.rect = self.c.get_rect()
        self.rect.midtop = self.ai.br.midtop
        self.y = float(self.rect.y)
        self.image = self.c
        self.shanghai = 50
    def update(self):
        self.y -= 4
        self.rect.y = self.y
    def draw_b(self):
        self.ai.sc.blit(self.image,self.rect)
class Enemy(pg.sprite.Sprite):
    def __init__(self,ai):
        super().__init__()
        self.ai = ai
        self.image = pg.image.load("olp.png")#.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = 25
        self.rect.y = 40
        self.x = float(self.rect.x)
        self.life = 50
    def update(self):
        self.x += (1.0 * self.ai.fl_d)
        self.rect.x = self.x
    def c_e(self):
        s_r = self.ai.sc_rect
        if self.rect.right >= s_r.right or self.rect.left <= 0:
            return True
class A_B(pg.sprite.Sprite):
    def __init__(self,ai):
        super().__init__()
        self.ai = ai
        self.d = pg.image.load("7801.png")#.convert_alpha()
        self.d_r = self.d.get_rect()
    def update1(self):
        self.d_r.y += self.ai.bspeed
    def d_a_b(self):
        self.ai.sc.blit(self.d,self.d_r)
class Base(pg.sprite.Sprite):
    def __init__(self,ai):
        super().__init__()
        self.ai = ai
        self.e = pg.image.load("base2.png")#.convert_alpha()
        self.e_r = self.e.get_rect()
        self.e_r.x = self.ai.width / 2
        self.e_r.y = self.ai.height - 130
    def update(self):
        if self.ai.b_d:
            self.e_r.x += 4
        else:
            self.e_r.x -= 4
    def c_e(self):
        if self.e_r.right >= 600 or self.e_r.left <= 200:
            return True
    def d_ba(self):
        self.ai.sc.blit(self.e,self.e_r)
class Button:
    def __init__(self,ai):
        self.ai = ai
        self.f = pg.image.load("begin_game1.png").convert_alpha()
        self.f1 = pg.image.load("begin_game2.png").convert_alpha()
        self.image = self.f
        self.f_r = self.f.get_rect()
        self.f_r.x = 300
        self.f_r.y = 200
    def d_b(self):
        self.ai.sc.blit(self.image,self.f_r)
class Skills:
    def __init__(self,ai):
        self.ai = ai
        self.g = pg.image.load("skills0.png")
        self.g1 = pg.image.load("skills1.png")
        self.g2 = pg.image.load("skills2.png")
        self.g3 = pg.image.load("skills3.png")
        self.g4 = pg.image.load("skills4.png")
        self.g5 = pg.image.load("skills5.png")
        self.g6 = pg.image.load("skills6.png")
        self.g7 = pg.image.load("skills6.png")
        self.image = self.g
        self.g_r = self.g.get_rect()
        self.g_r.x = self.ai.br.x
        self.g_r.bottom = self.ai.br.top
        self.i = 0
    def change(self):
        self.i += 1
        if self.i == 3:
            self.image = self.g1
        if self.i == 6:
            self.image = self.g2
        if self.i == 9:
            self.image = self.g3
        if self.i == 12:
            self.image = self.g4
            self.g_r.y -= 120
        if self.i == 15:
            self.image = self.g5
            self.g_r.y -= 120
        if self.i == 18:
            self.image = self.g6
            self.g_r.y -= 120
        if self.i == 21:
            self.image = self.g7
            self.ai.dz2 = False
            self.i = 0
            self.image = self.g
            self.g_r.bottom = self.ai.br.top
    def d_g(self):
        self.ai.sc.blit(self.image,self.g_r)
class Box:
    def __init__(self,ai):
        self.ai = ai
        self.h = pg.image.load("box1.png").convert_alpha()
        self.h1 = pg.image.load("box2.png").convert_alpha()
        self.h2 = pg.image.load("box3.png").convert_alpha()
        self.a1 = [self.h,self.h1,self.h2]
        self.image = random.choice(self.a1)
        self.h_r = self.image.get_rect()
        self.h_r.x = random.randint(0,800)
        self.h_r.y = 0
    def update(self):
        self.h_r.y += 3
    def d_h(self):
        self.ai.sc.blit(self.image,self.h_r)
class S_B:
    def __init__(self,ai):
        self.ai = ai
        self.font = pg.font.Font("simkai.ttf",28)
        self.p_s()
        self.p_l()
        self.p_li()
        self.p_h_s()
    def p_s(self):
        s_s = "得分：" + str(self.ai.score)
        self.s_i = self.font.render(s_s,True,(0,225,0))
        self.s_r = self.s_i.get_rect()
        self.s_r.right = self.ai.sc_rect.right - 10
        self.s_r.top = 0
    def p_l(self):
        s_l = "关卡：" + str(self.ai.level)
        self.l_i = self.font.render(s_l,True,(0,255,0))
        self.l_r = self.l_i.get_rect()
        self.l_r.y = self.s_r.y + 25
        self.l_r.x = self.s_r.x
    def p_li(self):
        if self.ai.s_s1:
            s_l = "血量：" + str(self.ai.life + self.ai.s_l)
        else:
            s_l = "血量：" + str(self.ai.life)
        self.li_i = self.font.render(s_l,True,(0,255,0))
    def p_h_s(self):
        s_h = "最高分：" + str(self.ai.high_score)
        self.l_h = self.font.render(s_h,True,(0,255,0))
        self.l_h_r = self.l_h.get_rect()
        self.l_h_r.x = 350
    def s_h_s(self):
        self.ai.sc.blit(self.l_h,self.l_h_r)
    def s_li_i(self):
        self.ai.sc.blit(self.li_i,self.li_i.get_rect())
    def s_l_i(self):
        self.ai.sc.blit(self.l_i,self.l_r)
    def s_s_i(self):
        self.ai.sc.blit(self.s_i,self.s_r)
class Life:
    def __init__(self,ai):
        self.ai = ai
        self.life = pg.image.load("life.png")#.convert_alpha()
        self.s_l = pg.image.load("h_1.jpg")#.convert_alpha()
        self.s_l1 = pg.image.load("h_0.jpg")#.convert_alpha()
        self.image = self.s_l
        self.li_r = self.life.get_rect()
        self.li_r.y = 35
        self.s_l_r = self.s_l.get_rect()
        self.s_l_r.y = self.li_r.y + 63
        self.c_c()
    def c_c(self):
        if self.ai.life <= 10:
            self.color = (255,0,0)
        elif self.ai.life < 20:
            self.color = (255,205,0)
        else:
            self.color = (0,255,0)
    def c_d(self):
        pg.draw.line(self.ai.sc,self.color,
            [self.li_r.right,45],[self.ai.life * 3 + self.li_r.right,45])
        if self.ai.s_s1:
            pg.draw.line(self.ai.sc,(0,0,255),
                [self.s_l_r.right + 5,118],[self.ai.s_l * 3 + self.s_l_r.right,118])
            self.ai.sc.blit(self.image,self.s_l_r)
        self.ai.sc.blit(self.life,self.li_r)
class Switch:
    def __init__(self,ai):
        self.ai = ai
        self.i = pg.image.load("开.png")#.convert_alpha()
        self.i1 = pg.image.load("关.png")#.convert_alpha()
        self.image = self.i
        self.i_r = self.i.get_rect()
        self.i_r.x = self.ai.width - 43
        self.i_r.y = 45
    def d_i(self):
        self.ai.sc.blit(self.image,self.i_r)
class Shield:
    def __init__(self,ai):
        self.ai = ai
        self.g = pg.image.load("19.jpg").convert_alpha()
        self.g_r = self.g.get_rect()
        self.g_r.top = self.ai.br.top
        self.g_r.x = 420
        self.g_r.y = 600 - 123
    def d_g(self):
        self.ai.sc.blit(self.g,self.g_r)
class Music:
    def __init__(self,ai):
        self.ai = ai
        self.k = pg.image.load("sn.png").convert_alpha()
        self.k1 = pg.image.load("sn1.png").convert_alpha()
        self.image = self.k
        self.k_r = self.k.get_rect()
        self.k_r.y = self.ai.li.s_l_r.bottom + 11
        pg.mixer.music.load("1.mp3")
        pg.mixer.music.play(-1)
    def d_k(self):
        self.ai.sc.blit(self.image,self.k_r)
class Help:
    def __init__(self,ai):
        self.ai = ai
        self.l = pg.image.load("help2.png")#.convert_alpha()
        self.l1 = pg.image.load("help1.png")#.convert_alpha()
        self.l3 = pg.image.load("90.jpg")#.convert_alpha()
        self.l2 = pg.image.load("c2.png")#.convert_alpha()
        self.l4 = pg.image.load("c1.png")
        self.image = self.l
        self.image1 = self.l2
        self.l_r = self.l.get_rect()
        self.l_r.x = self.ai.button.f_r.x
        self.l_r.y = self.ai.button.f_r.y + 120
        self.l2_r = self.l2.get_rect()
        self.l2_r.right = 800
        self.l2_r.bottom = 600
        self.font = pg.font.Font("STXINGKA.TTF",35)
        self.font1 = pg.font.Font("STXINWEI.TTF",22)
    def d_help(self):
        self.ai.sc.blit(self.l3,self.l3.get_rect())
        s_h = self.font.render("飞坦大战帮助",True,(255,255,255))
        text = "ad←→移动飞船，f发射子弹，碰到任意宝箱后空格大招、护盾，金宝箱2次，"
        text1 = "空格大招，h护盾，护盾10滴血。飞船30滴血。坦克子弹速度随关卡增加，5、10关"
        text2 = "换子弹。15关胜利。黄宝箱还加1滴血、蓝宝箱还减1滴血。VIP首次登录会送10金币"
        text3 = "，每次护盾值+10"
        s_h3 = self.font1.render(text2,True,(0,0,245))
        s_h1 = self.font1.render(text,True,(0,0,255))
        s_h2 = self.font1.render(text1,True,(0,0,250))
        s_h4 = self.font1.render(text3,True,(0,0,240))
        s_h1_r = s_h1.get_rect()
        s_h2_r = s_h2.get_rect()
        s_h3_r = s_h3.get_rect()
        s_h4_r = s_h4.get_rect()
        s_h1_r.x = 50
        s_h1_r.y = 50
        s_h4_r.x = 10
        s_h2_r.y = s_h1_r.y + 55
        s_h3_r.y = s_h2_r.y + 55
        s_h4_r.y = s_h3_r.y + 55
        s_h_r = s_h.get_rect()
        s_h_r.x = 320
        self.ai.sc.blit(s_h3,s_h3_r)
        self.ai.sc.blit(s_h2,s_h2_r)
        self.ai.sc.blit(s_h1,s_h1_r)
        self.ai.sc.blit(s_h4,s_h4_r)
        self.ai.sc.blit(s_h,s_h_r)
        self.ai.sc.blit(self.image1,self.l2_r)
    def d_l(self):
        self.ai.sc.blit(self.image,self.l_r)
class Shop:
    def __init__(self,ai):
        self.ai = ai
        self.shop1 = pg.image.load("shop1.png")#.convert_alpha()
        self.shop2 = pg.image.load("shop2.png")#.convert_alpha()
        self.shop3 = pg.image.load("780.png")#.convert_alpha()
        self.l2 = pg.image.load("c2.png")#.convert_alpha()
        self.l3 = pg.image.load("c1.png")
        self.shops = pg.image.load("water.png")
        self.shops1 = pg.image.load("bullet1.png")
        self.shops2 = pg.image.load("bullet3.png")
        self.shops3 = pg.image.load("u.png")
        self.hd = pg.image.load("h_1.jpg")
        self.hd_r = self.hd.get_rect()
        font = pg.font.Font("STXINGKA.TTF",15)
        self.goumai = font.render("购买",True,(0,0,0))
        self.zhuangbei = font.render("装备",True,(0,0,0))
        self.yizhuangbei = font.render("已装备",True,(0,0,0))
        self.s_c = font.render("0$",True,(0,0,0))
        self.s1_c = 0
        self.s_c1 = font.render("10$",True,(0,0,0))
        self.s2_c = 10
        self.s_c2 = font.render("VIP专属",True,(0,0,0))
        self.s1_r = self.shop1.get_rect()
        self.s2_r = self.shop2.get_rect()
        self.s1_r.x = ai.help.l_r.x
        self.s1_r.y = ai.help.l_r.y + 120
        self.s2_r = self.s1_r
        self.image = self.shop1
        self.l2_r = self.l2.get_rect()
        self.l2_r.right = 800
        self.l2_r.bottom = 600
        self.shops_r = self.shops.get_rect()
        self.shops_r.x = 100
        self.shops_r.y = 300
        self.jieshao = font.render("水弹，伤害极低",True,(255,0,0))
        self.jieshao1 = font.render("普通子弹，伤害一般",True,(255,0,0))
        self.jieshao2 = font.render("穿透弹，伤害一般",True,(255,0,0))
        self.jieshao3 = font.render("护盾增强器，加10护盾",True,(255,0,0))
        self.jieshao_r = self.jieshao.get_rect()
        self.jieshao_r.centerx = self.shops_r.centerx
        self.jieshao_r.y = self.shops_r.y + 100
        self.jieshao1_r = self.jieshao1.get_rect()
        self.jieshao2_r = self.jieshao2.get_rect()
        self.jieshao3_r = self.jieshao3.get_rect()
        self.goumai_r = self.goumai.get_rect()
        self.goumai_r.midtop = self.shops_r.midbottom
        self.shops1_r = self.shops1.get_rect()
        self.shops1_r.x = self.shops_r.x + 150
        self.shops1_r.y = self.shops_r.y
        self.shops2_r = self.shops2.get_rect()
        self.shops2_r.x = self.shops1_r.x + 150
        self.shops2_r.y = self.shops_r.y
        self.shops3_r = self.shops3.get_rect()
        self.shops3_r.x = self.shops2_r.x + 300
        self.shops3_r.y = self.shops_r.y
        self.hd_r.x = self.shops2_r.x + 150
        self.hd_r.y = self.shops2_r.y
        self.jieshao1_r.centerx = self.shops1_r.centerx
        self.jieshao1_r.y = self.shops1_r.y + 100
        self.jieshao2_r.centerx = self.shops2_r.centerx
        self.jieshao2_r.y = self.shops2_r.y + 100
        self.jieshao3_r.centerx = self.hd_r.centerx
        self.jieshao3_r.y = self.hd_r.y + 100
        self.goumai_r1 = self.goumai.get_rect()
        self.goumai_r1.midtop = self.shops2_r.midbottom
        self.yizhuangbei_r = self.yizhuangbei.get_rect()
        self.yizhuangbei_r.midtop = self.shops1_r.midbottom
        self.image1 = self.goumai
        self.image2 = self.yizhuangbei
        self.image3 = self.goumai
        self.image4 = self.l2
        self.s_c_r = self.s_c.get_rect()
        self.s_c_r.center = self.shops_r.center
        self.s_c1_r = self.s_c1.get_rect()
        self.s_c1_r.center = self.shops2_r.center
        self.s_c2_r = self.s_c2.get_rect()
        self.s_c2_r.center = self.hd_r.center
        self.zb1 = False
        self.zb2 = True
        self.zb3 = False
        if os.path.exists("D:\\"):
            with open("D:\\goumai") as f:
                a = f.readlines()
        else:
            with open("C:\\Users\\Public\\score") as f:
                a = f.readlines()
        if a[0] == '1\n':
            self.image1 = self.zhuangbei
        if a[1] == '1':
            self.image3 = self.zhuangbei
    def d_s(self):
        self.ai.sc.blit(self.image,self.s1_r)
    def d_s1(self):
        self.ai.sc.blit(self.shop3,self.shop3.get_rect())
        self.ai.sc.blit(self.image4,self.l2_r)
        self.ai.sc.blit(self.shops,self.shops_r)
        self.ai.sc.blit(self.jieshao,self.jieshao_r)
        self.ai.sc.blit(self.image1,self.goumai_r)
        self.ai.sc.blit(self.shops1,self.shops1_r)
        self.ai.sc.blit(self.image2,self.yizhuangbei_r)
        self.ai.sc.blit(self.jieshao1,self.jieshao1_r)
        self.ai.sc.blit(self.shops2,self.shops2_r)
        self.ai.sc.blit(self.shops3,self.shops3_r)
        self.ai.sc.blit(self.jieshao2,self.jieshao2_r)
        self.ai.sc.blit(self.image3,self.goumai_r1)
        self.ai.sc.blit(self.s_c,self.s_c_r)
        self.ai.sc.blit(self.s_c1,self.s_c1_r)
        self.ai.sc.blit(self.hd,self.hd_r)
        self.ai.sc.blit(self.jieshao3,self.jieshao3_r)
        self.ai.sc.blit(self.s_c2,self.s_c2_r)
class Coin:
    def __init__(self,ai):
        self.ai = ai
        self.coin = pg.image.load("coin.png")
        self.coin_r = self.coin.get_rect()
        self.coin_r.bottom = ai.height
        self.coin_r.left = 0
        self.font = pg.font.Font("simkai.ttf",20)
        self.u_c()
    def u_c(self):
        self.text = self.font.render(f"{self.ai.coin}枚",True,(0,255,0))
        self.text_r = self.text.get_rect()
        self.text_r.midleft = self.coin_r.midright
    def d_c(self):
        self.ai.sc.blit(self.coin,self.coin_r)
        self.ai.sc.blit(self.text,self.text_r)
class Vip:
    def __init__(self,ai):
        a = self.getnowuser()
        self.ai = ai
        '''if a['user_id'] in vip:
            self.vip = True
        else:'''
        self.vip = False
        font = pg.font.Font("C:\\Windows\\Fonts\\simkai.ttf",25)
        if self.vip:
            self.b = font.render(a['user_name']+"（VIP）",True,(255,255,255))
        else:
            self.b = font.render(a['user_name'],True,(255,255,255))
        self.b_r = self.b.get_rect()
        self.b_r.bottom = ai.height
        self.b_r.right = ai.width
    def _nice(self,emoji_str):
    	return ''.join(
    		c if c <= '\uffff' else ''.join(chr(x) for x in struct.unpack('>2H', c.encode('utf-16be'))) for c in emoji_str)
    def getCookies(self):
        cookies = ""
        if len(sys.argv) > 1:
            try:
                cookies = json.loads(sys.argv[1])["cookies"]
            except:
                pass
        return cookies
    def get_info(self,id):
	    s = requests.Session()
	    headers = {'Accept': 'application/json, text/plain, */*', 'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6', 
	        'Cookie': 'xesId=b524835904a4a420cba3dde34890bade; user-select=scratch;  xes_run_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiIuY29kZS54dWVlcnNpLmNvbSIsImF1ZCI6Ii5jb2RlLnh1ZWVyc2kuY29tIiwiaWF0IjoxNjAxODA5NDcxLCJuYmYiOjE2MDE4MDk0NzEsImV4cCI6MTYwMTgyMzg3MSwidXNlcl9pZCI6bnVsbCwidWEiOiJNb3ppbGxhXC81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXRcLzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZVwvODUuMC40MTgzLjEyMSBTYWZhcmlcLzUzNy4zNiBFZGdcLzg1LjAuNTY0LjY4IiwiaXAiOiIxMTIuNDkuNzIuMTc1In0.9bXcb813GhSPhoUJkezZpV8O50ynm0hhYvszNyczznQ; prelogid=ef8f6d12febabf75bf9599744b73c6f5; xes-code-id=87f66376f1afd34f70339baeca61b7a1.8dbd833da9122d69a17f91054066dbb3; X-Request-Id=82f1c3968c8ff01ee151a0413f56aa84; Hm_lpvt_a8a78faf5b3e92f32fe42a94751a74f1=1601809487', 'Host': 'code.xueersi.com', 
	        'Proxy-Connection': 'keep-alive', 'Referer': 'http://code.xueersi.com/space/11909587', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36 Edg/85.0.564.68'}
	    total = json.loads(self._nice(s.get("http://code.xueersi.com/api/space/profile?user_id=" + str(id), headers=headers).text))["data"]
	    a = {"name": total["realname"],"slogan": total["signature"],"fans": total["fans"],"follows": total["follows"],"icon": total["avatar_path"]}
	    return a
    def getnowuser(self):
        try:
            a = self.getCookies()
            num = a.index("stu_id=") + 7
            id = ""
            for i in range(num, num + 100):
                if a[i] != ";":
                    id = id + a[i]
                else:
                    break
            try:
                user_info = self.get_info(id)
            except:
                user_info={"name":id+"号未知用户"}
                # 获取这个人的大部分信息，返回一个字典
                #:返回这个人的名字
            return {'state':True,'user_id':id, "user_name":user_info["name"]}
        except:
            return {"state":False,'user_id':"未登录","user_name":"未登录"}
    def draw(self):
        self.ai.sc.blit(self.b,self.b_r)
class Chengjiu:
    def __init__(self,ai):
        self.ai = ai
        self.chengjiu = False
        self.font = pg.font.Font("STXINGKA.TTF",35)
        self.font1 = pg.font.Font("simkai.ttf",15)
        self.a = pg.image.load("d.png")
        self.b = pg.image.load("olp1.png")
        self.b1 = pg.image.load("olp2.png")
        self.d = pg.image.load("d.jpg")
        self.e = pg.image.load("c2.png")
        self.e1 = pg.image.load("c1.png")
        self.g = pg.image.load("VIP.png")
        self.g1 = pg.image.load("VIP1.png")
        self.f = self.font1.render("累计打败1000个坦克",True,(0,0,0))
        self.h = self.font1.render("成为VIP（三连）",True,(0,0,0))
        self.f_r = self.f.get_rect()
        self.h_r = self.h.get_rect()
        self.image = self.b1
        self.image1 = self.e
        if self.ai.vip.vip:
            self.image2 = self.g
        else:
            self.image2 = self.g1
        self.g_r = self.g.get_rect()
        if os.path.exists("D:\\"):
            with open("D:\\killtank","r") as f:
                if int(f.read()) >= 1000:
                    self.image = self.b
        else:
            with open("C:\\Users\\Public\\killtank","r") as f:
                if int(f.read()) >= 1000:
                    self.image = self.b
        self.b_r = self.b.get_rect()
        self.b_r.x = 100
        self.b_r.y = 55
        self.g_r.x = self.b_r.x + 190
        self.g_r.y = self.b_r.y
        a = 0
        if self.image == self.b:
            a += 1
        if self.image2 == self.g:
            a += 1
        self.c = self.font.render(f"成就（达成{a}/2）",True,(0,0,0))
        self.c_r = self.c.get_rect()
        self.c_r.midtop = [400,0]
        self.d_r = self.d.get_rect()
        self.d_r.centerx = self.ai.sw.i_r.centerx
        self.d_r.y = self.ai.sw.i_r.y + 50
        self.e_r = self.e.get_rect()
        self.e_r.bottom = 600
        self.e_r.right = 800
        self.f_r.midtop = self.b_r.midbottom
        self.h_r.midtop = self.g_r.midbottom
    def draw_c(self):
        self.ai.sc.blit(self.a,self.a.get_rect())
        self.ai.sc.blit(self.image,self.b_r)
        self.ai.sc.blit(self.c,self.c_r)
        self.ai.sc.blit(self.image1,self.e_r)
        self.ai.sc.blit(self.f,self.f_r)
        self.ai.sc.blit(self.image2,self.g_r)
        self.ai.sc.blit(self.h,self.h_r)
    def draw_d(self):
        self.ai.sc.blit(self.d,self.d_r)
class E_B(pg.sprite.Sprite):
    def __init__(self,ai):
        super().__init__()
        self.ai = ai
        self.image = pg.image.load("base2.png")
        self.rect = self.image.get_rect()
        self.a_l = 50 + ai.level * 10
        self.rect.y = 300
    def draw(self):
        self.ai.sc.blit(self.image,self.rect)
class A_I:
    def __init__(self):
        self.size = self.width,self.height = 800,600
        self.en = self.width // (80 + 5)
        self.lm,self.rm = False,False
        self.f_d_s = 10
        self.fl_d = 1
        self.life = 50
        self.b_d = True
        self.start = False
        self.dz = 0
        self.dz2 = False
        self.score = 0
        self.a_s = 1
        self.level = 0
        self.start1 = True
        self.s_l = 10
        self.s_s = 0
        self.s_s1 = False
        self.help1 = False
        self.bspeed = 3
        self.win = False
        self.win1 = False
        self.shopping = False
        if os.path.exists("D:\\"):
            with open("D:\\score") as f:
                self.high_score = int(f.read())
        else:
            with open("C:\\Users\\Public\\score") as f:
                self.high_score = int(f.read())
        if os.path.exists("D:\\"):
            with open("D:\\coin") as f:
                self.coin = int(f.read())
        else:
            with open("C:\\Users\\Public\\score") as f:
                self.coin = int(f.read())   
        self.sc = pg.display.set_mode((self.size))
        self.a = pg.image.load("bg2(1).png")#.convert_alpha()
        self.sc_rect = self.sc.get_rect()
        self.b = pg.image.load("player.png")#.convert_alpha()
        self.br = self.b.get_rect()
        self.br.bottom = self.height
        self.bullet1 = Bullet(self)
        self.button = Button(self)
        self.skills = Skills(self)
        self.box = Box(self)
        self.s_b = S_B(self)
        self.li = Life(self)
        self.sw = Switch(self)
        self.sh = Shield(self)
        self.music = Music(self)
        self.help = Help(self)
        self.shop = Shop(self)
        self.coin1 = Coin(self)
        self.vip = Vip(self)
        self.chengjiu = Chengjiu(self)
        self.bullet = pg.sprite.Group()
        self.ene = pg.sprite.Group()
        self.a_b = pg.sprite.Group()
        self.base = pg.sprite.Group()
        self.e_b = pg.sprite.Group()
        self.br.left = self.width // 2
        self.c_f()
        self.u_b()
        self.run_game()
    def run_game(self):
        while True:
            if self.win1:
                self.coin += 30
                self.coin1.u_c()
                self.win1 = False
                time.sleep(5)
                self.win = False
            if self.coin < 10 and self.vip.vip and not self.shop.zb3 and self.shop.image3 != self.shop.zhuangbei:
                self.coin += 10
                self.coin1.u_c()
            self.s_b.p_s()
            self.s_b.p_l()
            self.s_b.p_li()
            self.s_b.p_h_s()
            self.check_events()
            self.update_screen()
            self.s_b.p_li()
            self.dz1()
            for i in self.ene:
                if i.life <= 0:
                    self.ene.remove(i)
            if self.level > 15:
                self.win = True
                self.start = False
                self.win1 = True
                if os.path.exists("D:\\"):
                    with open("D:\\killtank","r") as f:
                        a = int(f.read())
                    with open("D:\\killtank","w") as f1:
                        f1.write(str(self.score + a))
                else:
                    with open("C:\\Users\\Public\\killtank","r") as f:
                        a = int(f.read())
                    with open("C:\\Users\\Public\\killtank","w") as f1:
                        f1.write(str(self.score + a))
            if not self.s_s1:
                self.s_l = 0
            if self.s_l == 0:
                self.s_s1 = False
            if self.score > self.high_score:
                self.high_score = self.score
                self.s_b.p_h_s()
            if self.start and self.start1 and not self.win:
                for ii in self.base.sprites():
                    for i in self.ene.sprites():
                        if ii.e_r.colliderect(i):
                            self.a_b.remove(i)
                            self.base.remove(ii)
                if self.life <= 0:
                    self.lm,self.rm = False,False
                    self.f_d_s = 10
                    self.fl_d = 1
                    self.life = 50
                    self.dz = 0
                    if os.path.exists("D:\\"):
                        with open("D:\\killtank","r") as f:
                            a = int(f.read())
                        with open("D:\\killtank","w") as f1:
                            f1.write(str(self.score + a))
                    else:
                        with open("C:\\Users\\Public\\killtank","r") as f:
                            a = int(f.read())
                        with open("C:\\Users\\Public\\killtank","w") as f1:
                            f1.write(str(self.score + a))
                    self.score = 0
                    self.a_s = 1
                    self.s_l = 10
                    self.s_s = 0
                    self.bspeed = 3
                    self.s_b.p_h_s()
                    self.s_b.p_l()
                    self.s_b.p_li()
                    self.ene.empty()
                    self.bullet.empty()
                    self.a_b.empty()
                    self.level = 0
                    self.start = False
                    self.b_d = True
                    self.dz2 = False
                    self.s_s1 = False
                self.bullet.update()
                self.c_f_e()
                self.ene.update()
                for bu in self.bullet.copy():
                    if bu.rect.bottom <= 0:
                        self.bullet.remove(bu)
                if self.lm and self.br.left > 0:
                    self.br.x -= 2.5
                    self.sh.g_r.centerx = self.br.centerx
                    self.skills.g_r.centerx = self.br.centerx
                if self.rm and self.br.right < self.width:
                    self.br.x += 2.5
                    self.sh.g_r.centerx = self.br.centerx
                    self.skills.g_r.centerx = self.br.centerx
                for i in self.a_b:
                    i.update1()
                coll = pg.sprite.groupcollide(self.bullet,self.ene,False,False)
                if coll:
                    for i in coll.values():
                        self.score += self.a_s * len(i)
                        self.s_b.p_s()
                        for i1 in i:
                            for i2 in coll.keys():
                                shanghai = i2.shanghai
                                if not self.shop.zb3:
                                    self.bullet.remove(i2)
                            i1.life -= shanghai
                coll1 = pg.sprite.groupcollide(self.bullet,self.e_b,False,False)
                if coll1:
                    for i in coll1.values():
                        for i1 in i:
                            for i2 in coll1.keys():
                                shanghai1 = i2.shanghai
                                if not self.shop.zb3:
                                    self.bullet.remove(i2)
                            i1.a_l -= shanghai1
                            if i1.a_l <= 0:
                                self.e_b.remove(i1)
                if not self.ene:
                    self.bullet.empty()
                    self.level += 1
                    self.s_b.p_l()
                    self.c_f()
                    self.bspeed *= 1.2
                    self.coin += 1
                    self.coin1.u_c()
                for i in self.a_b.sprites():
                    if i.d_r.colliderect(self.br):
                        self.life -= 1
                        self.s_b.p_li()
                        self.li.c_c()
                        self.a_b.remove(i)
                    if i.d_r.y >= self.width:
                        self.a_b.remove(i)
                    for ii in self.base:
                        if i.d_r.colliderect(ii.e_r):
                            self.a_b.remove(i)
                            self.base.remove(ii)
                    if i.d_r.colliderect(self.sh.g_r):
                        if self.s_s:
                            self.a_b.remove(i)
                            self.s_l -= 1
                for i in self.ene.sprites():
                    if i.rect.colliderect(self.skills.g_r):
                        self.ene.remove(i)
                        self.score += 1
                        self.s_b.p_s()
                for i in self.e_b.sprites():
                    if i.rect.colliderect(self.skills.g_r):
                        i.a_l -= 100
                        if i.a_l <= 0:
                            self.e_b.remove(i)
                        else:
                            self.dz2 = False
                if not self.a_b:
                    self.u_a_b()
                if not self.base:
                    self.u_b()
                if self.br.colliderect(self.box.h_r):
                    if self.box.image == self.box.h:
                        self.dz += 1
                        self.s_s += 1
                        self.life += 1
                        self.s_b.p_li()
                    if self.box.image == self.box.h1:
                        self.dz += 1
                        self.life -= 1
                        self.s_s += 1
                    if self.box.image == self.box.h2:
                        self.dz += 2
                        self.s_s += 1
                    self.box.h_r.x = random.randint(0,800)
                    self.box.h_r.y = 0
                    self.box.image = random.choice(self.box.a1)
                if self.box.h_r.top >= 600:
                    self.box.h_r.x = random.randint(0,800)
                    self.box.h_r.y = 0
                    self.box.image = random.choice(self.box.a1)
            if self.s_l < 5:
                self.li.image = self.li.s_l1
    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if os.path.exists("D:\\"):
                    with open("D:\\score","w") as f:
                        f.write(str(self.high_score))
                else:
                    with open("C:\\Users\\Public\\score","w") as f:
                        f.write(str(self.high_score))
                if os.path.exists("D:\\"):
                    with open("D:\\coin","w") as f:
                        f.write(str(self.coin))
                else:
                    with open("C:\\Users\\Public\\coin","w") as f:
                        f.write(str(self.coin))
                if os.path.exists("D:\\"):
                    with open("D:\\goumai","w") as f:
                        if self.shop.image1 == self.shop.zhuangbei or self.shop.image1 == self.shop.yizhuangbei:
                            f.write('1\n')
                        else:
                            f.write('0\n')
                        if self.shop.image3 == self.shop.zhuangbei or self.shop.image3 == self.shop.yizhuangbei:
                            f.write('1')
                        else:
                            f.write('0')
                else:
                    with open("C:\\Users\\Public\\goumai","w") as f:
                        if self.shop.image1 == self.shop.zhuangbei or self.shop.image1 == self.shop.yizhuangbei:
                            f.write('1\n')
                        else:
                            f.write('0\n')
                        if self.shop.image3 == self.shop.zhuangbei or self.shop.image3 == self.shop.yizhuangbei:
                            f.write('1')
                        else:
                            f.write('0')
                if os.path.exists("D:\\"):
                    with open("D:\\killtank","r") as f:
                        a = int(f.read())
                    with open("D:\\killtank","w") as f1:
                        f1.write(str(self.score + a))
                else:
                    with open("C:\\Users\\Public\\killtank","r") as f:
                        a = int(f.read())
                    with open("C:\\Users\\Public\\killtank","w") as f1:
                        f1.write(str(self.score + a))
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN:
                self.check_key_down(event)
            elif event.type == pg.KEYUP:
                self.check_key_up(event)
            elif event.type == pg.MOUSEMOTION:
                if self.button.f_r.collidepoint(event.pos):
                    self.button.image = self.button.f1
                else:
                    self.button.image = self.button.f
                if self.help.l_r.collidepoint(event.pos):
                    self.help.image = self.help.l1
                else:
                    self.help.image = self.help.l
                if self.shop.s1_r.collidepoint(event.pos):
                    self.shop.image = self.shop.shop2
                else:
                    self.shop.image = self.shop.shop1
                if self.help.l2_r.collidepoint(event.pos):
                    self.help.image1 = self.help.l4
                else:
                    self.help.image1 = self.help.l2
                if self.shop.l2_r.collidepoint(event.pos):
                    self.shop.image4 = self.shop.l3
                else:
                    self.shop.image4 = self.shop.l2
                if self.chengjiu.e_r.collidepoint(event.pos):
                    self.chengjiu.image1 = self.chengjiu.e1
                else:
                    self.chengjiu.image1 = self.chengjiu.e
            elif event.type == pg.MOUSEBUTTONDOWN:
                if self.button.f_r.collidepoint(event.pos) and self.start1:
                    self.start = True
                    self.win = False
                    self.level = 0
                    self.s_b.s_l_i()
                if self.sw.i_r.collidepoint(event.pos):
                    if self.start1:
                        self.start1 = False
                        self.sw.image = self.sw.i1
                    else:
                        self.start1 = True
                        self.sw.image = self.sw.i
                if self.music.k_r.collidepoint(event.pos):
                    if self.music.image == self.music.k:
                        self.music.image = self.music.k1
                        pg.mixer.music.pause()
                    elif self.music.image == self.music.k1:
                        self.music.image = self.music.k
                        pg.mixer.music.play(-1)
                if self.help.l_r.collidepoint(event.pos):
                    self.help1 = True
                if self.help.l2_r.collidepoint(event.pos):
                    self.help1 = False
                if self.shop.s1_r.collidepoint(event.pos) and not self.shopping:
                    self.shopping = True
                if self.shop.l2_r.collidepoint(event.pos):
                    self.shopping = False
                if self.shop.goumai_r.collidepoint(event.pos) and self.shopping:
                    if self.shop.image1 == self.shop.goumai:
                        self.shop.image1 = self.shop.zhuangbei
                    else:
                        self.shop.zb3 = False
                        self.shop.zb2 = False
                        self.shop.zb1 = True
                        if self.shop.image3 == self.shop.yizhuangbei:
                            self.shop.image3 = self.shop.zhuangbei
                        self.shop.image2 = self.shop.zhuangbei
                        self.shop.image1 = self.shop.yizhuangbei
                if self.shop.goumai_r1.collidepoint(event.pos) and self.shopping:
                    if self.shop.image3 == self.shop.goumai and self.coin >= 10:
                        self.shop.image3 = self.shop.zhuangbei
                        self.coin -= 10
                        self.coin1.u_c()
                    elif self.shop.image3 == self.shop.zhuangbei:
                        self.shop.zb3 = True
                        self.shop.zb2 = False
                        self.shop.zb1 = False
                        if self.shop.image1 == self.shop.yizhuangbei:
                            self.shop.image1 = self.shop.zhuangbei
                        self.shop.image2 = self.shop.zhuangbei
                        self.shop.image3 = self.shop.yizhuangbei
                if self.shop.yizhuangbei_r.collidepoint(event.pos) and self.shopping:
                    if self.shop.image2 == self.shop.zhuangbei:
                        self.shop.zb3 = False
                        self.shop.zb2 = True
                        self.shop.zb1 = False
                        if self.shop.image2 == self.shop.zhuangbei:
                            self.shop.image2 = self.shop.yizhuangbei
                        if self.shop.image1 == self.shop.yizhuangbei:
                            self.shop.image1 = self.shop.zhuangbei
                        if self.shop.image3 == self.shop.yizhuangbei:
                            self.shop.image3 = self.shop.zhuangbei
                if self.chengjiu.d_r.collidepoint(event.pos):
                    self.chengjiu.chengjiu = True
                elif self.chengjiu.e_r.collidepoint(event.pos) and self.chengjiu.chengjiu:
                    self.chengjiu.chengjiu = False
                if self.chengjiu.e_r.collidepoint(event.pos):
                    self.chengjiu.chengjiu = False
    def update_screen(self):
        self.sc.blit(self.a,self.a.get_rect())
        self.sc.blit(self.b,self.br)
        self.ene.draw(self.sc)
        self.e_b.draw(self.sc)
        if self.start and self.start1 and not self.win and not self.shopping:
            for bullets in self.bullet.sprites():
                bullets.draw_b()
            for i in self.a_b.sprites():
                i.d_a_b()
            self.box.d_h()
            self.box.update()
        else:
            self.button.d_b()
            self.help.d_l()
            self.shop.d_s()
            self.chengjiu.draw_d()
            if self.start and self.start1:
                ii.update()
                if ii.c_e():
                    if self.b_d:
                        self.b_d = False
                    else:
                        self.b_d = True
        for ii in self.base.sprites():
            ii.d_ba()
            if self.start and self.start1:
                ii.update()
                if ii.c_e():
                    if self.b_d:
                        self.b_d = False
                    else:
                        self.b_d = True
        if self.start and self.dz2:
            self.skills.d_g()
        if self.win:
            font = pg.font.Font("STXINGKA.TTF",30)
            win = font.render("胜利！",True,(255,255,250))
            w_r = win.get_rect()
            w_r.y,w_r.x = 300,350
            self.sc.blit(win,w_r)
        self.sw.d_i()
        self.music.d_k()
        self.s_b.s_h_s()
        self.s_b.s_s_i()
        self.s_b.s_l_i()
        self.s_b.s_li_i()
        self.li.c_d()
        if self.s_s1:
            self.sh.d_g()
        if self.help1:
            self.help.d_help()
        if self.shopping:
            self.shop.d_s1()
        self.coin1.d_c()
        self.vip.draw()
        if self.chengjiu.chengjiu:
            self.chengjiu.draw_c()
        pg.display.flip()
    def check_key_down(self,event):        
        if event.key == pg.K_a or event.key == pg.K_LEFT:
            self.lm = True
        elif event.key == pg.K_d or event.key == pg.K_RIGHT:
            self.rm = True
        elif event.key == pg.K_f:
            self.f_b()
        elif event.key == pg.K_q:
            if os.path.exists("D:\\"):
                with open("D:\\score","w") as f:
                    f.write(str(self.high_score))
            else:
                with open("C:\\Users\\Public\\score") as f:
                    f.write(str(self.high_score))
            if os.path.exists("D:\\"):
                with open("D:\\coin","w") as f:
                    f.write(str(self.coin))
            else:
                with open("C:\\Users\\Public\\coin") as f:
                    f.write(str(self.coin))
            if os.path.exists("D:\\"):
                with open("D:\\goumai","w") as f:
                    if self.shop.image1 == self.shop.zhuangbei or self.shop.image1 == self.shop.yizhuangbei:
                        f.write('1\n')
                    else:
                        f.write('0\n')
                    if self.shop.image3 == self.shop.zhuangbei or self.shop.image3 == self.shop.yizhuangbei:
                        f.write('1')
                    else:
                        f.write('0')
            else:
                with open("C:\\Users\\Public\\goumai","w") as f:
                    if self.shop.image1 == self.shop.zhuangbei or self.shop.image1 == self.shop.yizhuangbei:
                        f.write('1\n')
                    else:
                        f.write('0\n')
                    if self.shop.image3 == self.shop.zhuangbei or self.shop.image3 == self.shop.yizhuangbei:
                        f.write('1')
                    else:
                        f.write('0')
            if os.path.exists("D:\\"):
                with open("D:\\killtank","r") as f:
                    a = int(f.read())
                with open("D:\\killtank","w") as f1:
                    f1.write(str(self.score + a))
            else:
                with open("C:\\Users\\Public\\killtank","r") as f:
                    a = int(f.read())
                with open("C:\\Users\\Public\\killtank","w") as f1:
                    f1.write(str(self.score + a))
            pg.quit()
            sys.exit()
        elif event.key == pg.K_SPACE:
            if self.dz > 0:
                self.dz -= 1
                self.dz2 = True
        elif event.key == pg.K_h:
            if self.s_s > 0:
                self.s_s -= 1
                self.s_s1 = True
                self.li.image = self.li.s_l
                if self.vip.vip:
                    self.s_l = 20
                else:
                    self.s_l = 10
                self.s_b.p_li()
                self.li.c_d()
    def check_key_up(self,event):
        if event.key == pg.K_a or event.key == pg.K_LEFT:
            self.lm = False
        elif event.key == pg.K_d or event.key == pg.K_RIGHT:
            self.rm = False
    def f_b(self):
        bull = Bullet(self)
        if self.shop.zb1:
            bull.image = bull.c1
            bull.shanghai = 1
        if self.shop.zb3:
            bull.image = bull.c2
        self.bullet.add(bull)
    def c_f(self):
        self.e_b.empty()
        for ii in range(4):
            for i in range(self.en - 1):
                al = Enemy(self)
                al.x = i * 80 + 80
                al.rect.x = al.x
                al.rect.y = 45 + 25 * 2 * ii
                self.ene.add(al)
        self.u_e_b()
        self.u_a_b()
    def c_f_e(self):
        for i in self.ene.sprites():
            if i.c_e():
                self.fl_d *= -1
                break
    def u_a_b(self):
        for i in self.ene.sprites():
            a = A_B(self)
            if self.level > 9:
                a.d = pg.image.load("bullet2.png")
            elif self.level > 4:
                a.d = pg.image.load("bullet.png")
            a.d_r.x = i.rect.x
            a.d_r.top = i.rect.bottom
            self.a_b.add(a)
    def u_b(self):
        for i in range(2):
            for ii in range(5):
                b = Base(self)
                b.e_r.x = b.e_r.y - 50 * ii
                if i == 1:
                    b.e_r.y += 50
                self.base.add(b)
    def u_e_b(self):
        for i in range(self.width // 50):
            a = E_B(self)
            a.rect.x = i * 50
            self.e_b.add(a)
    def dz1(self):
        if self.dz2:
            self.skills.change()
if __name__ == "__main__":
    A_I()
