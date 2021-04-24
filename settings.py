class Settings:
    """存储游戏《标靶入侵》中所有设置的类"""

    def __init__(self):
        """初始化游戏的设置。"""
        # 屏幕设置
        self.screen_width = 1200
        self.screen_height = 700
        self.bg_color = (230, 230, 230)

        # 飞船设置
        self.ship_limit = 3

        # 子弹设置
        self.bullet_width = 15
        self.bullet_height = 3
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 5
        self.missed_allowed = 10

        # 标靶设置
        self.target_least = 2
        self.target_killed = 0
        # 设置标靶大小、颜色
        self.target_width = 30
        self.target_height = 150
        self.target_color = (255, 100, 100)
        self.targets_allowed = 1

        # 游戏难度等级设置
        self.easy = 0.25
        self.normal = 1
        self.difficulty = 5

        # 加快游戏节奏的速度
        self.speedup_scale = 1.1
        self.ship_speedup_scale = 1.01
        self.bullet_speedup_scale = 1.02
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """初始化随游戏进行而变化的设置（动态设置）。"""
        self.ship_speed = 1.5
        self.bullet_speed = 3.0
        self.target_speed = 0.25

        # target_direction为1时标靶向上运动，为-1时向下运动。
        self.target_direction = 1

        # 记分
        self.target_points = 50

    def increase_speed(self):
        """提高游戏的速度。"""
        self.ship_speed *= self.ship_speedup_scale
        self.bullet_speed *= self.bullet_speedup_scale
        self.target_speed *= self.speedup_scale

    def easy_level(self):
        """游戏容易等级设置。"""
        self.target_speed *= self.easy

    def normal_level(self):
        """游戏正常等级设置。"""
        self.target_speed *= self.normal

    def difficulty_level(self):
        """游戏困难等级设置。"""
        self.target_speed *= self.difficulty
