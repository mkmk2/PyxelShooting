import pyxel
import imp
import random
import shooting_sub

# id0
# 0:基本爆発
# 1:基本爆発移動有り

# --------------------------------------------------
# 敵クラス
class Effect(imp.Sprite):

    # コンストラクタ
    def __init__(self, x, y, id_0, id_1, item):
        imp.Sprite.__init__(self, imp.OBJEFF, x, y, id_0, id_1, item)       # Spriteクラスのコンストラクタ

        self.pos_adjx = -8
        self.pos_adjy = -4

        self.ptn_time = 4
        self.ptn_no = 0

#        if self.id0 == 1:       # 移動する
#            shooting_sub.SetVector(self, self.id1, (random.randrange(5, 20, 1) / 10))

        # Sound
        pyxel.play(0, 0, loop=False)

    # メイン
    def update(self):
        self.ptn_time -= 1
        if self.ptn_time <= 0:
            self.ptn_time = 6

            self.ptn_no += 1
            if self.ptn_no >= 3:
                self.ptn_no = 3
                self.death = 1

        if self.id0 == 1:       # 移動する
            self.pos_x += self.vector_x
            self.pos_y += self.vector_y

    # 描画
    def draw(self):
        if self.ptn_no == 0:
            x = self.pos_x - 4
            y = self.pos_y - 4
            pyxel.blt(x, y, 0, 0, 8*20, 8, 8, 0)
        elif self.ptn_no == 1:
            x = self.pos_x - 4
            y = self.pos_y - 4
            pyxel.blt(x, y, 0, 8, 8*20, 8, 8, 0)
        elif self.ptn_no == 2:
            x = self.pos_x - 4
            y = self.pos_y - 4
            pyxel.blt(x, y, 0, 16, 8*20, 12, 12, 0)
        elif self.ptn_no == 3:
            x = self.pos_x - 4
            y = self.pos_y - 4
            pyxel.blt(x, y, 0, 32, 8*20, 12, 12, 0)

# --------------------------------------------------

# --------------------------------------------------
