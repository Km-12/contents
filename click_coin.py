from enum import Enum, auto
from collections import deque, namedtuple

import pyxel
import random

# 初期値
WINDOW_H = 120
WINDOW_W = 160

class GAMEMODE(Enum):
    # 画面のシーンをEnum
    Title = auto()
    Coin = auto()

class Coin:

    def __init__(self):
        # 変数初期値
        self.IMG_ID0 = 0
        self.x = 0
        self.y = 65
        self.vx = 1
        self.pos = -16

        # コイン存在フラグ
        self.exists = True

    def update(self):
        # 移動する
        self.x += self.vx
        # 画面外に出ないようにする
        if self.x < 0:
            self.x = 0
            self.vx *= -1
            self.pos = -16
        if self.x > pyxel.width - 16:
            self.x = pyxel.width -16
            self.vx *= -1
            self.pos = 16

    def checkHit(self, x, y):
        # 判定
        left = self.x
        top = self.y
        right = self.x + 16
        bottom = self.y + 16
        if left <= x <= right:
            if top <= y <= bottom:
                return True
        return False

    def draw_coin(self):
        # 動くコイン描画
        pyxel.blt(self.x, self.y, self.IMG_ID0, 0, 16*(pyxel.frame_count % 4), self.pos, 16, 7)

class App:

    def __init__(self):
        pyxel.init(WINDOW_W, WINDOW_H, caption="coin", fps=12)
        pyxel.load("assets\coin_test.pyxres")

        self.coin_list = []
        self.count_coin = 10 # コインの枚数
        for i in range(self.count_coin):
            coin = Coin() # オブジェクト生成
            coin.x = random.randint(16, pyxel.width-16)
            self.coin_list.append(coin)

        self.my_gamemode = GAMEMODE.Title # 最初にタイトル画面を表示
        pyxel.run(self.update, self.draw)

    def update(self):
        # 選択update
        if self.my_gamemode == GAMEMODE.Title:
            self.update_title()
        elif self.my_gamemode == GAMEMODE.Coin:
            self.update_coin()
            pyxel.mouse(True)

    def update_title(self):
        # スペース押下で遷移する
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.my_gamemode = GAMEMODE.Coin

    def update_coin(self):
        for coin in self.coin_list:
            if coin.exists:
                if pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON):
                    if coin.checkHit(pyxel.mouse_x, pyxel.mouse_y):
                        # クリックされたらコインを消す
                        coin.exists = False
                        # コインの残り枚数
                        self.count_coin -= 1
                # 生存している場合のみ更新
                if coin.exists:
                    coin.update()

    def draw(self):

        pyxel.cls(0)
        # 選択draw
        if self.my_gamemode == GAMEMODE.Title:
            self.draw_title()

        elif self.my_gamemode == GAMEMODE.Coin:
            self.draw_coin()

    def draw_title(self):
        # タイトル画面
        pyxel.text(54, 50, "CLICK COIN", 7)
        pyxel.text(52, 60, "PUSH, SPACE", 7)

    def draw_coin(self):
        # 生存している場合のみ描画
        for coin in self.coin_list:
            if coin.exists:
                coin.draw_coin()
                # メッセージ
                pyxel.text(60, 0, "CLICK COIN!", 7)
                pyxel.text(0, 0, "COUNT: %d" %(self.count_coin), 7)
                # 地面
                pyxel.bltm(0, 88, 0, 0, 0, 24, 16)

        is_wiped = True # 全滅したかどうか
        for coin in self.coin_list:
            if coin.exists:
                is_wiped = False # 全滅していない
        if is_wiped:
           # 全滅させたのでクリア
           pyxel.text(60, 50, "GAME CLEAR", 7)
           # エンター押下で終了する
           if pyxel.btnp(pyxel.KEY_ENTER):
              pyxel.quit()

App()
