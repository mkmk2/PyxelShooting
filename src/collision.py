import imp


# ==================================================
def CheckColli(self, plat, embd):       # plat 攻撃側　　embd ダメージ側
    if plat.hit_st == 0:
        if embd.hit_st == 0:
            xx = abs(plat.pos.x - embd.pos.x)
            yy = abs(plat.pos.y - embd.pos.y)

            rx = (plat.hit_rectx / 2) + (embd.hit_rectx / 2)
            ry = (plat.hit_recty / 2) + (embd.hit_recty / 2)

            if xx < rx and yy < ry:
                plat.death = 1          # 攻撃側は消える

                plat.hit = 1
                embd.hit = 1
                imp.game_state.collision_hit_pos = plat.pos
                embd.collision_damage()         # 被ダメージ処理

                embd.life -= plat.hit_point      # ダメージ計算
                if embd.life <= 0:              # 0以下なら死ぬ
                    embd.life = 0
                    if imp._DEBUG_CONSOLE_ == 1:
                        print("hit")
                    return True                 # 当たり

    return False                    # 外れ


#  ------------------------------------------
def CheckColliBody(self, at, bd):       # at 攻撃側　　bd ダメージ側
    if at.hit_st == 0:
        if bd.hit_st == 0:
            xx = abs(at.pos.x - bd.pos.x)
            yy = abs(at.pos.y - bd.pos.y)

            rx = (at.hit_rectx / 2) + (bd.hit_rectx / 2)
            ry = (at.hit_recty / 2) + (bd.hit_recty / 2)

            if xx < rx and yy < ry:
                if at.__class__.__name__ != "EnemyBoss":    # ボス以外
                    at.death = 1          # 攻撃側は消える
                if imp._DEBUG_CONSOLE_ == 1:
                    print("hit body:" + bd.__class__.__name__)

                at.hit = 1
                bd.hit = 1
                imp.game_state.collision_hit_pos = at.pos
                bd.collision_damage()         # 被ダメージ処理

                bd.life -= 1                  # ダメージ計算
                if bd.life <= 0:              # 0以下なら死ぬ
                    bd.life = 0
                    return True                 # 当たり

    return False                    # 外れ


#  ------------------------------------------
def CheckColliPlItm(self, p, i):
    xx = abs(p.pos.x - i.pos.x)
    yy = abs(p.pos.y - i.pos.y)

    rx = p.hit_rectx + i.hit_rectx
    ry = p.hit_recty + i.hit_recty

    if xx < rx and yy < ry:
        i.death = 1

        if imp._DEBUG_CONSOLE_ == 1:
            print("item")
        imp.game_state.pl_item_num += 1          # 1個とる
        return True                 # 当たり

    return False                    # 外れ


# ==================================================
