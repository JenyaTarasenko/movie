from django.shortcuts import render, redirect
from django.views.generic import View, ListView, DetailView

from .models import *
from .forms import ReviewForm



# class MovieWievs(View):
#     """Список фильмов"""
#     def get(self, request):
#         movies = Movie.objects.all()
#         return render(request, 'movie/index.html', {'movie_list': movies})

class MovieWievs(ListView):
    """Список фильмов"""
    model = Movie
    queryset = Movie.objects.filter(draft=False)#фильтрует поле по умолчанию (не черновик)
    template_name = 'movie/index.html'



    # def get_context_data(self, *args, **kwargs):
    #     """
    #     Метод категории
    #     """
    #     context = super().get_context_data(*args, **kwargs)
    #     context['categories'] = Category.objects.all()
    #     return context

      # прописываем этот метод в templattetags




# class MovieDetail(View):
#     """Детальная информация фильма"""
#     def get(self, request, slug):
#         movies = Movie.objects.get(url=slug)#get метод который получает одну запись pk это id
#         return render(request, 'movie/movie_detail.html', {'movies_list': movies})


class MovieDetail(DetailView):
    """Детальная информация фильма"""
    model = Movie
    slug_field = 'url'#по какому полю нужно искать запесь
    template_name = 'movie/movie_detail.html'


class AddReview(View):
    """отзывы"""
    # def post(self, request, pk):
    #   print(request.POST)
    #   return redirect("/")
    def post(self, request, pk):
        form = ReviewForm(request.POST)
        movie = Movie.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            form.movie = movie
            form.save()
        return redirect("/")


class ActorView(DetailView):
    """Вывод информации о актере"""
    model = Actor
    template_name = 'movie/actor.html'
    slug_field = "name"#по полю name Actor


