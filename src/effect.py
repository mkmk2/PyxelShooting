import pyxel
import imp

# id0
# 0:基本爆発
# 1:基本爆発移動有り


# --------------------------------------------------
# 敵クラス
class Effect(imp.Sprite):

    # コンストラクタ
    def __init__(self, x, y, id_0, id_1, item):
        imp.Sprite.__init__(self, imp.OBJEFF, x, y, id_0, id_1, item)       # Spriteクラスのコンストラクタ

        self.ptn_time = 0

#        if self.id0 == 1:       # 移動する
#            shooting_sub.SetVector(self, self.id1, (random.randrange(5, 20, 1) / 10))

        # Sound
        pyxel.play(0, 0, loop=False)

    # メイン
    def update(self):
        self.ptn_time += 1
        if self.ptn_time >= 14:
            self.ptn_time = 0
            self.death = 1

        if self.id0 == 1:       # 移動する
            self.pos.x += self.vector.x
            self.pos.y += self.vector.y

    # 描画
    def draw(self):
        if self.ptn_time < 4:
            self.sprite_draw(self.pos.x - 8, self.pos.y - 8, 0, 16, 1, 16, 16)
        elif self.ptn_time < 8:
            self.sprite_draw(self.pos.x - 8, self.pos.y - 8, 0, 18, 1, 16, 16)
        elif self.ptn_time < 12:
            self.sprite_draw(self.pos.x - 8, self.pos.y - 8, 0, 20, 1, 16, 16)
        else:
            self.sprite_draw(self.pos.x - 8, self.pos.y - 8, 0, 22, 1, 16, 16)

# --------------------------------------------------

# --------------------------------------------------
