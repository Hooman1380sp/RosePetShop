from rest_framework.generics import ListAPIView


from accounts.models import User
from .serializers import UserScoreSerializer


class UserScoreListView(ListAPIView):
    serializer_class = UserScoreSerializer
    model = User
    queryset = User.get_user_by_score