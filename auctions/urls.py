from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('create_listing',views.new_listing, name='create_listing'),
    path("listing/<int:id>", views.listing, name='listing'),
    path('listing/<int:id>/watchlist_manager',views.watchlist_manager, name='watchlist'),
    path('listing/<int:user_id>/watchlist', views.watchlist_page, name='watchlist_page'),
    path('categories', views.categories, name='categories'),
    path('categories/<int:category_id>', views.category, name="category"),
    path('comment/<int:id>', views.comment, name="comment"),
    path('bid/<int:id>', views.bid, name="bid"),
    path('close/<int:id>', views.close, name="close"),
]
