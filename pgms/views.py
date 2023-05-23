from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Value
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import FormView, CreateView, TemplateView

from pgms.forms import Form_PGM, Form_PGM_add_Employees

from calendar import monthrange
from datetime import datetime
from django.utils import timezone

from pgms.models import *
from utils import log


def get_current_time_pgm(query):
    now = datetime.now().strftime("%H:%M")
    if len(query) == 1:
        query[0].now = True
        return query

    for x in query:
        if x.time_rec.strftime("%H:%M") > now:
            x.now = True

            break
    return query


# Create your views here.

class View_Pgms_Available(TemplateView):
    template_name = "pages/scale-pgms.html"

    def get(self, request, *args, **kwargs):
        today = datetime.today()
        query1 = Programs_Show.objects.filter(date_rec=today, channel="RIT").order_by('time_rec')
        query2 = Programs_Show.objects.filter(date_rec=today, channel="IIGD").order_by('time_rec')
        query3 = Programs_Show.objects.filter(date_rec=today, channel="RIT Noticias").order_by('time_rec')
        query4 = Programs_Show.objects.filter(date_rec=today, channel="Canal UM").order_by('time_rec')
        querys = [[query1, "RIT"], [query2, "IIGD"], [query3, "RIT Noticias"], [query4, "Canal UM"]]
        # querys = [query1, query2,query3, query4]

        for x, _ in querys:
            get_current_time_pgm(x)
        kwargs = {
            "querys": querys,
        }
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


@method_decorator(login_required(login_url="employees:login", redirect_field_name='next'), name='dispatch')
class View_Pgms_ADD(FormView):
    template_name = "pages/scale-add-pgm.html"
    form_class = Form_PGM
    extra_context = {
        'button': 'Cadastrar'
    }

    def post(self, request, *args, **kwargs):
        form = Form_PGM(
            data=request.POST or None,  # receive a request data or none
            files=request.FILES or None,
        )
        if form.is_valid():
            form.save()
            messages.success(request, "Programa cadastrado")
            return redirect(reverse('pgms:set-date'))

        else:
            messages.error(request, f"Programa não cadastrado")
        return redirect(reverse('pgms:add-pgm'))


@method_decorator(login_required(login_url="employees:login", redirect_field_name='next'), name='dispatch')
class View_Pgms_Set_Days(CreateView):
    template_name = "pages/scale-set-days.html"

    def get(self, request, *args, **kwargs):
        # MAKE CALENDARY
        session_data = self.request.session.get('form_data')
        today = timezone.now().date()
        month = int(request.GET.get('month', today.month))
        year = int(request.GET.get('year', today.year))

        if month == 13:
            month = 1
            year = year + 1
        elif month == 0:
            month = 12
            year = year - 1
        # month_start = datetime(int(year), int(month), 1)
        _, num_days = monthrange(int(year), int(month))
        # month_end = month_start + timedelta(days=num_days)

        # if str(today) == f'{year}-{str(month).zfill(2)}-{today.day}':  # GET TODAY

        # ADD EVENTS TO CALENDARY
        # events = When_Works.objects.filter(date__gte=month_start, date__lte=month_end)
        next_month = int(month) + 1

        previous_month = int(month) - 1
        weeks = []
        week = []

        for day in range(1, num_days + 1):
            """IS AN OLD DAY?"""

            if month >= today.month and day >= today.day or month > today.month or year > today.year:
                date = datetime(int(year), int(month), day)
                week.append((date, f'<input type="checkbox" name="DATES" '
                                   f'value="{date.strftime("%Y-%m-%d")}">'))
            else:

                date = datetime(int(year), int(month), day)
                # events_for_day = events.filter(date__year=date.year, date__month=date.month, date__day=date.day).order_by(
                #     '-id')

                week.append((date, ""))

            if date.weekday() == 5 or day == num_days:
                weeks.append(week)
                week = []
        while int(len(weeks[0])) < 7:  # make weeks feet property
            weeks[0].insert(0, [" ", ""])
        channels = ['RIT', 'Canal UM', 'Rit Noticias', 'IIGD']
        kwargs = {
            'form': Form_PGM_add_Employees(session_data),
            'today': today.day,
            'weeks': weeks,
            'month': month,
            'year': year,
            'previous_month': f'?month={previous_month}',
            'next_month': f'?month={next_month}',
            'channels': channels,
        }
        # print((qs[0])['values'])
        # context = self.get_context_data(**kwargs)
        return self.render_to_response(kwargs)

    def post(self, request, *args, **kwargs):
        POST = request.POST
        dates = POST.getlist('DATES')
        time_rec = POST.get("time-begin")
        channel = POST.get("channel")
        if len(dates) == 0:
            messages.error(request, "Selecione pelo menos um dia")
            request.session['form_data'] = POST  # Give data from POST to SESSION

            return redirect(reverse('pgms:set-date'))
        elif not time_rec:
            messages.error(request, "Selecione que horas será gravado...")
            request.session['form_data'] = POST  # Give data from POST to SESSION

            return redirect(reverse('pgms:set-date'))
        # form.is_valid()
        for date in dates:
            form = Form_PGM_add_Employees(self.request.POST)
            exist = Programs_Show.objects.filter(date_rec=date, channel=channel, time_rec=time_rec).first()
            if exist:
                log(f'{exist.name} atualizada pelo: {self.request.user}')
                exist.delete()

            form = form.save(commit=False)

            form.date_rec = date
            form.channel = channel
            form.time_rec = time_rec

            form.save()
            log(f'{form.name} Criada pelo: {self.request.user}')

        messages.success(request, "Programas registrados")
        # del request.session['form_data']
        return redirect(reverse('pgms:set-date'))
