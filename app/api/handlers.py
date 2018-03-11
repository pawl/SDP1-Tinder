from django.http import HttpResponse, HttpResponseNotFound, Http404

from rest_framework.renderers import JSONRenderer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view

from app.models import UserProfile, SwipeAction, Event
from app.serializers import UserProfileSerializer, SwipeActionSerializer


def get_active_event():
    active_events = Event.objects.filter(is_active=True)
    if active_events.count() == 0:
        raise Http404('<p>No event is active.</p>')
    else:
        return active_events.first()


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """

    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


@api_view(('GET',))
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'swipe-right': reverse('swipe-right', request=request, format=format),
        'swipe-left': reverse('swipe-left', request=request, format=format),
        'swipe-actions': reverse('swipe-action-list', request=request, format=format),
        # 'events': reverse('event-list', request=request, format=format),
        # 'stats': reverse('stats', request=request, format=format)
    })


class UserVoteStats(APIView):
    """
    List stats pertaining to user votes
    """

    def get(self, request, format=None):
        event = get_active_event()
        users = event.participants.order_by('-num_votes', 'first_name').all()
        series = []
        for i, user in enumerate(users):
            datapoint = {
                'name': user.full_name(),
                'y': user.get_num_votes(event=event)
            }
            if i == 0:
                datapoint['selected'] = True
            series.append(datapoint)

        return Response({'series': series})


class UserSwipeStats(APIView):
    """
    List stats pertaining to user votes
    """

    def get(self, request, is_percentage=False, format=None):
        event = get_active_event()
        users = event.participants.order_by('-num_right_swipes', 'num_left_swipes', 'first_name').all()
        user_data = UserProfileSerializer(users, many=True).data
        if is_percentage:
            for user_obj, user_dict in zip(users, user_data):
                user_dict['right'] = user_obj.get_pct_right_swipes(event=event)
                user_dict['left'] = 100 - user_dict['right'] if user_dict['right'] else None
        else:
            for user_obj, user_dict in zip(users, user_data):
                user_dict['right'] = user_obj.get_num_right_swipes(event=event)
                user_dict['left'] = user_obj.get_num_left_swipes(event=event)

        combined_user_data = [ (i, j) for i, j in zip(users, user_data)]
        combined_user_data = sorted(combined_user_data, key=lambda k: -k[1]['right'])

        categories = []
        right = []
        left = []
        for user_obj, user_dict in combined_user_data:
            categories.append(user_obj.full_name())
            right.append(user_dict['right'])
            left.append(user_dict['left'])
        series = [{
                'name': '% Right Swipes' if is_percentage else '# Right Swipes',
                'data': right
            }, {
                'name': '% Left Swipes' if is_percentage else '# Left Swipes',
                'data': left
            }]
        data = {
            'series': series,
            'categories': categories
        }
        return Response(data)


class UserProfileList(APIView):
    """
    List all users, or create a new user.
    """

    def get(self, request, format=None):
        users = UserProfile.objects.all()
        serializer = UserProfileSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """

    def get_object(self, pk):
        try:
            return UserProfile.objects.get(pk=pk)
        except UserProfile.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserProfileSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SwipeActionOnUser(APIView):

    def post(self, request, format=None, **kwargs):

        is_right = kwargs.get('is_right', None)
        is_vote = kwargs.get('is_vote', False)
        user_pk = self.kwargs.get('uid', None)

        active_events = Event.objects.filter(is_active=True)
        if active_events.count() == 0:
            return HttpResponseNotFound('<p>No event is active.</p>')
        else:
            active_event = active_events.first()

        swipe_action_data = {
            'on_user': user_pk,
            'is_right': is_right,
            'is_vote': is_vote,
            'event': active_event.pk
        }
        serializer = SwipeActionSerializer(data=swipe_action_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(('serializer invalid!', serializer.errors))
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None, **kwargs):
        user_pk = self.kwargs.get('uid', None)
        swipes = SwipeAction.objects.filter(on_user=user_pk, is_valid=True).all()
        serializer = SwipeActionSerializer(swipes, many=True)
        return Response(serializer.data)


class SwipeActionList(APIView):
    """
    List all users, or create a new user.
    """

    def get(self, request, format=None):
        swipes = SwipeAction.objects.all()
        serializer = SwipeActionSerializer(swipes, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = SwipeActionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SwipeActionDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """

    def get_object(self, user_pk):
        try:
            return SwipeAction.objects.get(pk=user_pk)
        except SwipeAction.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        swipe = self.get_object(pk)
        serializer = SwipeActionSerializer(swipe)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        swipe = self.get_object(pk)
        serializer = SwipeActionSerializer(swipe, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        swipe = self.get_object(pk)
        swipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
