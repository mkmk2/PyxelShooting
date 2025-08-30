import pyxel
import imp
import plitem
import shooting_sub


# ==================================================
# 敵：ノーマルクラス
# id0
# 0: まっすぐ下に移動するだけ
# 1: まっすぐ下に降りてきてプレイヤーに向かってカーブ
class EnemyNorm(imp.Sprite):
    BulletTime = 0

    MvTime = 0
    MvWait = 0
    BossMoveTblPtr = 0

    # コンストラクタ
    def __init__(self, x, y, i0, i1, item):
        imp.Sprite.__init__(self, imp.OBJEM, x, y, i0, i1, item)       # Spriteクラスのコンストラクタ

        self.pos_adj = imp.Vector2(-6, -6)
        self.hit_point = 1
        self.hit_rectx = 10
        self.hit_recty = 10
        if self.id0 == 0:
            # まっすぐ下
            self.score = 10
            self.life = 1
        elif self.id0 == 1:
            # まっすぐ下、プレイヤーにカーブ
            self.score = 10
            self.life = 1

#        self.BulletTime = random.randrange(30, 80, 1)

    # -----------------------------------------------
    # メイン
    def update(self):
        if self.id0 == 0:           # まっすぐ
            self.pos.y += 0.9

        elif self.id0 == 1:         # カーブ
            self.pos.y += 0.9
            if self.pos.y > 40:
                pl = imp.GetPl(self)
                if pl != 0:
                    if self.pos.x < pl.pos.x:
                        self.vector.x += 0.015
                        self.st1 = 1    # 右へカーブ、右回転
                    else:
                        self.vector.x -= 0.015
                        self.st1 = 2    # 左へカーブ、左回転

            self.pos.x += self.vector.x

#                self.BulletTime -= 1
#                if self.BulletTime <= 0:
#                    self.BulletTime = random.randrange(10, 20, 1)
#                    self.BulletTime = 99999     # 1回しか打たない
#                    imp.Em.append(EnemyBullet(self.pos_x,self.pos_y,0,0,0))

        # -----------------------------------------------
        # 死にチェック
        if self.life <= 0:          # 0以下なら死ぬ
            self.death = 1          # 死ぬ
            imp.game_state.score += self.score     # scoreを加算
            if imp._DEBUG_:
                print("enemy die")
            # アイテムセット
            if self.item_set != 0:
                if imp._DEBUG_:
                    print("item")
                imp.game_state.itm.append(plitem.PlItem(self.pos.x, self.pos.y, 0, 0, 0))

        # 画面内チェック
        self.CheckScreenIn()

    # -----------------------------------------------
    def draw(self):
        pos = self.pos + self.pos_adj

        if self.id0 == 0:
            # まっすぐ下
            self.sprite_draw(pos.x, pos.y, 0, 2, 6, 16, 16)

        elif self.id0 == 1:
            # まっすぐ下、プレイヤーにカーブ
            if self.st1 == 0:
                # まっすぐ下
                self.sprite_draw(pos.x, pos.y, 0, 0, 56, 12, 12)
            else:
                self.ptn_time -= 1
                if self.ptn_time <= 0:
                    self.ptn_time = 7

                    if self.st1 == 1:
                        # 右回転
                        self.ptn_no += 1
                        if self.ptn_no >= 7:
                            self.ptn_no = 0
                    else:
                        # 左回転
                        self.ptn_no -= 1
                        if self.ptn_no < 0:
                            self.ptn_no = 7

                self.sprite_draw(pos.x, pos.y, 0, 16 * self.ptn_no, 56, 12, 12)

        # 中心の表示
        if imp._DEBUG_HIT_:
            shooting_sub.DebugDrawPosHitRect(self)

    # -----------------------------------------------
    def TestSpriteUpdate(self):
        self.ptn_time -= 1
        if self.ptn_time <= 0:
            self.ptn_time = 10
            self.ptn_no += 1
            if self.ptn_no >= 7:
                self.ptn_no = 0

    def TestSprite(self):
        self.sprite_draw(self.pos.x + self.pos_adj.x, self.pos.y + self.pos_adj.y, 0, 2, 6, 16, 16)


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
    def __init__(self, x, y, i0, i1, item):
        imp.Sprite.__init__(self, imp.OBJEM, x, y, i0, i1, item)       # Spriteクラスのコンストラクタ

        self.pos_adj = imp.Vector2(-6, -6)
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
                self.pos.y += 1.2
                if self.pos.y > 40:
                    pl = imp.GetPl(self)
                    if pl != 0:
                        if self.pos.x < pl.pos.x:
                            self.vector.x += 0.015
                            self.st1 = 1    # 右回転
                        else:
                            self.vector.x -= 0.015
                            self.st1 = 2    # 左回転

                self.pos.x += self.vector.x

        elif self.id0 == 1:         # まっすぐ
            self.pos.y += 0.9

        # -----------------------------------------------
        # 死にチェック
        if self.life <= 0:          # 0以下なら死ぬ
            self.death = 1          # 死ぬ
            imp.game_state.score += self.score     # scoreを加算
            if imp._DEBUG_:
                print("enemy die")
            # アイテムセット
            if self.item_set != 0:
                # GroupIdのチェック
                find_group = 0
                for eg in imp.game_state.em:
                    if eg.obj_type == imp.OBJEM:
                        if eg.__class__.__name__ == "EnemyItemGroup":
                            if self.id1 == eg.id1:
                                find_group += 1         # 同じId1を見つけた、同じGroup
                                if find_group >= 2:     # 2以上になったら > 1の時、自分自身も含んでいるため、2個目を発見したら、自分以外の同じGroupが居るということ
                                    break

                if find_group == 1:
                    if imp._DEBUG_:
                        print("item")
                    imp.game_state.itm.append(plitem.PlItem(self.pos.x, self.pos.y, 0, 0, 0))

        # 画面内チェック
        self.CheckScreenIn(self)

        # -----------------------------------------------
    def draw(self):
        pos = self.pos + self.pos_adj

        if self.id0 == 0:
            if self.st1 == 0:
                self.sprite_draw(pos.x, pos.y, 0, 0, 56, 12, 12)
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

                self.sprite_draw(pos.x, pos.y, 0, 16 * self.ptn_no, 56, 12, 12)

        elif self.id0 == 1:
            if pyxel.frame_count & 0x08:
                self.sprite_draw(pos.x, pos.y, 0, 40, 72, 12, 12)
            else:
                self.sprite_draw(pos.x, pos.y, 0, 56, 72, 12, 12)

        # 中心の表示
        if imp._DEBUG_HIT_:
            shooting_sub.DebugDrawPosHitRect(self)
