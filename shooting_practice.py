import sys
import pygame
from time import sleep

from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from target import Target
from button import PlayButton, EasyButton, NormalButton, DifficultyButton
from scoreboard import Scoreboard


class ShootingPractice:
    """管理游戏资源和行为的类。"""

    def __init__(self):
        """初始化游戏并创建游戏资源。"""
        pygame.init()
        self.settings = Settings()

        # 在全屏模式下运行游戏
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height

        # # 在窗口模式下运行游戏
        # self.screen = pygame.display.set_mode(
        #     (self.settings.screen_width, self.settings.screen_height))

        pygame.display.set_caption("Shooting Practice")

        # 创建一个用于存储游戏统计信息的实例。
        self.stats = GameStats(self)
        # 创建记分牌。
        self.sb = Scoreboard(self)

        # 显示飞船、子弹、标靶。
        self.ship = Ship(self)
        self.bullet = Bullet(self)
        self.target = Target(self)
        self.bullets = pygame.sprite.Group()
        self.targets = pygame.sprite.Group()

        # 创建Play按钮。
        self.play_button = PlayButton(self, "Play")
        # 创建游戏难度等级按钮。
        self.easy_button = EasyButton(self, "Easy")
        self.normal_button = NormalButton(self, "Normal")
        self.difficulty_button = DifficultyButton(self, "Difficulty")

    def run_game(self):
        """开始游戏的主循环。"""
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_targets()

            self._create_target()
            self._update_screen()

    def _check_events(self):
        """响应按键和鼠标事件。"""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # self.sb.save_score_record()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
                self._choice_level(mouse_pos)

    def _check_keydown_events(self, event):
        """响应按键。"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_q:
            self.sb.save_score_record()
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_p:
            self._start_game()

    def _check_keyup_events(self, event):
        """响应松开。"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False

    def _check_play_button(self, mouse_pos):
        """在玩家单击Play按钮时开始游戏。"""
        play_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if play_clicked and not self.stats.game_active:
            # 重置游戏统计信息。
            self._start_game()

    def _choice_level(self, mouse_pos):
        """在玩家单击level按钮时选择对应的难度等级。"""
        choice_easy = self.easy_button.rect.collidepoint(mouse_pos)
        if choice_easy and not self.stats.game_active:
            # 选择容易难度等级。
            self._start_game()
            self.settings.easy_level()

        choice_normal = self.normal_button.rect.collidepoint(mouse_pos)
        if choice_normal and not self.stats.game_active:
            # 选择正常难度等级。
            self._start_game()
            self.settings.normal_level()

        choice_difficulty = self.difficulty_button.rect.collidepoint(mouse_pos)
        if choice_difficulty and not self.stats.game_active:
            # 选择困难难度等级。
            self._start_game()
            self.settings.difficulty_level()

    def _start_game(self):
        """开始游戏。"""
        # 重置游戏统计信息
        self.stats.reset_stats()
        self.stats.game_active = True
        pygame.mouse.set_visible(False)
        self.sb.prep_score()
        self.sb.prep_level()
        self.sb.prep_ship()

        # 清空余下的飞船、子弹。
        self.bullets.empty()
        self.targets.empty()

    def _fire_bullet(self):
        """创建一颗子弹，并将其加入编组bullets中。"""
        if len(self.bullets) <= self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """更新子弹的位置，并删除消失的子弹。"""
        # 更新子弹的位置。
        self.bullets.update()

        # 子弹未击中目标时，删除消失的子弹，并记录射失的次数。
        for bullet in self.bullets.copy():
            if bullet.rect.left >= self.settings.screen_width:
                self.bullets.remove(bullet)
                self.stats.shot_missed_allowed -= 1
                self._check_ship_left()

        # 检查是否有子弹击中标靶。
        # 如果是，就删除相应的子弹和标靶。
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.targets, True, True)
        self.stats.killed_targets += len(collisions)
        if collisions:
            for targets in collisions.values():
                self.stats.score += self.settings.target_points * len(targets)

            self.stats.level += 1
            self.sb.prep_score()
            self.sb.check_high_score()
            self.sb.prep_level()
            self.settings.increase_speed()

    def _check_missed_times(self):
        """检查射失次数达到设置要求时，减少飞船，清空子弹、重置飞船等，停止0.5秒。"""
        if not self.stats.shot_missed_allowed:
            self.stats.ship_left -= 1
            self.sb.prep_ship()
            self.ship.center_ship()
            self.bullets.empty()
            self.stats.reset_shot_missed()
            sleep(0.5)

    def _check_ship_left(self):
        """飞船寿命用完，游戏结束。"""
        self._check_missed_times()
        if not self.stats.ship_left:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)
            self.ship.center_ship()

    def _create_target(self):
        """创建一个标靶并将放在屏幕右侧。"""
        if len(self.targets) < self.settings.targets_allowed:
            new_target = Target(self)
            self.targets.add(new_target)

    def _check_target_edges(self):
        """检查标靶到达屏幕边缘后，改变运动方向。"""
        for target in self.targets.sprites():
            if target.check_edges():
                self._change_target_direction()
                break

    def _change_target_direction(self):
        for target in self.targets.sprites():
            target.rect.x -= self.settings.target_speed
        self.settings.target_direction *= -1

    def _update_targets(self):
        """更新标靶的位置。"""
        self.targets.update()
        self._check_target_edges()

    def _update_screen(self):
        """更新屏幕上的图像，并切换到新屏幕。"""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        for target in self.targets.sprites():
            target.draw_target()

        # 显示得分牌。
        self.sb.show_score()

        if not self.stats.game_active:
            self.sb.show_game_over()

        # 如果游戏处于非活动状态，就绘制Play按钮、游戏难度等级按钮、窗口模式按钮。
        if not self.stats.game_active:
            self.play_button.draw_button()

            self.easy_button.draw_button()
            self.normal_button.draw_button()
            self.difficulty_button.draw_button()

        pygame.display.flip()


if __name__ == '__main__':
    # 创建游戏实例并运行游戏。
    ai = ShootingPractice()
    ai.run_game()
