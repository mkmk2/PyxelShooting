import pyxel
import imp

# Id0
# 0:
# 1:


# --------------------------------------------------
# 敵クラス
class PlItem(imp.Sprite):

    # コンストラクタ
    def __init__(self, x, y, id_0, id_1, item):
        imp.Sprite.__init__(self, imp.OBJITM, x, y, id_0, id_1, item)       # Spriteクラスのコンストラクタ

        self.pos_adj.x = -4
        self.pos_adj.y = -4

        self.vector.y = -4

        self.ptn_type = 300
        self.ptn_no = 0

        self.hit_point = 1
        self.hit_rectx = 8
        self.hit_recty = 8

        self.screen_time = 120

    # メイン
    def update(self):

        if self.vector.y < 0:
            self.vector.y += 0.2
            self.pos.y += self.vector.y
        else:
            self.vector.y = 0

        self.pos.y += 0.5

    #    self.ptn_type -= 1
    #    if self.ptn_type <= 0:
    #        self.death = 1

        # 画面内チェック
        self.screen_time -= 1
        if self.screen_time < 0:
            if imp.CheckScreenIn(self) is False:
                self.death = 1

    # 描画
    def draw(self):
        x = self.pos.x - 4
        y = self.pos.y - 4
        pyxel.blt(x, y, 0, 48, 0, 8, 8, 0)

# --------------------------------------------------

# --------------------------------------------------
