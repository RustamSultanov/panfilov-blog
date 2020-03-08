from mickroservices.models import Blog, NewsPage
from .models import Message


def messages_for_user(request):
    # if request.user.is_authenticated:
    #     messages = Message.objects.select_related(
    #         "sender", "recipient", "requests", "idea", "task", "feedback"
    #     ).filter(recipient=request.user). \
    #         filter(status=Message.ST_WAITNG).order_by('-created_at')
    #     # messages_requests = Message.objects.exclude(requests__isnull=True).filter(status=Message.ST_WAITNG,
    #     #                                                                           recipient=request.user).count
    #     # messages_idea = Message.objects.exclude(idea__isnull=True).filter(status=Message.ST_WAITNG,
    #     #                                                                   recipient=request.user).count
    #     # messages_task = Message.objects.exclude(task__isnull=True).filter(status=Message.ST_WAITNG,
    #     #                                                                   recipient=request.user).count
    #     # messages_feedback = Message.objects.exclude(feedback__isnull=True).filter(status=Message.ST_WAITNG,
    #     #                                                                           recipient=request.user).count
    #     return {
    #             # 'messages_requests': messages_requests,
    #             # 'messages_idea': messages_idea,
    #             'messages_for_user': messages,
    #             # 'messages_task': messages_task,
    #             # 'messages_feedback': messages_feedback,
    #             }
    blogs_all = Blog.objects.all().order_by(
        '-first_published_at')
    if len(blogs_all) == 0 or len(blogs_all) == 1 or len(blogs_all) == 2 or len(blogs_all) == 3:
        blogs = blogs_all
    else:
        blogs = blogs_all[len(blogs_all) - 3:]
    programs_all = NewsPage.objects.all().order_by(
        '-first_published_at')
    if len(programs_all) == 0 or len(programs_all) == 1 or len(programs_all) == 2 or len(programs_all) == 3:
        programs = programs_all
    else:
        programs = programs_all[len(programs_all) - 3:]
    return {"blogs": blogs, "programs": programs}
