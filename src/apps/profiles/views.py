from ajax_datatable.views import AjaxDatatableView
from django.views.generic import ListView, View

from django.http import JsonResponse
from django.template.loader import render_to_string
from apps.profiles.models import Profile

from django.contrib.postgres.search import TrigramSimilarity
from django.db.models.functions import Cast
from django.db.models import CharField


class ProfileListView(ListView):
    model = Profile
    template_name = 'profiles/list2.html'
    context_object_name = 'profiles'


class ProfileTableView(View):
    def post(self, request):
        data = {}
        if 'search' in request.POST.keys():
            search = request.POST['search']
            vector_trgm = TrigramSimilarity('phone', search) + TrigramSimilarity('username', search) \
                          + TrigramSimilarity('full_name', search) + TrigramSimilarity(Cast('telegram_id', output_field=CharField()), search)
            context = {'rows': Profile.objects.annotate(similarity=vector_trgm).filter(similarity__gt=0.35).order_by('-similarity')}
        else:
            context = {'rows': Profile.objects.all()}
        data['rows'] = render_to_string('profiles/row.html',
                                        context, request=request)
        return JsonResponse(data)


class ProfileDatatableView(AjaxDatatableView):
    model = Profile
    title = 'Пользователи Telegram'
    last_by = 'registration_date'
    show_date_filters = True

    CHOICES_GROUP = (
        (0, 'Все'),
        (1, 'Только подписчики'),
        (2, 'Все, исключая подписчиков'),
        (3, 'Кто не продлил'),
        (4, 'Кто не продлил более 1 мес'),
        (5, 'Ни разу не платил')
    )

    column_defs = [
        {'name': 'id', 'title': 'ID', 'visible': True, 'searchable': False},
        {'name': 'telegram_id', 'visible': True, 'searchable': True},
        {'name': 'username', 'visible': True, 'searchable': True},
        {'name': 'first_name', 'visible': False, 'searchable': False},
        {'name': 'last_name', 'visible': False, 'searchable': False},
        {'name': 'phone', 'visible': True, 'searchable': True},
        {'name': 'full_name', 'visible': False, 'searchable': False},
        {'name': 'registration_date', 'visible': True, 'searchable': False},
        {'name': 'last_action_date', 'visible': False, 'searchable': False},
        {'name': 'activity', 'visible': False, 'searchable': False},
        {'name': 'count_actions_in_current_day', 'visible': False, 'searchable': False},
        {'name': 'count_days_in_bot', 'visible': False, 'searchable': False},
        {'name': 'count_actions', 'visible': False, 'searchable': False},
    ]

    def customize_row(self, row, obj):
        row['telegram_id'] = f"""<a href="{row['pk']}">{row['telegram_id']}</a>"""
