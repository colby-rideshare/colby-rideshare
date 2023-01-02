from django.urls import path
from .views import RideListView, RideDetailView, RideCreateView, RideUpdateView, RideDeleteView, UserRideListView

urlpatterns = [
    path('', RideListView.as_view(), name='carpool-home'),
    path('user/<str:username>', UserRideListView.as_view(), name='user-rides'),
    path('ride/<int:pk>/', RideDetailView.as_view(), name='ride-detail'),
    path('ride/new/', RideCreateView.as_view(), name='ride-create'),
    path('ride/<int:pk>/update/', RideUpdateView.as_view(), name='ride-update'),
    path('ride/<int:pk>/delete/', RideDeleteView.as_view(), name='ride-delete'),
]