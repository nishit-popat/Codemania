'''
	views.py file is main file where whole logic of application lies.
	It will have different functions according to different usage.
	It will render and redirect to appropriate template pages.
	Authors : Nishit Popat, Meet Patel, Manil Patel, Jay Patel

'''
#Importing required Libraries
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User, auth
import os
from django.shortcuts import get_object_or_404
from django.db.models import Sum
import datetime
from .forms import SnippetForm

#Importing required Models from models.py file
from .models import Contest, Problem, ProblemSolved, Snippet


#This function will render admin page.
def admin(request):
	return render(request,'admin')

#Home Function, First Page of website.
def home(request):

	#It will check that whether form has used 'POST' method to pass the data
    if request.method == 'POST':
		#If user clicks on sign in button then it will redirect it to sign in page.
        if request.POST.get("signin"): 
            return render(request, 'signin.html')

		#If user clicks on sign up button then it will redirect to sign up page.
        elif request.POST.get("signup"): 
            return render(request, 'signup.html')
    else:

        return render(request, 'home.html')

#It will return user_home page which is page that will be shown after sucessful login of user.
def user_home(request):
    return render(request, 'user_home.html')

#Login function
def login(request):

	#Checks whether method is POST or not
    if request.method == 'POST':

		#retrieve username from form
        username = request.POST.get('username')

		#retrieve password from form	
        password = request.POST.get('password')

		#Authenticate username and password
        user = auth.authenticate(username=username, password=password)

		#If authentication is successful then user object will be return
        if user is not None:

			#login of user using user object
            auth.login(request, user)

			#redirect to user_home page
            return redirect('user_home') 
        else:

			#on wrong credentials error message will be displayed
            messages.error(request, 'Invalid Credentials')

			#redirect to login page again
            return render(request, 'signin.html')
    else:
        return render(request, 'signin.html')


#Log out function
def logout(request):

	#Log out from current user
    auth.logout(request)

	#redirect to first page which is home page
    return redirect('/')

#Register function
def register(request):
	return render(request, 'signup.html')

#After clicking register button this functin will be called
def postregister(request):

	#Check if it uses POST method
	if request.POST:
		#retrieve first name
		first_name = request.POST.get('first_name')
		
		#retrieve last name
		last_name = request.POST.get('last_name')

		#retrieve email
		email = request.POST.get('email')

		#retrieve username
		username = request.POST.get('username')

		#retrieve password 
		password1 = request.POST.get('password1')

		#retrieve confirm password
		password2 = request.POST.get('password2')
		
		#checks if password and confirmed password
		if password1 == password2:

			#Checks if username is already taken
			if User.objects.filter(username=username).exists():
				messages.error(request, 'Username is Taken Please Try Again')
				return render(request,'signup.html')

			#Checks if email is already taken
			elif User.objects.filter(email=email).exists():
				messages.error(request, 'Email is Taken Please Try Again')
				return render(request,'signup.html')

			else:
				#Create user and add required fields
				user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password1)
				
				#Save user object
				user.save()

				print('You are registered successfully, Please sign to continue.')
				return redirect('login')
				
		else:
			#If password is not matching then show the error
			messages.error(request, 'Password is not matching Please Try Again')
			return render(request,'signup.html')
	else:
		return redirect('register')


def plg(request):
	if request.method == 'POST':
		form = SnippetForm(request.POST)
		print(form.data.get("text"))
		code = form.data.get("text")
		context={}
		
		with open("q.cpp","w") as t:
			t.write(code)
		b=os.system("g++ q.cpp 2> error")
		if(b==0):
			os.system("a >aout.txt")
			with open("aout.txt","r+") as t:
				str1 = t.read()
				print(str1)
				context['output'] = str1
				context['form'] = form
				context['snippets'] = Snippet.objects.all
			return render(request, 'practice.html', context)
		else:
			with open("error","r") as t:
				count = t.read()
				print(count)
				context['output']=count
				context['form'] = form
				context['snippets'] = Snippet.objects.all()
			return render(request,'practice.html', context)
		if form.is_valid():
			form.save()
			context['form']=form
			context['snippets']=Snippet.objects.all()
			return render(request, "practice.html", context)
	else:
		context={}
		form = SnippetForm()
		context['form']=form
		context['snippets']=Snippet.objects.all()
	return render(request, "practice.html", context)


#Retrieves list of all contests 
def contest_list(request):

	try:
		#Retrieve all contests ordered by date
		contest_names = Contest.objects.order_by('-contest_date')
	except Contest.DoesNotExist:

		#If it does not exist then give response that contest does not exist
		raise Http404("Contest does not exist")

	return render(request, 'user_contest_home.html', {'contest_names': contest_names})

#Details about problems given contest_id
def detail(request, contest_id):
	try:

		#Retrieval of all the problems belonging to contest_id
		problem_list=Problem.objects.filter(contest_reference_id=contest_id)

		#Retrieve contest object from contest id
		contest_obj=Contest.objects.get(pk=contest_id)

	except Contest.DoesNotExist:

		#If Contest does not exist then it will give error
		raise Http404("Problems does not exist")

	return render(request, 'contestpage.html', {'problem_list': problem_list,'contest_obj':contest_obj})

#About us page function
def aboutus(request):
	return render(request,'about_us.html')

#Page for particular Problem's Coding area
#It will take contest_id and problem_id as input arguments
def problem_playground(request, contest_id, problem_id):
	try:
		form = SnippetForm(request.POST)
		glb=""
		problem_obj = Problem.objects.get(pk=problem_id)
		contest_obj = Contest.objects.get(pk=contest_id)
		problem_file_url = problem_obj.testfile.url[1:]
		print("Problem File Url : ",problem_file_url)
		
		context={}
		typo = 'C++'
		context['typo']=typo
		context['form']=form
		context['snippets']=Snippet.objects.all()
		context['problem_obj'] = problem_obj
		context['contest_obj'] = contest_obj
  
		str = ""
		if request.method == "POST":
			op = open(problem_file_url, 'r').read()
			code = form.data.get("text")
			context['code']=code
			
			if(typo=='C++'):
				with open("q.cpp","w") as t:
					t.write(code)
				b=os.system("g++ q.cpp 2> error")
				if(b==0):
					os.system("a >aout.txt")
					with open("aout.txt","r+") as t:
						str1 = t.read()
						if op == str1:
							contest_obj = Contest.objects.get(pk=contest_id)
							problem_obj = Problem.objects.get(pk=problem_id)
							current_user = request.user
							marks = problem_obj.marks

							problem_solved_instance, isExisted = ProblemSolved.objects.get_or_create(
								contest_ref=contest_obj, problem_ref=problem_obj, user_ref=current_user,
          						points_get=marks, defaults={'time_submitted': datetime.datetime.now()})

							problem_solved_instance.save()

							print(problem_solved_instance)
							context['output']=str1
							print("Already exists : ", isExisted)
							print("Success")
							messages.success(request, 'Congratulations you got Right Answer')
						else:
							messages.error(request, 'Wrong Answer Please try Again')
							count = str1
							context['output']=count
						
					return render(request,'contest_playground.html',context)
				else:
					with open("error","r") as t:
						count=t.read()
						print(count)
						context['output'] = count
						messages.error(request, 'Syntax Error please check and submit')
					return render(request,'contest_playground.html',context)				
		else:
			return render(request, 'contest_playground.html', context)

	except Problem.DoesNotExist:
		raise Http404("Problem does not exist")

#Points table creation function, It will have contest_id as input parameter.
def pointtable(request, contest_id):
    context = {}

	#retrieval of contest object from contest id
    contest_obj=Contest.objects.get(pk=contest_id)

	#Query to retrieve user objects by filteriing contest reference and aggregate of points get and order by point sum.
    contest_users = User.objects.filter(
        problemsolved__contest_ref = contest_obj
    ).annotate(
        point_sum=Sum('problemsolved__points_get')
    ).order_by('-point_sum')

	#Add contest_users to dictionary
    context['contest_users'] = contest_users
    return render(request,'leaderboard.html', context)    