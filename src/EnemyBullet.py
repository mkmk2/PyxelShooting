import imp
import shooting_sub
import math

BULLET_SPEED = 2.5


# ==================================================
# 敵の弾クラス
# id0
# 0: まっすぐ下
# 1: プレイヤーに向かって移動
# 2: 斜め左下に移動する弾
# 3: 斜め右下に移動する弾
class EnemyBullet(imp.Sprite):

    # コンストラクタ
    def __init__(self, x, y, id_0, id_1, item):
        imp.Sprite.__init__(self, imp.OBJEMB, x, y, id_0, id_1, item)  # Spriteクラスのコンストラクタ

        # ヒット判定の設定
        self.hit_point = 1
        self.hit_rectx = 6
        self.hit_recty = 6
        self.life = 1

        # 弾の種類に応じた移動ベクトルの設定
        if self.id0 == imp.BulletId.STRAIGHT:
            # まっすぐ下に移動する基本弾
            self.vector = imp.Vector2(0, BULLET_SPEED)

        elif self.id0 == imp.BulletId.PLAYER:
            # プレイヤーに向かって移動する弾（仮の角度）
            # 実際の実装時にプレイヤーの位置を取得して角度を計算
            pl = imp.GetPl(self)
            if pl != 0:
                shooting_sub.SetVector(self, shooting_sub.GetDirection(self, self.pos.x, self.pos.y, pl.pos.x, pl.pos.y), BULLET_SPEED)

        elif self.id0 == imp.BulletId.LEFT:
            # 斜め左下に移動する弾
            shooting_sub.SetVector(self, math.radians(130), BULLET_SPEED)

        elif self.id0 == imp.BulletId.RIGHT:
            # 斜め右下に移動する弾
            shooting_sub.SetVector(self, math.radians(50), BULLET_SPEED)

        else:
            # デフォルト（まっすぐ下）
            self.vector = imp.Vector2(0, 3.5)

    # -----------------------------------------------
    # メイン更新処理
    def update(self):
        # 弾の移動
        self.pos += self.vector

        # 画面内チェック（画面外に出たら削除）
        self.CheckScreenIn()

    # -----------------------------------------------
    # 描画処理
    def draw(self):
        pos = self.pos + self.pos_adj

        if self.id0 == imp.BulletId.STRAIGHT:
            # 基本弾
            self.sprite_draw(pos.x-3, pos.y-3, 0, 2, 3, 6, 6)

        elif self.id0 == imp.BulletId.PLAYER:
            # プレイヤー追跡弾
            self.sprite_draw(pos.x-3, pos.y-3, 0, 2, 3, 6, 6)

        elif self.id0 == imp.BulletId.LEFT:
            # 斜め左下弾
            self.sprite_draw(pos.x-3, pos.y-3, 0, 2, 3, 6, 6)

        elif self.id0 == imp.BulletId.RIGHT:
            # 斜め右下弾
            self.sprite_draw(pos.x-3, pos.y-3, 0, 2, 3, 6, 6)

        else:
            # デフォルト表示
            self.sprite_draw(pos.x-3, pos.y-3, 0, 2, 3, 6, 6)

        # デバッグ用ヒット判定表示
        if imp._DEBUG_HIT_:
            shooting_sub.DebugDrawPosHitRect(self)
