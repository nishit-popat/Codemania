'''
	views.py file is main file where whole logic of application lies.
	It will have different functions according to different usage.
	It will render and redirect to appropriate template pages.
	Authors : Nishit Popat, Meet Patel, Manil Patel, Jay Patel

'''
#Importing required Libraries
from django.shortcuts import render, redirect
from django.http import HttpResponse,Http404
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
				messages.success(request, "You are registered sucessfully, Please sign in to continue")
				return redirect('login')
				
		else:
			#If password is not matching then show the error
			messages.error(request, 'Password is not matching Please Try Again')
			return render(request,'signup.html')
	else:
		return redirect('register')

#This Function will compile and run code written in practice playground.
def plg(request):

	#if request is POST then proceed further
	if request.method == 'POST':

		#creating instance of SnippetForm which have ace editor area 
		form = SnippetForm(request.POST)

		#print(form.data.get("text"))

		#retrieve text written in ace editor area in variable 'code'
		code = form.data.get("text")

		#code_input variable will store custom input provided by user
		code_input = request.POST.get('code_input')
		
		#open practice_input.txt for custom input which is stored in code_input, w+ means file can be readable and writable
		f= open("practice_input.txt","w+")

		#write code_input in file practice_input.txt
		f.write(code_input)

		#close file instance
		f.close()

		#Create dictionary context which will pass in render function
		context={}
		
		#open q.cpp in write mode as t
		with open("q.cpp","w") as t:
			#write code in q.cpp
			t.write(code)

		#Compile q.cpp using os.system method
		b=os.system("g++ q.cpp 2> error")

		#if it compiles sucessfully it will return 0 
		if(b==0):

			#run q.cpp using os.system and take input from custom_input.txt and write output in aout.txt 
			os.system("a < practice_input.txt >aout.txt")

			#open aout.txt in r+ mode
			with open("aout.txt","r+") as t:

				#read contents of aout.txt in output_content variable
				output_content = t.read()

				#print(output_content)

				#store necessary variables in context dictionary
				context['output'] = output_content
				context['code_input'] = code_input
				context['form'] = form
				context['snippets'] = Snippet.objects.all

			return render(request, 'practice.html', context)
		else:
			#if b does not return 0 as output then open error file in read mode as t
			with open("error","r") as t:

				#read contents of error file in error_content variable
				error_content = t.read()

				#print(count)

				#store all necessary variables as key pair in context dictionary
				context['output']=error_content
				context['code_input'] = code_input
				context['form'] = form
				context['snippets'] = Snippet.objects.all()

			return render(request,'practice.html', context)

		#If form is valid then save the form and add contents to snippet object
		if form.is_valid():
			form.save()
			context['form']=form
			context['snippets']=Snippet.objects.all()
		
			return render(request, "practice.html", context)

	#if form is loading first time then request will not be POST and form will load from below part
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

	except Contest.DoesNotExist or Problem.DoesNotExist:

		#If Contest does not exist then it will give error
		raise Http404("Problems does not exist")

	return render(request, 'contestpage.html', {'problem_list': problem_list,'contest_obj':contest_obj})

#About us page function
def aboutus(request):
	return render(request,'about_us.html')

#Page for particular Problem's Coding area
#It will take contest_id and problem_id as input arguments
def problem_playground(request, contest_id, problem_id):

	#Using try block
	try:

		#create instance of Snippetform which have ace editor area
		form = SnippetForm(request.POST)
		#glb=""

		# Retrieve problem object from problem_id
		problem_obj = Problem.objects.get(pk=problem_id)

		#Retrieve contest object from contest_id
		contest_obj = Contest.objects.get(pk=contest_id)

		#Retrieve test case file url
		problem_file_url = problem_obj.testfile.url[1:]

		#Retrieve input file url
		input_file_url = problem_obj.inputfile.url[1:]
		#print("Problem File Url : ",problem_file_url)
		#print("Input File Url : ",input_file_url)
		
		#Create empty dictionary context
		context={}

		#language of program is C++
		typo = 'C++' 

		#save necessary information in context dictionary in order to render information in template
		context['typo']=typo
		context['form']=form
		context['snippets']=Snippet.objects.all()
		context['problem_obj'] = problem_obj
		context['contest_obj'] = contest_obj
  
		#str = ""

		#If request method is POST then proceed with following block
		if request.method == "POST":

			#Open the test case file url in op variable
			op = open(problem_file_url, 'r').read()

			#Retrieve ace editor content in code variable
			code = form.data.get("text")

			#save code to dictionary of code
			context['code']=code
			
			#type is already C++
			if(typo=='C++'):

				#open q.cpp file in write mode
				with open("q.cpp","w") as t:

					#write code in q.cpp file
					t.write(code)

				#compile q.cpp file
				b=os.system("g++  q.cpp 2> error")

				#If it compiles sucessfully then it will return 0 
				if(b==0):

					#create argument with custom input file in  background provided at problem creation
					argument = "a <" +input_file_url + " >aout.txt"

					#run file and save output in aout.txt
					os.system(argument)

					#open aout.txt in r+ mode
					with open("aout.txt","r+") as t:

						#read contents of aout.txt and store it in output_content variable
						output_content = t.read()

						#compare test_file content and output derieved after running the program and if both are same then user 
						# it means that user wrote right program 
						if op == output_content:

							# create contest, problem object from their ids and retrieve logged in user
							contest_obj = Contest.objects.get(pk=contest_id)
							problem_obj = Problem.objects.get(pk=problem_id)
							current_user = request.user
							# store marks which is defined in problem object in marks variable
							marks = problem_obj.marks

							#Create instance of problem_Solved object from above information and if it already 
							# exists then override it
							problem_solved_instance, isExisted = ProblemSolved.objects.get_or_create(
								contest_ref=contest_obj, problem_ref=problem_obj, user_ref=current_user,
          						points_get=marks, defaults={'time_submitted': datetime.datetime.now()})

							#save problem solved instance
							problem_solved_instance.save()

							#print(problem_solved_instance)

							#save output_content in context dictionary
							context['output']=output_content

							#print("Already exists : ", isExisted)
							#print("Success")

							#Show message that user got points
							messages.success(request, 'Congratulations you got Right Answer')
						else:

							#Otherwise ans is wrong and try again
							messages.error(request, 'Wrong Answer Please try Again')

							#Store output of program
							context['output']=output_content
						
					return render(request,'contest_playground.html',context)
				else:

					#If program gives error then open error file in read mode
					with open("error","r") as t:

						#read error in error_content variable
						error_content=t.read()

						#Save error output in context dictionary
						context['output'] = error_content

						#Show message that program has syntax errors
						messages.error(request, 'Syntax Error please check and submit')
					return render(request,'contest_playground.html',context)				
		else:
			return render(request, 'contest_playground.html', context)

	#Catch try block that if problem does not exist then raise Http404 Exception
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