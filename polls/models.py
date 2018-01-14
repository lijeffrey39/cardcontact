from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import random
import string

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
    	return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
    	return self.choice_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)






def code_generator(size = 6, chars = string.ascii_lowercase + string.digits):
    return '' .join(random.choice(chars) for _ in range(size))

def create_shortcode(size = 6):
    new_code = code_generator(size = size)
    qs_exists = UserProfile.objects.filter(shortcode = new_code).exists()
    if qs_exists:
        create_shortcode(size = size)
    return new_code


class UserProfileManager(models.Manager):

    def all(self, *args, **kwargs):
        qs_main = super(UserProfileManager, self).all(*args, **kwargs)
        qs = qs_main.filter(active = True)
        return qs

    def refresh_shortcodes(self):
        qs = UserProfile.objects.filter(id__gte = 1)
        newCodes = 0
        for q in qs:
            q.shortcode = create_shortcode()
            q.save()
            newCodes += 1
        return "New codes made: {i}".format(i = newCodes)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.IntegerField(default = 0)
    facebook = models.CharField(max_length = 100, default = '', blank=True)
    snapchat = models.CharField(max_length = 100, default = '', blank=True)
    insta = models.CharField(max_length = 100, default = '', blank=True)
    twitter = models.CharField(max_length = 100, default = '', blank=True)

    active = models.BooleanField(default = True)

    shortcode = models.CharField(max_length = 15, unique = True, blank = True)

    objects = UserProfileManager()

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        if self.shortcode is None or self.shortcode == "":
            self.shortcode = create_shortcode()
        super(UserProfile, self).save(*args, **kwargs)

def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user = kwargs['instance'])

post_save.connect(create_profile, sender = User)