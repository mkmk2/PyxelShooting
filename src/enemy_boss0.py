import imp
import plitem
import shooting_sub


# ==================================================
# 敵：ボス0クラス
# id0
# 0: まっすぐ下に移動するだけ
class EnemyBoss0(imp.Sprite):
    BulletTime = 0

    MvTime = 0
    MvWait = 0
    BossMoveTblPtr = 0

    # コンストラクタ
    def __init__(self, x, y, i0, i1, item):
        imp.Sprite.__init__(self, imp.OBJEM, x, y, i0, i1, item)       # Spriteクラスのコンストラクタ

        self.pos_adj = imp.Vector2(-76, -40)
        self.hit_point = 1

        self.hit_rectx = 144
        self.hit_recty = 80
        self.vector = imp.Vector2(0, 0.2)
        self.score = 10
        self.life = 1

    # -----------------------------------------------
    # メイン
    def update(self):

        self.pos += self.vector

        if self.pos.y > 50:
            self.vector = imp.Vector2(0, 0)

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

        # まっすぐ下
        self.sprite_draw(pos.x, pos.y, 0, 0, 22, 152, 80)

        # 中心の表示
        if imp._DEBUG_HIT_:
            shooting_sub.DebugDrawPosHitRect(self)
