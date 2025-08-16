from django.urls import path
from .views import RecommendationListView, RecommendationActionView

urlpatterns = [
    path("recommendations/", RecommendationListView.as_view(), name="ai-recommendations-list"),
    path("recommendations/<int:rec_id>/<str:action>/", RecommendationActionView.as_view(), name="ai-recommendation-action"),
]
