import pyxel
import random
import math
import imp
import shooting_sub
import effect
import input_manager
from enum import Enum

PL_SPEED = 2.5


class PlayerState(Enum):
    DEMO = 0
    PLAY = 1
    DAMAGE = 2
    DEATH = 3
    CLEAR = 4


# --------------------------------------------------
# プレイヤークラス
class Player(imp.Sprite):

    shot_time = 0

    # コンストラクタ
    def __init__(self, x, y, id0, id1, item):
        imp.Sprite.__init__(self, imp.OBJPL, x, y, id0, id1, item)

        self.pl_dir = 0              # 上下のパターン切り替え
        self.pl_st0 = PlayerState.DEMO      # st0

        self.pos = imp.Vector2(128, 250)
        self.pos_adj = imp.Vector2(-8, -8)

        self.life = 3
        self.hit_rectx = 4
        self.hit_recty = 4

        self.vector = imp.Vector2(0, 0)

    def __del__(self):
        pass

    # メイン
    def update(self):

        self.hit_st = 0                  # 当たりアリ

        if self.pl_st0 == PlayerState.DEMO:             # デモ
            self.pos.y -= 2
            if self.pos.y < 200:
                self.pl_st0 = PlayerState.PLAY

        elif self.pl_st0 == PlayerState.PLAY:           # ゲームプレイ中

            if imp.game_state.game_status == imp.GameStatus.MAIN:     # ゲーム中のみ死にチェック
                if self.life <= 0:          # 0以下なら死ぬ
                    self.pl_st0 = PlayerState.DEATH    # 死に
                    self.mv_wait = 10           # 爆発数
                    self.mv_time = 0            # 爆発タイマー

                if self.hit != 0:           # 何かにあたった
                    self.pl_st0 = PlayerState.DAMAGE  # ダメージ
                    self.ptn_no = 0
                    self.mv_wait = 0
                    self.mv_time = 40

            if imp.game_state.game_status == imp.GameStatus.STAGECLEAR:    # ステージクリア
                self.pl_st0 = PlayerState.CLEAR     # クリア
                self.pl_dir = 0                       # 前

            else:
                # プレイヤー移動
                self.PlayerLeverMove()

                # 弾セット(スペースキー)
                if input_manager.input_manager.is_shot_held():
                    self.shot_time -= 1
                    if self.shot_time < 0:
                        self.shot_time = 6
                        if imp.game_state.pl_level == 0:
                            imp.game_state.pl.append(PlayerBullet(self.pos.x, self.pos.y, 0, 0, 0))
                        elif imp.game_state.pl_level == 1:
                            imp.game_state.pl.append(PlayerBullet(self.pos.x - 5, self.pos.y, 0, 0, 0))
                            imp.game_state.pl.append(PlayerBullet(self.pos.x + 5, self.pos.y, 0, 0, 0))
                        else:
                            imp.game_state.pl.append(PlayerBullet(self.pos.x - 6, self.pos.y, 1, 0, 0))  # 左側
                            imp.game_state.pl.append(PlayerBullet(self.pos.x, self.pos.y, 0, 0, 0))
                            imp.game_state.pl.append(PlayerBullet(self.pos.x + 6, self.pos.y, 2, 0, 0))  # 右側

                else:
                    self.shot_time = 0

                if imp.game_state.pl_item_num >= imp.PL_ITEM_LEVEL_UP:
                    imp.game_state.pl_item_num = 0
                    imp.game_state.pl_level += 1
                    imp.game_state.pl_levelup_eff = 40      # 点滅時間

        elif self.pl_st0 == PlayerState.DAMAGE:           # ダメージ
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
                self.pl_st0 = PlayerState.PLAY

        elif self.pl_st0 == PlayerState.DEATH:           # 死に
            # 爆発
            self.mv_time -= 1
            if self.mv_time <= 0:
                imp.game_state.eff.append(
                    effect.Effect(
                        self.pos.x - 10 + random.randrange(0, 20, 1),
                        self.pos.y - 10 + random.randrange(0, 20, 1),
                        imp.EFF_BOOM, 0, 0
                    )
                )
                imp.game_state.eff.append(
                    effect.Effect(
                        self.pos.x - 10 + random.randrange(0, 20, 1),
                        self.pos.y - 10 + random.randrange(0, 20, 1),
                        imp.EFF_BOOM, 0, 0
                    )
                )
                self.mv_time = 4
                self.Display = self.mv_wait & 1      # 点滅
                self.mv_wait -= 1
                if self.mv_wait <= 0:
                    self.death = 1          # 死ぬ
                    if imp._DEBUG_:
                        print("pl die")

        elif self.pl_st0 == PlayerState.CLEAR:           # クリア
            if self.pos.y > -100:
                self.pos.y -= 2

# 描画
    def draw(self):
        x = self.pos.x
        y = self.pos.y

        if self.pl_dir == 0:
            self.DrawPlayer00(x, y)
        elif self.pl_dir == 1:
            self.DrawPlayer01(x, y)
        else:
            self.DrawPlayer02(x, y)

        # 中心の表示
        if imp._DEBUG_:
            shooting_sub.DebugDrawPosHitRect(self)

# --------------------------------------------------
# 前
    def DrawPlayer00(self, x, y):
        self.sprite_draw(x + self.pos_adj.x, y + self.pos_adj.y, 0, 16, 0, 16, 16)      # 前

        if pyxel.frame_count & 0x04:
            self.sprite_draw(x + 0, y + 8, 0, 8, 16, 6, 6)
            self.sprite_draw(x - 6, y + 8, 0, 8, 16, -6, 6)
        else:
            self.sprite_draw(x + 0, y + 8, 0, 8, 24, 6, 6)
            self.sprite_draw(x - 6, y + 8, 0, 8, 24, -6, 6)

# --------------------------------------------------
# 左
    def DrawPlayer01(self, x, y):
        self.sprite_draw(x + self.pos_adj.x, y + self.pos_adj.y, 0,  0, 0, 16, 16)      # 左

        if pyxel.frame_count & 0x04:
            self.sprite_draw(x + 0, y + 8, 0, 8, 16, 6, 6)
            self.sprite_draw(x - 6, y + 8, 0, 8, 16, -6, 6)
        else:
            self.sprite_draw(x + 0, y + 8, 0, 8, 24, 6, 6)
            self.sprite_draw(x - 6, y + 8, 0, 8, 24, -6, 6)

        if pyxel.frame_count & 0x04:
            self.sprite_draw(x - 1, y + 8, 0, 8, 16, 6, 6)
            self.sprite_draw(x - 5, y + 8, 0, 8, 16, -6, 6)
        else:
            self.sprite_draw(x - 1, y + 8, 0, 8, 24, 6, 6)
            self.sprite_draw(x - 5, y + 8, 0, 8, 24, -6, 6)

# --------------------------------------------------
# 右
    def DrawPlayer02(self, x, y):
        self.sprite_draw(x + self.pos_adj.x, y + self.pos_adj.y, 0,  32, 0, 16, 16)      # 右

        if pyxel.frame_count & 0x04:
            self.sprite_draw(x + 0, y + 8, 0, 8, 16, 6, 6)
            self.sprite_draw(x - 6, y + 8, 0, 8, 16, -6, 6)
        else:
            self.sprite_draw(x + 0, y + 8, 0, 8, 24, 6, 6)
            self.sprite_draw(x - 6, y + 8, 0, 8, 24, -6, 6)

        if pyxel.frame_count & 0x04:
            self.sprite_draw(x - 1, y + 8, 0, 8, 16, 6, 6)
            self.sprite_draw(x - 5, y + 8, 0, 8, 16, -6, 6)
        else:
            self.sprite_draw(x - 1, y + 8, 0, 8, 24, 6, 6)
            self.sprite_draw(x - 5, y + 8, 0, 8, 24, -6, 6)

# --------------------------------------------------
    # プレイヤー移動
    def PlayerLeverMove(self):
        # プレイヤー移動
        self.pl_dir = 0                       # 前
        self.vector.x = 0
        self.vector.y = 0

        # キー入力
        direction = input_manager.input_manager.get_movement_direction()

        if direction is not None:
            # 移動方向設定
            self.pl_dir = input_manager.input_manager.get_player_direction_sprite()

            shooting_sub.SetVector(self, math.radians(direction), PL_SPEED)
            self.pos += self.vector

            # 画面内制限
            if self.pos.y < 50:
                self.pos.y = 50
            if self.pos.y > imp.WINDOW_H - 16:
                self.pos.y = imp.WINDOW_H - 16
            if self.pos.x > imp.WINDOW_W - 8:
                self.pos.x = imp.WINDOW_W - 8
            if self.pos.x < 8:
                self.pos.x = 8


# --------------------------------------------------
# プレイヤークラス
class PlayerBullet(imp.Sprite):

    # コンストラクタ
    def __init__(self, x, y, id_0, id_1, item):
        imp.Sprite.__init__(self, imp.OBJPLB, x, y, id_0, id_1, item)

        self.pos_adj = imp.Vector2(-3, -3)
        self.life = 1
        self.hit_point = 1
        self.hit_rectx = 8
        self.hit_recty = 8

        if self.id0 == 0:   # 前
            self.vector = imp.Vector2(0, -6.5)

        if self.id0 == 1:   # 左側
            self.vector = imp.Vector2(-0.25, -6.5)

        if self.id0 == 2:   # 右側
            self.vector = imp.Vector2(0.25, -6.5)

    # メイン
    def update(self):
        self.pos += self.vector

        # 画面内チェック
        self.CheckScreenIn()

    # 描画
    def draw(self):
        pos = self.pos + self.pos_adj
        self.sprite_draw(pos.x, pos.y, 0, 0, 16, 6, 6)

        # 中心の表示
        if imp._DEBUG_:
            shooting_sub.DebugDrawPosHitRect(self)
