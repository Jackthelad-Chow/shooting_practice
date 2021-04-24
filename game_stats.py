import json


class GameStats:
    """跟踪游戏的统计信息。"""

    def __init__(self, ai_game):
        """初始化统计信息。"""
        self.settings = ai_game.settings
        self.reset_stats()
        # 刚启动游戏时处于活动状态。
        self.game_active = False
        # 任何情况下都不应该重置最高得分。
        self.high_score = 0
        self.load_score_record()

    def reset_stats(self):
        """初始化在游戏运行期间可能变化的统计信息。"""
        self.killed_targets = self.settings.target_killed
        self.shot_missed_allowed = self.settings.missed_allowed
        self.settings.initialize_dynamic_settings()

        self.score = 0
        self.level = 0
        self.ship_left = self.settings.ship_limit

    def reset_shot_missed(self):
        self.shot_missed_allowed = self.settings.missed_allowed

    def load_score_record(self):
        """读取最高得分。"""
        score_record = "record.json"
        try:
            with open(score_record) as s_r:
                self.high_score = json.load(s_r)
        except FileNotFoundError:
            message = "The first time you start the game, no highest score is recorded."
            print(message)

