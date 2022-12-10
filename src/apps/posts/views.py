from django.http import JsonResponse

from apps.posts.services.post import delete_user_post


def test_view(request):
    print(delete_user_post(1, 1234))
    return JsonResponse({"success": True})
