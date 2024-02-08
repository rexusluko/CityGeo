import requests
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from decouple import config

from .models import City
from .serializers import CitySerializer, CityCreateSerializer
from .utils import GeoUtils


class EmptySerializer:
    pass


class CityViewSet(GenericViewSet, ListModelMixin):
    permission_classes = [IsAuthenticated]
    queryset = City.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return CitySerializer
        elif self.action == "create":
            return CityCreateSerializer
        else:
            return EmptySerializer

    def create(self, request, *args, **kwargs):
        city_name = request.data.get('name')

        if not city_name:
            return Response({'error': 'City name is required'}, status=status.HTTP_400_BAD_REQUEST)
        if City.objects.filter(name=city_name).first():
            return Response({'error': f'{city_name} already added'}, status=status.HTTP_400_BAD_REQUEST)

        url = "https://graphhopper.com/api/1/geocode"
        query = {
            "q": city_name,
            "locale": "en",
            "key": config('GRAPHHOPPER_KEY')
        }

        try:
            response = requests.get(url, params=query)
            response.raise_for_status()
            data = response.json()

            if data.get('hits'):
                hit = data['hits'][0]
                city_lat = hit['point']['lat']
                city_lon = hit['point']['lng']

                city = City.objects.create(name=city_name, latitude=city_lat, longitude=city_lon)
                serializer = CitySerializer(city)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'Failed to retrieve city data'}, status=status.HTTP_400_BAD_REQUEST)
        except requests.RequestException as e:
            return Response({'error': f'Failed to connect to external API: {str(e)}'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({'error': f'Failed to create city: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(
        parameters=[
            OpenApiParameter(name='latitude', type=float,default=0),
            OpenApiParameter(name='longitude', type=float,default=0),
            OpenApiParameter(name='number_of_cities', type=int,default=0)
        ]
    )
    @action(methods=["GET"], detail=False)
    def get_closest_cities(self, request: Request):
        number_of_cities = int(request.query_params.get('number_of_cities'))
        if number_of_cities <= 0:
            return Response({'message': 'number_of_cities must be a positive number'}, status=status.HTTP_400_BAD_REQUEST)
        latitude = float(request.query_params.get('latitude'))
        longitude = float(request.query_params.get('longitude'))
        all_cities = City.objects.all()
        distances = []
        for city in all_cities:
            distance = GeoUtils.get_distance(latitude, longitude, city.latitude, city.longitude)
            distances.append((city.name, distance))
        closest_cities = sorted(distances, key=lambda x: x[1])[:number_of_cities]
        if len(closest_cities) < number_of_cities:
            return Response({'message': 'Less cities found than requested','closest_cities': closest_cities}, status=status.HTTP_200_OK)
        return Response({'closest_cities': closest_cities}, status=status.HTTP_200_OK)
