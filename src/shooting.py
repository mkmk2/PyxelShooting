import pyxel
import random
import math
import imp
import player
import enemy
import effect
import plitem
import enemy_set


# ==================================================
class App:

    # ゲームの状態
    imp.game_status = imp.GAME_STATUS_TITLE

    # メインシーン
    imp.main_scene = None
    # サブシーン
    imp.sub_scene = None

    # 初期化---------------------------------------
    def __init__(self):
        pyxel.init(imp.WINDOW_W, imp.WINDOW_H, title="Pyxel Shooting", display_scale=3, fps=60)
        pyxel.load("assets/my_resource.pyxres")

        pyxel.images[0].load(0, 0, "assets/img0.png")

        # メインScene タイトル　セット
        self.SetSubScene(SceneTitle())

        pyxel.run(self.update, self.draw)

    # メイン---------------------------------------
    def update(self):
        
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        # メインシーン
        if imp.main_scene != None:
            imp.main_scene.update()

        # サブシーン
        if imp.sub_scene != None:
            imp.sub_scene.update()


    # 画面描画---------------------------------------
    def draw(self):
        # 画面クリア
        pyxel.cls(0)

        # メインシーン
        if imp.main_scene != None:
            imp.main_scene.draw()

            if imp._DEBUG_ == True:
                sc = imp.main_scene.__class__.__name__
                pyxel.text(0, 1, sc, 7)

        # サブシーン
        if imp.sub_scene != None:
            imp.sub_scene.draw()

            if imp._DEBUG_ == True:
                sc = imp.sub_scene.__class__.__name__
                pyxel.text(0, 9, sc, 7)

    # メインシーンセット-----------------------------
    def SetMainScene(self, scene):
        if imp.main_scene != None:
            del imp.main_scene
        imp.main_scene = scene

    # サブシーンセット-------------------------------
    def SetSubScene(self, scene):
        if imp.sub_scene != None:
            del imp.sub_scene
        imp.sub_scene = scene

# ==================================================
# Scene タイトル
class SceneTitle:

    select_pos = 0

    # 初期化---------------------------------------
    def __init__(self):
        imp.game_status = imp.GAME_STATUS_TITLE    # タイトルに戻る

        self.select_pos = 0
        imp.stage_no = 1

    def __del__(self):
        pass

    # メイン---------------------------------------
    def update(self):
        # タイトル画面
        # 上移動(上カーソルキー)
        if pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP):
            if self.select_pos > 0:
                self.select_pos -= 1

        # 下移動(下カーソルキー)
        if pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN):
            if self.select_pos == 0:
                self.select_pos += 1

        # 右移動(右カーソルキー) UP
        if pyxel.btnp(pyxel.KEY_RIGHT) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
            if imp.stage_no < imp.STAGE_NO_MAX:
                imp.stage_no += 1

        # 左移動(左カーソルキー) DOWN
        if pyxel.btnp(pyxel.KEY_LEFT) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
            if imp.stage_no > 1:
                imp.stage_no -= 1

        if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_A) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_B):
            if self.select_pos == 1:
                imp.stage_no += 10               # テストステージは+10

            
            # メインシーン ゲームメイン セット
            imp.score = 0         # スコア
            imp.pl_item_num = 0     # アイテム取得数
            imp.pl_level = 0       # レベル
            imp.pl_levelup_eff = 0

            App.SetMainScene(self,SceneGameMain())

            # サブシーン Start セット
            App.SetSubScene(self,SceneStart())
        
    def draw(self):
        # タイトル画面
        pyxel.bltm(0, 0, 0, 8 * 9, 0, 32, 30)

#        ti = "TITLE"
#        pyxel.text(100, 100, ti, 7)

        st = ">"
        pyxel.text(100-10, 180 + (self.select_pos * 10), st, 7)

        st = " START"
        pyxel.text(100, 180, st, 7)
        test = " TEST"
        pyxel.text(100, 190, test, 7)

        # ステージNoの表示
        no = "{:02}".format(imp.stage_no)
        pyxel.text(180, 180, no, 7)

# ==================================================
# Scene ゲームメイン
class SceneGameMain:

    stage_pos = 0

    # 初期化---------------------------------------
    def __init__(self):

        imp.game_status = imp.GAME_STATUS_MAIN

        # 敵セットのテーブル
        if imp.stage_no < 10:
            if imp.stage_no == 1:
                imp.StageSetTbl = enemy_set.STAGE_SET_1
        else:
            imp.StageSetTbl = enemy_set.STAGE_SET_TEST

        self.stage_pos = 0              # ステージ

        # プレイヤーのセット
        imp.pl.append(player.Player(30, 40, 0, 100, 0))

    def __del__(self):
        # 全てのオブジェクトを消す
        self.deathAllObject()

    # メイン---------------------------------------
    def update(self):
        # ゲームオーバーになったらスクロール(敵セット)止める
        if imp.game_status == imp.GAME_STATUS_MAIN:
            self.stage_pos += 1

        self.SetStageEnemy()

        # プレイヤー
        for p in imp.pl:
            if p.obj_type == imp.OBJPL:
                p.update()
                p.hit = 0

        # プレイヤーの弾
        for p in imp.pl:
            if p.obj_type == imp.OBJPLB:
                p.update()
                p.hit = 0

        # 敵
        for e in imp.em:
            if e.obj_type == imp.OBJEM:
                e.update()
                e.hit = 0

        # 敵の弾
        for e in imp.em:
            if e.obj_type == imp.OBJEMB:
                e.update()
                e.hit = 0

        # エフェクト
        for n in imp.eff:
            n.update()

        # アイテム
        for n in imp.itm:
            n.update()
            n.hit = 0

        # 当たり判定 ---------------------------------
        # プレイヤーの弾と敵
        for p in imp.pl:
            if p.obj_type == imp.OBJPLB:
                for embd in imp.em:
                    if embd.obj_type == imp.OBJEM:
                        self.CheckColli(p, embd)

        # 敵の弾とプレイヤー
        for em in imp.em:
            if em.obj_type == imp.OBJEMB:
                for p in imp.pl:
                    if p.obj_type == imp.OBJPL:
                        self.CheckColli(em, p)

        # 敵とプレイヤー
        for em in imp.em:
            if em.obj_type == imp.OBJEM:
                for p in imp.pl:
                    if p.obj_type == imp.OBJPL:
                        self.CheckColliBody(em, p)

        # プレイヤーがアイテムをとる
        for p in imp.pl:
            if p.obj_type == imp.OBJPL:
                for i in imp.itm:
                    self.CheckColliPlItm(p, i)

        # プレイヤーが死んだらゲームオーバーへ
        if imp.game_status != imp.GAME_STATUS_GAMEOVER:       # ゲームオーバーでないとき
            for p in imp.pl:
                if p.obj_type == imp.OBJPL:
                    if p.death == 1:
                        # サブシーン ゲームオーバー セット
                        App.SetSubScene(self,SceneGameOver())

        # ボスが死んだらステージクリアへ
        if imp.game_status == imp.GAME_STATUS_MAIN:       # ゲーム中のみ
            for e in imp.em:
                if e.__class__.__name__ == "EnemyBoss":
                    if e.death == 1:

                        # サブシーン ゲームクリアー　セット
                        App.SetSubScene(self,SceneGameClear())

        # オブジェクトを消す ---------------------------------
        # プレイヤー・プレイヤーの弾を消す
        for n,p in enumerate(imp.pl):
            if p.death != 0:
                del imp.pl[n]     # リストから削除する

        # 敵を消す
        for n,e in enumerate(imp.em):
            if e.death != 0:
                del imp.em[n]        # リストから削除する

        # エフェクトを消す
        for n,e in enumerate(imp.eff):
            if e.death != 0:
                del imp.eff[n]        # リストから削除する

        # アイテムを消す
        for n,e in enumerate(imp.itm):
            if e.death != 0:
                del imp.itm[n]        # リストから削除する
        
    def draw(self):
        # ゲーム画面
        if imp.game_status == imp.GAME_STATUS_MAIN or imp.game_status == imp.GAME_STATUS_GAMEOVER or imp.game_status == imp.GAME_STATUS_STAGECLEAR:
            # プレイヤー
            for p in imp.pl:
                if p.obj_type == imp.OBJPL:
                    p.draw()

            # プレイヤーの弾
            for p in imp.pl:
                if p.obj_type == imp.OBJPLB:
                    p.draw()

            # 敵
            for e in imp.em:
                if e.obj_type == imp.OBJEM:
                    e.draw()

            # 敵の弾
            for e in imp.em:
                if e.obj_type == imp.OBJEMB:
                    e.draw()


            # エフェクト
            for n in imp.eff:
                n.draw()

            # アイテム
            for n in imp.itm:
                n.draw()

            # スコアの表示
            sc = "{:5}".format(imp.score)
            pyxel.text(220, 230, sc, 7)

            # ゲージ
            for p in imp.pl:
                if p.obj_type == imp.OBJPL:
                    # Itemゲージ
                    if imp.pl_levelup_eff == 0:
                        for n in range(imp.PL_ITEM_LEVEL_UP):
                            if n >= imp.pl_item_num:
                                pyxel.blt(((imp.WINDOW_W / 2) - ((imp.PL_ITEM_LEVEL_UP / 2) * 8)) + 8 * n, imp.WINDOW_H - 12, 0, 8 * 6, 8 * 1, 8, 8, 0)  # 空
                            else:
                                pyxel.blt(((imp.WINDOW_W / 2) - ((imp.PL_ITEM_LEVEL_UP / 2) * 8)) + 8 * n, imp.WINDOW_H - 12, 0, 8 * 6, 8 * 2, 8, 8, 0)  # とった分
                    else:
        # ステージの位置から敵をセットする
                    # 点滅
                        imp.pl_levelup_eff -= 1
                        if pyxel.frame_count & 0x02:
                            for n in range(imp.PL_ITEM_LEVEL_UP):
                                pyxel.blt(((imp.WINDOW_W / 2) - ((imp.PL_ITEM_LEVEL_UP / 2) * 8)) + 8 * n, imp.WINDOW_H - 12, 0, 8 * 6, 8 * 2, 8, 8, 0)  # とった分

                    # lifeゲージ
                    for n in range(3):
                        if n >= p.life:
                            pyxel.blt(10 + 8 * n, imp.WINDOW_H - 12, 0, 8 * 7, 8 * 1, 8, 8, 0)  # 空
                        else:
                            pyxel.blt(10 + 8 * n, imp.WINDOW_H - 12, 0, 8 * 7, 8 * 2, 8, 8, 0)  # とった分
            # スクロールPos
            if imp._DEBUG_ == True:
                pos = "{:5}".format(self.stage_pos)
                pyxel.text(220, 200, pos, 7)


    #  ------------------------------------------
    def SetStageEnemy(self):
        l = len(imp.StageSetTbl)                # ステージTbl数
        n = 0                                   # 頭からの順番
        pos = 0

        while l > 0:
            e = imp.StageSetTbl[n]
            pos += e[0]
            if self.stage_pos == pos:          # 等しい時のみ敵セットする
                while self.stage_pos == pos:   # 同じPosを繰り返しセット
                    t = e[3]
                    imp.em.append(t(e[1], e[2], e[4], e[5], e[6]))

                    n += 1                      # 次のTblへ
                    e = imp.StageSetTbl[n]
                    pos += e[0]
                break
            l -= 1                              # 次のTblへ
            n += 1

    #  ------------------------------------------
    def CheckColli(self, plat, embd):       # plat 攻撃側　　embd ダメージ側
        if plat.hit_st == 0:
            if embd.hit_st == 0:
                xx = abs(plat.pos_x - embd.pos_x)
                yy = abs(plat.pos_y - embd.pos_y)

                rx = (plat.hit_rectx / 2) + (embd.hit_rectx / 2)
                ry = (plat.hit_recty / 2) + (embd.hit_recty / 2)

                if xx < rx and yy < ry:
                    plat.death = 1          # 攻撃側は消える
                    # エフェクト
                    imp.eff.append(effect.Effect(plat.pos_x, plat.pos_y, 0, 0, 0))

                    plat.hit = 1
                    embd.hit = 1
                    embd.life -= plat.hit_point      # ダメージ計算
                    if embd.life <= 0:              # 0以下なら死ぬ
                        embd.life = 0
                        if imp._DEBUG_ == True:
                            print("hit")
                        return True                 # 当たり

        return False                    # 外れ

    #  ------------------------------------------
    def CheckColliBody(self, at, bd):       # at 攻撃側　　bd ダメージ側
        if at.hit_st == 0:
            if bd.hit_st == 0:
                xx = abs(at.pos_x - bd.pos_x)
                yy = abs(at.pos_y - bd.pos_y)

                rx = (at.hit_rectx / 2) + (bd.hit_rectx / 2)
                ry = (at.hit_recty / 2) + (bd.hit_recty / 2)

                if xx < rx and yy < ry:
                    if at.__class__.__name__ != "EnemyBoss":    # ボス以外
                        at.death = 1          # 攻撃側は消える
                    # エフェクト
                    imp.eff.append(effect.Effect(at.pos_x, at.pos_y, 0, 0, 0))
                    if imp._DEBUG_ == True:
                        print("hit body:" + bd.__class__.__name__)

                    at.hit = 1
                    bd.hit = 1
                    bd.life -= 1                  # ダメージ計算
                    if bd.life <= 0:              # 0以下なら死ぬ
                        bd.life = 0
                        return True                 # 当たり

        return False                    # 外れ

    #  ------------------------------------------
    def CheckColliPlItm(self, p, i):
        xx = abs(p.pos_x - i.pos_x)
        yy = abs(p.pos_y - i.pos_y)

        rx = p.hit_rectx + i.hit_rectx
        ry = p.hit_recty + i.hit_recty

        if xx < rx and yy < ry:
            i.death = 1
            
            if imp._DEBUG_ == True:
                print("item")
            imp.pl_item_num += 1          # 1個とる
            return True                 # 当たり

        return False                    # 外れ

    #  ------------------------------------------
    def deathAllObject(self):
        # プレイヤー・プレイヤーの弾を消す
        imp.pl.clear()

        # 敵を消す
        imp.em.clear()

        # エフェクトを消す
        imp.eff.clear()

        # アイテムを消す
        imp.itm.clear()

# ==================================================
# Scene スタート
class SceneStart:

    # 初期化---------------------------------------
    def __init__(self):
        self.WaitTime = 60 * 3

    def __del__(self):
        pass

    # メイン---------------------------------------
    def update(self):
        self.WaitTime -= 1
        if self.WaitTime <= 0:
            imp.sub_scene = None
        
    def draw(self):
        # タイトル画面
        st = "START"
        pyxel.text(100, 100, st, 7)

# ==================================================
# Scene ゲームオーバー
class SceneGameOver:

    # 初期化---------------------------------------
    def __init__(self):
        imp.game_status = imp.GAME_STATUS_GAMEOVER       # ゲームオーバー

        self.pos_x = 128 - (8 * 4) - 4
        self.pos_y = 100
        self.WaitTime = 60 * 5

    def __del__(self):
        pass

    # メイン---------------------------------------
    def update(self):
        self.WaitTime -= 1
        if self.WaitTime <= 0:
            # メイン ゲームシーンのデリート
            App.SetMainScene(self,None)
            # サブScene タイトル　セット
            App.SetSubScene(self,SceneTitle())
        
    def draw(self):
        # GAME OVER
        pyxel.blt(self.pos_x,      self.pos_y, 0, 0,    8*18, 8*4, 16, 0)
        pyxel.blt(self.pos_x + 40, self.pos_y, 0, 8*4,  8*18, 8*4, 16, 0)

# ==================================================
# Scene ゲームクリアー
class SceneGameClear:
    # 初期化---------------------------------------
    def __init__(self):
        imp.game_status = imp.GAME_STATUS_STAGECLEAR       # ステージクリア

        self.pos_x = 128 - (8 * 2.5)
        self.pos_y = 100
        self.WaitTime = 60 * 5

    def __del__(self):
        pass

    # メイン---------------------------------------
    def update(self):
        self.WaitTime -= 1
        if self.WaitTime <= 0:
            # メイン ゲームシーンのデリート
            App.SetMainScene(self,None)
            # サブScene タイトル　セット
            App.SetSubScene(self,SceneNextStage())
        
    def draw(self):
        # STAGE CLEAR
        pyxel.blt(self.pos_x - (8 * 2.5),      self.pos_y, 0, 8*9,  8*18, 8*5, 16, 0)

# ==================================================
# Scene 次のステージへ送る
class SceneNextStage:
    # 初期化---------------------------------------
    def __init__(self):
        imp.game_status = imp.GAME_STATUS_NEXTSTAGE       # 次のステージ

    def __del__(self):
        pass

    # メイン---------------------------------------
    def update(self):
            # メインシーン ゲームメイン セット
            imp.stage_no += 1
            if imp.stage_no > imp.STAGE_NO_MAX:
                # メイン ゲームシーンのデリート
                App.SetMainScene(self,None)
                # サブシーン Start セット
                App.SetSubScene(self,SceneTitle())
            else:
                # 次のステージ
                App.SetMainScene(self,SceneGameMain())

                # サブシーン Start セット
                App.SetSubScene(self,SceneStart())

    def draw(self):
        pass


App()

# ==================================================
