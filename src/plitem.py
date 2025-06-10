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

        self.PosVectorY = -4

        self.PtnTime = 300
        self.PtnNo = 0

        self.HitPoint = 1
        self.HitRectX = 8
        self.HitRectY = 8

        self.ScreenTime = 120

    # メイン
    def update(self):

        if self.PosVectorY < 0:
            self.PosVectorY += 0.2
            self.pos.y += self.PosVectorY
        else:
            self.PosVectorY = 0

        self.pos.y += 0.5

    #    self.PtnTime -= 1
    #    if self.PtnTime <= 0:
    #        self.Death = 1

        # 画面内チェック
        self.ScreenTime -= 1
        if self.ScreenTime < 0:
            if imp.CheckScreenIn(self) is False:
                self.Death = 1

    # 描画
    def draw(self):
        x = self.pos.x - 4
        y = self.pos.y - 4
        pyxel.blt(x, y, 0, 48, 0, 8, 8, 0)

# --------------------------------------------------

# --------------------------------------------------
