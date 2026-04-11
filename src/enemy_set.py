import imp
import enemy
import enemy_boss0

# --------------------------------------------------
# 敵のセット位置
# 1
STAGE_SET_1 = [
    # 時間, X, Y, id0, id1, item, 0
    [120,  128-30,   0,  imp.EnemyId.EM_STR_DOWN,  0, 0, 0,],
    [0,    128-60,   0,  imp.EnemyId.EM_STR_DOWN,  0, 0, 0,],

    [120,  128+30,   0,  imp.EnemyId.EM_LR_HORI,  0, 0, 0,],
    [0,    128+60,   0,  imp.EnemyId.EM_LR_HORI,  0, 0, 0,],

    [120,  128-30,   0,  imp.EnemyId.EM_LE_HORI_RET,  0, 0, 0,],
    [0,    128-60,   0,  imp.EnemyId.EM_LE_HORI_RET,  0, 0, 0,],

    [120,  0,   200,  imp.EnemyId.EM_SIDE_LR,  0, 0, 0,],
    [0,    256,   200,  imp.EnemyId.EM_SIDE_LR,  0, 0, 0,],

    [120,  128+30,   0,  imp.EnemyId.EM_SIN_DOWN,  0, 0, 0,],
    [30,    128+60,   0,  imp.EnemyId.EM_SIN_DOWN,  0, 0, 0,],

    [120,  128+30,   0,  imp.EnemyId.EM_SIN_DOWN,  0, 0, 0,],
    [30,    128+60,   0,  imp.EnemyId.EM_SIN_DOWN,  0, 0, 0,],

    [120,  128+30,   0,  imp.EnemyId.EM_SIN_DOWN,  0, 0, 0,],
    [30,    128+60,   0,  imp.EnemyId.EM_SIN_DOWN,  0, 0, 0,],

    [100,  128,   0,  imp.EnemyId.EM_STR_ANGLE,  0, 0, 0,],
    [20,  100,   0,  imp.EnemyId.EM_STR_ANGLE,  0, 0, 0,],
    [20,  148,   0,  imp.EnemyId.EM_STR_ANGLE,  0, 0, 0,],
    [20,  128,   0,  imp.EnemyId.EM_STR_ANGLE,  0, 0, 0,],

    [100,  128,   0,  imp.EnemyId.EM_LR_DOWN,  0, 0, 0,],
    [20,   128-50,   0,  imp.EnemyId.EM_LR_DOWN,  0, 0, 0,],
    [20,   128+50,   0,  imp.EnemyId.EM_LR_DOWN,  0, 0, 0,],

    [100,  128,   0,  imp.EnemyId.EM_SIN_DOWN_S,  0, 0, 0,],
    [20,   128-50,   0,  imp.EnemyId.EM_SIN_DOWN_S,  0, 0, 0,],
    [20,   128+50,   0,  imp.EnemyId.EM_SIN_DOWN_S,  0, 0, 0,],

    [100,  128,   0,  imp.EnemyId.EM_TRI_DOWN_S,  0, 0, 0,],
    [20,   128-50,   0,  imp.EnemyId.EM_TRI_DOWN_S,  0, 0, 0,],
    [20,   128+50,   0,  imp.EnemyId.EM_TRI_DOWN_S,  0, 0, 0,],

    [100,   128 - 80,   -30,  imp.EnemyId.EM_MID_BOSS_0,  2, 0, 0,],
    [100,   128,        -30,  imp.EnemyId.EM_MID_BOSS_0,  2, 0, 0,],
    [100,   128 + 80,   -30,  imp.EnemyId.EM_MID_BOSS_0,  2, 0, 0,],

    [800,   128,   -128,  imp.EnemyId.EM_BOSS_0,  0, 0, 0,],
    [100000, 128+60,   0,  imp.EnemyId.EM_SIN_DOWN,  1, 0, 0,],
]

STAGE_SET_2 = [
    # 時間, X, Y, id0, id1, item, 0
    # --- 横移動系で幕開け ---
    [120,  128-40,   0,  imp.EnemyId.EM_LR_HORI,  0, 0, 0,],
    [0,    128+40,   0,  imp.EnemyId.EM_LR_HORI,  0, 0, 0,],
    [0,    128,      0,  imp.EnemyId.EM_LR_HORI,  0, 0, 0,],

    # --- サイド左右から同時侵入 ---
    [120,  0,    80,  imp.EnemyId.EM_SIDE_LR,  0, 0, 0,],
    [0,    256,  80,  imp.EnemyId.EM_SIDE_LR,  0, 0, 0,],
    [60,   0,   160,  imp.EnemyId.EM_SIDE_LR,  0, 0, 0,],
    [0,    256, 160,  imp.EnemyId.EM_SIDE_LR,  0, 0, 0,],

    # --- 帰り型の横移動 3体ずつ2波 ---
    [120,  50,    0,  imp.EnemyId.EM_LE_HORI_RET,  0, 0, 0,],
    [15,   100,   0,  imp.EnemyId.EM_LE_HORI_RET,  0, 0, 0,],
    [15,   150,   0,  imp.EnemyId.EM_LE_HORI_RET,  0, 0, 0,],
    [60,   200,   0,  imp.EnemyId.EM_LE_HORI_RET,  0, 0, 0,],
    [15,   80,    0,  imp.EnemyId.EM_LE_HORI_RET,  0, 0, 0,],
    [15,   130,   0,  imp.EnemyId.EM_LE_HORI_RET,  0, 0, 0,],

    # --- 斜め角度付きで中央集中砲火 ---
    [120,  64,    0,  imp.EnemyId.EM_STR_ANGLE,  0, 0, 0,],
    [15,   96,    0,  imp.EnemyId.EM_STR_ANGLE,  0, 0, 0,],
    [15,   128,   0,  imp.EnemyId.EM_STR_ANGLE,  0, 0, 0,],
    [15,   160,   0,  imp.EnemyId.EM_STR_ANGLE,  0, 0, 0,],
    [15,   192,   0,  imp.EnemyId.EM_STR_ANGLE,  0, 0, 0,],

    # --- まっすぐ降下の素直な3体 ---
    [120,  60,    0,  imp.EnemyId.EM_STR_DOWN,  0, 0, 0,],
    [0,    128,   0,  imp.EnemyId.EM_STR_DOWN,  0, 0, 0,],
    [0,    196,   0,  imp.EnemyId.EM_STR_DOWN,  0, 0, 0,],

    # --- 左右往復しながら降下2波 ---
    [120,  128-60,  0,  imp.EnemyId.EM_LR_DOWN,  0, 0, 0,],
    [20,   128,     0,  imp.EnemyId.EM_LR_DOWN,  0, 0, 0,],
    [20,   128+60,  0,  imp.EnemyId.EM_LR_DOWN,  0, 0, 0,],
    [60,   128-40,  0,  imp.EnemyId.EM_LR_DOWN,  0, 0, 0,],
    [20,   128+40,  0,  imp.EnemyId.EM_LR_DOWN,  0, 0, 0,],

    # --- 中ボス2体 ---
    [150,  128-60,  -30,  imp.EnemyId.EM_MID_BOSS_0,  1, 0, 0,],
    [100,  128+60,  -30,  imp.EnemyId.EM_MID_BOSS_0,  1, 0, 0,],

    [800,   128,   -128,  imp.EnemyId.EM_BOSS_0,  0, 0, 0,],
    [100000, 128+60,   0,  imp.EnemyId.EM_SIN_DOWN,  1, 0, 0,],
]

STAGE_SET_3 = [
    # 時間, X, Y, id0, id1, item, 0
    # --- サイン波の群れで幕開け(3連波) ---
    [120,  50,    0,  imp.EnemyId.EM_SIN_DOWN,  0, 0, 0,],
    [15,   100,   0,  imp.EnemyId.EM_SIN_DOWN,  0, 0, 0,],
    [15,   150,   0,  imp.EnemyId.EM_SIN_DOWN,  0, 0, 0,],
    [15,   200,   0,  imp.EnemyId.EM_SIN_DOWN,  0, 0, 0,],
    [60,   70,    0,  imp.EnemyId.EM_SIN_DOWN,  0, 0, 0,],
    [15,   120,   0,  imp.EnemyId.EM_SIN_DOWN,  0, 0, 0,],
    [15,   170,   0,  imp.EnemyId.EM_SIN_DOWN,  0, 0, 0,],

    # --- 三角波(小) 5連隊 ---
    [120,  30,    0,  imp.EnemyId.EM_TRI_DOWN_S,  0, 0, 0,],
    [20,   80,    0,  imp.EnemyId.EM_TRI_DOWN_S,  0, 0, 0,],
    [20,   128,   0,  imp.EnemyId.EM_TRI_DOWN_S,  0, 0, 0,],
    [20,   176,   0,  imp.EnemyId.EM_TRI_DOWN_S,  0, 0, 0,],
    [20,   224,   0,  imp.EnemyId.EM_TRI_DOWN_S,  0, 0, 0,],

    # --- サイン波(小)とサイドからの挟撃 ---
    [120,  128-70,  0,  imp.EnemyId.EM_SIN_DOWN_S,  0, 0, 0,],
    [15,   128,    0,  imp.EnemyId.EM_SIN_DOWN_S,  0, 0, 0,],
    [15,   128+70,  0,  imp.EnemyId.EM_SIN_DOWN_S,  0, 0, 0,],
    [0,    0,    120,  imp.EnemyId.EM_SIDE_LR,  0, 0, 0,],
    [0,    256,  120,  imp.EnemyId.EM_SIDE_LR,  0, 0, 0,],

    # --- 斜め降下 + まっすぐ同時押し ---
    [120,  50,    0,  imp.EnemyId.EM_STR_ANGLE,  0, 0, 0,],
    [15,   128,   0,  imp.EnemyId.EM_STR_ANGLE,  0, 0, 0,],
    [15,   200,   0,  imp.EnemyId.EM_STR_ANGLE,  0, 0, 0,],
    [0,    80,    0,  imp.EnemyId.EM_STR_DOWN,   0, 0, 0,],
    [0,    160,   0,  imp.EnemyId.EM_STR_DOWN,   0, 0, 0,],

    # --- 帰り型 + 左右往復の混合波 ---
    [120,  60,    0,  imp.EnemyId.EM_LE_HORI_RET,  0, 0, 0,],
    [15,   128,   0,  imp.EnemyId.EM_LE_HORI_RET,  0, 0, 0,],
    [15,   196,   0,  imp.EnemyId.EM_LE_HORI_RET,  0, 0, 0,],
    [0,    90,    0,  imp.EnemyId.EM_LR_HORI,  0, 0, 0,],
    [0,    165,   0,  imp.EnemyId.EM_LR_HORI,  0, 0, 0,],

    # --- 左右往復降下の密集部隊 ---
    [120,  50,    0,  imp.EnemyId.EM_LR_DOWN,  0, 0, 0,],
    [20,   105,   0,  imp.EnemyId.EM_LR_DOWN,  0, 0, 0,],
    [20,   155,   0,  imp.EnemyId.EM_LR_DOWN,  0, 0, 0,],
    [20,   205,   0,  imp.EnemyId.EM_LR_DOWN,  0, 0, 0,],

    # --- 中ボス3体 ---
    [150,  128-80,  -30,  imp.EnemyId.EM_MID_BOSS_0,  2, 0, 0,],
    [100,  128,     -30,  imp.EnemyId.EM_MID_BOSS_0,  0, 0, 0,],
    [100,  128+80,  -30,  imp.EnemyId.EM_MID_BOSS_0,  2, 0, 0,],

    [800,   128,   -128,  imp.EnemyId.EM_BOSS_0,  0, 0, 0,],
    [100000, 128+60,   0,  imp.EnemyId.EM_SIN_DOWN,  1, 0, 0,],
]

STAGE_SET_4 = [
    # 時間, X, Y, id0, id1, item, 0
    # --- 全員揃い踏み！まっすぐ5連隊 ---
    [120,  30,    0,  imp.EnemyId.EM_STR_DOWN,   0, 0, 0,],
    [0,    80,    0,  imp.EnemyId.EM_STR_DOWN,   0, 0, 0,],
    [0,    128,   0,  imp.EnemyId.EM_STR_DOWN,   0, 0, 0,],
    [0,    176,   0,  imp.EnemyId.EM_STR_DOWN,   0, 0, 0,],
    [0,    224,   0,  imp.EnemyId.EM_STR_DOWN,   0, 0, 0,],

    # --- サイドから4方向挟撃 ---
    [120,  0,    60,  imp.EnemyId.EM_SIDE_LR,  0, 0, 0,],
    [0,    256,  60,  imp.EnemyId.EM_SIDE_LR,  0, 0, 0,],
    [0,    0,   140,  imp.EnemyId.EM_SIDE_LR,  0, 0, 0,],
    [0,    256, 140,  imp.EnemyId.EM_SIDE_LR,  0, 0, 0,],
    [60,   0,   100,  imp.EnemyId.EM_SIDE_LR,  0, 0, 0,],
    [0,    256, 100,  imp.EnemyId.EM_SIDE_LR,  0, 0, 0,],

    # --- サイン波(大)とサイン波(小)の同時降下 ---
    [120,  40,    0,  imp.EnemyId.EM_SIN_DOWN,    0, 0, 0,],
    [20,   100,   0,  imp.EnemyId.EM_SIN_DOWN,    0, 0, 0,],
    [20,   160,   0,  imp.EnemyId.EM_SIN_DOWN,    0, 0, 0,],
    [20,   220,   0,  imp.EnemyId.EM_SIN_DOWN,    0, 0, 0,],
    [0,    70,    0,  imp.EnemyId.EM_SIN_DOWN_S,  0, 0, 0,],
    [0,    130,   0,  imp.EnemyId.EM_SIN_DOWN_S,  0, 0, 0,],
    [0,    190,   0,  imp.EnemyId.EM_SIN_DOWN_S,  0, 0, 0,],

    # --- 三角波(小)ジグザグ大群 ---
    [120,  20,    0,  imp.EnemyId.EM_TRI_DOWN_S,  0, 0, 0,],
    [15,   60,    0,  imp.EnemyId.EM_TRI_DOWN_S,  0, 0, 0,],
    [15,   100,   0,  imp.EnemyId.EM_TRI_DOWN_S,  0, 0, 0,],
    [15,   140,   0,  imp.EnemyId.EM_TRI_DOWN_S,  0, 0, 0,],
    [15,   180,   0,  imp.EnemyId.EM_TRI_DOWN_S,  0, 0, 0,],
    [15,   220,   0,  imp.EnemyId.EM_TRI_DOWN_S,  0, 0, 0,],

    # --- 帰り型 + 斜め降下の複合波 ---
    [120,  40,    0,  imp.EnemyId.EM_LE_HORI_RET,  0, 0, 0,],
    [15,   100,   0,  imp.EnemyId.EM_LE_HORI_RET,  0, 0, 0,],
    [15,   160,   0,  imp.EnemyId.EM_LE_HORI_RET,  0, 0, 0,],
    [15,   220,   0,  imp.EnemyId.EM_LE_HORI_RET,  0, 0, 0,],
    [0,    70,    0,  imp.EnemyId.EM_STR_ANGLE,    0, 0, 0,],
    [0,    128,   0,  imp.EnemyId.EM_STR_ANGLE,    0, 0, 0,],
    [0,    185,   0,  imp.EnemyId.EM_STR_ANGLE,    0, 0, 0,],

    # --- 左右往復 + 横移動の波状攻撃 ---
    [120,  40,    0,  imp.EnemyId.EM_LR_DOWN,  0, 0, 0,],
    [20,   90,    0,  imp.EnemyId.EM_LR_DOWN,  0, 0, 0,],
    [20,   140,   0,  imp.EnemyId.EM_LR_DOWN,  0, 0, 0,],
    [20,   190,   0,  imp.EnemyId.EM_LR_DOWN,  0, 0, 0,],
    [0,    65,    0,  imp.EnemyId.EM_LR_HORI,  0, 0, 0,],
    [0,    115,   0,  imp.EnemyId.EM_LR_HORI,  0, 0, 0,],
    [0,    165,   0,  imp.EnemyId.EM_LR_HORI,  0, 0, 0,],
    [0,    215,   0,  imp.EnemyId.EM_LR_HORI,  0, 0, 0,],

    # --- 中ボス3体、全パターン ---
    [150,  128-80,  -30,  imp.EnemyId.EM_MID_BOSS_0,  0, 0, 0,],
    [80,   128,     -30,  imp.EnemyId.EM_MID_BOSS_0,  1, 0, 0,],
    [80,   128+80,  -30,  imp.EnemyId.EM_MID_BOSS_0,  2, 0, 0,],

    [800,   128,   -128,  imp.EnemyId.EM_BOSS_0,  0, 0, 0,],
    [100000, 128+60,   0,  imp.EnemyId.EM_SIN_DOWN,  1, 0, 0,],
]

STAGE_SET_TEST = [
    # 時間, X, Y, class, id0, id1, item
    # [120,  128+30,   0,  enemy.EnemyNorm,  1, 0, 0,],
    # [0,    128+60,   0,  enemy.EnemyNorm,  1, 0, 0,],

    # [120,  128+30,   0,  enemy.EnemyNorm,  1, 0, 0,],
    # [0,    128+60,   0,  enemy.EnemyNorm,  1, 0, 0,],
    # [ 100,  128-40,   0,  enemy.EnemyItemGroup,  0, 1, 1,],
    # [  30,  128-40,   0,  enemy.EnemyItemGroup,  0, 1, 1,],
    # [  30,  128-40,   0,  enemy.EnemyItemGroup,  0, 1, 1,],

    # [ 200,  128-00,   0,  enemy.EnemyItemGroup,  0, 2, 1,],
    # [  10,  128-40,   0,  enemy.EnemyItemGroup,  0, 2, 1,],
    # [  10,  128-80,   0,  enemy.EnemyItemGroup,  0, 2, 1,],

    # [ 150,  128-40,   0,  enemy.EnemyDir,  0, 0, 1,],    #
    # [ 150,  128-40,   0,  enemy.EnemyWide,  0, 0, 1,],    # 撃ってもどる
    [100000, 128+60,   0,  enemy.EnemyNorm,  1, 0, 0,],
]


STAGE_SET_ENEMY = [
    # 時間, X, Y, class, id0, id1, item
    [0,    128,   0,  enemy.EnemyNorm,  0, 0, 0,],          # まっすぐ
    [0,    128,   0,  enemy.EnemyNorm,  1, 0, 0,],          # 斜め左右往復
    [0,    128,   0,  enemy.EnemyNorm,  2, 0, 0,],          # 左右往復
    [0,    128,   0,  enemy.EnemyNorm,  3, 0, 0,],          # 左右往復して画面下の方で上に帰る
    [0,    0,   200,  enemy.EnemyNorm,  4, 0, 0,],          # 画面左右から出現、中央まで移動後、降りながら弾を撃つ
    [0,    128,   0,  enemy.EnemyNorm,  5, 0, 0,],          # サイン波で左右に揺れながら下降
    [0,    128,   0,  enemy.EnemyNorm,  6, 0, 0,],          # 画面上部から登場、1/3まで降下→停止→斜め移動→停止を繰り返し
    [0,    128,   0,  enemy.EnemyNorm,  7, 0, 0,],          # 下に移動しながら左右往復する
    [0,    128,   0,  enemy.EnemyNorm,  8, 0, 0,],          # サイン波(小)で左右に揺れながら下降
    [0,    128,   0,  enemy.EnemyNorm,  9, 0, 0,],          # 三角波で左右に揺れながら下降
    [0,    128,   -30,  enemy.EnemyMBoss,  0, 0, 0,],          # 中ボス
    [0,    128,   -30,  enemy.EnemyMBoss,  1, 0, 0,],          # 中ボス
    [0,    128,   -30,  enemy.EnemyMBoss,  2, 0, 0,],          # 中ボス
    [0,    128,   0,  enemy_boss0.EnemyBoss0,  0, 0, 0,],         # ボス0
]
# ==================================================
