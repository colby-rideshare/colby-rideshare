from django.urls import path
from .views import landing_page, RideListView, RideCreateView, RideUpdateView, RideDeleteView, RideSignUpView, UserRideListView, RideRequestView, RideDeclineView, RideInfoView

urlpatterns = [
    path('', landing_page, name='landing-page'),
    path('rides/', RideListView.as_view(), name='carpool-home'),
    path('user/<str:username>/rides/', UserRideListView.as_view(), name='my-rides'),
    path('ride/new/', RideCreateView.as_view(), name='ride-create'),
    path('ride/<int:pk>/update/', RideUpdateView.as_view(), name='ride-update'),
    path('ride/<int:ride_pk>/signup/', RideSignUpView.as_view(), name='ride-signup'),
    path('ride/<int:pk>/delete/', RideDeleteView.as_view(), name='ride-delete'),
    path('ride/<int:ride_pk>/request/<int:pk>/', RideRequestView.as_view(), name='ride-request'),
    path('ride/<int:ride_pk>/request/<int:pk>/decline', RideDeclineView.as_view(), name='decline-ride'),
    path('ride/<int:pk>/info', RideInfoView.as_view(), name='ride-info'),
]