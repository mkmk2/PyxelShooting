import pyxel
import imp
import shooting_sub
import EnemyBullet as enemybullet
import random
import effect


# ==================================================
# 敵：ボス0クラス
# id0
# 0: まっすぐ下に移動するだけ
class EnemyBoss0(imp.Sprite):
    BulletTime = 0

    MvTime = 0
    MvWait = 0
    BossMoveTblPtr = 0

    # コンストラクタ
    def __init__(self, x, y, i0, i1, item):
        imp.Sprite.__init__(self, imp.OBJEM, x, y, i0, i1, item)       # Spriteクラスのコンストラクタ

        self.pos = imp.Vector2(0, 0)
        self.pos_adj = imp.Vector2(-76, -40)
        self.tmx_pos = imp.Vector2(0, 128)

        self.hit_point = 1

        self.hit_rectx = 20
        self.hit_recty = 40
        self.vector = imp.Vector2(0, -0.2)
        self.score = 10
        self.life = 100

        imp.game_state.boss_area = 1   # ボスエリアに入った

        # Canon
        imp.game_state.em.append(EnemyBossCanon0(68, 92, 0, 0, 0))
        imp.game_state.em.append(EnemyBossCanon0(84, 92, 0, 0, 0))
        imp.game_state.em.append(EnemyBossCanon0(100, 92, 0, 0, 0))
        imp.game_state.em.append(EnemyBossCanon0(156, 92, 0, 0, 0))
        imp.game_state.em.append(EnemyBossCanon0(172, 92, 0, 0, 0))
        imp.game_state.em.append(EnemyBossCanon0(188, 92, 0, 0, 0))

        if imp.game_state.game_status == imp.GameStatus.TEST:       # テスト
            self.file_tmx = "assets/boss00.tmx"
            pyxel.tilemaps[1] = pyxel.Tilemap.from_tmx(self.file_tmx, 1)

    # -----------------------------------------------
    # メイン
    def update(self):

        self.tmx_pos += self.vector

        if self.tmx_pos.y < 0:
            self.vector = imp.Vector2(0, 0)

        imp.game_state.tile_pos_boss = self.tmx_pos

        self.pos.x = self.tmx_pos.x + 128
        self.pos.y = 80 - self.tmx_pos.y

        # -----------------------------------------------
        # 死にチェック
        if self.life <= 0:          # 0以下なら死ぬ
            self.death = 1          # 死ぬ
            imp.game_state.score += self.score     # scoreを加算
            if imp._DEBUG_:
                print("boss die")

    # -----------------------------------------------
    def draw(self):

        # 中心の表示
        if imp._DEBUG_HIT_:
            shooting_sub.DebugDrawPosHitRect(self)

    # -----------------------------------------------
    def collision_damage(self):
        # エフェクト
        imp.game_state.eff.append(effect.Effect(imp.game_state.collision_hit_pos.x, imp.game_state.collision_hit_pos.y, 0, 0, 0))


# ==================================================
# 敵：ボスCanon0
# id0
# 0:
class EnemyBossCanon0(imp.Sprite):
    BulletTime = 0

    # コンストラクタ
    def __init__(self, x, y, i0, i1, item):
        imp.Sprite.__init__(self, imp.OBJEM, x, y, i0, i1, item)       # Spriteクラスのコンストラクタ

        self.offset_pos = self.pos                  # オフセット位置(オブジェクト生成時に指定)

        self.pos = imp.Vector2(0, 0)
        self.pos_adj = imp.Vector2(-4, -4)
        self.hit_point = 1
        self.hit_rectx = 10
        self.hit_recty = 10

        self.score = 10
        self.life = 10

    # -----------------------------------------------
    # メイン
    def update(self):

        # 弾を撃つ
        self.BulletTime -= 1
        if self.BulletTime <= 0:
            self.BulletTime = random.randint(10, 30)
            if random.random() > 0.5:
                imp.game_state.em.append(enemybullet.EnemyBullet(self.pos.x, self.pos.y, imp.BulletId.PLAYER, 0, 0))

        # -----------------------------------------------
        # 死にチェック
        if self.life <= 0:          # 0以下なら死ぬ
            self.death = 1          # 死ぬ
            imp.game_state.score += self.score     # scoreを加算
            if imp._DEBUG_:
                print("canon die")

                pyxel.tilemaps[2].pset(self.offset_pos.x // 8, self.offset_pos.y // 8, (1, 11))

    # -----------------------------------------------
    def draw(self):

        self.pos.x = imp.game_state.tile_pos_boss.x + self.offset_pos.x
        self.pos.y = 0 - imp.game_state.tile_pos_boss.y + self.offset_pos.y

        pos = self.pos + self.pos_adj

        if self.id0 == 0:
            self.sprite_draw(pos.x, pos.y, 0, 0, 11, 8, 8)

        # 中心の表示
        if imp._DEBUG_HIT_:
            shooting_sub.DebugDrawPosHitRect(self)

    # -----------------------------------------------
    def collision_damage(self):
        # エフェクト
        imp.game_state.eff.append(effect.Effect(self.pos.x, self.pos.y, 0, 0, 0))

