from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User, auth
import os
from django.shortcuts import get_object_or_404
from django.db.models import Sum
import datetime

from .models import Contest, Problem, Profile, ProblemSolved



def admin(request):
	return render(request,'admin')


def home(request):

    if request.method == 'POST':
        if request.POST.get("signin"):
            return render(request, 'signin.html')
        elif request.POST.get("signup"):
            return render(request, 'signup.html')
    else:
        return render(request, 'home.html')


def user_home(request):
    return render(request, 'user_home.html')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('user_home')
        else:
            messages.error(request, 'Invalid Credentials')
            return render(request, 'signin.html')
    else:
        return render(request, 'signin.html')


def logout(request):
    auth.logout(request)
    return redirect('/')


def register(request):
	return render(request, 'signup.html')

def postregister(request):

	if request.POST:
		first_name = request.POST.get('first_name')
		last_name = request.POST.get('last_name')
		email = request.POST.get('email')
		username = request.POST.get('username')
		password1 = request.POST.get('password1')
		password2 = request.POST.get('password2')
		
		if password1 == password2:
			if User.objects.filter(username=username).exists():
				messages.error(request, 'Username is Taken Please Try Again')
				return render(request,'signup.html')
			elif User.objects.filter(email=email).exists():
				messages.error(request, 'Email is Taken Please Try Again')
				return render(request,'signup.html')
			else:
				user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password1)
				user.save()
				print('You are registered successfully, Please sign to continue.')
				return redirect('login')
				
		else:
			messages.error(request, 'Password is not matching Please Try Again')
			return render(request,'signup.html')
	else:
		return redirect('register')



def plg(request):
	context={}
	code = request.POST.get('code', '')
	context['code']=code
	typo = request.POST.get('typo', '')
	context['typo']=typo
	print(typo)
	if (typo=='C'):
		with open("p.c","w") as t:
		# with open("p.c","w") as t:
			t.write(code)
		b=os.system("gcc p.c 2> error")# | a.exe")# >aout.txt")
		if(b==0):
			os.system("a >aout.txt")
			with open("aout.txt","r+") as t:
				str=t.read()
				count=str
				print(count)
				context['output']=count
			return render(request,'practice.html',context)
		else:
			with open("error","r") as t:
				count=t.read()
				print(count)
				context['output']=count
			return render(request,'practice.html',context)

	elif(typo=='C++'):
		with open("q.cpp","w") as t:
		# with open("p.c","w") as t:
			t.write(code)
		b=os.system("g++ q.cpp 2> error")# | a.exe")# >aout.txt")
		if(b==0):
			os.system("a >aout.txt")
			with open("aout.txt","r+") as t:
				str=t.read()
				count=str
				print(count)
				context['output']=count
			return render(request,'practice.html',context)
		else:
			with open("error","r") as t:
				count=t.read()
				print(count)
				context['output']=count
			return render(request,'practice.html',context)

	elif(typo=='Java'):
		with open("CODEMANIA.java","w") as t:
			t.write(code)
		
		os.system("javac CODEMANIA.java")
		os.system("java CODEMANIA > aout.txt")
		with open("aout.txt","r") as t:
			count = t.read()
			#count=str
			print(count)
			context['output']=count
		return render(request,'practice.html',context)# | a.exe")# >aout.txt")


	return render(request,'practice.html',context)


def contest_list(request):
	#contest_list = Contest.objects.order_by('-contest_date')
	#context = { 'contest_list': contest_list}
	#return render(request, 'user_contest_home.html')
	try:
		contest_names = Contest.objects.order_by('-contest_date')
	except Contest.DoesNotExist:
		raise Http404("Contest does not exist")
	return render(request, 'user_contest_home.html', {'contest_names': contest_names})

def detail(request, contest_id):
	try:
		problem_list=Problem.objects.filter(contest_reference_id=contest_id)
		contest_obj=Contest.objects.get(pk=contest_id)
        #contest = Contest.objects.get(pk=contest_id)
	except Contest.DoesNotExist:
		raise Http404("Problems does not exist")
	return render(request, 'contestpage.html', {'problem_list': problem_list,'contest_obj':contest_obj})

def aboutus(request):
	return render(request,'about_us.html')

def problem_playground(request, contest_id, problem_id):
	try:
		glb=""
		problem_obj = Problem.objects.get(pk=problem_id)
		contest_obj = Contest.objects.get(pk=contest_id)
		problem_file_url = problem_obj.testfile.url[1:]
		print("Problem File Url : ",problem_file_url)
  

		context = {'problem_obj': problem_obj,
					'contest_obj': contest_obj,
				}		
		str = ""
		if request.method == "POST":
					op = open(problem_file_url, 'r').read()
					code = request.POST.get('code', '')
					context['code']=code
					typo = request.POST.get('typo', '')
					context['typo']=typo
					#print(typo)
					#print(op)
					if (typo=='C'):
						with open("p.c","w") as t:
							t.write(code)
						b=os.system("gcc p.c 2> error")
						if(b==0):
							os.system("a >aout.txt")
							with open("aout.txt","r+") as t:
								str=t.read()
								count = str
								if op == str:
									current_user = request.user
									marks = problem_obj.marks
									problem_solved_instance = ProblemSolved.objects.create(
										contest_ref=contest_obj, problem_ref=problem_obj, user_ref=current_user, points_get=marks)
									problem_solved_instance.save()
									priint(problem_solved_instance)
									print("Success")
									messages.success(request, 'Congratulations you got 100 pts')
								else:
									messages.error(request, 'Wrong Answer Please try Again')
								print(count)
								context['output']=count
							return render(request,'contest_playground.html',context)
						else:
							with open("error","r") as t:
								count=t.read()
								print(count)
								context['output'] = count
							messages.error(request, 'Syntax Error please check and submit')
							return render(request,'contest_playground.html',context)

					elif(typo=='C++'):
						with open("q.cpp","w") as t:
							t.write(code)
						b=os.system("g++ q.cpp 2> error")
						if(b==0):
							os.system("a >aout.txt")
							with open("aout.txt","r+") as t:
								str = t.read()
								if op == str:
									contest_obj = Contest.objects.get(pk=contest_id)
									problem_obj = Problem.objects.get(pk=problem_id)
									current_user = request.user
									marks = problem_obj.marks

									problem_solved_instance, created = ProblemSolved.objects.get_or_create(
										contest_ref=contest_obj, problem_ref=problem_obj, user_ref=current_user,
          								points_get=marks, time_submitted=datetime.datetime.now())
									problem_solved_instance.save()
									print(problem_solved_instance)
									print("Success")
									messages.success(request, 'Congratulations you got 100 pts')
								else:
									messages.error(request, 'Wrong Answer Please try Again')
								count = str
								context['output']=count
							return render(request,'contest_playground.html',context)
						else:
							with open("error","r") as t:
								count=t.read()
								print(count)
								context['output'] = count
							messages.error(request, 'Syntax Error please check and submit')
							return render(request,'contest_playground.html',context)

					elif(typo=='Java'):
						with open("CODEMANIA.java","w") as t:
							t.write(code)
						
						os.system("javac CODEMANIA.java")
						os.system("java CODEMANIA > aout.txt")
						with open("aout.txt","r") as t:
							count = t.read()
							print(count)
							context['output']=count
						return render(request, 'contest_playground.html', context)  
						
					return render(request,'contest_playground.html',context)
									
		else:
			return render(request, 'contest_playground.html', context)


	except Problem.DoesNotExist:
		raise Http404("Problem does not exist")

def pointtable(request, contest_id):
    context = {}
    contest_obj=Contest.objects.get(pk=contest_id)
    contest_users = User.objects.filter(
        problemsolved__contest_ref = contest_obj
    ).annotate(
        point_sum=Sum('problemsolved__points_get')
    ).order_by('-point_sum')
    context['contest_users'] = contest_users
    print(contest_users)
    return render(request,'leaderboard.html', context)    