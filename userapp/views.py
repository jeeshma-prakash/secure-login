from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import User
import bcrypt


def homepage(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = User.objects.filter(email=email).first()

        if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            print(user)
            request.session['user_id'] = user.id
            request.session['user_role'] = user.role
            messages.success(request, 'Login successful')

            if user.role == 'admin':
                return redirect('admin_dashboard')
            else:
                return redirect('user_dashboard')  # You'll need to create this view and URL
        else:
            messages.error(request, 'Invalid email or password')

    return render(request, 'index.html')




def register(request):
    print('register page')

    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        role = request.POST['role']

        # Encrypt the password using bcrypt
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        user = User(name=name, email=email, password=hashed_password.decode('utf-8'), role=role)
        user.save()
        print(user)

        return redirect(homepage)

    return render(request,'register.html')

def is_admin(user):
    return user.role == 'admin'

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    users = User.objects.all()
    return render(request, 'admin_dashboard.html', {'users': users})

@login_required
@user_passes_test(is_admin)
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.name = request.POST['name']
        user.email = request.POST['email']
        user.role = request.POST['role']
        if request.POST['password']:
            hashed_password = bcrypt.hashpw(request.POST['password'].encode('utf-8'), bcrypt.gensalt())
            user.password = hashed_password.decode('utf-8')
        user.save()
        return redirect('admin_dashboard')
    return render(request, 'edit_user.html', {'user': user})

@login_required
@user_passes_test(is_admin)
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('admin_dashboard')