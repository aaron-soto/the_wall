from django.db import models
import re


class UserManager(models.Manager):
	def register_validator(self, postData):
		errors = {}

		# name lengths
		if len(postData['first_name_input']) < 2:
			errors["first_name_input"] = "First name should be at least 2 characters."
		if len(postData['last_name_input']) < 2:
			errors["last_name_input"] = "Last name should be at least 2 characters."
		# email pattern
		EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
		if not EMAIL_REGEX.match(postData['email_input']):          
			errors['email_input'] = "Invalid email address!"
		# CHECK IF EMAIL ALREADY EXISTS WITH THE DB
		user_list = User.objects.filter(email = postData['email_input'])
		if len(user_list) > 0:
			errors['email_duplicate'] = "Email aleady exists, try logging in with this email."
		# password length
		if len(postData['password_input']) < 8:
			errors["password_input"] = "Password should be at least 8 characters long."
		# passwords matching
		if postData['password_input'] != postData['confirm_password_input']:
			errors['match_password'] = "Passwords do not match."

		return errors

class User(models.Model):
	first_name = models.CharField(max_length=55)
	last_name = models.CharField(max_length=55)
	email = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	birthday = models.DateField()

	objects = UserManager()

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)


class Message(models.Model):
	user = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
	message = models.TextField()

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)


class Comment(models.Model):
	message = models.ForeignKey(Message, related_name='comments', on_delete=models.CASCADE)
	user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
	comments = models.TextField()

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)