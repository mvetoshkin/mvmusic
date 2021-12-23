from mvmusic.common.exceptions import AccessDeniedError
from mvmusic.models.user import User
from . import BaseView
from ..serializers.user import user_serializer


class GetUserView(BaseView):
    def process_request(self, username):
        if not self.current_user.is_admin and \
                self.current_user.username != username:
            raise AccessDeniedError

        user = User.query.get_by(username=username)

        return {
            'user': user_serializer(user)
        }
