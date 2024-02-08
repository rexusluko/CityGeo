from rest_framework.routers import DefaultRouter
from .views import CityViewSet

router = DefaultRouter()
router.register(r'cities', CityViewSet)
#router.register(r'users/favorite-airports', FavoriteAirportsViewSet)