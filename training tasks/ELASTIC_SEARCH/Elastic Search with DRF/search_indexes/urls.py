from rest_framework.routers import DefaultRouter
from django.urls import path
from django.conf.urls import include
from search_indexes.viewsets.book import BookDocumentView

router = DefaultRouter()
books = router.register(
    r'books',
    BookDocumentView,
    basename='bookdocument'
)

urlpatterns = [
    path('', include(router.urls)),
]
