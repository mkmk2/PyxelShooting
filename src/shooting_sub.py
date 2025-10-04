import pyxel
import math
import imp


#  ------------------------------------------
def GetDirection(self, x1, y1, x2, y2):
    x = x2 - x1
    y = y2 - y1
    a = math.atan2(y, x)
#        print(math.degrees(a))

    return a


#  ------------------------------------------
def GetDirection32(self, x1, y1, x2, y2):
    # 0度を基準に32方向（11.25度刻み）に制限した角度（ラジアン）を返す。
    x = x2 - x1
    y = y2 - y1
    angle = math.atan2(y, x)  # -π～π

    # 0度を右方向（x軸正方向）とし、0～2πに正規化
    if angle < 0:
        angle += 2 * math.pi

    # 32方向に分割（1方向あたり11.25度 = π/16ラジアン）
    direction_index = int((angle + (math.pi / 32)) // (math.pi / 16)) % 32
    quantized_angle = direction_index * (math.pi / 16)

    return quantized_angle


#  ------------------------------------------
def SetVector(self, r, rate):
    self.vector.x = math.cos(r) * rate
    self.vector.y = math.sin(r) * rate


#  ------------------------------------------
def DebugDrawPosHitRect(self):
    if imp._DEBUG_:
        pyxel.rectb(self.pos.x - 1, self.pos.y - 1, 2, 2, pyxel.frame_count % 16)
        pyxel.rectb(self.pos.x - (self.hit_rectx / 2), self.pos.y - (self.hit_recty / 2), self.hit_rectx, self.hit_recty, pyxel.frame_count % 16)
    return
