from django.shortcuts import render
from .models import Task
from django.shortcuts import redirect
import requests
from django.http import JsonResponse
from curd_opp import settings
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q


#! REGISTER FUNCTION
def register(request):
    if request.method=="POST":
        first_name=request.POST.get('first_name','').strip()
        last_name=request.POST.get('last_name','').strip()
        username=request.POST.get('username','').strip()
        email=request.POST.get('email','').strip()
        password1=request.POST.get('password1','').strip()
        password2=request.POST.get('password2','').strip()
        
        user=User.objects.filter(username=username)
        if user.exists():
            messages.error(request, "Username already taken")
            return redirect('/register/')
        
        if password1!=password2:
           messages.warning(request, "Password do not match")
           return redirect('/register/')
        else:
            user=User.objects.create(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
            )
            user.set_password(password2)
            user.save()
            messages.success(request, "Profile created successfully")
        
    return render(request, "register.html")


#! LOGIN FUNCTION
def login_page(request):
    if request.method=="POST":
        username=request.POST.get("username","").strip()
        password=request.POST.get("password","").strip()
        
        user=User.objects.filter(username=username)
        
        if user.exists():            
            user_login=authenticate(username=username,password=password)
            if user_login is not None:
                login(request,user_login)
                return redirect("home")
            else:
                messages.warning(request, "Password is incorrect")
                return redirect("/login/")
        
        else:
            messages.warning(request, "Username is incorrect")
            return redirect("/login/")
        
    return render(request,"login.html")



#! LOGOUT FUNCTION
def  logout_page(request):
    logout(request)
    return redirect('/login/')



#! READ FUNCTION
@login_required(login_url="/login/")
def view_tasks(request):
    #?sorting the tasks
    sort_tasks=request.GET.get('sort',"-priority")
    tasks = Task.objects.filter(
        user=request.user
    ).filter(
        Q(status="pending") | Q(status="in_progress")
    ).order_by(sort_tasks)
    return render(request,'index.html',{'tasks':tasks,'sort_tasks':sort_tasks})



#! ADD FUNCTION
@login_required(login_url="/login/")
def add_task(request):
    if request.method=="POST":
        print("Form submitted")
        title=request.POST.get('title','').strip()
        desc=request.POST.get('desc','').strip()
        priority=request.POST.get('priority')
        status=request.POST.get('status')
        Task.objects.create(
            user=request.user,
            title=title,
            description=desc,
            priority=priority,
            status=status
        )
        return redirect("home")
    return redirect('home')



#! DELETE FUNCTION
@login_required(login_url="/login/")
def delete_task(request,id):
    if request.method=="POST":
        task=Task.objects.get(id=id,user=request.user)
        if task:
            task.delete()
            return redirect('home')
        else:
            messages.warning(request, "Task not found")
            return redirect('home')
    return redirect('home')

def delete_all_tasks(request):
    Task.objects.filter(user=request.user).delete()
    return redirect('home')



#! EDIT FUNCTION
@login_required(login_url="/login/")
def edit_task(request,id):
    task=Task.objects.get(id=id,user=request.user)
    if request.method=="POST":
        print("Form updated")
        task.title=request.POST.get('title','').strip()
        task.description=request.POST.get('desc','').strip()
        task.priority=request.POST.get('priority')
        task.status=request.POST.get('status')
        task.updated_at=timezone.now()

        task.save()
        return redirect('home')
    return redirect("home")
    
    
#! HISTORY FUNCTION
@login_required(login_url="/login/")
def history_tasks(request):
    tasks=Task.objects.filter(user=request.user,status="completed").order_by("-created_at")
    return render(request,"history.html",{'tasks':tasks})


#! THIS IS THE AI GENERATED DESCRIPTION FUNCTION 
@login_required(login_url="/login/")
def generate_description(request):
    if request.method == "POST" and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        title = request.POST.get('title', '')
        
        try:
            # Use the Ollama API to generate a response
            response = requests.post(
                f"{settings.OLLAMA_HOST}api/generate",
                json={
                    "model": "gemma3:1b",
                    "prompt": f"Give me a 2-word description of '{title}'. Provide a concise answer followed by a brief explanation for a todo list.",
                    "stream": False
                }
            )
            
            response_data = response.json()
            ai_response = response_data.get('response', '')
            

            explanation = ""
            if "Explanation:" in ai_response:
                explanation = ai_response.split("Explanation:")[1].strip()
            elif "**Explanation:**" in ai_response:
                explanation = ai_response.split("**Explanation:**")[1].strip()
            
            return JsonResponse({'description': explanation})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

