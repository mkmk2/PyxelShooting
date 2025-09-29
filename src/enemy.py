import pyxel
import math
import random
import imp
import plitem
import shooting_sub
from EnemyBullet import EnemyBullet


# ==================================================
# 敵：ノーマルクラス
# id0
# 0: まっすぐ下に移動するだけ
# 1: 下に移動しながら斜めに左右往復する
# 2: 下に移動しながら左右往復する
# 3: 左右往復して画面下の方で上に帰る
# 4: サイン波で左右に揺れながら下降
class EnemyNorm(imp.Sprite):
    BulletTime = 0

    MvTime = 0
    MvWait = 0
    BossMoveTblPtr = 0

    # コンストラクタ
    def __init__(self, x, y, i0, i1, item):
        imp.Sprite.__init__(self, imp.OBJEM, x, y, i0, i1, item)       # Spriteクラスのコンストラクタ

        self.pos_adj = imp.Vector2(-8, -8)
        self.hit_point = 1
        self.hit_rectx = 12
        self.hit_recty = 12
        if self.id0 == 0:            # まっすぐ下
            self.vector = imp.Vector2(0, 2.2)
            self.score = 10
            self.life = 1

        elif self.id0 == 1:          # 斜めに左右往復
            self.vector = imp.Vector2(0, 1.4)
            if self.pos.x < 128:
                self.vector.x = 2.8
            else:
                self.vector.x = -2.8
            self.score = 10
            self.life = 1

        elif self.id0 == 2 or self.id0 == 3:          # まっすぐ下、左右往復    まっすぐ下、左右往復して画面下の方で上に帰る
            self.vector = imp.Vector2(0, 2.2)
            self.score = 10
            self.life = 1

        elif self.id0 == 4:                           # 画面左右から出現、中央まで移動後、降りながら弾を撃つ
            self.vector = imp.Vector2(0, -1.8)

            if self.pos.x < 128:
                self.vector.x = 2.8
            else:
                self.vector.x = -2.8

            self.score = 10
            self.life = 1

        elif self.id0 == 5:                         # サイン波で左右に揺れながら下降
            self.vector = imp.Vector2(0, 1.8)
            self.score = 10
            self.life = 1
            self.swing_amplitude = imp.WINDOW_W / 3  # 揺れ幅（画面の1/3）
            self.swing_speed = 2 * math.pi / 100     # 周期100フレーム（左右のピークが50フレーム）
            self.initial_x = self.pos.x              # 初期X座標を記録
            self.swing_timer = 0                     # 個別の揺れタイマー

    # -----------------------------------------------
    # メイン
    def update(self):
        if self.id0 == 0:           # まっすぐ
            self.pos += self.vector
        # -----------------------------------------------
        elif self.id0 == 1:         # 斜めに左右往復
            if self.vector.x > 0:
                if self.pos.x > imp.WINDOW_W - 50:
                    self.vector.x *= -1
            else:
                if self.pos.x < 50:
                    self.vector.x *= -1

            self.pos += self.vector

        # -----------------------------------------------
        elif self.id0 == 2 or self.id0 == 3:         # 左右往復 左右往復して画面下の方で上に帰る
            if self.st0 == 0:       # 下移動
                self.vector = imp.Vector2(0, 2.2)
                self.tmp_ctr += 1
                if self.tmp_ctr >= 30:
                    self.vector = imp.Vector2(0, 0)
                    if self.pos.x < 128:
                        self.vector.x = 2.4
                    else:
                        self.vector.x = -2.4
                    self.tmp_ctr = 0
                    self.st0 = 1

                if self.id0 == 3:         # 左右往復して画面下の方で上に帰る
                    if self.pos.y > imp.WINDOW_H - 50:
                        self.vector = imp.Vector2(0, -1.8)  # 上に帰る速度
                        self.st0 = 2

            elif self.st0 == 1:                   # 左右移動
                self.tmp_ctr += 1
                if self.tmp_ctr >= 35:
                    self.tmp_ctr = 0
                    self.st0 = 0

            else:                   # 上に帰る
                pass

            self.pos += self.vector

        # -----------------------------------------------
        elif self.id0 == 4:         # 画面左右から出現、中央まで移動後、降りながら弾を撃つ
            if self.st0 == 0:       # 上移動
                self.vector.y -= 0.08
                if self.vector.x > 0:
                    self.vector.x -= 0.02
                    if self.vector.x < 0:
                        self.vector.x = 0
                else:
                    self.vector.x += 0.02
                    if self.vector.x > 0:
                        self.vector.x = 0

                if self.pos.y < 50:
                    self.vector = imp.Vector2(0, 0)
                    self.tmp_ctr = 0
                    self.st0 = 1

            elif self.st0 == 1:       # 一時停止
                self.tmp_ctr += 1
                if self.tmp_ctr >= 13:
                    if random.random() > 0.5:
                        shooting_sub.SetVector(self, math.radians(130), 2.8)
                    else:
                        shooting_sub.SetVector(self, math.radians(50), 2.8)
                    self.tmp_ctr = 0
                    # 弾を撃つ
                    imp.game_state.em.append(EnemyBullet(self.pos.x, self.pos.y + 4, imp.BulletId.PLAYER, 0, 0))
                    self.st0 = 2

            elif self.st0 == 2:       # 降下
                self.tmp_ctr += 1
                if self.tmp_ctr >= 20:
                    self.vector = imp.Vector2(0, 0)
                    self.tmp_ctr = 0
                    self.st0 = 1

            self.pos += self.vector

        # -----------------------------------------------
        elif self.id0 == 5:         # サイン波で左右に揺れながら下降
            # Y方向は一定速度で下降
            self.pos.y += self.vector.y

            # 個別タイマーを更新
            self.swing_timer += 1

            # X方向はサイン波で左右に揺れる
            # 個別タイマーを基準にサイン波を計算
            swing_offset = self.swing_amplitude * math.sin(self.swing_timer * self.swing_speed)
            self.pos.x = self.initial_x + swing_offset

            # 移動方向を記録（描画時の反転用）
            if self.swing_timer > 0:
                current_swing = math.sin(self.swing_timer * self.swing_speed)
                previous_swing = math.sin((self.swing_timer - 1) * self.swing_speed)
                if current_swing > previous_swing:
                    self.vector.x = 1  # 右向き
                else:
                    self.vector.x = -1  # 左向き

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
            self.sprite_draw(pos.x, pos.y, 0, 0, 6, 16, 16)

        elif self.id0 == 1:
            # まっすぐ下、移動方向を見て表示反転
            if self.vector.x < 0:
                self.sprite_draw(pos.x, pos.y, 0, 2, 6, 16, 16)
            else:
                self.sprite_draw(pos.x, pos.y, 0, 2, 6, -16, 16)

        elif self.id0 == 2 or self.id0 == 3:
            # まっすぐ下、移動方向を見て表示反転
            if self.vector.x < 0:
                self.sprite_draw(pos.x, pos.y, 0, 4, 6, 16, 16)
            else:
                self.sprite_draw(pos.x, pos.y, 0, 6, 6, -16, 16)

        elif self.id0 == 4:
            # サイン波で揺れながら下降、移動方向を見て表示反転（id0=1と同じスプライト使用）
            if self.vector.x < 0:
                self.sprite_draw(pos.x, pos.y, 0, 2, 6, 16, 16)
            else:
                self.sprite_draw(pos.x, pos.y, 0, 2, 6, -16, 16)

        elif self.id0 == 5:
            # サイン波で揺れながら下降、移動方向を見て表示反転（id0=1と同じスプライト使用）
            if self.vector.x < 0:
                self.sprite_draw(pos.x, pos.y, 0, 2, 6, 16, 16)
            else:
                self.sprite_draw(pos.x, pos.y, 0, 2, 6, -16, 16)

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
        self.sprite_draw(self.pos.x + self.pos_adj.x, self.pos.y + self.pos_adj.y, 0, 0, 6, 16, 16)

        if self.ptn_no <= 3:
            self.sprite_draw(self.pos.x + self.pos_adj.x, self.pos.y + self.pos_adj.y + 32, 0, 2, 6, 16, 16)
        else:
            self.sprite_draw(self.pos.x + self.pos_adj.x, self.pos.y + self.pos_adj.y + 32, 0, 2, 6, -16, 16)

        if self.ptn_no <= 3:
            self.sprite_draw(self.pos.x + self.pos_adj.x, self.pos.y + self.pos_adj.y + 64, 0, 4, 6, 16, 16)
        else:
            self.sprite_draw(self.pos.x + self.pos_adj.x, self.pos.y + self.pos_adj.y + 64, 0, 6, 6, 16, 16)


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
        self.CheckScreenIn()

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
