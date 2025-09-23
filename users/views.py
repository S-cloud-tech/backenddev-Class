from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from django.contrib.auth import login, authenticate
from .forms import UserSignupForm, LibrarianSignupForm, LoginForm

def user_signup(request):
    if request.method == "POST":
        form = UserSignupForm(request.POST)
        if form.is_valid():
            user = form.save()

            # assign to "User" group
            user_group = Group.objects.get(name="User")
            user.groups.add(user_group)

            login(request, user)
            return redirect("library:home")
    else:
        form = UserSignupForm()
    return render(request, "auth/signup.html", {"form": form})


def librarian_signup(request):
    if request.method == "POST":
        form = LibrarianSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()

            # assign to "Librarian" group
            group = Group.objects.get(name="Librarian")
            user.groups.add(group)

            login(request, user)
            return redirect("library:home")
    else:
        form = LibrarianSignupForm()
    return render(request, "auth/signup_librarian.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("library:home")
            else:
                form.add_error(None, "Invalid username or password")
    else:
        form = LoginForm()
    return render(request, "auth/login.html", {"form": form})