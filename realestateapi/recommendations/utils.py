from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .models import User, Recommendation
from bookmarks.models import BookMark
from listings.models import Listing

from django.db.models import Count


def calculate_user_similarity(user_a_id):
    user_a = User.objects.get(id=user_a_id)
    print("\n\nvalue_a_A-a\n\n", user_a_id, '\n\n', user_a)
    # Retrieve user A's recommendations and bookmarks
    user_a_recommendations = Recommendation.objects.filter(user=user_a).values_list('last_search', flat=True)
    print("\n\nuser recommendations\n\n",user_a_recommendations)
    user_a_bookmarks = BookMark.objects.filter(user=user_a).values_list('listing__id', flat=True)
    print("\n\nuser bookmarks\n\n",user_a_recommendations)

    # Retrieve all users' recommendations and bookmarks
    all_users = User.objects.exclude(id=user_a.id)
    user_profiles = []
    user_ids = []
    print("\n\nall users\n\n",all_users)
    for user in all_users:
        recommendations = Recommendation.objects.filter(user=user).values_list('last_search', flat=True)
        bookmarks = BookMark.objects.filter(user=user).values_list('listing__id', flat=True)
        print("\n\nuser recommendation\n\n",recommendations, '\n\n',bookmarks)
        user_profile = list(recommendations) + list(bookmarks)
        user_profiles.append(' '.join(map(str, user_profile)))
        user_ids.append(user.id)
    
    print("\n\nuser profiles\n\n",user_profile, '\n\n',user_ids)
    # Convert recommendations and bookmarks to vectors
    vectorizer = CountVectorizer()
    user_profiles_vectors = vectorizer.fit_transform(user_profiles)
    user_a_profile = list(user_a_recommendations) + list(user_a_bookmarks)
    user_a_vector = vectorizer.transform([' '.join(map(str, user_a_profile))])
    
    # Calculate cosine similarity between user A and all other users
    similarities = cosine_similarity(user_a_vector, user_profiles_vectors)
    
    # Sort users by similarity (descending)
    similar_users_indices = similarities.argsort()[0][::-1]
    similar_users = [(user_ids[idx], similarities[0, idx]) for idx in similar_users_indices]
    print("\n\n values of he user recommednation\n\n", similar_users)
    return similar_users

def generate_recommendations(user_a_id, top_n=5):
    print("\n\nvalue\n\n", user_a_id)
    similar_users = calculate_user_similarity(user_a_id)
    print('\n\n\n\nsimilar users \n\n', similar_users)
    
    # Get the top-N similar users
    top_similar_users = similar_users[:top_n]
    
    # Aggregate recommendations from similar users
    recommended_listings = {}
    
    for similar_user_id, similarity in top_similar_users:
        recommendations = Recommendation.objects.filter(user_id=similar_user_id)
        for rec in recommendations:
            listing_id = rec.interest.id
            if listing_id not in recommended_listings:
                recommended_listings[listing_id] = similarity
            else:
                recommended_listings[listing_id] += similarity
    
    print("\n\n values of he user recommednationmmmmmmf\n\n", recommended_listings)
    # Sort listings by aggregated similarity score (descending)
    sorted_recommended_listings = sorted(recommended_listings.items(), key=lambda x: x[1], reverse=True)
    
    # Retrieve the actual listing objects
    recommended_listings = [Listing.objects.get(id=listing_id) for listing_id, _ in sorted_recommended_listings[:top_n]]
    
    return recommended_listings
