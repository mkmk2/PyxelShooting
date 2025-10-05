import pyxel
import imp
import player
import enemy_set
import enemy
import collision
import input_manager

import os           # タイムスタンプ


# ==================================================
# メインシーンセット-----------------------------
def SetMainScene(self, scene):
    if imp.game_state.main_scene is not None:
        del imp.game_state.main_scene
    imp.game_state.main_scene = scene


# サブシーンセット-------------------------------
def SetSubScene(self, scene):
    if imp.game_state.sub_scene is not None:
        del imp.game_state.sub_scene
    imp.game_state.sub_scene = scene


# ==================================================
# Scene タイトル
class SceneTitle:

    select_pos = 0

    # 初期化---------------------------------------
    def __init__(self):
        imp.game_state.game_status = imp.GameStatus.TITLE    # タイトルに戻る

        self.file = "assets/img00.png"
        pyxel.images[0].from_image(self.file, incl_colors=True)

        self.file_tmx = "assets/bg00.tmx"
        pyxel.tilemaps[0] = pyxel.Tilemap.from_tmx(self.file_tmx, 0)

        self.select_pos = 0
        imp.game_state.stage_no = 0

    # メイン---------------------------------------
    def update(self):
        # タイトル画面
        # 上
        if input_manager.input_manager.is_menu_up_pressed():
            self.select_pos -= 1
            if self.select_pos < 0:
                self.select_pos = 3

        # 下
        if input_manager.input_manager.is_menu_down_pressed():
            self.select_pos += 1
            if self.select_pos > 3:
                self.select_pos = 0

        # 右
        if input_manager.input_manager.is_menu_right_pressed():
            if imp.game_state.stage_no < imp.STAGE_NO_MAX:
                imp.game_state.stage_no += 1

        # 左
        if input_manager.input_manager.is_menu_left_pressed():
            if imp.game_state.stage_no > 1:
                imp.game_state.stage_no -= 1

        # スペース
        if input_manager.input_manager.is_menu_select_pressed():
            if self.select_pos == 1:
                imp.game_state.stage_no += 10               # テストステージは+10


# メインシーン ゲームメイン セット
            imp.game_state.score = 0         # スコア
            imp.game_state.pl_item_num = 0     # アイテム取得数
            imp.game_state.pl_level = 0       # レベル
            imp.game_state.pl_levelup_eff = 0

            if self.select_pos <= 1:
                # ゲームメイン、ゲームテスト
                SetMainScene(self, SceneGameMain())
                SetSubScene(self, SceneStart())
            elif self.select_pos == 2:
                # テスト
                SetMainScene(self, SceneTest())
                SetSubScene(self, None)
            elif self.select_pos == 3:
                # BG
                SetMainScene(self, SceneTestBG())
                SetSubScene(self, None)

    def draw(self):
        # タイトル画面
        pyxel.bltm(0, 0, 0, 0, 0, imp.WINDOW_W, imp.WINDOW_H)

#        ti = "TITLE"
#        pyxel.text(100, 100, ti, 7)

        st = ">"
        pyxel.text(100-10, 180 + (self.select_pos * 10), st, 7)

        st = " START"
        pyxel.text(100, 180, st, 7)
        st = " GAME TEST"
        pyxel.text(100, 190, st, 7)
        st = " SPRITE"
        pyxel.text(100, 200, st, 7)
        st = " BG"
        pyxel.text(100, 210, st, 7)

        # ステージNoの表示
        no = "{:02}".format(imp.game_state.stage_no)
        pyxel.text(180, 180, no, 7)

        pyxel.text(0, 232, "Q:Quit", 7)


# ==================================================
# Scene ゲームメイン
class SceneGameMain:

    # 初期化---------------------------------------
    def __init__(self):

        imp.game_state.game_status = imp.GameStatus.MAIN

        self.file = "assets/img00.png"
        pyxel.images[0].from_image(self.file, incl_colors=True)

        if imp.game_state.stage_no == 0:
            self.file_tmx = "assets/bg00.tmx"
        else:
            self.file_tmx = "assets/bg01.tmx"

        pyxel.tilemaps[0] = pyxel.Tilemap.from_tmx(self.file_tmx, 0)
        pyxel.tilemaps[1] = pyxel.Tilemap.from_tmx(self.file_tmx, 1)

        # 敵セットのテーブル
        if imp.game_state.stage_no < 10:
            if imp.game_state.stage_no == 0:
                imp.game_state.StageSetTbl = enemy_set.STAGE_SET_1
        else:
            imp.game_state.StageSetTbl = enemy_set.STAGE_SET_TEST

        imp.game_state.stage_pos = 0              # ステージ
        imp.game_state.tile_pos.x = 0
        imp.game_state.tile_pos.y = imp.TILE_Y_START
        imp.game_state.BossArea = 0

        # プレイヤーのセット
        imp.game_state.pl.append(player.Player(30, 40, 0, 100, 0))

    def __del__(self):
        # 全てのオブジェクトを消す
        SceneGameMain.DeathAllObject()

    # メイン---------------------------------------
    def update(self):
        # ゲームオーバーになったらスクロール(敵セット)止める
        if imp.game_state.game_status == imp.GameStatus.MAIN:
            imp.game_state.stage_pos += 1

        # 背景
        if imp.game_state.game_status == imp.GameStatus.MAIN or imp.game_state.game_status == imp.GameStatus.STAGECLEAR:
            if imp.game_state.BossArea == 0:
                # ボスエリアに入っていない
                imp.game_state.tile_pos.y -= 1.0
                if imp.game_state.tile_pos.y < 0:
                    imp.game_state.tile_pos.y = 0
            else:
                # ボスエリアに入っている
                imp.game_state.tile_pos.y -= 1.0
                if imp.game_state.tile_pos.y < 0:
                    imp.game_state.tile_pos.y = imp.WINDOW_H * 2

        # ボスエリア(2画面分前でボスエリアに入る)
        if imp.game_state.BossArea == 0 and imp.game_state.tile_pos.y <= imp.WINDOW_H * 2:
            imp.game_state.BossArea = 1

        # ステージに合わせて敵をセット
        self.SetStageEnemy()

        # プレイヤー
        for p in imp.game_state.pl:
            if p.obj_type == imp.OBJPL:
                p.update()
                p.hit = 0

        # プレイヤーの弾
        for p in imp.game_state.pl:
            if p.obj_type == imp.OBJPLB:
                p.update()
                p.hit = 0

        # 敵
        for e in imp.game_state.em:
            if e.obj_type == imp.OBJEM:
                e.update()
                e.hit = 0

        # 敵の弾
        for e in imp.game_state.em:
            if e.obj_type == imp.OBJEMB:
                e.update()
                e.hit = 0

        # エフェクト
        for n in imp.game_state.eff:
            n.update()

        # アイテム
        for n in imp.game_state.itm:
            n.update()
            n.hit = 0

        # 当たり判定 ---------------------------------
        # プレイヤーの弾と敵
        for p in imp.game_state.pl:
            if p.obj_type == imp.OBJPLB:
                for embd in imp.game_state.em:
                    if embd.obj_type == imp.OBJEM:
                        collision.CheckColli(self, p, embd)

        # 敵の弾とプレイヤー
        for em in imp.game_state.em:
            if em.obj_type == imp.OBJEMB:
                for p in imp.game_state.pl:
                    if p.obj_type == imp.OBJPL:
                        collision.CheckColli(self, em, p)

        # 敵とプレイヤー
        for em in imp.game_state.em:
            if em.obj_type == imp.OBJEM:
                for p in imp.game_state.pl:
                    if p.obj_type == imp.OBJPL:
                        collision.CheckColliBody(self, em, p)

        # プレイヤーがアイテムをとる
        for p in imp.game_state.pl:
            if p.obj_type == imp.OBJPL:
                for i in imp.game_state.itm:
                    collision.CheckColliPlItm(self, p, i)

        # プレイヤーが死んだらゲームオーバーへ
        if imp.game_state.game_status != imp.GameStatus.GAMEOVER:       # ゲームオーバーでないとき
            for p in imp.game_state.pl:
                if p.obj_type == imp.OBJPL:
                    if p.death == 1:
                        # サブシーン ゲームオーバー セット
                        SetSubScene(self, SceneGameOver())

        # ボスが死んだらステージクリアへ
#        if imp.game_state.game_status == imp.GameStatus.MAIN:       # ゲーム中のみ
#            for e in imp.game_state.em:
#                if e.__class__.__name__ == "EnemyBoss":
#                    if e.death == 1:

                        # サブシーン ゲームクリアー　セット
#                        SetSubScene(self, SceneGameClear())

        # オブジェクトを消す ---------------------------------
        # プレイヤー・プレイヤーの弾を消す
        for n, p in enumerate(imp.game_state.pl):
            if p.death != 0:
                del imp.game_state.pl[n]     # リストから削除する

        # 敵を消す
        for n, e in enumerate(imp.game_state.em):
            if e.death != 0:
                del imp.game_state.em[n]        # リストから削除する

        # エフェクトを消す
        for n, e in enumerate(imp.game_state.eff):
            if e.death != 0:
                del imp.game_state.eff[n]        # リストから削除する

        # アイテムを消す
        for n, e in enumerate(imp.game_state.itm):
            if e.death != 0:
                del imp.game_state.itm[n]        # リストから削除する

        if input_manager.input_manager.is_quit_pressed():
            SetMainScene(self, SceneTitle())
            SetSubScene(self, None)

    def draw(self):
        # ゲーム画面
        # 後景
        pyxel.bltm(
            0, 0, 0, imp.game_state.tile_pos.x, imp.game_state.tile_pos.y / 2,
            imp.WINDOW_W, imp.WINDOW_H, 0
        )
        # 前景
        pyxel.bltm(
            0, 0, 1, imp.game_state.tile_pos.x,
            imp.game_state.tile_pos.y,
            imp.WINDOW_W, imp.WINDOW_H, 0
        )

        # オブジェクト
        if imp.game_state.game_status == imp.GameStatus.MAIN or imp.game_state.game_status == imp.GameStatus.GAMEOVER\
                or imp.game_state.game_status == imp.GameStatus.STAGECLEAR:
            # プレイヤー
            for p in imp.game_state.pl:
                if p.obj_type == imp.OBJPL:
                    p.draw()

            # プレイヤーの弾
            for p in imp.game_state.pl:
                if p.obj_type == imp.OBJPLB:
                    p.draw()

            # 敵
            for e in imp.game_state.em:
                if e.obj_type == imp.OBJEM:
                    e.draw()

            # 敵の弾
            for e in imp.game_state.em:
                if e.obj_type == imp.OBJEMB:
                    e.draw()

            # エフェクト
            for n in imp.game_state.eff:
                n.draw()

            # アイテム
            for n in imp.game_state.itm:
                n.draw()

            # スコアの表示
            sc = "{:5}".format(imp.game_state.score)
            pyxel.text(220, 230, sc, 7)

            # ゲージ
            for p in imp.game_state.pl:
                if p.obj_type == imp.OBJPL:
                    # Itemゲージ
                    if imp.game_state.pl_levelup_eff == 0:
                        # for n in range(imp.PL_ITEM_LEVEL_UP):
                        #    if n >= imp.game_state.pl_item_num:
                        #        pyxel.blt(
                        #            ((imp.WINDOW_W / 2) - ((imp.PL_ITEM_LEVEL_UP / 2) * 8)) + 8 * n,
                        #            imp.WINDOW_H - 12, 0, 8 * 6, 8 * 1, 8, 8, 0
                        #        )
                        #    else:
                        #        pyxel.blt(
                        #            ((imp.WINDOW_W / 2) - ((imp.PL_ITEM_LEVEL_UP / 2) * 8)) + 8 * n,
                        #            imp.WINDOW_H - 12, 0, 8 * 6, 8 * 2, 8, 8, 0
                        #        )
                        #    else:
                        # ステージの位置から敵をセットする
                        # 点滅
                        imp.game_state.pl_levelup_eff -= 1
                        if pyxel.frame_count & 0x02:
                            for n in range(imp.PL_ITEM_LEVEL_UP):
                                pyxel.blt(
                                    ((imp.WINDOW_W / 2) - ((imp.PL_ITEM_LEVEL_UP / 2) * 8)) + 8 * n,
                                    imp.WINDOW_H - 12, 0, 8 * 6, 8 * 2, 8, 8, 0
                                )

                    # lifeゲージ
                    for n in range(3):
                        if n >= p.life:
                            pyxel.blt(10 + 8 * n, imp.WINDOW_H - 12, 0, 8 * 7, 8 * 1, 8, 8, 0)  # 空
                        else:
                            pyxel.blt(10 + 8 * n, imp.WINDOW_H - 12, 0, 8 * 7, 8 * 2, 8, 8, 0)  # とった分
            # スクロールPos
            if imp._DEBUG_:
                pos = "{:3}".format(imp.game_state.tile_pos.y)
                pyxel.text(220, 190, pos, 7)

                pos = "{:3}".format(imp.game_state.stage_pos)
                pyxel.text(220, 200, pos, 7)

#  ------------------------------------------
    def SetStageEnemy(self):
        sl = len(imp.game_state.StageSetTbl)                # ステージTbl数
        n = 0                                   # 頭からの順番
        pos = 0

        while sl > 0:
            e = imp.game_state.StageSetTbl[n]
            pos += e[0]
            if imp.game_state.stage_pos == pos:          # 等しい時のみ敵セットする
                while imp.game_state.stage_pos == pos:   # 同じPosを繰り返しセット
                    em_id = e[3]
                    # em_idがEnum型の場合、値（int）に変換する
                    if hasattr(em_id, 'value'):
                        em_id_value = em_id.value
                    else:
                        em_id_value = em_id
                    em_tbl = enemy_set.STAGE_SET_ENEMY[em_id_value]
                    t = em_tbl[3]
                    imp.game_state.em.append(t(e[1], e[2], e[4], e[5], e[6]))

                    n += 1                      # 次のTblへ
                    e = imp.game_state.StageSetTbl[n]
                    pos += e[0]
                break
            sl -= 1                              # 次のTblへ
            n += 1

    #  ------------------------------------------
    @staticmethod
    def DeathAllObject():
        # プレイヤー・プレイヤーの弾を消す
        imp.game_state.pl.clear()

        # 敵を消す
        imp.game_state.em.clear()

        # エフェクトを消す
        imp.game_state.eff.clear()

        # アイテムを消す
        imp.game_state.itm.clear()


# ==================================================
# Scene スタート
class SceneStart:

    # 初期化---------------------------------------
    def __init__(self):
        self.WaitTime = 60 * 3

    # メイン---------------------------------------
    def update(self):
        self.WaitTime -= 1
        if self.WaitTime <= 0:
            if imp.game_state.stage_no < 10:
                imp.game_state.sub_scene = None
            else:
                SetSubScene(self, SceneGameTest())

    def draw(self):
        # タイトル画面
        st = "START"
        pyxel.text(100, 100, st, 7)


# ==================================================
# Scene ゲームオーバー
class SceneGameOver:

    # 初期化---------------------------------------
    def __init__(self):
        imp.game_state.game_status = imp.GameStatus.GAMEOVER       # ゲームオーバー

        self.pos_x = 128 - (8 * 4) - 4
        self.pos_y = 100
        self.WaitTime = 60 * 5

    # メイン---------------------------------------
    def update(self):
        self.WaitTime -= 1
        if self.WaitTime <= 0:
            # メイン ゲームシーンのデリート
            SetMainScene(self, None)
            # サブScene タイトル　セット
            SetSubScene(self, SceneTitle())

    def draw(self):
        # GAME OVER
        pyxel.blt(self.pos_x,      self.pos_y, 0, 0,    8*18, 8*4, 16, 0)
        pyxel.blt(self.pos_x + 40, self.pos_y, 0, 8*4,  8*18, 8*4, 16, 0)


# ==================================================
# Scene ゲームクリアー
class SceneGameClear:
    # 初期化---------------------------------------
    def __init__(self):
        imp.game_state.game_status = imp.GameStatus.STAGECLEAR       # ステージクリア

        self.pos_x = 128 - (8 * 2.5)
        self.pos_y = 100
        self.WaitTime = 60 * 5

    # メイン---------------------------------------
    def update(self):
        self.WaitTime -= 1
        if self.WaitTime <= 0:
            # メイン ゲームシーンのデリート
            SetMainScene(self, None)
            # サブScene タイトル　セット
            SetSubScene(self, SceneNextStage())

    def draw(self):
        # STAGE CLEAR
        pyxel.blt(self.pos_x - (8 * 2.5),      self.pos_y, 0, 8*9,  8*18, 8*5, 16, 0)


# ==================================================
# Scene 次のステージへ送る
class SceneNextStage:
    # 初期化---------------------------------------
    def __init__(self):
        imp.game_state.game_status = imp.GameStatus.NEXTSTAGE       # 次のステージ

    # メイン---------------------------------------
    def update(self):
        # メインシーン ゲームメイン セット
        imp.game_state.stage_no += 1
        if imp.game_state.stage_no > imp.STAGE_NO_MAX:
            # メイン ゲームシーンのデリート
            SetMainScene(self, None)
            # サブシーン Start セット
            SetSubScene(self, SceneTitle())
        else:
            # 次のステージ
            SetMainScene(self, SceneGameMain())

            # サブシーン Game Test セット
            SetSubScene(self, SceneGameTest())

    def draw(self):
        pass


# ==================================================
# ==================================================
# Scene Game Test
class SceneGameTest:

    # 初期化---------------------------------------
    def __init__(self):
        self.select_pos = 0
        self.WaitTime = 60 * 3

    # メイン---------------------------------------
    def update(self):
        # 敵選択
        if input_manager.input_manager.is_menu_right_pressed():
            e = enemy_set.STAGE_SET_ENEMY[self.select_pos + 1]
            if e[0] != 9999:
                self.select_pos += 1

        if input_manager.input_manager.is_menu_left_pressed():
            if self.select_pos > 0:
                self.select_pos -= 1

        # スペース
        if input_manager.input_manager.is_menu_enemy_set_pressed():
            # 敵セット
            e = enemy_set.STAGE_SET_ENEMY[self.select_pos]
            t = e[3]
            imp.game_state.em.append(t(e[1], e[2], e[4], e[5], e[6]))

        if input_manager.input_manager.is_quit_pressed():
            SetMainScene(self, SceneTitle())
            SetSubScene(self, None)

    def draw(self):
        # 敵Noの表示
        no = "{:02}".format(self.select_pos)
        pyxel.text(40, 40, "No:"+no, 7)

        pyxel.text(40, 60, "Set Enemy 'A'", 7)
        # enemy_set.pyのSTAGE_SET_TEST_ENEMYで指定されているクラス名の文字列を表示する
        e = enemy_set.STAGE_SET_ENEMY[self.select_pos]
        t = e[3]
        class_str = f"{t.__module__}.{t.__name__}"  # クラス名を表示
        pyxel.text(40, 80, class_str, 7)
        pyxel.text(40, 90, "ID0:"+str(e[4]), 7)
        pyxel.text(40, 100, "ID1:"+str(e[5]), 7)
        pyxel.text(40, 110, "Item:"+str(e[6]), 7)

        pyxel.text(0, 232, "Q:Quit", 7)


# ==================================================
# Scene テスト
class SceneTest:
    # 初期化---------------------------------------
    def __init__(self):
        imp.game_state.game_status = imp.GameStatus.TEST       # テスト
        self.select_pos = 0                     # 敵No

        self.file_anim = "assets/img00.png"             # セットしたい敵に応じてロードを変える必要？
        self.file_anim_time = 0
        pyxel.images[0].load(0, 0, self.file_anim, incl_colors=True)
        self.file_anim_time = os.path.getmtime(self.file_anim)
        self.reload_text_time = 0

        imp.game_state.pl.append(player.Player(128, 128, 0, 0, 0))

    def __del__(self):
        # 全てのオブジェクトを消す
        SceneGameMain.DeathAllObject()

    # メイン---------------------------------------
    def update(self):
        if input_manager.input_manager.is_menu_up_pressed() or input_manager.input_manager.is_menu_down_pressed():
            if input_manager.input_manager.is_menu_up_pressed():
                if self.select_pos > 0:
                    self.select_pos -= 1

            if input_manager.input_manager.is_menu_down_pressed():
                if self.select_pos < 2:
                    self.select_pos += 1

            # オブジェクトを消す
            imp.game_state.pl.clear()
            imp.game_state.em.clear()

            # オブジェクトのセット
            if self.select_pos == 0:
                # プレイヤー
                imp.game_state.pl.append(player.Player(128, 128, 0, 0, 0))
            elif self.select_pos == 1:
                # 敵
                imp.game_state.em.append(enemy.EnemyNorm(128, 128, 0, 0, 0))
            elif self.select_pos == 2:
                # 弾
                imp.game_state.pl.append(player.Player(128, 128, 0, 100, 0))

        for p in imp.game_state.pl:
            p.TestSpriteUpdate()
        for e in imp.game_state.em:
            e.TestSpriteUpdate()

        # ファイルのタイムスタンプが更新されたらリロードする
        t = os.path.getmtime(self.file_anim)
        if self.file_anim_time != t:
            self.file_anim_time = t
            pyxel.images[0].load(0, 0, self.file_anim, incl_colors=True)
            self.reload_text_time = 60

        if input_manager.input_manager.is_quit_pressed():
            SetMainScene(self, SceneTitle())
            SetSubScene(self, None)

    def draw(self):
        st = ">"
        pyxel.text(32-10, 100 + (self.select_pos * 10), st, 7)

        st = " pl"
        pyxel.text(32, 100, st, 7)
        st = " em00"
        pyxel.text(32, 110, st, 7)
        st = " XXX"
        pyxel.text(32, 120, st, 7)

        # ステージNoの表示
        no = "{:02}".format(imp.game_state.stage_no)
        pyxel.text(180, 180, no, 7)

        if self.reload_text_time > 0:
            self.reload_text_time -= 1
            pyxel.text(100, 60, "Reload", pyxel.frame_count % 16)

        # プレイヤー
        for p in imp.game_state.pl:
            p.TestSprite()
        # 敵
        for e in imp.game_state.em:
            e.TestSprite()

        pyxel.text(0, 232, "Q:Quit", 7)


# ==================================================
# Scene テストBG
class SceneTestBG:
    # 初期化---------------------------------------
    def __init__(self):
        imp.game_state.game_status = imp.GameStatus.TEST       # テスト

        self.img_file = "assets/img00.png"
        pyxel.images[0].from_image(self.img_file, incl_colors=True)
        self.img_file = "assets/img01.png"
        pyxel.images[1].from_image(self.img_file, incl_colors=True)

        if imp.game_state.stage_no == 0:
            self.file_tmx = "assets/bg00.tmx"
        else:
            self.file_tmx = "assets/bg01.tmx"

        pyxel.tilemaps[0] = pyxel.Tilemap.from_tmx(self.file_tmx, 0)
        pyxel.tilemaps[1] = pyxel.Tilemap.from_tmx(self.file_tmx, 1)

        imp.game_state.pl.append(player.Player(128, 128, 0, 0, 0))
        imp.game_state.tile_pos.x = 0
        imp.game_state.tile_pos.y = imp.TILE_Y_START

    def __del__(self):
        # 全てのオブジェクトを消す
        SceneGameMain.DeathAllObject()

    # メイン---------------------------------------
    def update(self):
        step = 1.0
        if input_manager.input_manager.is_shot_held():
            step = 10.0

        if input_manager.input_manager.is_input_up_held():
            imp.game_state.tile_pos.y -= step
            if imp.game_state.tile_pos.y < 0:
                imp.game_state.tile_pos.y = 0
        if input_manager.input_manager.is_input_down_held():
            imp.game_state.tile_pos.y += step
            if imp.game_state.tile_pos.y > imp.TILE_Y_START:
                imp.game_state.tile_pos.y = imp.TILE_Y_START
        if input_manager.input_manager.is_input_left_held():
            imp.game_state.tile_pos.x -= step
            if imp.game_state.tile_pos.x < 0:
                imp.game_state.tile_pos.x = 0
        if input_manager.input_manager.is_input_right_held():
            imp.game_state.tile_pos.x += step
            if imp.game_state.tile_pos.x > 256 * 2:
                imp.game_state.tile_pos.x = 0

        if input_manager.input_manager.is_quit_pressed():
            SetMainScene(self, SceneTitle())
            SetSubScene(self, None)

    def draw(self):
        # 背景
        pyxel.bltm(0, 0, 0, imp.game_state.tile_pos.x, imp.game_state.tile_pos.y / 2, imp.WINDOW_W, imp.WINDOW_H, 0)
        pyxel.bltm(0, 0, 1, imp.game_state.tile_pos.x, imp.game_state.tile_pos.y, imp.WINDOW_W, imp.WINDOW_H, 0)

        no = "{:02}".format(imp.game_state.tile_pos.x)
        pyxel.text(100, 80, no, 7)
        no = "{:02}".format(imp.game_state.tile_pos.y)
        pyxel.text(100, 100, no, 7)
        no = "{:02}".format(imp.game_state.tile_pos.y / 2)
        pyxel.text(140, 100, no, 7)

        # ステージNoの表示
        no = "{:02}".format(imp.game_state.stage_no)
        pyxel.text(180, 180, no, 7)

        # プレイヤー
        for p in imp.game_state.pl:
            p.TestSprite()

        pyxel.text(0, 232, "Q:Quit", 7)
