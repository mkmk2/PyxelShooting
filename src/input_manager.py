import pyxel


# キー入力管理
class InputManager:
    def __init__(self):
        pass

    def update(self):
        pass

    # ゲーム終了 Q
    def is_quit_pressed(self):
        return pyxel.btnp(pyxel.KEY_Q)

    # メニュー操作
    def is_menu_up_pressed(self):
        return (pyxel.btnp(pyxel.KEY_UP) or
                pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP))

    def is_menu_down_pressed(self):
        return (pyxel.btnp(pyxel.KEY_DOWN) or
                pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN))

    def is_menu_left_pressed(self):
        return (pyxel.btnp(pyxel.KEY_LEFT) or
                pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT))

    def is_menu_right_pressed(self):
        return (pyxel.btnp(pyxel.KEY_RIGHT) or
                pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT))

    def is_menu_select_pressed(self):
        return (pyxel.btnp(pyxel.KEY_SPACE) or
                pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A) or
                pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B))

# プレイヤーの移動
    # 上
    def is_input_up_held(self):
        return (pyxel.btn(pyxel.KEY_UP) or
                pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP))

    # 下
    def is_input_down_held(self):
        return (pyxel.btn(pyxel.KEY_DOWN) or
                pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN))

    # 右
    def is_input_left_held(self):
        return (pyxel.btn(pyxel.KEY_LEFT) or
                pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT))

    # 左
    def is_input_right_held(self):
        return (pyxel.btn(pyxel.KEY_RIGHT) or
                pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT))

    # 上下右左
    def is_any_movement_held(self):
        return (self.is_input_up_held() or
                self.is_input_down_held() or
                self.is_input_left_held() or
                self.is_input_right_held())

    def get_movement_direction(self):
        up = self.is_input_up_held()
        down = self.is_input_down_held()
        left = self.is_input_left_held()
        right = self.is_input_right_held()

        # 8方向の判定
        if up and right:
            return 315  # 上右
        elif up and left:
            return 225  # 上左
        elif down and right:
            return 45   # 下右
        elif down and left:
            return 135  # 下左
        elif up:
            return 270  # 上
        elif down:
            return 90   # 下
        elif right:
            return 0    # 右
        elif left:
            return 180  # 左
        else:
            return None  # 移動なし

    def get_player_direction_sprite(self):

        if self.is_input_left_held():
            return 1  # 左向き
        elif self.is_input_right_held():
            return 2  # 右向き
        else:
            return 0  # 前向き

    # ショット
    def is_shot_held(self):
        return (pyxel.btn(pyxel.KEY_SPACE) or
                pyxel.btn(pyxel.GAMEPAD1_BUTTON_A) or
                pyxel.btn(pyxel.GAMEPAD1_BUTTON_B))

    def is_shot_pressed(self):
        return (pyxel.btnp(pyxel.KEY_SPACE) or
                pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A) or
                pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B))


# インスタンス化
input_manager = InputManager()
