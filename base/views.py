from django.shortcuts import render
from django.views.generic import View
# Create your views here.
from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate
from .forms import UserRegisterForm, ProfileRegisterForm, contestEntryForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Profile, Contest, Prediction
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
import calendar
from calendar import HTMLCalendar
from django.http import JsonResponse

class CustomHTMLCalendar(HTMLCalendar):

    # CSS classes for the day <td>s
    cssclasses = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
#<a href="#">
    def formatday(self, date_row):
        """
        Return a day as a table cell.
        """
        if date_row.month != self.month:
            return '<td class="noday">&nbsp;</td>' # day outside month
        else:
            return '<td class="%s"><div class="btn-group"><button class="btn btn-secondary btn-lg dropdown-toggle" data-bs-toggle="dropdown" type="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">%d</button><div class="dropdown-menu" aria-labelledby="dropdownMenuButton"><a class="dropdown-item" href="#">Action</a><a class="dropdown-item" href="#">Another action</a><a class="dropdown-item" href="#">Something else here</a></div></div></td>' % (self.cssclasses[date_row.weekday()], date_row.day)

    def formatweek(self, theweek):
        """
        Return a complete week as a table row.
        """
        s = ''.join(self.formatday(date_row) for date_row in theweek)
        return '<tr>%s</tr>' % s

    def formatmonth(self, theyear, themonth, withyear=True):
        """
        Return a formatted month as a table.
        """
        v = []
        a = v.append
        a('<table border="0" cellpadding="0" cellspacing="0" class="month">')
        a('\n')
        a(self.formatmonthname(theyear, themonth, withyear=withyear))
        a('\n')
        a(self.formatweekheader())
        a('\n')
        dates = list(self.itermonthdates(theyear, themonth))
        self.month = themonth
        records = [ dates[i:i+7] for i in range(0, len(dates), 7) ]
        for week in records:
            a(self.formatweek(week))
            a('\n')
        a('</table>')
        a('\n')
        return ''.join(v)

    def formatyear(self, theyear, width=3):
        """
        Return a formatted year as a table of tables.
        """
        v = []
        a = v.append
        width = max(width, 1)
        a('<table border="0" cellpadding="0" cellspacing="0" class="year">')
        a('\n')
        a('<tr><th colspan="%d" class="year">%s</th></tr>' % (width, theyear))
        for i in range(0, 0+12, width):
            # months in this row
            months = range(i, min(i+width, 13))
            a('<tr>')
            for m in months:
                a('<td>')
                a(self.formatmonth(theyear, m, withyear=False))
                a('</td>')
            a('</tr>')
        a('</table>')
        return ''.join(v)

class index(View):
    def get(self,request):
        template='index.html'
        context={}
        return render(request,template,context)

class profileView(View):
    def get(self, request):
        today = datetime.now()
        year = today.year
        month = today.strftime("%B")
        month_num = list(calendar.month_name).index(month)
        cal = CustomHTMLCalendar().formatmonth(year, month_num)
        template = 'Dashboard.html'
        profile = Profile.objects.get(user=request.user)
        contest = Contest.objects.all()
        prediction = Prediction.objects.filter(source_id = request.user.id)

        context = {'profile': profile,
                   'contest': contest,
                   'prediction': prediction,
                   'month': month,
                   'cal': cal,
                   'prev':month_num - 1,
                   'next':month_num + 1,
                   }
        return render(request, template, context)

class updateCalendarView(View):
    def get(self,request,year,month):
        #NEED - error control using logic
        today = datetime.now()
        yearr = today.year
        monthh = today.strftime("%B")
        if month == monthh:
            pass
        else:
            prev = month - 1
            next = month + 1

        month_str = today.strftime("%B")
        cal = CustomHTMLCalendar().formatmonth(year, month)
        return JsonResponse({"cal":cal,
                             "prevv":prev,
                             "nextt":next,})

'http://blog.ankitjaiswal.tech/customizing-htmlcalendar-in-python-to-populate-date-numbers-with-date-objects/'

def updateEntry(request, slug=None):
    form = contestEntryForm(request.POST)
    if request.method == 'POST' and slug is not None:
        if form.is_valid():
            if request.user.is_authenticated:
                form = contestEntryForm(request.POST)
                if form.is_valid():
                    # https://stackoverflow.com/questions/44045233/django-request-user-in-form
                    # set user for the form and we gucci
                    source = Profile.objects.get(id=request.user.id)
                    contest = Contest.objects.get(slug=slug)

                    t1 = request.POST['temp1']
                    t2 = request.POST['temp2']
                    t3 = request.POST['coverage']
                    obj = Prediction.objects.get(source_id=request.user.id,contest=contest)
                    obj.temp1 = t1
                    obj.temp2 = t2
                    obj.coverage = t3
                    obj.save()
                    messages.success(request, f'Response updated for {request.user}!')
                    return HttpResponseRedirect('/dashboard')
            else:
                form = contestEntryForm(source_id = request.user.id)
        else:
            form = contestEntryForm(source_id = request.user.id)
    contests = Contest.objects.get(slug=slug)
    obj = Prediction.objects.get(source_id=request.user.id, contest=contests)

    template = 'update-submission.html'
    context = {'form': form,
               'current':obj,
               'contests': contests}
    return render(request, template, context)


def contestEntry(request, slug=None):
    form = contestEntryForm(request.POST)
    if request.method == 'POST' and slug is not None:

        if form.is_valid():
            if request.user.is_authenticated:
                form = contestEntryForm(request.POST)
                if form.is_valid():
                #https://stackoverflow.com/questions/44045233/django-request-user-in-form
                #set user for the form and we gucci

                    source = Profile.objects.get(id=request.user.id)
                    print(source)
                    contest = Contest.objects.get(slug=slug)
                    t1 = request.POST['temp1']
                    t2 = request.POST['temp2']
                    t3 = request.POST['coverage']
                    entry = Prediction.objects.create(source_id=source.id, contest=contest,temp1=t1,temp2=t2,coverage=t3,predictionSlug=slug)
                    messages.success(request, f'Response Submitted for {request.user}!')
                    return HttpResponseRedirect('/')
            else:
                form = contestEntryForm(request.POST)
        else:
            form = contestEntryForm(request.POST)

    contests = Contest.objects.get(slug=slug)
    template = 'contest-submission.html'
    context = {'form': form,
               'contests': contests}
    return render(request, template, context)


class contest(View):
    def get(self, request):
        #Most of the following code is simply finding
        contests = Contest.objects.all()
        noLink=[]
        cont = []
        for contest in contests:
            try:
                print(contest)

                prediction = Prediction.objects.get(source=Profile.objects.get(user=request.user),contest=contest)

                noLink.append(prediction.contest.id)
            except ObjectDoesNotExist:
                print('funk')
                pass
            finally:
                if noLink != []:
                    for i in noLink:
                        if contest.id == i:
                            pass
                        else:
                            cont.append(contest)
                    contests = cont
                else:
                    pass

        template = 'contest.html'
        context = {'contests': contests}
        return render(request, template, context)


def registerUser(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        #pform = ProfileRegisterForm()
        if form.is_valid():
            username = form.cleaned_data.get('username')
            print(username)
            user = form.save()

            login(request,user)
            messages.success(request, f'account created for {username}!')
            #pform.save()
            return HttpResponseRedirect('/')
        else:
            form = UserRegisterForm()
            pform = ProfileRegisterForm()
            template = 'register.html'
            context = {'form': form,
                       'pform': pform}


    else:
        form = UserRegisterForm()
        pform = ProfileRegisterForm()
        template = 'register.html'
        context = {'form':form,
                   'pform':pform}

    return render(request, template, context)


def logout_view(request):
    username = User.username(request)
    if username != None:
        logout(request)
        return HttpResponseRedirect('/')

