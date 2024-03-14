from typing import List

from src.utils import RedisClient


class RankingService:
    LEADER_BOARD_KEY = "leaderboard"

    redis_client = RedisClient()

    def set_score(self, user_id: str, score: int) -> bool:
        self.redis_client.client.zadd(
            self.LEADER_BOARD_KEY,
            {
                user_id: score
            }
        )
        return True

    def get_user_ranking(self, user_id: str) -> int:
        ranks = self.redis_client.client.zrevrank(self.LEADER_BOARD_KEY, user_id)

        return ranks

    def get_toprank(self, limit: int) -> List[str]:
        rankers = self.redis_client.client.zrevrange(self.LEADER_BOARD_KEY, start=0, end=limit - 1)
        return list(rankers)
