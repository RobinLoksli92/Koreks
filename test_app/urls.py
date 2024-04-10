from django.urls import path, include
from rest_framework import routers

from .views import get_test, get_tests, TestViewSet, QuestionViewSet, register


router = routers.SimpleRouter()
router.register(r'tests', TestViewSet)
router.register(r'question', QuestionViewSet)


urlpatterns = [
    path('', register, name='auth'),
    path('tests', get_tests, name='tests'),
    path('api/v1/', include(router.urls)),
    path('tests/<int:test_number>/', get_test, name='test'),
]