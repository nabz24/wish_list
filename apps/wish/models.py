from __future__ import unicode_literals


from django.db import models
import re, bcrypt
import datetime

# Create your models here.
Email_REGEX =re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]{2,3}$')
Name_REGEX = re.compile(r'^[A-Za-z]{3,30}$')
Password_REGEX = re.compile(r'^[A-Za-z0-9@#$%^&*+=]{8,}')
message_REGEX = re.compile(r'^[A-Za-z ]{3,}$')

# Create your models here.

class UsersManager(models.Manager):
    def register(self, postData):
        error_list = []
        cur_date = datetime.datetime.today().strftime('%Y-%m-%d')
        if not Name_REGEX.match(postData['name']):
            error_list.append("First name is not valid. Must be be all letters and longer than three characters")
        if not Name_REGEX.match(postData['username']):
            error_list.append("Username is not valid. Must be be all letters and between 3 to 30 characters in length")
        if not Name_REGEX.match(postData['username']):
            error_list.append("username is not valid")
        if not Password_REGEX.match(postData["password"]):
            error_list.append('Password must be at least 8 characters')
        if not cur_date > postData['date_hired']:
            error_list.append('Date hired is after current date')
        if postData['date_hired'] is "":
            error_list.append('Invalid Date')
        if not postData['password'] == postData['conf_pass']:
            error_list.append('Password does not match confirm password')

        if len(error_list)<1:
            hashed_password = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
            if self.filter(username = postData['username']).exists():
                error_list.append("username is already registered")
            new_user = self.create(name = postData['name'], username = postData['username'], password = hashed_password, date_hired = postData['date_hired'])
            user_id = self.get(username=postData['username']).id
            return{'success' : True, 'user_id' : user_id}
        else:
            return {'success' : False, 'errors' : error_list}

    def login(self, postData):
        error_l = []
        if Users.objects.filter(username = postData['log_username']).exists():
            password = postData['log_password'].encode()
            stored_hashed = Users.objects.get(username= postData['log_username']).password
            if bcrypt.hashpw(password, stored_hashed.encode()) != stored_hashed:
                error_l.append("incorrect password")
            else:
                user = Users.objects.get(username = postData['log_username'])
        else:
            error_l.append("username does not exist!")
        if len(error_l) < 1:
            return {'success' : True, 'user_id' : user.id}
        else:
            print error_l
            return {'success' : False, 'errors' : error_l}


class WishManager(models.Manager):
    def quoteReg(self,postData):
        error_list = []
        if not message_REGEX.match(postData['item']):
            error_list.append("Item is invalid")
        if len(error_list)<1:
            # quote =
            new_quote = self.create(item = postData['item'], contributer_id = postData['user_id'])
            return{'success' :True}
        else:
            return{ 'success' :False, 'errors': error_list}



class Users(models.Model):
    name = models.CharField(max_length = 45)
    username = models.CharField(max_length = 45)
    password = models.CharField(max_length = 45)
    created_at = models.DateField(auto_now_add = True)
    date_hired = models.DateField()
    objects = UsersManager()

class Wish(models.Model):
    item = models.CharField(max_length = 45)
    created_at = models.DateField(auto_now_add = True)
    contributer = models.ForeignKey(Users, related_name = "quoter")
    wish_item = models.ManyToManyField(Users, related_name = "wished")
    objects = WishManager()
