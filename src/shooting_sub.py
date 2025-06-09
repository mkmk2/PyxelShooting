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
    self.vector_x = math.cos(r) * rate
    self.vector_y = math.sin(r) * rate

#        print(self.vector_x)
#        print(self.vector_y)


#  ------------------------------------------
def DebugDrawPosHitRect(self):
    if imp._DEBUG_:
        pyxel.pset(self.pos_x, self.pos_y, pyxel.frame_count % 16)
        pyxel.rectb(self.pos_x - (self.hit_rectx / 2), self.pos_y - (self.hit_recty / 2), self.hit_rectx, self.hit_recty, pyxel.frame_count % 16)
    return
