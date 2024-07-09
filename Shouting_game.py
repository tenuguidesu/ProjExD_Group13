import pygame as pg
import random
import math

pg.init()

# ディスプレイの設定
SCREEN_WIDTH = pg.display.Info().current_w
SCREEN_HEIGHT = pg.display.Info().current_h
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pg.FULLSCREEN)
pg.display.set_caption("しゅぅてぃんぐげぇむ")

# 色の定義
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# ゲームエリア
GAME_AREA_SIZE = min(SCREEN_WIDTH, SCREEN_HEIGHT) * 0.6
GAME_AREA_X = (SCREEN_WIDTH - GAME_AREA_SIZE) / 2
GAME_AREA_Y = (SCREEN_HEIGHT - GAME_AREA_SIZE) / 2

class Player:
    """
    Playerの操作するキャラのクラス
    """
    def __init__(self):
        self.width = 50
        self.height = 50
        self.x = SCREEN_WIDTH // 2 - self.width // 2
        self.y = SCREEN_HEIGHT // 2 - self.height // 2
        self.speed = 5

    def move(self, dx:int, dy:int):
        """
        自機を速度ベクトルself.x,self.yに基づき,
        new_x,new_yとして移動させる
        プレイヤーの行動範囲を制御する
        """
        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed
        if (GAME_AREA_X < new_x < GAME_AREA_X + GAME_AREA_SIZE - self.width and
            GAME_AREA_Y < new_y < GAME_AREA_Y + GAME_AREA_SIZE - self.height):
            self.x = new_x
            self.y = new_y

    def draw(self, screen: pg.Surface):
        """
        引数 screen：画面surface
        """
        pg.draw.rect(screen, BLUE, (self.x, self.y, self.width, self.height))


class Enemy:
    """
    敵キャラを表示するクラス
    """
    def __init__(self):
        self.width = 60
        self.height = 60
        self.x = random.randint(0, SCREEN_WIDTH - self.width)
        self.y = 50
        self.speed = random.uniform(2, 5)
        self.direction = random.choice([-1, 1])

    def move(self):
        """
        敵キャラを速度ベクトルself.x,self.directionに基づき移動させる
        """
        self.x += self.speed * self.direction
        if self.x <= 0 or self.x >= SCREEN_WIDTH - self.width:
            self.direction *= -1

    def draw(self, screen: pg.Surface):
        """
        引数 screen：画面surface
        """
        pg.draw.rect(screen, RED, (self.x, self.y, self.width, self.height))

class Bullet:
    """
    敵味方が攻撃を行う弾を表すクラス。

    Attributes:
        x (float): 弾の現在のx座標
        y (float): 弾の現在のy座標
        dx (float): x方向の移動速度
        dy (float): y方向の移動速度

    Methods:
        move(): 弾を移動させる
        draw(screen): 弾を画面上に描画する
    """

    def __init__(self, x:float, y:float, target_x:float, target_y:float):
        """
        Bulletオブジェクトを初期化する。

        Args:
            x (float): 弾の初期x座標
            y (float): 弾の初期y座標
            target_x (float): 目標のx座標
            target_y (float): 目標のy座標
        """
        self.x = x
        self.y = y
        angle = math.atan2(target_y - y, target_x - x)
        speed = 5
        self.dx = math.cos(angle) * speed
        self.dy = math.sin(angle) * speed

    def move(self):
        """弾を現在の速度に基づいて移動させる。"""
        self.x += self.dx
        self.y += self.dy

    def draw(self, screen: pg.Surface):
        """
        弾を画面上に描画する。

        Args:
            screen (pygame.Surface): 描画対象の画面
        """
        pg.draw.circle(screen, WHITE, (int(self.x), int(self.y)), 5)

def main():
    player = Player()
    enemy = Enemy() # enemy関数の呼び出し
    player_bullets = [] #プレイヤーと敵の弾を保持するリスト
    enemy_bullets = []
    clock = pg.time.Clock()

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
                elif event.key == pg.K_SPACE: # スペースキーで弾の発射
                    player_bullets.append(Bullet(player.x + player.width // 2, player.y,
                                                 player.x + player.width // 2, 0))

        keys = pg.key.get_pressed()
        player.move(keys[pg.K_RIGHT] - keys[pg.K_LEFT], keys[pg.K_DOWN] - keys[pg.K_UP])

        enemy.move()


        if random.random() < 0.02: # 弾の発生
            enemy_bullets.append(Bullet(enemy.x + enemy.width // 2, enemy.y + enemy.height,
                                        player.x + player.width // 2, player.y + player.height // 2))

        for bullet in player_bullets[:]: # 弾の動きと衝突
            bullet.move()
            if bullet.y < 0:
                player_bullets.remove(bullet)
            elif (enemy.x < bullet.x < enemy.x + enemy.width and
                  enemy.y < bullet.y < enemy.y + enemy.height):
                player_bullets.remove(bullet)

        for bullet in enemy_bullets[:]:
            bullet.move()
            if bullet.y > SCREEN_HEIGHT:
                enemy_bullets.remove(bullet)
            elif (player.x < bullet.x < player.x + player.width and
                  player.y < bullet.y < player.y + player.height):
                enemy_bullets.remove(bullet)

        screen.fill((0, 0, 0))
        # プレイヤーの行動範囲を視覚的に表示する
        pg.draw.rect(screen, WHITE, (GAME_AREA_X, GAME_AREA_Y, GAME_AREA_SIZE, GAME_AREA_SIZE), 2)
        player.draw(screen)
        # 敵キャラを表示
        enemy.draw(screen)
        for bullet in player_bullets + enemy_bullets: # 弾の描画
            bullet.draw(screen)
        pg.display.flip()
        clock.tick(60)

    pg.quit()


if __name__ == "__main__":
    main()

#HPとSPの追加、敵の動きの改善
#敵の弾の改善、ゲームオーバー条件の追加
