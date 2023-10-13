from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .models import Advertisement, Category, Message, User, MessageType
from django.db.models import Q # for filtering purposes in search bar
from .forms import MyUserCreationForm, UserForm, AdvertisementForm, MessageForm
from django.contrib import messages # for messages and alerts
from .helpers import adv_plural_2
import random
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):
    advertisements = Advertisement.objects.all()
    num_all_advertisements = Advertisement.objects.all().count
    q = request.GET.get('q')
    q_category = request.GET.get('q_category')

    if q_category is not None:
        q=q_category    
        advertisements = advertisements.filter(category__name=q)                              
    elif q is not None:
        advertisements = advertisements.filter(
                            Q(category__name__icontains=q) |
                            Q(title__icontains=q) |
                            Q(description__icontains=q) |
                            Q(user__username__icontains=q)
                            )
    else:
        q = ''

    categories = Category.objects.all()[:5]

    advertisement_follower_messages = None
    user_follow_advs = []
    if request.user.is_authenticated:     
        advertisement_follower_messages = Message.objects.filter(advertisement__user = request.user,  type__name = "follow").order_by('-created_at')
        user_follow_advs = Advertisement.objects.filter(message__user = request.user,message__type__name ='follow').values_list("id", flat=True)
   
    context = {
        'advertisements': advertisements.order_by('-updated_at'),
        'num_all_advertisements': num_all_advertisements,
        'categories': categories,
        'activity_column_messages': advertisement_follower_messages,
        'advertisement_count': adv_plural_2 (advertisements.count()),
        'user_follow_advs' : user_follow_advs
    }
    return render(request, 'board/home.html', context)

def categoriesPage(request):
    num_all_advertisements = Advertisement.objects.all().count

    q = request.GET.get('q')
    if q == None:
        q = ''

    categories = Category.objects.filter(name__icontains=q)

    context = {
        'categories': categories,
        'num_all_advertisements': num_all_advertisements,
    }
    return render(request, 'board/categories.html', context)



def activityPage(request):
    advertisement_messages = Message.objects.all()
    context = {
        'advertisement_messages': advertisement_messages
    }
    return render(request, 'board/activity.html', context)

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect ('board_app:home')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        user = None
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request,"Пользователь не существует")
            return redirect ('board_app:login')
        if (user is not None) and (user.confirmation_code != ''):
            return redirect('board_app:confirmation', user_id=user.id)
        
        user = authenticate (request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect ('board_app:home')
        else:
             messages.error(request,"Имя пользователя или пароль неверены")

    context = {'page':page }
    return render (request, 'board/login_register.html', context)


def registerPage(request):
    page = 'register'
    form = MyUserCreationForm()
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False) # to clean up the data and have access to to the user object
            user.username = user.username.lower()
            user.confirmation_code = str(random.randrange(10000,99999))
            send_mail(
                "MessageBoard - код активации",
                "Введите этот код для подтверждения регистрации на MessageBoard: " + user.confirmation_code,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            user.save()
            messages.success(request, 'Пользователь успешно создан')
            messages.info(request, 'Код подтверждения был отправлен на вашу электронную почту')

            return redirect ('board_app:confirmation', user_id=user.id)
        else:
            messages.error(request, 'Произошла ошибка при создании нового пользователя')

    context = {'form':form,   'page':page }
    return render (request, 'board/login_register.html',context)


def confirmationPage(request, user_id):
    page = 'confirmation'
    if request.user.is_authenticated:
        return redirect ('board_app:home')
    user =  User.objects.get(id=user_id)
    if request.method == 'POST':
        confirmation_code = request.POST.get('confirmation_code')
        if user.confirmation_code != confirmation_code:
            messages.error(request,"Неверный код активации")
            return redirect ('board_app:confirmation', user_id = user.id)
            

        if user is not None:
            login(request, user)
            user.confirmation_code = ''
            user.save()
            messages.success(request, "User" + user.email + " has been Activated")
            return redirect ('board_app:home')
        else:
            messages.error(request,"Имя пользователя или пароль неверены")

    context = {'page':page }
    return render (request, 'board/login_register.html', context)



def logoutUser(request):
    logout (request)
    return redirect ('board_app:home')

def advertisement (request, adv_id,  open_chat = 0, chat_user_id = 0):
    adv = Advertisement.objects.get(id=adv_id)
    advertisement_messages = None
    activity_column_messages = None
    activity_column_title = "Отклики"
    
    if request.user.is_authenticated:
        if chat_user_id:
            chat_user = User.objects.get(pk = chat_user_id)
        #shows all advs which have received a request for follow
        activity_column_messages = Message.objects.filter(advertisement=adv, type__name ='follow' ).order_by('-created_at')
        if request.user != adv.user:
            #shows all advs that the user is following
            activity_column_title = "Последние действия"
            
            activity_column_messages =  Message.objects.filter(user = request.user, type__name ='follow').order_by('-created_at')
        
        if open_chat:
            advertisement_messages = Message.objects.filter(Q(advertisement = adv), 
                                                            (Q(user = chat_user) & Q(user_receiver = adv.user))  | 
                                                            (Q(user = adv.user) & Q(user_receiver = chat_user))    
                                                        )
                                                            
        
        if request.method == 'POST':
            messages = Message.objects.create(
                user = request.user,
                user_receiver = chat_user if request.user == adv.user else adv.user,
                advertisement = adv,
                type = MessageType.objects.get(name = "chat"),
                text = request.POST.get('text')
            )
            return redirect('board_app:advertisement', adv.id, open_chat, chat_user_id)

    context = {'advertisement': adv, 
               'advertisement_messages': advertisement_messages, 
               'activity_column_messages': activity_column_messages,
               'activity_column_title': activity_column_title,
               'open_chat': open_chat
    }
    return render(request, 'board/advertisement.html',context)

@login_required (login_url='board_app:login')
def createAdvertisement(request):
    form = AdvertisementForm()
    categories = Category.objects.all()

    if request.method == 'POST':
        category_name = request.POST.get('category')
        category, create = Category.objects.get_or_create (name=category_name)
        form = AdvertisementForm(request.POST, request.FILES)
        if form.is_valid():
            new_adv = form.save(commit=False)
            new_adv.category = category
            new_adv.user = request.user
            new_adv.save()
            messages.success(request, "Вы успешно создали объявление: " + new_adv.title)
            return redirect('board_app:home')
        else:
            messages.error(request,"Введены неверные данные при попытке создания объявления ")

    context = { 'form':form,
                'categories': categories
    }
    return render (request, 'board/advertisement_form.html', context)

@login_required (login_url='board_app:login')
def updateAdvertisement (request, adv_id):
    adv = Advertisement.objects.get(id=adv_id)
    form = AdvertisementForm (instance=adv)
    categories = Category.objects.all()
    if request.user != adv.user:
        messages.error(request,"У Вас нет прав для редактирования этого объявления")
        return redirect('board_app:advertisement',adv_id=adv.id)

    if request.method == 'POST':
        category_name = request.POST.get('category')
        category, create = Category.objects.get_or_create (name=category_name)
        form = AdvertisementForm(request.POST, request.FILES, instance=adv)
        if form.is_valid():
            adv = form.save(commit=False)
            adv.category = category
            adv.user = request.user
            adv.save()
            messages.success(request, "Вы успешно отредактировали объявление: " + adv.title)
            return redirect('board_app:home')
        else:
            messages.error(request,"Введены неверные данные при попытке редактирования объявления ")
            
    context = { 'form':form,
                'categories':categories,
                'advertisement': adv,
    }
    return render (request, 'board/advertisement_form.html',context)

@login_required (login_url='board_app:login')
def deleteAdv(request, adv_id):
    adv = Advertisement.objects.get(id=adv_id)
    if request.user != adv.user:
        messages.error(request,"У Вас нет прав удалить это объявление")
        return redirect('board_app:advertisement',adv_id=adv.id)
    
    if request.method == 'POST':
        title = adv.title
        adv.delete()
        messages.success(request, "Вы успешно удалили объявление: " + title)
        return redirect('board_app:home')
    return render (request, 'board/delete.html',{'obj':adv})

@login_required (login_url='board_app:login')
def follow(request, adv_id):
    form = MessageForm()
    adv = Advertisement.objects.get(id=adv_id)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        sender_user = User.objects.get(id=request.user.id)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.user = sender_user
            msg.user_receiver = adv.user
            msg.advertisement = adv
            msg.type = MessageType.objects.get(name="follow")
            msg.save()
            if  adv.user != sender_user:
                send_mail(
                    "MessageBoard - Follow Notification",
                    "User " + sender_user.email + " откликнулся на ваше объявление: " +  msg.advertisement.title,
                    settings.DEFAULT_FROM_EMAIL,
                    [adv.user.email],
                    fail_silently=False,
                )
                
                messages.success(request, "Вы успешно откликнулись на объявление: " + adv.title)
            
            return redirect('board_app:home')
            
    context = { 'form':form,
                'adv_title': adv.title,
    }
    return render (request, 'board/follow_form.html', context)

@login_required(login_url='board_app:login')
def acceptFollow(request, msg_id):
    msg = Message.objects.get(id=msg_id)
    if request.user != msg.user and request.user != msg.advertisement.user:
        messages.error(request,"У Вас нет прав принимать отклик ")
        return redirect('board_app:home')
    
    if request.method == 'POST':
        msg.accepted = True
        msg.save()
        if msg.type.name == "follow":
            send_mail(
                "MessageBoard - Отклик принят",
                "Отклик на объявление: «" + msg.text + "» принят пользователем  " + request.user.email,
                settings.DEFAULT_FROM_EMAIL,
                [msg.user.email],
                fail_silently=False,
            )
        messages.success(request, "Вы успешно приняли Отклик: «" + msg.text + "»")
        
    return redirect('board_app:home')
    
   

@login_required (login_url='board_app:login')
def deleteMessage(request, msg_id):
    msg = Message.objects.get(id=msg_id)
    msg_type_str = "отклик" if msg.type.name=="follow" else "сообщение"
    if request.user != msg.user and request.user != msg.advertisement.user:
        messages.error(request,"У Вас нет прав удалить " + msg_type_str)
        return redirect('board_app:home')
    
    if request.method == 'POST':
        if msg.type.name == "follow":
            adv = msg.advertisement
            messages_to_delete = Message.objects.filter(Q(advertisement = adv), 
                                                (Q(user = msg.user) & Q(user_receiver = msg.user_receiver))  | 
                                                (Q(user = msg.user_receiver) & Q(user_receiver = msg.user))    
                                            )
            messages_to_delete.delete()
            send_mail(
                "MessageBoard - Отклик отклонен",
                "Отклик на объявление: «" + msg.text + "» отклонен пользователем  " + request.user.email,
                settings.DEFAULT_FROM_EMAIL,
                [msg.user.email, msg.user_receiver.email],
                fail_silently=False,
            )
        elif msg.type.name == "chat":
            msg.delete()
            return redirect('board_app:advertisement', adv_id = msg.advertisement.id, open_chat=1, chat_user_id=msg.user_receiver.id if request.user== msg.user else msg.user.id)

        messages.success(request, "Вы успешно удалили " + msg_type_str +": «" + msg.text + "»")
        return redirect('board_app:home')
    return render (request, 'board/delete.html', {'obj': msg})

def userProfile(request, user_id):
    user = User.objects.get(id=user_id)
    advs = Advertisement.objects.filter(user=user)
    categories = Category.objects.all()
    num_all_advs = Advertisement.objects.all().count()
    advertisement_follower_messages = None
    if request.user.is_authenticated:     
        advertisement_follower_messages = Message.objects.filter(advertisement__user = request.user, type__name = "follow" ).order_by('-created_at')
    context =  {'user': user, 
                'advertisements': advs, 
                'activity_column_messages': advertisement_follower_messages,
                'categories':categories,
                'num_all_advertisements':num_all_advs}
    return render(request, 'board/profile.html', context)
