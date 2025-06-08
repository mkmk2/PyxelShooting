
#_DEBUG_ = True
_DEBUG_ = True

WINDOW_W = 255
WINDOW_H = 240
CAT_H = 16
CAT_W = 16

COLOR_WhitE = 7
COLOR_RED = 8

BLOCK_DOWN_WAIT = 6

GAME_STATUS_TITLE = 0
GAME_STATUS_MAIN = 1
GAME_STATUS_GAMEOVER = 2
GAME_STATUS_STAGECLEAR = 3
GAME_STATUS_NEXTSTAGE = 4


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

# サブシーン
main_scene = None
sub_scene = None             # Nextsub_scene から sub_scene へ入れるときにインスタンス化する、SubScnenに何か入ってたらdelしてから入れる


#
#  プレイヤー・プレイヤーの弾オブジェクト
pl = []

# 敵・敵の弾オブジェクト
em = []

# エフェクト
eff = []

# アイテム
itm = []

game_status = GAME_STATUS_TITLE

# スコア
score = 0

# ステージNo(1から)
stage_no = 0

STAGE_NO_MAX = 4       # 最終ステージ

# 敵セットTbl
StageSetTbl = ""

# プレイヤーレベル
pl_item_num = 0     # アイテム取得数
pl_level = 0        # レベル
pl_levelup_eff = 0  # レベルアップ点滅
PL_ITEM_LEVEL_UP = 3    # レベルアップする個数

# --------------------------------------------------
# スプライト表示の共通クラス
class Sprite:

    # コンストラクタ
    def __init__(self, obj, x, y, id_0, id_1, item):
        self.obj_type = obj
        self.pos_x = x
        self.pos_y = y
        self.vector_x = 0
        self.vector_y = 0
        self.pos_adjx = 0
        self.pos_adjy = 0
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
# 画面内チェック
def CheckScreenIn(self):
    if self.screen_time >= SCREEN_TIME:
        SafeArea = 10           # 画面外のチェックする幅
        if _DEBUG_ == True:
            SafeArea = -20       # Debug 画面の中で判定する

        if -SafeArea < self.pos_x and self.pos_x < WINDOW_W + SafeArea:
            if -SafeArea < self.pos_y and self.pos_y < WINDOW_H + SafeArea:
                return True     # 画面内

        self.death = 1          # 消す
        if _DEBUG_ == True:
            print("out:"+self.__class__.__name__)
        return False            # 画面外

    else:
        self.screen_time += 1
    return True     # 画面内

#  ------------------------------------------
def GetPl(self):
    if len(pl) > 0:
        return pl[0]
    
    return 0
    
