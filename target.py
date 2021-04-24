import pygame
from pygame.sprite import Sprite


class Target(Sprite):
    """管理标靶的类。"""

    def __init__(self, ai_game):
        """初始化标靶并设置其起始位置。"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()
        self.color = self.settings.target_color

        # 在（0，0）处创建一个表示标靶的矩形，再设置正确的位置。
        self.rect = pygame.Rect(0, 0, self.settings.target_width,
                                self.settings.target_height)
        self.rect.midright = self.screen_rect.midright

        # 存储标靶的精确水平位置。
        self.y = float(self.rect.y)

    def check_edges(self):
        # 设置标靶运行方向，如果标靶到达屏幕上、下边缘就返回True。
        screen_rect = self.screen.get_rect()
        if (self.rect.top <= 0) or (self.rect.bottom >= screen_rect.bottom):
            return True

    def update(self):
        # 更新表示标靶位置的小数值。
        self.y += (self.settings.target_speed *
                   self.settings.target_direction)
        self.rect.y = self.y

    def draw_target(self):
        """在屏幕上绘制标靶。"""
        pygame.draw.rect(self.screen, self.color, self.rect)
