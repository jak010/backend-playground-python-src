from src.service import RankingService

import random
import time
import datetime


class LeaderBoardProducer:
    serivce = RankingService()

    def execute(self):
        while True:
            time.sleep(0.5)
            print(f"[*]Logger LEADER BOARD RANK CHANGE...{datetime.datetime.now()}")
            user_id = random.randint(0, 50)
            score = random.randint(0, 100_00)

            self.serivce.set_score(
                user_id=user_id,
                score=score
            )
