import enemy

# --------------------------------------------------
# 敵のセット位置
# 1
STAGE_SET_1 = [
    # 時間, X, Y, class, id0, id1, item
    # まっすぐ
    [120,  128-30,   0,  enemy.EnemyNorm,  0, 0, 0,],
    [0,    128-60,   0,  enemy.EnemyNorm,  0, 0, 0,],

    [120,  128+30,   0,  enemy.EnemyNorm,  2, 0, 0,],
    [0,    128+60,   0,  enemy.EnemyNorm,  2, 0, 0,],

    [120,  128-30,   0,  enemy.EnemyNorm,  3, 0, 0,],
    [0,    128-60,   0,  enemy.EnemyNorm,  3, 0, 0,],

    [120,  128+30,   0,  enemy.EnemyNorm,  1, 0, 0,],
    [30,    128+60,   0,  enemy.EnemyNorm,  1, 0, 0,],

    [120,  128+30,   0,  enemy.EnemyNorm,  1, 0, 0,],
    [30,    128+60,   0,  enemy.EnemyNorm,  1, 0, 0,],

    [120,  128+30,   0,  enemy.EnemyNorm,  1, 0, 0,],
    [30,    128+60,   0,  enemy.EnemyNorm,  1, 0, 0,],

    [100000, 128+60,   0,  enemy.EnemyNorm,  1, 0, 0,],



]

STAGE_SET_2 = [
    # 時間, X, Y, class, id0, id1, item


]

STAGE_SET_3 = [
    # 時間, X, Y, class, id0, id1, item

]

STAGE_SET_4 = [
    # 時間, X, Y, class, id0, id1, item
]

STAGE_SET_TEST = [
    # 時間, X, Y, class, id0, id1, item
    [120,  128+30,   0,  enemy.EnemyNorm,  1, 0, 0,],
    [0,    128+60,   0,  enemy.EnemyNorm,  1, 0, 0,],

    [120,  128+30,   0,  enemy.EnemyNorm,  1, 0, 0,],
    [0,    128+60,   0,  enemy.EnemyNorm,  1, 0, 0,],
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


STAGE_SET_TEST_ENEMY = [
    # 時間, X, Y, class, id0, id1, item
    [0,    128,   0,  enemy.EnemyNorm,  0, 0, 0,],          # まっすぐ
    [0,    128,   0,  enemy.EnemyNorm,  1, 0, 0,],          # 斜め左右往復
    [0,    128,   0,  enemy.EnemyNorm,  2, 0, 0,],          # 左右往復
    [0,    128,   0,  enemy.EnemyNorm,  3, 0, 0,],          # 左右往復して画面下の方で上に帰る 
    
    [9999, 128,   0,  enemy.EnemyNorm,  1, 0, 0,],
]
# ==================================================
