from django.shortcuts import render,redirect
from datetime import datetime
from django.http import HttpResponse
from food.models import CreateContact,item,my_cart,address
from django.contrib.auth.models import User,auth
from django.contrib.auth import logout,authenticate,login
from django.contrib import messages
from django.core.mail import EmailMessage
from django.core.mail import send_mail, BadHeaderError
# Create your views here.
added=[]
unadded=[
 'Strawberry Milkshake','Egg Fried Rice','Paneer','Roti','Maggi','Cake','Chicken Momo','Samosa','Sandwich','Tandoori Chicken','Pasta','Noodles','Veg Pizza',
 'Chicken Pizza','Chicken Burger','Chicken Biryani',
 ]

def Index(request):
    global added
    global unadded
    if(not request.user.is_anonymous):
        context = {'items': item.objects.filter(name__in=unadded),'user':request.user,'cart':my_cart.objects.filter(user=request.user)}
        return render(request,'index.html',context)
    else:
        messages.info(request, "Invalid Username or Password")
        return redirect('/loginUser')
def delet(request):
    global added
    global unadded
    if request.method == 'POST':
            added_item = request.POST['del']
            a = my_cart.objects.get(pk=int(added_item))
            if(my_cart.objects.filter(user=request.user,name=a.name).exists()):
                x=my_cart.objects.get(user=request.user,name=a.name)
                x.totalprice=x.totalprice-x.price
                x.number=x.number-1
                x.save()
                if(x.number==0):
                    print(x.name,added,unadded)
                    added.remove(a.name)
                    unadded.append(a.name)
                    messages.info(request,x.name+" removed from your cart")
                    my_cart.objects.filter(name=a.name,user=request.user).delete()
                else:
                    messages.info(request,x.name+"x"+str(x.number)+"in your cart")
    return redirect('/')
def add(request):
    global added
    global unadded
    if request.method == 'POST':
            added_item = request.POST['id']
            a = item.objects.get(pk=int(added_item))
            if(my_cart.objects.filter(user=request.user,name=a.name).exists()):
                x=my_cart.objects.get(user=request.user,name=a.name)
                x.number=x.number+1
                x.totalprice=x.totalprice+x.price
                x.save()
                
                messages.info(request,x.name+"x"+str(x.number)+"in your cart")
            else:
                new = my_cart(name = a.name, price = a.price,image = a.image, user=request.user,number=1,totalprice=a.price)
                added.append(a.name)
                unadded.remove(a.name)
                print(new.name,added,unadded)
                new.save()
                print(added,unadded)
    return redirect('/')
def addx(request):
    global added
    global unadded
    if request.method == 'POST':
            added_item = request.POST['id']
            a = my_cart.objects.get(pk=int(added_item))
            if(my_cart.objects.filter(user=request.user,name=a.name).exists()):
                x=my_cart.objects.get(user=request.user,name=a.name)
                x.number=x.number+1
                x.totalprice=x.totalprice+x.price
                x.save()
                
                messages.info(request,x.name+"x"+str(x.number)+"in your cart")
            else:
                new = my_cart(name = a.name, price = a.price,image = a.image, user=request.user,number=1,totalprice=a.price)
                added.append(a.name)
                unadded.remove(a.name)
                print(new.name,added,unadded)
                new.save()
                print(added,unadded)
    return redirect('/')
def home(request):
    return render(request,'about.html')

def loginUser(request):
    if request.method=="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)

        # check if user has entered correct credentials
        user = authenticate(username=username, password=password)

        if user is not None:
            # A backend authenticated the credentials
            login(request, user)
            
            if request.user.is_anonymous:
                messages.info(request, 'No such user exits')
                return redirect("/loginUser")
            else:
                
                return redirect('/')
            

        else:
            messages.info(request, 'No such user exits')
            return render(request, 'login.html')

    return render(request, 'login.html')
    

def logoutUser(request):
    logout(request)
    return redirect("/loginUser")
def register(request):
    global username
    if request.method == "POST":
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        email = request.POST.get('email')
        password2 = request.POST.get('password2')
        if(password1==password2):
            if(User.objects.filter(username=username).exists()):
                print('Username')
                messages.success(request, 'There exists an account with this username!')
            elif(User.objects.filter(email=email).exists()):
                print('email')
                messages.success(request, 'There exists an account with this email account!')   
            else:
                user=User.objects.create_user(username=username,password=password1,email=email)
                user.save()
                return redirect("/loginUser")
        else:
            messages.info(request,'Passwords donot match')
            print("passwords donot match")
        return render(request,'register.html')   
    return render(request,'register.html')
     
def payment(request):
    if request.user.is_anonymous:
        return redirect('/')
    items = set(my_cart.objects.filter(user=request.user))
    flag = True
    num=0
    sum = 0 
    for i in items:
        sum += i.price*i.number
    for i in items:
        num += i.number
    context = {
        'items': items,
        'sum':sum,
        'num':num,
    }
    if address.objects.filter(user=request.user).exists():
        context = {
        'items': items,
        'sum':sum,
        'num':num,
        'address':address.objects.filter(user=request.user)
    }
    return render(request,'payment.html',context)    
def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        desc = request.POST.get('desc')
        contact = CreateContact(name=name, email=email, phone=phone, desc=desc, date = datetime.today())
        contact.save()
        subject="Response from Contact Sheet"
        if(len(phone)==10):
            try:
                send_mail(subject, desc, email, ['mohithpokala@gmail.com'])
                messages.info(request, "Thank you for contacting us")
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
                messages.info(request, "Invalid Email Id")
        else:
            messages.info(request, "Invalid Phone Number")
    return render(request, 'contact.html') 
def dell(request):
    items = my_cart.objects.filter(user=request.user)
    items.delete()
    return redirect('/')
def addres(request):
    items = my_cart.objects.filter(user=request.user)

    flag = True
    num=0
    sum = 0 
    for i in items:
        sum += i.price*i.number
    for i in items:
        num += i.number
    if request.method == "POST":
        try:
            if not address.objects.filter(pk=request.POST['old']).exists():
                street = request.POST['street']
                city = request.POST['city']
                house = request.POST['house']
                pincode = request.POST['pincode']
                phone = request.POST['phone']
                name = request.POST['name']
                new = address(street=street,city=city,house=house,name=name,pincode=pincode,phone=phone,user=request.user)
                new.save()
                return redirect
            else:
                new=address.objects.filter(user=request.user,pk=request.POST['old'])
        except:
            street = request.POST['street']
            city = request.POST['city']
            house = request.POST['house']
            pincode = request.POST['pincode']
            phone = request.POST['phone']
            name = request.POST['name']
            new = address(street=street,city=city,house=house,name=name,pincode=pincode,phone=phone,user=request.user)
            new.save()
        context = {
            'items': items,
            'sum':sum,
            'num':num,
            'address':new,
            'date':datetime.now()
        }
        
        messages.info(request, "Order successfully placed :)")
        return render(request,'cart.html',context)   
    return redirect('/')


     

