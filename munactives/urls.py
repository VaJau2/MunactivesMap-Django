from rest_framework.routers import DefaultRouter
from .views import FoundationViewSet, SprTypeFoundationViewSet, CompanyViewSet, SprTypeCompanyViewSet
from .views import HousingStockViewSet, SprTypeStockViewSet, MunitipallandViewSet
from .views import HolderViewSet

app_name = "munactives"

router = DefaultRouter()
router.register(r'foundation', FoundationViewSet, basename='user')
router.register(r'sprtypefoundation', SprTypeFoundationViewSet, basename='user')
router.register(r'company', CompanyViewSet, basename='user')
router.register(r'sprtypecompany', SprTypeCompanyViewSet, basename='user')
router.register(r'housingstock', HousingStockViewSet, basename='user')
router.register(r'sprtypestock', SprTypeStockViewSet, basename='user')
router.register(r'munitipalland', MunitipallandViewSet, basename='user')
router.register(r'holder', HolderViewSet, basename='user')

urlpatterns = router.urls