import pygame.font
from pygame.sprite import Group
from ship import Ship

import json


class Scoreboard:
    """显示得分信息的类。"""

    def __init__(self, ai_game):
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # 显示得分所使用的字体设置。
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)
        # 准备包含最高得分和初始得分图像、等级图像等。
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ship()
        self.prep_game_over()

    def prep_score(self):
        """将得分转换为一幅渲染的图像。"""
        rounded_score = round(self.stats.score, -1)
        score_str = "Score:" + "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True,
                                            self.text_color, self.settings.bg_color)

        # 在屏幕右上角显示得分。
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 5

    def prep_high_score(self):
        """将最高得分转换为一幅渲染的图像。"""
        high_score = round(self.stats.high_score, -1)
        high_score_str = "High Score:" + "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True,
                                            self.text_color, self.settings.bg_color)

        # 在屏幕上方中间显示最高得分。
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.midtop = self.screen_rect.midtop
        self.high_score_rect.top = 5

    def prep_level(self):
        """将玩家等级转换为一幅渲染的图像。"""
        level = round(self.stats.level, 0)
        level_str = "Level:" + "{:,}".format(level)
        self.level_image = self.font.render(level_str, True,
                                            self.text_color, self.settings.bg_color)

        # 在得分下方显示玩家等级。
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ship(self):
        """显示飞船剩余数量。"""
        self.ships = Group()
        for ship_number in range(self.stats.ship_left):
            ship = Ship(self.ai_game)
            ship.rect.x = 10 + ship_number * ship.rect.height
            ship.rect.y = 5
            self.ships.add(ship)

    def prep_game_over(self):
        """将游戏结束转换为一幅渲染的图像。"""
        game_over_str = "GAME OVER!"
        self.game_over_image = self.font.render(game_over_str, True,
                                            self.text_color, self.settings.bg_color)

        # 在屏幕中央显示游戏结束。
        self.game_over_rect = self.game_over_image.get_rect()
        self.game_over_rect.center = self.screen_rect.center
        self.game_over_rect.bottom = self.screen_rect.centery - 100

    def show_score(self):
        """在屏幕上显示得分。"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)

    def show_game_over(self):
        """在屏幕上显示游戏结束。"""
        self.screen.blit(self.game_over_image, self.game_over_rect)

    def check_high_score(self):
        """检查是否产生了最高分。"""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    def save_score_record(self):
        """保存最高得分。"""
        score_record = "record.json"
        try:
            with open(score_record, 'w') as s_r:
                json.dump(self.stats.high_score, s_r)
        except FileNotFoundError:
            None
