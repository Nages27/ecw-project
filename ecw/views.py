
from django.shortcuts import render,redirect
from .models import CustomerData
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.http import HttpResponse
from .models import CartItem, Order
from .models import CustomerData, Cart



def home(request):
    return render(request,'ecw/home.html')

def signup(request):
    if request.method=="POST":
        
        name=request.POST.get('name')
        email=request.POST.get('email')
        password=request.POST.get('password')
    
        if CustomerData.objects.filter(email=email).exists():
            return render(request,'ecw/signup.html',{"error_message":"Email already exists"})
        else:
            CustomerData.objects.create(
            name=name,
            email=email, 
            password=make_password(password)
              )
            return redirect('dashboard')
    else:
        return render(request,'ecw/signup.html')

def profile(request):
    user_id = request.session.get('user_id')
    user = CustomerData.objects.get(id=user_id)
    if not user_id:
        return redirect('login')
    return render(request, 'ecw/profile.html', {
        'user': user
    })

def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = CustomerData.objects.filter(email=email).first()

        if not user:
            return render(request, 'ecw/login.html', {
                "error_message": "User does not exist"
            })

        if check_password(password, user.password):
            request.session['user_id'] = user.id
            request.session.modified = True  
            return redirect('dashboard')

        return render(request, 'ecw/login.html', {
            "error_message": "Incorrect password"
        })

    return render(request, 'ecw/login.html')




def dashboard(request):
    return render(request,'ecw/dashboard.html')


def electronics(request):
      products = [
        {   
            'id':1,
            'name': 'Samsung TV',
            'image': 'ecw/images/tv.jpg'
        },
        {     
            'id':2,
            'name': 'Headphones',
            'image': 'ecw/images/headphones.webp'
        },
        {    
            'id':3,
            'name': 'iPhone 14',
            'image': 'ecw/images/mobile.jpg'
        }
    ]
      return render(request,'ecw/electronics.html',{'products':products})




def view(request, id):
    products= {
        1: {
            'id':1,
            'name': 'Samsung TV',
            'description' : 'Enjoy stunning picture quality with vibrant colors and crystal-clear visuals on this Samsung Smart LED TV. With smart features and seamless connectivity, it offers an immersive entertainment experience for movies, shows, and games right at home.',
            'price': '₹45,000',
            'quantity' : 2,
            'image': 'ecw/images/tv.jpg'
        },
        2: {
             'id':2,
            'name': 'Headphones',
            'description' : 'Experience powerful sound with deep bass and clear vocals using these wireless Bluetooth headphones. Designed for comfort and long listening hours, they are perfect for music, calls, and everyday use.',
            'price': '₹5,000',
              'quantity' : 3,
            'image': 'ecw/images/headphones.webp'
        },
        3: {
             'id':3,
            'name': 'iPhone 14',
            'description' :'The iPhone delivers a powerful performance with its advanced processor, stunning display, and high-quality camera. Designed for speed, security, and a smooth user experience, it’s perfect for everyday use and creativity.',
            'price': '₹1,20,000',
              'quantity' : 5,
            'image': 'ecw/images/mobile.jpg'
        }
    }

    product = products.get(id)
    return render(request, 'ecw/electronics_details.html', {'product': product})

def add_to_cart(request, id):
    cart = request.session.get('cart', [])

    cart.append(id)

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('view_cart')


def view_cart(request):
    cart_ids = request.session.get('cart', [])

    products = {
        1: {
            'id': 1,
            'name': 'Samsung TV',
            'price': 45000,
            'quantity' : 2,
            'image': 'ecw/images/tv.jpg',
            'description' : 'Enjoy stunning picture quality with vibrant colors and crystal-clear visuals on this Samsung Smart LED TV. With smart features and seamless connectivity, it offers an immersive entertainment experience for movies, shows, and games right at home.'
        },
        2: {
            'id': 2,
            'name': 'Headphones',
            'price': 5000,
            'image': 'ecw/images/headphones.webp',
              'quantity' : 3,
            'description' : 'Experience powerful sound with deep bass and clear vocals using these wireless Bluetooth headphones. Designed for comfort and long listening hours, they are perfect for music, calls, and everyday use.'
        },
        3: {
            'id': 3,
            'name': 'iPhone 14',
            'price': 120000,
              'quantity' : 5,
            'image': 'ecw/images/mobile.jpg',
            'description' :'The iPhone delivers a powerful performance with its advanced processor, stunning display, and high-quality camera. Designed for speed, security, and a smooth user experience, it’s perfect for everyday use and creativity.'
        }
    }

    cart_items = []

    for pid in cart_ids:
        product = products.get(int(pid))
        if product:
            cart_items.append(product)

    return render(request, 'ecw/view_cart.html', {'cart': cart_items})



def logout(request):
    request.session.flush()
    return redirect('home')

def place_order(request, item_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    try:
        user = CustomerData.objects.get(id=user_id)
    except CustomerData.DoesNotExist:
        request.session.flush()
        return redirect('login')

    products = {
        1: {'name': 'Samsung TV', 'description': '4K Smart TV', 'price': 45000},
        2: {'name': 'Headphones', 'description': 'Noise cancelling', 'price': 5000},
        3: {'name': 'iPhone 14', 'description': 'Super Retina Display', 'price': 120000},
    }

    product = products.get(item_id)
    if not product:
        return redirect('electronics') 

    Order.objects.create(
        user=user,
        product_name=product['name'],
        product_description=product['description'],
        price=product['price'],
        quantity=1,
        status="Pending"
    )

    return redirect('order_success')



def order_success(request):
    return render(request, 'ecw/order_success.html')

def my_orders(request):
    user_id = request.session.get('user_id')
    user = CustomerData.objects.get(id=user_id)
    orders = Order.objects.filter(user=user)

    return render(request, 'ecw/my_orders.html', {'orders': orders})

def order(request,id):
    products= {
        1: {
            'id':1,
            'name': 'Samsung TV',
            'description' : 'Enjoy stunning picture quality with vibrant colors and crystal-clear visuals on this Samsung Smart LED TV. With smart features and seamless connectivity, it offers an immersive entertainment experience for movies, shows, and games right at home.',
            'price': '₹45,000',
            'quantity' : 2,
            'image': 'ecw/images/tv.jpg'
        },
        2: {
             'id':2,
            'name': 'Headphones',
            'description' : 'Experience powerful sound with deep bass and clear vocals using these wireless Bluetooth headphones. Designed for comfort and long listening hours, they are perfect for music, calls, and everyday use.',
            'price': '₹5,000',
             'quantity' : 3,
            'image': 'ecw/images/headphones.webp'
        },
        3: {
             'id':3,
            'name': 'iPhone 14',
            'description' :'The iPhone delivers a powerful performance with its advanced processor, stunning display, and high-quality camera. Designed for speed, security, and a smooth user experience, it’s perfect for everyday use and creativity.',
            'price': '₹1,20,000',
             'quantity' : 5,
            'image': 'ecw/images/mobile.jpg'
        }
    }
    product = products.get(id)
    return render(request, 'ecw/order_view.html', {'product': product})