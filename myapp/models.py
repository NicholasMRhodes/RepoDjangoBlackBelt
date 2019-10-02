from django.db import models
import re
import bcrypt

class UserManager(models.Manager):
    def registration_validator(self, postData):
        #VARIABLES
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+-]+@[a-zA-Z0-9._-]+.[a-zA-Z]+$')
        already_registered_user = User.objects.filter(email = postData['email'])
        errors = {}

        #NAME VALIDATION
        if len(postData['name']) < 2:
            errors['name'] = "Name should be at least 2 characters"
        
        #ALIAS VALIDATION
        if len(postData['alias']) < 2:
            errors['alias'] = "Alias should be at least 2 characters"
        
        #USERNAME/EMAIL VALIDATION
        if len(postData['email']) < 3:
            errors['email_blank'] = "Username email is required"
        if len(postData['email']) > 3:   
            if not EMAIL_REGEX.match(postData['email']):
                errors['email_pattern'] = "Username has invalid email address"
        if len(already_registered_user) > 0:
            errors['email_already_exists'] = "Username email already exists"

        #PASSWORD VALIDATION
        if len(postData['password']) < 8:
            errors['password_length'] = "Password must be at least 8 characters"
        if postData['confirm_password'] != postData['password']:
            errors['password_match'] = "Password and confirm password must match"
        
        print(errors)
        return errors

    def login_validator(self, postData):
        user_in_database = User.objects.filter(email = postData['email'])
        
        print ('printing user_in_database: ')
        print (user_in_database)
        print('printing user: ')
        
        errors = {}
        
        if len(postData['email']) < 1:
            errors['email_required'] = "Username email is required"

        if len(postData['password']) < 1:
            errors['password_required'] = "You must enter a password"
        
        if len(user_in_database) < 1:
            errors['email_not_found'] = "Username email is not registered"
        else:
            user = user_in_database[0]
            if bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
                print("password match")
            else:
                print("failed password")
                errors['password_invalid'] = "The password is incorrect"
        
        print(errors)
        return errors

    def addQuote_validator(self, postData):
        errors = {}
        if len(postData['quoteBy']) < 2:
            errors['quoteBy_required'] = "Quoted By must be 2 or more characters"
        if len(postData['quoteMessage']) < 10:
            errors['quoteMessage_required'] = "Message must be 10 or more characters"
        print(errors)
        return(errors)

    def updateQuote_validator(self, postData):
        errors = {}
        if len(postData['quoteBy']) < 2:
            errors['quoteBy_required'] = "Quoted By must be 2 or more characters"
        if len(postData['quoteMessage']) < 10:
            errors['quoteMessage_required'] = "Message must be 10 or more characters"
        print(errors)
        return(errors)

class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Quote(models.Model):
    quoteBy = models.CharField(max_length=255)
    quoteMessage = models.CharField(max_length=255)
    creator = models.ForeignKey(User, related_name="QuotesCreated", on_delete=models.CASCADE, null=True)
    joiner = models.ManyToManyField(User, related_name="joiner")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

