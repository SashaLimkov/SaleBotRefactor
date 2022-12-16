from django.http import JsonResponse

from apps.posts.services.post import get_formatted_user_settings_posts_by_compilation_id
from apps.profiles.services.metric import update_metrics_profiles_for_past_day
from apps.profiles.services.profile import create_user, get_profile_is_helper, update_last_action_date_profile
from apps.profiles.services.subscription import get_user_active_subscription, decrement_number_of_days_left
from apps.settings.services.course import add_or_update_course_user
from apps.settings.services.settings_user import update_field_settings


def test_view(request):
    print(get_formatted_user_settings_posts_by_compilation_id(1, 12341))
    return JsonResponse({"success": True})
