
from django.urls import path
from .views import *

urlpatterns = [
    path( '',  IndexView.as_view()  ),
    path( 'testing',  TestingView.as_view()  ),
    path( 'result',  ResultView.as_view()  ),
    path( 'initial',  InitialView.as_view()  )
]
