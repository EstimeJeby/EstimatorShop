from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from .forms import createUserForm,UserUpdateForm,ProfileUpdateForm
# from django.contrib.auth.models import User

def register(request):
    form =createUserForm()
    if request.method== 'POST':
        
         form = createUserForm(request.POST)
         if form.is_valid():
             form.save()
             messages.success(request, f'Your account has been created! You are now able to log in')
             return redirect('login')
         else:
             messages.info(request, f'Your password must contain at least 8 characters.')
        
    context={'form': form}
        # username=request.POST.get('username')
        # email=request.POST.get('email')
        # pass1=request.POST.get('pass1')
        # pass2=request.POST.get('pass2')
    
        # if pass1 != pass2 :
        #      messages.info(request, f'your first and second password are different')
        # else :
        #     my_user = User.objects.create_user(username,email,pass1)
        #     my_user.save()
        #     messages.success(request, f'Your account has been created! You are now able to log in')
        #     return redirect('login')
    
    return render(request, 'users/register.html',context)


def login_1(request):
    if request.method== 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        # print(username,password)
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request, f' User connect succesfully !!')
            return redirect('blog-home')
        else:
            messages.info(request, f'Found a such error please try again')
        
    return render(request, 'users/login.html')

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)


