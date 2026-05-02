import pyxel
import imp
import shooting_sub

# --------------------------------------------------
# 敵クラス
class PlItem(imp.Sprite):

    # コンストラクタ
    def __init__(self, x, y, id_0, id_1, item):
        imp.Sprite.__init__(self, imp.OBJITM, x, y, id_0, id_1, item)       # Spriteクラスのコンストラクタ

        self.pos_adj = imp.Vector2(-8, -8)

        self.vector = imp.Vector2(0, 0.2)

        self.hit_point = 1
        self.hit_rectx = 16
        self.hit_recty = 16

    # メイン
    def update(self):

        self.pos += self.vector

        # 画面内チェック
        self.CheckScreenIn()

    # 描画
    def draw(self):
        pos = self.pos + self.pos_adj
        self.sprite_draw(pos.x, pos.y, 0, 0, 1, 16, 16)

        # 中心の表示
        if imp._DEBUG_HIT_:
            shooting_sub.DebugDrawPosHitRect(self)


# --------------------------------------------------
