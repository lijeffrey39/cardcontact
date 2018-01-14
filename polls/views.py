from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views import generic
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserChangeForm
from .forms import UserForm, UserFormLogin, EditProfileForm, EditProfileFormRest
from django.views.generic import UpdateView
from django.contrib.auth.models import User
from django.contrib import messages

from django.contrib.sites.models import Site

from .models import Choice, Question, UserProfile

import mimetypes

# def index(request):
# 	latest_question_list = Question.objects.order_by('-pub_date')[:5]
# 	# template = loader.get_template('polls/index.html')
# 	context = {
#         'latest_question_list': latest_question_list,
#     }
# 	# return HttpResponse(template.render(context, request))
# 	return render(request, 'polls/index.html', context)

def detail(request, question_id):
    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise Http404("Question does not exist")
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {'question': question})



# class IndexView(generic.ListView):
#     template_name = 'polls/index.html'
#     context_object_name = 'latest_question_list'

#     def get_queryset(self):
#         """Return the last five published questions."""
#         return Question.objects.order_by('-pub_date')[:5]


def index(request):
    return render(request, 'polls/index.html', {'user': request.user})

def editProfile(request):
    if request.user.is_authenticated:
        if (request.method == 'POST'):
            #form = EditProfileForm(request.POST, instance = request.user)
            profile_form = EditProfileFormRest(request.POST, instance=request.user.userprofile)

            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, 'Your profile was successfully updated!')
                return redirect('/profile')
            else:
                messages.error(request, 'Please correct the error below.')
        else:
            profile_form = EditProfileFormRest(instance=request.user.userprofile)
            return render(request, 'polls/editprofile.html', {'profForm' : profile_form})
    else:
        return redirect('/')

def profileView(request, code):
    u = UserProfile.objects.get(shortcode = code)
    username = str(u)
    user = User.objects.get(username = username)
    return render(request, 'polls/viewprof.html', {'user': user})

def profileViewReal(request):
    if request.user.is_authenticated:
        domain = 'cardcontact.herokuapp.com/' + request.user.userprofile.shortcode
        return render(request, 'polls/viewprof.html', {'user': request.user, 'domain': domain})
    else:
        return redirect('/')

# class EditProfile(UpdateView):
#     model = UserProfile
#     form_class = EditProfileForm
#     template_name = "polls/editprofile.html"

#     def get_object(self, *args, **kwargs):
#         user = get_object_or_404(User, pk=self.kwargs['pk'])

#         # We can also get user object using self.request.user  but that doesnt work
#         # for other models.

#         return user.userprofile

#     def get_success_url(self, *args, **kwargs):
#         return redirect('/polls')

# class DetailView(generic.DetailView):
#     model = Question
#     template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


class UserFormView(generic.View):
    form_class = UserForm
    template_name = 'polls/registration.html'

    #display blank form
    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    #process form data
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit = False)

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            user = authenticate(username = username, password = password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('/profile')

        return render(request, self.template_name, {'form': form})


def loginView(request):
    form = UserFormLogin(request.POST or None)
    print(request.user.is_authenticated)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username = username, password = password)
        login(request, user)
        return redirect("/profile")
    return render(request, "polls/login.html", {'form': form})


def logoutView(request):
    logout(request)
    return redirect("/")


def getFile(request, code):

    u = UserProfile.objects.get(shortcode = code)
    username = str(u)
    user = User.objects.get(username = username)
    email = user.email
    first = user.first_name 
    last = user.last_name
    name = first + " " + last

    fileContent = 'BEGIN:VCARD\r\nVERSION:3.0\r\nEMAIL;TYPE=INTERNET:' + email + '\r\nFN:' + name + '\r\nN:' + last + ';' + first + ';;;\r\nEND:VCARD\r\n'
    res = HttpResponse(content_type=mimetypes.guess_type(first))
    res.write(fileContent)
    res['Content-Disposition'] = 'attachment; filename=yourname.vcf'
    return res


