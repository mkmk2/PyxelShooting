import imp
import enemy
import enemy_boss0

# --------------------------------------------------
# 敵のセット位置
# 1
STAGE_SET_1 = [
    # 時間, X, Y, id0, id1, item, 0
    # まっすぐ
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

    [100,   128,   0,  imp.EnemyId.EM_MID_BOSS_0,  0, 0, 0,],
    [100000, 128+60,   0,  imp.EnemyId.EM_SIN_DOWN,  1, 0, 0,],
]

STAGE_SET_2 = [
    # 時間, X, Y, id0, id1, item, 0


]

STAGE_SET_3 = [
    # 時間, X, Y, id0, id1, item, 0

]

STAGE_SET_4 = [
    # 時間, X, Y, id0, id1, item, 0
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
    [0,    128,   0,  enemy.EnemyMBoss,  0, 0, 0,],          # 中ボス
    [0,    128,   0,  enemy_boss0.EnemyBoss0,  0, 0, 0,],         # ボス0

    [9999, 128,   0,  enemy.EnemyNorm,  1, 0, 0,],
]
# ==================================================
