from django.http import HttpResponse, Http404

from rest_framework.renderers import JSONRenderer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view

from app.models import Image, SwipeAction
from app.serializers import ImageSerializer, SwipeActionSerializer


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
        'images': reverse('image-list', request=request, format=format),
        'swipe-right': reverse('swipe-right', request=request, format=format),
        'swipe-left': reverse('swipe-left', request=request, format=format),
        'swipe-actions': reverse('swipe-action-list', request=request, format=format),
        # 'stats': reverse('stats', request=request, format=format)
    })


class ImageVoteStats(APIView):
    """
    List stats pertaining to image votes
    """

    def get(self, request, format=None):
        images = Image.objects.all()
        series = []
        for i, image in enumerate(images):
            datapoint = {
                'name': image.name,
                'y': image.num_votes,
            }
            if i == 0:
                datapoint['selected'] = True
            series.append(datapoint)

        return Response({'series': series})


class ImageSwipeStats(APIView):
    """
    List stats pertaining to image votes
    """

    def get(self, request, is_percentage=False, format=None):
        images = Image.objects.all()
        image_data = ImageSerializer(images, many=True).data
        if is_percentage:
            for image_obj, image_dict in zip(images, image_data):
                image_dict['right'] = image_obj.get_pct_right_swipes()
                image_dict['left'] = 100 - image_dict['right'] if image_dict['right'] else None
        else:
            for image_obj, image_dict in zip(images, image_data):
                image_dict['right'] = image_obj.num_right_swipes
                image_dict['left'] = image_obj.num_left_swipes

        combined_image_data = [(i, j) for i, j in zip(images, image_data)]
        combined_image_data = sorted(combined_image_data, key=lambda k: -k[1]['right'])

        categories = []
        right = []
        left = []
        for image_obj, image_dict in combined_image_data:
            categories.append(image_obj.name)
            right.append(image_dict['right'])
            left.append(image_dict['left'])
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


class ImageList(APIView):
    """
    List all images, or create a new image.
    """

    def get(self, request, format=None):
        images = Image.objects.all()
        serializer = ImageSerializer(images, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ImageDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """

    def get_object(self, pk):
        try:
            return Image.objects.get(pk=pk)
        except Image.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        image = self.get_object(pk)
        serializer = ImageSerializer(image)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        image = self.get_object(pk)
        serializer = ImageSerializer(image, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        image = self.get_object(pk)
        image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SwipeActionOnImage(APIView):

    def post(self, request, format=None, **kwargs):
        is_right = kwargs.get('is_right', None)
        is_vote = kwargs.get('is_vote', False)
        image_pk = self.kwargs.get('uid', None)

        swipe_action_data = {
            'on_image': image_pk,
            'is_right': is_right,
            'is_vote': is_vote,
        }
        serializer = SwipeActionSerializer(data=swipe_action_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(('serializer invalid!', serializer.errors))
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None, **kwargs):
        image_pk = self.kwargs.get('uid', None)
        swipes = SwipeAction.objects.filter(on_image=image_pk, is_valid=True).all()
        serializer = SwipeActionSerializer(swipes, many=True)
        return Response(serializer.data)


class SwipeActionList(APIView):
    """
    List all images, or create a new image.
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

    def get_object(self, image_pk):
        try:
            return SwipeAction.objects.get(pk=image_pk)
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
