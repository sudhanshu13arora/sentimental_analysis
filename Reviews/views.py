import pickle

from io import BytesIO

from django.core.files.base import ContentFile
from django.views.decorators.cache import cache_control
from matplotlib import pyplot as plt

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, render_to_response, redirect
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.template import RequestContext

from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from .forms import ReviewsForm, UserForm, StudentForm
from .models import Reviews, Meal

with open('Reviews\\modelTry2', 'rb') as f:
    model = pickle.load(f)

print(type(model))


def meal_plots(mealname, x_date):
    y_breakfast = []
    for i in range(0, 8):
        d = timezone.now().date() - timedelta(days=(7 - i))
        obj_breakfast = Reviews.objects.filter(pub_date=d, meal__meal=mealname)
        print(obj_breakfast)
        s_breakfast = 0
        if obj_breakfast:
            for ob in obj_breakfast:
                s_breakfast += ob.score

            y_breakfast.append(s_breakfast / len(obj_breakfast))
        else:
            y_breakfast.append(0)

    plt.figure()
    plt.plot(x_date, y_breakfast, color='black')
    plt.xlabel("Past 7 days")
    plt.ylabel("Average Score for " + str(mealname))
    plt.savefig(settings.MEDIA_ROOT + "\\" + mealname)


def pie_chart(positive, neutral, negative, nb):
    total = positive + neutral + negative + nb
    pos_percent = (positive / float(total)) * 100
    neu_percent = (neutral / float(total)) * 100
    nega_percent = (negative / float(total)) * 100
    nb_percent = (nb/float(total)) * 100

    explode = (0.05, 0.05, 0.05, 0.05)
    labels = 'Positive, ' + str(round(pos_percent,2)) + "%", 'Not Bad, ' + str(round(nb_percent,2)) + "%", 'Neutral, ' + str(round(neu_percent,2)) + "%", 'Negative, ' + str(round(nega_percent,2)) + "%"
    plt.figure(figsize=(10, 10))
    patches, text = plt.pie([pos_percent, nb_percent, neu_percent, nega_percent], explode=explode, labels=labels,
                            colors=['green', 'orange', 'grey', 'red'])
    text[0].set_fontsize(13)
    text[1].set_fontsize(13)
    text[2].set_fontsize(13)
    text[3].set_fontsize(13)
    plt.savefig(settings.MEDIA_ROOT + "\\Pie")


# Create your views here


def login_success(request):
    """
    Redirects users based on whether they are in the admins group
    """
    if request.user.is_staff:
        # user is an admin
        return HttpResponseRedirect('/reviews/view/')
    else:
        return HttpResponseRedirect('/reviews/give/')


@csrf_protect
@csrf_exempt
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def signup(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return HttpResponseRedirect('/reviews/view/')
        else:
            return HttpResponseRedirect('/reviews/give/')

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        student_form = StudentForm(request.POST)
        if user_form.is_valid() and student_form.is_valid():
            print(user_form)
            print(student_form)
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            student = student_form.save(commit=False)
            student.user = user
            student.save()

            print("Great success")
            user_signup = User.objects.get(username=user.username)

            login(request, user_signup)
            return HttpResponseRedirect("/reviews/give/")

        else:
            print(student_form.errors)
            print(user_form.errors)
            messages.error(request, user_form.errors)
            messages.error(request, student_form.errors)

    else:
        user_form = UserForm()
        student_form = StudentForm()

    return render(request, 'signup.html', {'userform': user_form, 'studentform': student_form})


@csrf_protect
@csrf_exempt
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_login(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return HttpResponseRedirect('/reviews/view/')
        else:
            return HttpResponseRedirect('/reviews/give/')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user_login = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, 'It seems that you are not registered with us. Please Sign Up')
            return HttpResponseRedirect("")

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user_login)
                if user_login.is_staff:
                    print("Staff")
                    return HttpResponseRedirect('/reviews/view/')
                else:
                    print("Unpriviledged")
                    return HttpResponseRedirect('/reviews/give/')
            else:
                messages.error(request, 'Error!')
                return render(request, 'index1.html')


        else:
            print("Invalid credentials: {0}, {1}".format(username, password))
            messages.error(request, 'Invalid Login Credentials')
            return HttpResponseRedirect("")

    else:
        return render(request, 'index1.html')


@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_logout(request):
    logout(request)
    messages.success(request, "You have been successfully logged out")
    return HttpResponseRedirect("/reviews/login/")


@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def view_reviews(request):
    if request.user.is_authenticated and not request.user.is_staff:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    reviews = Reviews.objects.all().order_by('-date_time')
    context = {'reviews': reviews}
    return render(request, 'adminreviews.html', context)


@login_required
@csrf_protect
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def submit_review(request):
    if request.user.is_authenticated and request.user.is_staff:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    print(request.method)
    if request.method == 'POST':
        review_form = ReviewsForm(request.POST)
        print(review_form)
        if review_form.is_valid():
            print(type(model))
            rev = Reviews()
            rev.review = review_form.cleaned_data['review']
            actual_review = str(review_form.cleaned_data['review'])
            print(actual_review + "**********************")
            rev.rating = review_form.cleaned_data['rating']

            print(rev.rating)
            rev.meal = review_form.cleaned_data['meal']
            rev.student = request.user.student
            prediction = model.predict([actual_review])[0]
            print(type(prediction))
            print(prediction)
            if prediction == 2:
                rev.sentiment = '5'
            elif prediction == 1:
                rev.sentiment = '3'
            elif prediction == 0:
                rev.sentiment = '1'

            print(rev.sentiment)
            rev.score = round(0.5 * review_form.cleaned_data['rating'] + 0.5 * int(rev.sentiment), 3)
            rev.save()
            context = {'meals': Meal.objects.all(), 'other_reviews': Reviews.objects.all().order_by('-date_time')}
            messages.success(request, "Your feedback is appreciated!")
            return render(request, 'yash.html', context)

        else:
            print(review_form.errors)
            review_form = ReviewsForm()
            messages.error(request, "There has been an error in submitting the review")
            return render(request, 'yash.html',
                          {'meals': Meal.objects.all(), 'other_reviews': Reviews.objects.all().order_by('-date_time')})

    return render(request, 'yash.html',
                  {'meals': Meal.objects.all(), 'other_reviews': Reviews.objects.all().order_by('-date_time')})


@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def view_self_comments(request, username):
    try:
        u = User.objects.get(username=username)
    except User.DoesNotExist as e:
        raise Http404("The user does not exist")

    comments = Reviews.objects.filter(student=u.student).order_by('-date_time')
    context = {'comments': comments}
    return render(request, "pastreviews.html", context)


@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def analysis(request):
    # some_day_last_week = timezone.now().date() - timedelta(days=7)
    # obj = Reviews.objects.filter(pub_date__gte=some_day_last_week, pub_date__lt=timezone.now().date()).order_by('pub_date').values_list('pub_date','sentiment')

    if request.user.is_authenticated and not request.user.is_staff:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    x_date = []
    y_date = []
    y_breakfast = []
    for i in range(0, 8):
        d = timezone.now().date() - timedelta(days=(7 - i))
        x_date.append(d.strftime("%d/%m"))
        obj = Reviews.objects.filter(pub_date=d)
        print(obj)
        print("****************")
        s = 0
        if obj:
            for o in obj:
                s += o.score
            print(s)
            y_date.append(s / len(obj))
        else:
            y_date.append(0)

    print(x_date, y_date)
    plt.figure()
    plt.plot(x_date, y_date, color='black')
    plt.xlabel("Past 7 days")
    plt.ylabel("Average Score")
    plt.savefig(settings.MEDIA_ROOT + "\\one")

    for meal in Meal.objects.all():
        meal_plots(str(meal), x_date)

    # # pos_query = Reviews.objects.filter(sentiment='5')
    # # neu_query = Reviews.objects.filter(sentiment='3')
    # # nega_query = Reviews.objects.filter(sentiment='1')
    # #
    # # print(pos_query)
    # # print(neu_query)
    # # print(nega_query)
    #
    # if len(pos_query) and len(neu_query) and len(nega_query):
    #     pie_chart(len(pos_query), len(neu_query), len(nega_query))

    pos = 0
    neu = 0
    neg = 0
    nb = 0

    rev = Reviews.objects.all()
    total_number = len(rev)
    average_score = 0
    for r in rev:
        average_score += r.score
        if(r.score >= 4):
            pos +=1
        elif(r.score >=3 and r.score <4):
            neu += 1
        elif(r.score >= 2 and r.score < 3):
            nb += 1
        elif(r.score >= 1 and r.score < 2):
            neg += 1

    if pos and nb and neg and neu:
        pie_chart(pos,neutral=neu,negative=neg, nb=nb)

    average_score /= total_number

    print(Reviews.objects.values_list('score'))



    return render(request, "ERP_Analysis.html", {'total_number': total_number, 'average_score':round(average_score,3)})


@login_required
def profile_view(request, username):
    try:
        u = User.objects.get(username=username)
    except User.DoesNotExist as e:
        raise Http404("The user does not exist")

    reviews = Reviews.objects.filter(student=u.student)
    number_of_reviews = len(reviews)
    if number_of_reviews:
        average_rating = 0

        for r in reviews:
            average_rating += r.score

        average_rating = round(average_rating / number_of_reviews, 2)
    else:
        number_of_reviews = 0
        average_rating = 0

    return render(request, 'profile.html',
                  {'user_info': u, 'number_of_reviews': number_of_reviews, 'average_rating': average_rating})
