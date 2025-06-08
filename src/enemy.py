import pyxel
import random
import math
import imp
import shooting_sub
import plitem
import effect

# ==================================================
# 敵Normクラス
# id0
# 0: まっすぐ下に降りてきてプレイヤーに向かってカーブ
# 1: まっすぐ下に移動するだけ
class EnemyNorm(imp.Sprite):
    BulletTime = 0

    MvTime = 0
    MvWait = 0
    BossMoveTblPtr = 0

    # コンストラクタ
    def __init__(self, x, y, id0, id1, item):
        imp.Sprite.__init__(self, imp.OBJEM, x, y, id0, id1, item)       # Spriteクラスのコンストラクタ

        self.pos_adjx = -6
        self.pos_adjy = -6
        self.hit_point = 1
        self.hit_rectx = 8
        self.hit_recty = 8
        if self.id0 == 0:
            self.score = 10
            self.life = 2
        elif self.id0 == 1:
            self.score = 10
            self.life = 1

#        self.BulletTime = random.randrange(30, 80, 1)

    # メイン
    def update(self):
        if self.id0 == 0:           # カーブ
            if self.st0 == 0:
                self.pos_y += 1.2
                if self.pos_y > 40:
                    pl = imp.GetPl(self)
                    if pl != 0:
                        if self.pos_x < pl.pos_x:
                            self.vector_x += 0.015
                            self.st1 = 1    # 右回転
                        else:
                            self.vector_x -= 0.015
                            self.st1 = 2    # 左回転

                self.pos_x += self.vector_x

#                self.BulletTime -= 1
#                if self.BulletTime <= 0:
#                    self.BulletTime = random.randrange(10, 20, 1)
#                    self.BulletTime = 99999     # 1回しか打たない
#                    imp.Em.append(EnemyBullet(self.pos_x,self.pos_y,0,0,0))

        elif self.id0 == 1:         # まっすぐ
            self.pos_y += 0.9

        # -----------------------------------------------
        # 死にチェック
        if self.life <= 0:          # 0以下なら死ぬ
            self.death = 1          # 死ぬ
            imp.score += self.score     # scoreを加算
            if imp._DEBUG_ == True:
                print("enemy die")
            # アイテムセット
            if self.item_set != 0:
                if imp._DEBUG_ == True:
                    print("item")
                imp.itm.append(plitem.PlItem(self.pos_x,self.pos_y,0,0,0))

        # 画面内チェック
        imp.CheckScreenIn(self)

        # -----------------------------------------------
    def draw(self):
        x = self.pos_x + self.pos_adjx
        y = self.pos_y + self.pos_adjy

        if self.id0 == 0:
            if self.st1 == 0:
                pyxel.blt(x, y, 0, 0, 56, 12, 12, 0)
            else:
                self.ptn_time -= 1
                if self.ptn_time <= 0:
                    self.ptn_time = 7

                    if self.st1 == 1:
                        self.ptn_no += 1
                        if self.ptn_no >= 7:
                            self.ptn_no = 0
                    else:
                        self.ptn_no -= 1
                        if self.ptn_no < 0:
                            self.ptn_no = 7

                pyxel.blt(x, y, 0, 16 * self.ptn_no, 56, 12, 12, 0)

        elif self.id0 == 1:
            if pyxel.frame_count & 0x08:
                pyxel.blt(x, y, 0, 40, 72, 12, 12, 0)
            else:
                pyxel.blt(x, y, 0, 56, 72, 12, 12, 0)

        # 中心の表示
#        shooting_sub.DebugDrawPosHitRect(self)

# ==================================================
# 敵ItemGroupクラス
# セットされたグループNoにより、全滅させた際にアイテムを落とす
# id0
# 0: まっすぐ下に降りてきてプレイヤーに向かってカーブ
# 1: まっすぐ下に移動するだけ
# Id1
# 任意のGroupId
# 同じグループの敵は同じIdをセットする
# 死んだときに同じIdの敵が居なければアイテムを落とす
# 例：5機のグループをセットしたい時には、画面街などに同時にセットしなければならない
# 同時に複数のグループをセットしようとするとき、それぞれ別のIdを設定しなければならない
class EnemyItemGroup(imp.Sprite):
    BulletTime = 0

    MvTime = 0
    MvWait = 0
    BossMoveTblPtr = 0

    # コンストラクタ
    def __init__(self, x, y, id0, id1, item):
        imp.Sprite.__init__(self, imp.OBJEM, x, y, id0, id1, item)       # Spriteクラスのコンストラクタ

        self.pos_adjx = -6
        self.pos_adjy = -6
        self.hit_point = 1
        self.hit_rectx = 8
        self.hit_recty = 8
        if self.id0 == 0:
            self.score = 10
            self.life = 2
        elif self.id0 == 1:
            self.score = 10
            self.life = 1

    # メイン
    def update(self):
        if self.id0 == 0:           # カーブ
            if self.st0 == 0:
                self.pos_y += 1.2
                if self.pos_y > 40:
                    pl = imp.GetPl(self)
                    if pl != 0:
                        if self.pos_x < pl.pos_x:
                            self.vector_x += 0.015
                            self.st1 = 1    # 右回転
                        else:
                            self.vector_x -= 0.015
                            self.st1 = 2    # 左回転

                self.pos_x += self.vector_x

        elif self.id0 == 1:         # まっすぐ
            self.pos_y += 0.9

        # -----------------------------------------------
        # 死にチェック
        if self.life <= 0:          # 0以下なら死ぬ
            self.death = 1          # 死ぬ
            imp.score += self.score     # scoreを加算
            if imp._DEBUG_ == True:
                print("enemy die")
            # アイテムセット
            if self.item_set != 0:
                # GroupIdのチェック
                find_group = 0
                for eg in imp.Em:
                    if eg.ObjType == imp.OBJEM:
                        if eg.__class__.__name__ == "EnemyItemGroup":
                            if self.Id1 == eg.Id1:
                                find_group += 1         # 同じId1を見つけた、同じGroup
                                if find_group >= 2:     # 2以上になったら > 1の時、自分自身も含んでいるため、2個目を発見したら、自分以外の同じGroupが居るということ
                                    break

                if find_group == 1:
                    if imp._DEBUG_ == True:
                        print("item")
                    imp.itm.append(plitem.PlItem(self.pos_x,self.pos_y,0,0,0))

        # 画面内チェック
        imp.CheckScreenIn(self)

        # -----------------------------------------------
    def draw(self):
        x = self.pos_x + self.pos_adjx
        y = self.pos_y + self.pos_adjy

        if self.id0 == 0:
            if self.st1 == 0:
                pyxel.blt(x, y, 0, 0, 56, 12, 12, 0)
            else:
                self.ptn_time -= 1
                if self.ptn_time <= 0:
                    self.ptn_time = 7

                    if self.st1 == 1:
                        self.ptn_no += 1
                        if self.ptn_no >= 7:
                            self.ptn_no = 0
                    else:
                        self.ptn_no -= 1
                        if self.ptn_no < 0:
                            self.ptn_no = 7

                pyxel.blt(x, y, 0, 16 * self.ptn_no, 56, 12, 12, 0)

        elif self.id0 == 1:
            if pyxel.frame_count & 0x08:
                pyxel.blt(x, y, 0, 40, 72, 12, 12, 0)
            else:
                pyxel.blt(x, y, 0, 56, 72, 12, 12, 0)

        # 中心の表示
#        shooting_sub.DebugDrawPosHitRect(self)

