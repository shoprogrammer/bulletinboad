from django.contrib import admin
from django.urls import path,include
from .views import (createboard,listboard,detailboard,updateboard,
                    deleteboard,my_boards,comment_create,comment_delete,
                    board_search,board_sort,add_favorite,remove_favorite,contact,contact_success)
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('boardlist/',listboard,name='board-list'),
    path('boardcreate/',login_required(createboard),name='board-create'),
    path('boarddetail/<int:pk>/',login_required(detailboard),name="board-detail"),
    path('boardupdate/<int:pk>/',login_required(updateboard),name="board-update"),
    path('boarddelete/<int:pk>/',login_required(deleteboard),name="board-delete"),

    #commentに対する処理
    path('comment/<int:pk>/',login_required(comment_create),name="comment_create"),
    path('comment/<int:board_pk>/delete/<int:comment_pk>/',login_required(comment_delete),name="comment_delete"),

    path('my_boards/',login_required(my_boards),name="my_boards"),
    path('serch/',board_search,name='search'),
    path('sort/',board_sort,name='sort'),
    path('add_favorite/',add_favorite,name='add_favorite'),
    path('remove_favorite/',remove_favorite,name='remove_favorite'),
    path('contact/',contact,name='contact'),
    path('contact/success/',contact_success,name='contact_success'),

]
