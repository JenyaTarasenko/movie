from django.contrib import admin
from ckeditor.widgets import CKEditorWidget
from django import forms

from .models import *



class MovieAdminForm(forms.ModelForm):
    """
    форма расширяющая админку description
    """
    description = forms.CharField(widget=CKEditorWidget())#азвание модели название поля
    class Meta:
        model = Movie
        fields = '__all__'


@admin.register(Category)#регистрация через декоратор
class CategoryAdmin(admin.ModelAdmin):
    """
     категории
    """
    list_display = ('id', 'name', 'description', 'url')
    list_display_links = ('name',)#имя поля которое будет ссылкой


    # def get_image(self, obj):
    #     """
    #     метод выводит изображение в админку
    #     """
    #     return mark_safe(f'<img src={obj.image.url} width="50" height="60"')
    #
    # get_image.short_description = "Изображение"




class ReviewInline(admin.StackedInline):
    """
    Передать все отзывы к фильму класс должен
    быть написан выше данный атрибут работает many-to-many, faregn-key
    """
    model = Reviews
    extra = 1#доп поле



class MovieShotsInline(admin.StackedInline):
    """
    привязать кадры из фильма к фильму в админке
    """
    model = MovieShots
    extra = 1




@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    """
    Фильмы поиск
    """
    list_display = ('title', 'category', 'description', 'url', 'draft')
    list_filter = ('category', 'year', 'actors',)#фильтрация фильмов по категориям
    search_fields = ('title', 'category__name')#фильтрация поля по title,category
    inlines = [ReviewInline, MovieShotsInline]#класс подвязан к фильму
    save_on_top = True#меню вверху
    form = MovieAdminForm#подключаем форму
    actions = ['publish', 'unpublish']#подключаем методы для форм
    list_editable = ('draft',)#поле для редактирования
    #fields = (("actors", "directors", 'genres')) #поле где можно выбрать свои поля
    fieldsets = (
        (None, {"fields": (("title", "tagline"),)}),
        (None, {"fields": (("description", "poster"),)}),
        #(None, {"fields": (("year", "world_premier", "country"),)}),
        (None, {"fields": (("actors", "directors", "genres", "category"),)}),
        (None, {"fields": (("budget", "fees_in_usa", "fess_in_world"),)}),
        (None, {"fields": (("url", "draft","year"),)}),
    )#поля модели выстроиные в ряд по горизонтали

    def publish(self, request, queryset):
        """
        Снять с публикации
        """
        row_udate = queryset.update(draft=True)
        if row_update == '1':
            massege_bit = '1 запись обновлена'
        else:
            massage_bit = f"{row_update} запись обновлена"
        self.massage_user(request, f"{massage_bit}")



        def unpublish(self, request, queryset):
            """
            Публиковать
            """
            row_update = queryset.update(draft=False)
            if row_udate == '1':
                massage_bit = '1 запись обновлена'
            else:
                massage_bit = f"{row_udate} запись обновлена"
            self.massage_user(request, f"{massage_bit}")

        publish.short_description="Опубликовать"
        publish.allowed_permission = ('cnange')#чтобы применять у пользователя должны быть права

        unpublish.short_description = "Снять с публикации"
        unpublish.allowed_permission = ('cnange')  # чтобы применять у пользователя должны быть права



admin.site.site_title = "Кино"# поменять в админке в верхней части приложение название
admin.site.site_header = "Кино"# поменять в админке









@admin.register(Reviews)
class ReviewAdmin(admin.ModelAdmin):
    """
    Отзывы
    """
    list_display = ('name', 'email', 'movie', 'parent', 'id')
    readonly_fields = ('name', 'email')#поля скрыты от редактирования





#admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre)
#admin.site.register(Movie)
admin.site.register(MovieShots)
admin.site.register(Actor)
admin.site.register(Rating)
admin.site.register(RatingStar)
#admin.site.register(Reviews)


