
from django.views.generic import ListView, DetailView, TemplateView
from django.core.cache import cache  
from app.models import *
import os
import requests
from dotenv import load_dotenv

load_dotenv()

def fetch_news_from_api(query=None, category=None, page_size=6):
    api_key = os.getenv('NEWS_API_KEY')
    if not api_key:
        print("NewsAPI key not found in environment variables")
        return []
    
    base_url = 'https://newsapi.org/v2/top-headlines'
    
    # Create cache key based on parameters
    cache_key = f"news_api_{query}_{category}_{page_size}"
    cached_data = cache.get(cache_key)
    if cached_data:
        return cached_data
    
    params = {
        'apiKey': api_key,
        'pageSize': page_size,
        'language': 'en',
        'country': 'us'
    }
    
    if query:
        params['q'] = query
    if category:
        params['category'] = category
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json().get('articles', [])
        
        cache.set(cache_key, data, timeout=900)
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching news: {e}")
        return []

class HomeView(ListView):
    model = News
    template_name = 'news.html'
    context_object_name = 'news_list'
    paginate_by = 6
    ordering = ['-created_at'] 

    def get_queryset(self):
        queryset = super().get_queryset().select_related('category')
        category = self.request.GET.get('category')
        search_query = self.request.GET.get('search')
        
        if category and category != 'all':
            queryset = queryset.filter(category__id=category)
        
        if search_query:
            queryset = queryset.filter(title__icontains=search_query)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
       
        category = self.request.GET.get('category')
        search_query = self.request.GET.get('search')
        
       
        api_news = fetch_news_from_api(
            query=search_query,
            category=category,
            page_size=6
        )
        
        formatted_api_news = []
        for news in api_news:
            formatted_news = {
                'title': news.get('title', ''),
                'description': news.get('description', ''),
                'url': news.get('url', '#'),
                'urlToImage': news.get('urlToImage', ''),
                'publishedAt': news.get('publishedAt', ''),
                'source': {'name': news.get('source', {}).get('name', 'API News')}
            }
            formatted_api_news.append(formatted_news)
        
        context['api_news_list'] = formatted_api_news
        context['categories'] = Category.objects.all()
        
        context['search_query'] = search_query
        
        return context