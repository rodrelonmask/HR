from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm, ExcelUploadForm, VerificationForm
from .models import Record

def home(request):
    records = Record.objects.all()
    # Check to see if logging in
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # Authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You Have Been Logged In!")
            return redirect('home')
        else:
            messages.error(request, "There Was An Error Logging In, Please Try Again...")
            return redirect('home')
    else:
        return render(request, 'home.html', {'records':records})

def logout_user(request):
    logout(request)
    messages.success(request, "You Have Been Logged Out...")
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        verification_form = VerificationForm(request.POST)
        form = SignUpForm(request.POST)
        if form.is_valid() and verification_form.is_valid():
            verification_id = verification_form.cleaned_data.get('verification_id')
            # Static verification ID
            if verification_id == "HLSHRADMIN":
                form.save()
                # Authenticate and login
                username = form.cleaned_data['username']
                password = form.cleaned_data['password1']
                user = authenticate(username=username, password=password)
                login(request, user)
                messages.success(request, "You Have Successfully Registered! Welcome!")
                return redirect('home')
            else:
                messages.error(request, "Invalid verification ID.")
    else:
        form = SignUpForm()
        verification_form = VerificationForm()
    return render(request, 'register.html', {'form': form, 'verification_form': verification_form})

def employee_record(request, pk):
    if request.user.is_authenticated:
        # Look Up Records
        employee_record = Record.objects.get(id=pk)
        return render(request, 'record.html', {'employee_record':employee_record})
    else:
        messages.error(request, "You Must Be Logged In To View That Page...")
        return redirect('home')

def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_it = Record.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, "Record Deleted Successfully...")
        return redirect('home')
    else:
        messages.error(request, "You Must Be Logged In To Do That...")
        return redirect('home')

def add_record(request):
    form = AddRecordForm(request.POST or None)
    excel_form = ExcelUploadForm(request.POST or None, request.FILES or None)

    if request.user.is_authenticated:
        if request.method == "POST":
            if 'excel_file' in request.FILES:
                if excel_form.is_valid():
                    excel_form.save()
                    messages.success(request, "Excel file uploaded and records added...")
                    return redirect('home')
            elif form.is_valid():
                add_record = form.save()
                messages.success(request, "Record Added...")
                return redirect('home')
        return render(request, 'add_record.html', {'form': form, 'excel_form': excel_form})
    else:
        messages.error(request, "You Must Be Logged In...")
        return redirect('home')

def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request, "Record Has Been Updated!")
            return redirect('home')
        return render(request, 'update_record.html', {'form':form})
    else:
        messages.error(request, "You Must Be Logged In...")
        return redirect('home')

