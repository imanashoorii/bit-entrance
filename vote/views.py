from django.db.models import Avg
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Article, Rating
from .serializers import ArticleSerializer, RatingSerializer


class ArticleListView(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        data = serializer.data
        for article_data in data:
            article_id = article_data['id']

            if self.request.user.is_authenticated:
                ratings = Rating.objects.filter(article_id=article_id, user=self.request.user)
            else:
                ratings = Rating.objects.filter(article_id=article_id)

            num_ratings = ratings.count()
            avg_rating = ratings.aggregate(Avg('score'))['score__avg']
            article_data['num_ratings'] = num_ratings
            article_data['avg_rating'] = avg_rating

        return Response(data)

    def perform_create(self, serializer):
        serializer.save()

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response({'success': 'Article added successfully'}, status=status.HTTP_201_CREATED)


class RateArticleView(generics.CreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user
        article_id = kwargs.get('article_id')

        existing_rating = Rating.objects.filter(user=user, article_id=article_id).first()

        if existing_rating:
            serializer = self.get_serializer(existing_rating, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=user, article_id=article_id)

        return Response({'success': 'Rating added successfully'}, status=status.HTTP_201_CREATED)
