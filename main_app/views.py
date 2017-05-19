from django.shortcuts import render
from .models import Treasure
from .forms import TreasureForm, LoginForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout

def like_treasure(request):
    treasure_id = request.GET.get('treasure_id', None)

    likes = 0
    if(treasure_id):
        treasure = Treasure.objects.get(id=int(treasure_id))
        if treasure is not None:
            likes = treasure.likes + 1
            treasure.likes = likes
            treasure.save()
            
    return HttpResponse(likes)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            u = form.cleaned_data['username']
            p = form.cleaned_data['password']
            user = authenticate(username = u, password = p)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/')
                else:
                    print('The account has been disabled!')
            else:
                print("The username and password were incorrect.")
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form':form})



# Create your views here.
def index(request):
    # return HttpResponse('<h1>Hello Explorers!</h1>')
    # name = 'Gold Nugget'
    # value = 1000.00
    # context = {'treasure_name':name,'treasure_val': value}
    treasures = Treasure.objects.all()
    #to render form
    form = TreasureForm()
    return render(request, 'index.html', {'treasures':treasures,'form':form})

def profile(request, username):
    user = User.objects.get(username=username)
    treasures = Treasure.objects.filter(user=user)
    return render(request, 'profile.html',{'username':username,'treasures':treasures})

def detail(request, treasure_id):
    treasure = Treasure.objects.get(id=treasure_id)
    return render(request, 'detail.html', {'treasure':treasure})

def post_treasure(request):
    form = TreasureForm(request.POST, request.FILES)
    if form.is_valid():
        treasure = form.save(commit = False)
        treasure.user=request.user
        treasure.save()
        # treasure = Treasure(name = form.cleaned_data['name'],
        # value = form.cleaned_data['value'],
        # material = form.cleaned_data['material'],
        # location = form.cleaned_data['location'],
        # img_url = form.cleaned_data['img_url'])


    return HttpResponseRedirect ('/')


    #checks if form is valid
    #if form is value will create treasure, by looking up attributes in form.clean_data
# def post_treasure(request):
#     form = TreasureForm(request.POST)
#     if form.is_valid():
#         treasure = Treasure(name = form.cleaned_data['name'],
#         value = form.cleaned_data['value'],
#         material = form.cleaned_data['material'],
#         location = form.cleaned_data['location'],
#         img_url = form.cleaned_data['img_url'])
#
#         treasure.save()
#
#     return HttpResponseRedirect('/')
# class Treasure:
#     def __init__(self,name,value,material,location,img_url):
#         self.name = name
#         self.value = value
#         self.material = material
#         self.location = location
#         self.img_url = img_url

treasures = [
    Treasure('Gold Nugget', 500.00, 'gold', "Curly's Creek, NM",'/images/gold-nugget.jpg'),
    Treasure("Fool's Gold", 0, 'pyrite', "Fool's Falls, CO",'/images/pyrite.jpg'),
    Treasure('Coffee Can', 20.00, 'tin', 'Acme, CA','images/coffee-can.jpg')
]
