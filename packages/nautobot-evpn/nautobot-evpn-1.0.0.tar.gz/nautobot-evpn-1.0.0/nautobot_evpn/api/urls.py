from nautobot.core.api.routers import OrderedDefaultRouter
from .views import EthernetSegmentsViewSet

router = OrderedDefaultRouter()

router.register("ethernet-segments", EthernetSegmentsViewSet)

app_name = "nautobot_evpn-api"
urlpatterns = router.urls
