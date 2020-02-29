from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.views.decorators.http import require_POST


from .models import Message

@require_POST
def close_message(request):
    if 'message_id' in request.POST:
        try:
            message = Message.objects.get(pk=request.POST['message_id'])
        except ObjectDoesNotExist:
            return JsonResponse(status=404, data={"message": "Message not found"})
        else:
            message.status =Message.ST_READING
            message.save()
            return JsonResponse(status=200, data={"message": "Message reading"})
