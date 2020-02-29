from .models import Message


def messages_for_user(request):
    if request.user.is_authenticated:
        messages = Message.objects.select_related(
            "sender", "recipient", "requests", "idea", "task", "feedback"
        ).filter(recipient=request.user). \
            filter(status=Message.ST_WAITNG).order_by('-created_at')
        # messages_requests = Message.objects.exclude(requests__isnull=True).filter(status=Message.ST_WAITNG,
        #                                                                           recipient=request.user).count
        # messages_idea = Message.objects.exclude(idea__isnull=True).filter(status=Message.ST_WAITNG,
        #                                                                   recipient=request.user).count
        # messages_task = Message.objects.exclude(task__isnull=True).filter(status=Message.ST_WAITNG,
        #                                                                   recipient=request.user).count
        # messages_feedback = Message.objects.exclude(feedback__isnull=True).filter(status=Message.ST_WAITNG,
        #                                                                           recipient=request.user).count
        return {
                # 'messages_requests': messages_requests,
                # 'messages_idea': messages_idea,
                'messages_for_user': messages,
                # 'messages_task': messages_task,
                # 'messages_feedback': messages_feedback,
                }
    return {}
