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
def SetVector(self, r, rate):
    self.vector.x = math.cos(r) * rate
    self.vector.y = math.sin(r) * rate


#  ------------------------------------------
def DebugDrawPosHitRect(self):
    if imp._DEBUG_:
        pyxel.pset(self.pos.x, self.pos.y, pyxel.frame_count % 16)
        pyxel.rectb(self.pos.x - (self.hit_rectx / 2), self.pos.y - (self.hit_recty / 2), self.hit_rectx, self.hit_recty, pyxel.frame_count % 16)
    return
