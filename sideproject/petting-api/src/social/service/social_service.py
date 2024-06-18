from src.social.enums import SocialInviteRequestStatus

from src.social.entity import SocialEntity


class SocialService:

    def invite(self, sender, receiver):
        return SocialEntity.new(
            sender=sender,
            receiver=receiver,
            status=SocialInviteRequestStatus.WAIT.value
        )
