from django.http import JsonResponse
from django.db.models import Avg, Min, Max, Count, Q
from .models import Product
import pandas as pd
import numpy as np
from rest_framework.decorators import api_view
from rest_framework.response import Response


def _products_df():
    rows = list(Product.objects.values("name", "category", "price", "rating", "review_count"))
    df = pd.DataFrame(rows)
    if not df.empty:
        df["price"] = pd.to_numeric(df["price"])
        df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
        df["review_count"] = pd.to_numeric(df["review_count"])
    return df

@api_view(['GET'])
def summary(request):
    qs = Product.objects.all()
    stats = qs.aggregate(
        total_products=Count("id"),
        average_price=Avg("price"),
        minimum_price=Min("price"),
        maximum_price=Max("price"),
        average_rating=Avg("rating"),
        total_reviews=Count("id"),
    )
    stats["total_reviews"] = sum(qs.values_list("review_count", flat=True))
    # Pandas is used to calculate a robust median for the dashboard.
    df = _products_df()
    stats["median_price"] = round(float(np.median(df["price"])), 2) if not df.empty else 0
    for key in ["average_price", "minimum_price", "maximum_price", "average_rating"]:
        if stats[key] is not None:
            stats[key] = round(float(stats[key]), 2)
    return Response(stats)


@api_view(['GET'])
def categories(request):
    qs = Product.objects.values("category").annotate(
        product_count=Count("id"), average_price=Avg("price"), average_rating=Avg("rating")
    ).order_by("-product_count")
    data = [{**x, "average_price": round(float(x["average_price"] or 0), 2),
             "average_rating": round(float(x["average_rating"] or 0), 2)} for x in qs]
    return Response({"results": data})

def top_rated(request):
    qs = Product.objects.filter(rating__isnull=False).order_by("-rating", "-review_count")[:10]
    from .serializers import ProductSerializer
    return JsonResponse({"results": ProductSerializer(qs, many=True).data})

def price_distribution(request):
    df = _products_df()
    if df.empty:
        return JsonResponse({"results": []})
    bins = [0, 500, 1000, 2000, 5000, float("inf")]
    labels = ["0-499", "500-999", "1000-1999", "2000-4999", "5000+"]
    df["price_range"] = pd.cut(df["price"], bins=bins, labels=labels, right=False)
    counts = df["price_range"].value_counts(sort=False)
    return JsonResponse({"results": [{"range": str(k), "count": int(v)} for k, v in counts.items()]})

def rating_distribution(request):
    qs = Product.objects.aggregate(
        unrated=Count("id", filter=Q(rating__isnull=True)),
        one=Count("id", filter=Q(rating__gte=0, rating__lt=1)),
        two=Count("id", filter=Q(rating__gte=1, rating__lt=2)),
        three=Count("id", filter=Q(rating__gte=2, rating__lt=3)),
        four=Count("id", filter=Q(rating__gte=3, rating__lt=4)),
        five=Count("id", filter=Q(rating__gte=4, rating__lte=5)),
    )
    labels = ["0-1", "1-2", "2-3", "3-4", "4-5", "Unrated"]
    keys = ["one", "two", "three", "four", "five", "unrated"]
    return JsonResponse({"results": [{"range": label, "count": qs[key]} for label, key in zip(labels, keys)]})
