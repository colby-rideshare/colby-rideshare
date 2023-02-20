from django.urls import path
from .views import landing_page, RideListView, RideDetailView, RideCreateView, RideUpdateView, RideDeleteView, RideSignUpView

urlpatterns = [
    path('', landing_page, name='landing-page'),
    path('rides/', RideListView.as_view(), name='carpool-home'),
    path('ride/<int:pk>/', RideDetailView.as_view(), name='ride-detail'),
    path('ride/new/', RideCreateView.as_view(), name='ride-create'),
    path('ride/<int:pk>/update/', RideUpdateView.as_view(), name='ride-update'),
    path('ride/<int:pk>/signup/', RideSignUpView.as_view(), name='ride-signup'),
    path('ride/<int:pk>/delete/', RideDeleteView.as_view(), name='ride-delete'),
]