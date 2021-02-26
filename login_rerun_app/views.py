from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Message, Comment
import bcrypt

def login(request):
	return render(request, 'login.html')


def register(request):
	return render(request, 'register.html')


def process_register(request):

	print(request.POST)
	errors = User.objects.register_validator(request.POST)

	if len(errors) > 0:
		for key, value in errors.items():
			messages.error(request, value)
        # redirect the user back to the form to fix the errors
		return redirect('/register')

	else:
		hash_pw = bcrypt.hashpw(request.POST['password_input'].encode(), bcrypt.gensalt()).decode()

		new_user = User.objects.create(
			first_name=request.POST['first_name_input'],
			last_name=request.POST['last_name_input'],
			email=request.POST['email_input'],
			password = hash_pw,
			birthday = request.POST['birthday_input'],
		)

		request.session['user_id'] = new_user.id

		return redirect('/wall')


def wall(request):
	context = {
		'logged_in_user': User.objects.get(id = request.session['user_id']),
		'all_the_messages': Message.objects.all(),
	}

	return render(request, 'wall.html', context)


def process_logout(request):
	request.session.clear()
	return redirect('/')


def process_login(request):
	user_list = User.objects.filter(email = request.POST['email_input'])
	if len(user_list) == 0:
		messages.error(request, "INVALID CREDENTIALS")
		return redirect("/login")
	logged_user = user_list[0]
	if bcrypt.checkpw(request.POST['password_input'].encode(), logged_user.password.encode()):
		# PASSWORD MATCHES
		request.session['user_id'] = logged_user.id
		return redirect("/wall")
	else:
		# PASSWORD DOES NOT MATCHES
		messages.error(request, "INVALID CREDENTIALS")
		return redirect("/login")


def post_message(request):
	Message.objects.create(
		user=User.objects.get(id=request.session['user_id']),
		message = request.POST['message_input']
	)
	return redirect("/wall")


def add_comment(request, num):
	Comment.objects.create(
		message= Message.objects.get(id=num),
		user=User.objects.get(id=request.session['user_id']),
		comments=request.POST['comment_input']
	)

	return redirect("/wall")


def delete_this_message(request, num):
	Message.objects.filter(id=num).delete()
	return redirect("/wall")