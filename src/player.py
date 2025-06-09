import pyxel
import random
import math
import imp
import shooting_sub
import effect

PL_SPEED = 1.5

PLST_DEMO = 0
PLST_PLAY = 1
PLST_DAMAGE = 2
PLST_DEATH = 3
PLST_CLEAR = 4


# --------------------------------------------------
# プレイヤークラス
class Player(imp.Sprite):

    ShotTime = 0

    # コンストラクタ
    def __init__(self, x, y, id0, id1, item):
        imp.Sprite.__init__(self, imp.OBJPL, x, y, id0, id1, item)

        self.pl_dir = 0              # 上下のパターン切り替え
        self.pl_st0 = PLST_DEMO      # st0

        self.pos_x = 128
        self.pos_y = 250
        self.pos_adjx = -8
        self.pos_adjy = -8

        self.life = 3
        self.hit_rectx = 4
        self.hit_recty = 4

    def __del__(self):
        pass

    # メイン
    def update(self):

        self.hit_st = 0                  # 当たりアリ

        if self.pl_st0 == 0:             # デモ
            self.pos_y -= 2
            if self.pos_y < 200:
                self.pl_st0 = PLST_PLAY

        elif self.pl_st0 == 1:           # ゲームプレイ中

            if imp.game_status == imp.GAME_STATUS_MAIN:     # ゲーム中のみ死にチェック
                if self.life <= 0:          # 0以下なら死ぬ
                    self.pl_st0 = PLST_DEATH    # 死に
                    self.mv_wait = 10           # 爆発数
                    self.mv_time = 0            # 爆発タイマー

                if self.hit != 0:           # 何かにあたった
                    self.pl_st0 = PLST_DAMAGE  # ダメージ
                    self.ptn_no = 0
                    self.mv_wait = 0
                    self.mv_time = 40

            if imp.game_status == imp.GAME_STATUS_STAGECLEAR:    # ステージクリア
                self.pl_st0 = PLST_CLEAR     # クリア
                self.pl_dir = 0                       # 前

            else:
                # プレイヤー移動
                self.PlayerLeverMove()

                # 弾セット(スペースキー)
                if pyxel.btn(pyxel.KEY_SPACE)\
                        or pyxel.btn(pyxel.GAMEPAD1_BUTTON_A)\
                        or pyxel.btn(pyxel.GAMEPAD1_BUTTON_B):
                    self.ShotTime -= 1
                    if self.ShotTime < 0:
                        self.ShotTime = 6
                        if imp.pl_level == 0:
                            imp.pl.append(PlayerBullet(self.pos_x, self.pos_y, 0, 0, 0))
                        elif imp.pl_level == 1:
                            imp.pl.append(PlayerBullet(self.pos_x - 5, self.pos_y, 0, 0, 0))
                            imp.pl.append(PlayerBullet(self.pos_x + 5, self.pos_y, 0, 0, 0))
                        else:
                            imp.pl.append(PlayerBullet(self.pos_x - 6, self.pos_y, 1, 0, 0))  # 左側
                            imp.pl.append(PlayerBullet(self.pos_x, self.pos_y, 0, 0, 0))
                            imp.pl.append(PlayerBullet(self.pos_x + 6, self.pos_y, 2, 0, 0))  # 右側

                else:
                    self.ShotTime = 0

                if imp.pl_item_num >= imp.PL_ITEM_LEVEL_UP:
                    imp.pl_item_num = 0
                    imp.pl_level += 1
                    imp.pl_levelup_eff = 40      # 点滅時間

        elif self.pl_st0 == PLST_DAMAGE:           # ダメージ
            self.hit_st = 1                          # 当たりナシ
            # プレイヤー移動
            cpDir = self.pl_dir       # pl_dirの保存・・・
            self.PlayerLeverMove()
            self.pl_dir = cpDir

            self.mv_wait -= 1
            if self.mv_wait <= 0:
                self.mv_wait = 6
                if self.ptn_no == 0:
                    self.pl_dir = 0                   # 前
                    self.ptn_no = 1
                elif self.ptn_no == 1:
                    self.pl_dir = 1                   # 左
                    self.ptn_no = 2
                elif self.ptn_no == 2:
                    self.pl_dir = 2                   # 右
                    self.ptn_no = 3
                elif self.ptn_no == 3:
                    self.pl_dir = 1                   # 左
                    self.ptn_no = 0

            self.mv_time -= 1
            if self.mv_time <= 0:
                self.pl_st0 = PLST_PLAY

        elif self.pl_st0 == PLST_DEATH:           # 死に
            # 爆発
            self.mv_time -= 1
            if self.mv_time <= 0:
                imp.eff.append(effect.Effect(self.pos_x - 10 + random.randrange(0, 20, 1),
                                             self.pos_y - 10 + random.randrange(0, 20, 1), imp.EFF_BOOM, 0, 0))
                imp.eff.append(effect.Effect(self.pos_x - 10 + random.randrange(0, 20, 1),
                                             self.pos_y - 10 + random.randrange(0, 20, 1), imp.EFF_BOOM, 0, 0))
                self.mv_time = 4
                self.Display = self.mv_wait & 1      # 点滅
                self.mv_wait -= 1
                if self.mv_wait <= 0:
                    self.death = 1          # 死ぬ
                    if imp._DEBUG_ is True:
                        print("pl die")

        elif self.pl_st0 == PLST_CLEAR:           # クリア
            if self.pos_y > -100:
                self.pos_y -= 2

# 描画
    def draw(self):
        x = self.pos_x + self.pos_adjx
        y = self.pos_y + self.pos_adjy

        if self.pl_dir == 0:
            pyxel.blt(x, y, 0, 16, 0, 16, 16, 0)      # 前

            if pyxel.frame_count & 0x04:
                pyxel.blt(self.pos_x + 0, self.pos_y + 8, 0, 8, 16, 6, 6, 0)
                pyxel.blt(self.pos_x - 6, self.pos_y + 8, 0, 8, 16, -6, 6, 0)
            else:
                pyxel.blt(self.pos_x + 0, self.pos_y + 8, 0, 8, 24, 6, 6, 0)
                pyxel.blt(self.pos_x - 6, self.pos_y + 8, 0, 8, 24, -6, 6, 0)
        else:
            if self.pl_dir == 1:
                pyxel.blt(x, y, 0,  0, 0, 16, 16, 0)      # 左
            else:
                pyxel.blt(x, y, 0, 32, 0, 16, 16, 0)      # 右

            if pyxel.frame_count & 0x04:
                pyxel.blt(self.pos_x - 1, self.pos_y + 8, 0, 8, 16, 6, 6, 0)
                pyxel.blt(self.pos_x - 5, self.pos_y + 8, 0, 8, 16, -6, 6, 0)
            else:
                pyxel.blt(self.pos_x - 1, self.pos_y + 8, 0, 8, 24, 6, 6, 0)
                pyxel.blt(self.pos_x - 5, self.pos_y + 8, 0, 8, 24, -6, 6, 0)

        # 中心の表示
#        shooting_sub.DebugDrawPoshitRect(self)

# --------------------------------------------------
    # プレイヤー移動
    def PlayerLeverMove(self):
        # プレイヤー移動
        self.pl_dir = 0                       # 前
        self.vector_x = 0
        self.vector_y = 0
        d = 0

        if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_LEFT)\
                or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN)\
                or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):

            # 上右
            if (pyxel.btn(pyxel.KEY_UP) and pyxel.btn(pyxel.KEY_RIGHT))\
                    or (pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP) and pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT)):
                d = 315
                self.pl_dir = 2                   # 右
            # 上左
            elif (pyxel.btn(pyxel.KEY_UP) and pyxel.btn(pyxel.KEY_LEFT))\
                    or (pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP) and pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT)):
                d = 225
                self.pl_dir = 1                   # 左
            # 下右
            elif (pyxel.btn(pyxel.KEY_DOWN) and pyxel.btn(pyxel.KEY_RIGHT))\
                    or (pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN) and pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT)):
                d = 45
                self.pl_dir = 2                   # 右
            # 下左
            elif (pyxel.btn(pyxel.KEY_DOWN) and pyxel.btn(pyxel.KEY_LEFT))\
                    or (pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN) and pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT)):
                d = 135
                self.pl_dir = 1                   # 左
            else:
                # 上移動(上カーソルキー)
                if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP):
                    d = 270
                # 下移動(下カーソルキー)
                elif pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN):
                    d = 90
                # 右移動(右カーソルキー)
                elif pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
                    d = 0
                    self.pl_dir = 2                   # 右
                # 左移動(左カーソルキー)
                elif pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
                    d = 180
                    self.pl_dir = 1                   # 左

            shooting_sub.SetVector(self, math.radians(d), PL_SPEED)
            self.pos_x += self.vector_x
            self.pos_y += self.vector_y

            if self.pos_y < 50:
                self.pos_y = 50
            if self.pos_y > imp.WINDOW_H - 16:
                self.pos_y = imp.WINDOW_H - 16
            if self.pos_x > imp.WINDOW_W - 8:
                self.pos_x = imp.WINDOW_W - 8
            if self.pos_x < 8:
                self.pos_x = 8


# --------------------------------------------------
# プレイヤークラス
class PlayerBullet(imp.Sprite):

    # コンストラクタ
    def __init__(self, x, y, id_0, id_1, item):
        imp.Sprite.__init__(self, imp.OBJPLB, x, y, id_0, id_1, item)

        self.pos_adjx = -3
        self.pos_adjy = -3
        self.life = 1
        self.hit_point = 1
        self.hit_rectx = 2
        self.hit_recty = 3

        if self.id0 == 0:   # 前
            self.vector_x = 0
            self.vector_y = -3.5
        if self.id0 == 1:   # 左側
            self.vector_x = -0.25
            self.vector_y = -3.5
        if self.id0 == 2:   # 右側
            self.vector_x = 0.25
            self.vector_y = -3.5

    # メイン
    def update(self):
        self.pos_x += self.vector_x
        self.pos_y += self.vector_y

        # 画面内チェック
        imp.CheckScreenIn(self)

    # 描画
    def draw(self):
        x = self.pos_x + self.pos_adjx
        y = self.pos_y + self.pos_adjy
        pyxel.blt(x, y, 0, 0, 16, 6, 6, 0)

        # 中心の表示
#        shooting_sub.DebugDrawPoshitRect(self)
