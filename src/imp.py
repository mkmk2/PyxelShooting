import pyxel
from enum import Enum

# _DEBUG_ = True
_DEBUG_ = True
_DEBUG_LV_ = False
_DEBUG_HIT_ = True
_DEBUG_CONSOLE_ = 0  # 0:無効 1:screen,hit  2:  3:

pause_flag = False

WINDOW_W = 255
WINDOW_H = 240
CAT_H = 16
CAT_W = 16

COLOR_WHITE = 7
COLOR_RED = 8


class GameStatus(Enum):
    TITLE = 0
    MAIN = 1
    GAMEOVER = 2
    STAGECLEAR = 3
    NEXTSTAGE = 4
    TEST = 5


POS_FIELD_X = 10
POS_FIELD_Y = 4

SCREEN_TIME = 100           # 画面外にセットされたあとに画面内判定を開始するまでの時間

OBJPL = "OBJPL"
OBJPLB = "OBJPLB"
OBJEM = "OBJEM"
OBJEMB = "OBJEMB"
OBJEFF = "OBJEFF"
OBJITM = "OBJITM"

# エフェクトId
EFF_BOOM = 0
EFF_BOOM_MOVE = 1

STAGE_NO_MAX = 4       # 最終ステージ
# プレイヤーレベル
PL_ITEM_LEVEL_UP = 3    # レベルアップする個数

TILE_Y_START = 256 * 12 - WINDOW_H


class EnemyId(Enum):
    EM_STR_DOWN = 0     # まっすぐ下に移動するだけ
    EM_LR_TILT = 1      # 下に移動しながら斜めに左右往復する
    EM_LR_HORI = 2      # 下に移動しながら左右往復する
    EM_LE_HORI_RET = 3  # 左右往復して画面下の方で上に帰る
    EM_SIDE_LR = 4      # 画面左右から出現、中央まで移動後、降りながら弾を撃つ
    EM_SIN_DOWN = 5     # サイン波で左右に揺れながら下降
    EM_STR_ANGLE = 6    # 上から出現、左右にランダム移動と停止を繰り返す
    EM_LR_DOWN = 7      # 下に移動しながら左右往復する
    EM_SIN_DOWN_S = 8     # サイン波(小)で左右に揺れながら下降
    EM_MID_BOSS_0 = 9   # 中ボス0


class BulletId(Enum):
    STRAIGHT = 0
    PLAYER = 1
    LEFT = 2
    RIGHT = 3
    DEFAULT = 4


# --------------------------------------------------
# スプライト表示の共通クラス
class Sprite:

    # コンストラクタ
    def __init__(self, obj, x, y, id_0, id_1, item):
        self.obj_type = obj
        self.pos = Vector2(x, y)
        self.vector = Vector2(0, 0)
        self.pos_adj = Vector2(0, 0)
        self.rot = 0
        self.id0 = id_0
        self.id1 = id_1
        self.item_set = item

        self.st0 = 0
        self.st1 = 0
        self.st2 = 0

        self.ptn_time = 0
        self.ptn_no = 0

        self.display = 1
        self.life = 10
        self.death = 0                  # 1:インスタンスを削除する
        self.screen_time = 0             # 画面内チェックの開始時間
        self.score = 0

        self.hit_st = 0                  # 1:当たりナシ
        self.hit_rectx = 0
        self.hit_recty = 0
        self.hit_point = 0
        self.hit = 0                    # 1:何かに当たった

        self.tmp_ctr = 0

#  ------------------------------------------
# スプライト表示
    def sprite_draw(self, x, y, img, u, v, w, h):
        pyxel.blt(x, y, img, u * 8, v * 8, w, h, 0)

#  ------------------------------------------
# 画面内チェック
    def CheckScreenIn(self):
        if self.screen_time >= SCREEN_TIME:
            SafeArea = 16           # 画面外のチェックする幅

            if -SafeArea < self.pos.x and self.pos.x < WINDOW_W + SafeArea:
                if -SafeArea < self.pos.y and self.pos.y < WINDOW_H + SafeArea:
                    return True     # 画面内

            self.death = 1          # 消す
            if _DEBUG_CONSOLE_ == 1:
                print("out:"+self.__class__.__name__)
            return False            # 画面外

        else:
            self.screen_time += 1
        return True     # 画面内


#  ------------------------------------------
def GetPl(self):
    if len(game_state.pl) > 0:
        return game_state.pl[0]

    return 0


# Vector2型の定義
class Vector2:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        return Vector2(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar):
        return Vector2(self.x / scalar, self.y / scalar)

    def __repr__(self):
        return f"Vector2({self.x}, {self.y})"


class GameState:
    def __init__(self):
        self.main_scene = None      # シーン
        self.sub_scene = None

        self.pl = []                # プレイヤー・プレイヤーの弾オブジェクト
        self.em = []                # 敵・敵の弾オブジェクト
        self.eff = []               # エフェクト
        self.itm = []               # アイテム
        self.game_status = GameStatus.TITLE
        self.score = 0
        self.stage_no = 0           # ステージNo(1から)
        self.stage_pos = 0          # 敵セット
        self.StageSetTbl = ""       # 敵セットTbl
        self.BossArea = 0           # ボスエリア
        # プレイヤーレベル
        self.pl_item_num = 0        # アイテム取得数
        self.pl_level = 0           # アイテム取得数
        self.pl_levelup_eff = 0     # レベルアップ点滅
        self.tile_pos = Vector2(0, 0)   # タイルPos


# GameStateのインスタンスを作成
# これを他ファイルでimportして使う
game_state = GameState()
