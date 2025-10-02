import pyxel
import imp
import scene
# import input_manager


# ==================================================
class App:
    # ゲームの状態
    imp.game_state.game_status = imp.GameStatus.TITLE
    # メインシーン
    imp.game_state.main_scene = None
    # サブシーン
    imp.game_state.sub_scene = None

    # 初期化---------------------------------------
    def __init__(self):
        pyxel.init(imp.WINDOW_W, imp.WINDOW_H, title="Pyxel Shooting",
                   display_scale=3, fps=60)

        pyxel.images[0].load(0, 0, "assets/img00.png")

        # メインScene タイトル　セット
        scene.SetSubScene(self, scene.SceneTitle())

        imp.pause_flag = False

        pyxel.run(self.update, self.draw)

    # メイン---------------------------------------
    def update(self):

        # F1キーでPause
        if pyxel.btnp(pyxel.KEY_F1) is True and imp._DEBUG_ is True:
            imp.pause_flag = not imp.pause_flag

        if imp.pause_flag is False and imp._DEBUG_ is True:

            # メインシーン
            if imp.game_state.main_scene is not None:
                imp.game_state.main_scene.update()

            # サブシーン
            if imp.game_state.sub_scene is not None:
                imp.game_state.sub_scene.update()

# 画面描画---------------------------------------
    def draw(self):
        # 画面クリア
        pyxel.cls(0)

        # メインシーン
        if imp.game_state.main_scene is not None:
            imp.game_state.main_scene.draw()

            if imp._DEBUG_:
                sc = imp.game_state.main_scene.__class__.__name__
                pyxel.text(0, 1, sc, 7)

        # サブシーン
        if imp.game_state.sub_scene is not None:
            imp.game_state.sub_scene.draw()

            if imp._DEBUG_:
                sc = imp.game_state.sub_scene.__class__.__name__
                pyxel.text(0, 9, sc, 7)


App()
# ==================================================
