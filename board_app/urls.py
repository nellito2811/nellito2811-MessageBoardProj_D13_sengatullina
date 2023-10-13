from django.urls import path
from . import views

app_name = 'board_app'
urlpatterns = [
    path ('', views.home, name='home'),
    path ('categories/', views.categoriesPage, name='categories'),
    path ('login/', views.loginPage, name='login'),
    path ('logout/', views.logoutUser, name='logout'),
    path ('activity/', views.activityPage, name='activity'),
    path ('register', views.registerPage, name='register'),
    path ('user-profile/<int:user_id>', views.userProfile, name='user-profile'),
    path ('confirmation/<int:user_id>', views.confirmationPage, name='confirmation'),
    path ('advertisement/<int:adv_id>/<int:open_chat>/<int:chat_user_id>', views.advertisement, name='advertisement'),
    path ('create-adv/', views.createAdvertisement, name='create-adv'),
    path ('update-adv/<int:adv_id>', views.updateAdvertisement, name='update-adv'),
    path ('delete-adv/<int:adv_id>', views.deleteAdv, name='delete-adv'),
    
    path ('follow/<int:adv_id>', views.follow, name='follow'),
    path ('accept-follow/<int:msg_id>', views.acceptFollow, name='accept-follow'),
    path ('delete-message/<int:msg_id>', views.deleteMessage, name='delete-message'),

]