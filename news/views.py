from django.shortcuts import render
from news.async_parser.gather_data_technologies import main_technologies
from news.async_parser.gather_data_science import main_science

from news.models import News


def main(request):
    news = News.objects.all().order_by('date').reverse()[0:15]
    r_news = News.objects.order_by('?')[0:20]

    if request.method == 'POST':

        # Ajax запускает обновление каждые 5 минут
        if request.POST.get('Refresh'):
            main_science()
            main_technologies()

        # Ловим запрос перехода на вкладку "Наука"
        elif request.POST.get('Science'):
            science = News.objects.filter(category__category='Наука').order_by('date').reverse()
            r_news = News.objects.filter(category__category='Наука').order_by('?')

            # Получаем список источников в категории "Наука"
            list_of_science = []
            for new in News.objects.filter(category__category='Наука'):
                list_of_science.append(new.name)

            # Получаем список источников в категории "Технологии"
            list_of_technology = []
            for new in News.objects.filter(category__category='Технологии'):
                list_of_technology.append(new.name)

            context = {'news': science, 'r_news': r_news, 'list_of_science': set(list_of_science), 'list_of_technology': set(list_of_technology)}
            return render(request, 'news/main.html', context)

        # Ловим запрос перехода на вкладку "Наука"
        elif request.POST.get('Technologies'):
            technologies = News.objects.filter(category__category='Технологии').order_by('date').reverse()
            r_news = News.objects.filter(category__category='Технологии').order_by('?')

            # Получаем список источников в категории "Наука"
            list_of_science = []
            for new in News.objects.filter(category__category='Наука'):
                list_of_science.append(new.name)

            # Получаем список источников в категории "Технологии"
            list_of_technology = []
            for new in News.objects.filter(category__category='Технологии'):
                list_of_technology.append(new.name)

            context = {'news': technologies, 'r_news': r_news, 'list_of_science': set(list_of_science), 'list_of_technology': set(list_of_technology)}
            return render(request, 'news/main.html', context)

        # Попытка отображения всех новостей
        elif request.POST.get('More'):
            news = News.objects.all().order_by('date').reverse()
            r_news = News.objects.order_by('?')

            # Получаем список источников в категории "Наука"
            list_of_science = []
            for new in News.objects.filter(category__category='Наука'):
                list_of_science.append(new.name)

            # Получаем список источников в категории "Технологии"
            list_of_technology = []
            for new in News.objects.filter(category__category='Технологии'):
                list_of_technology.append(new.name)

            context = {'news': news, 'r_news': r_news, 'list_of_science': set(list_of_science), 'list_of_technology': set(list_of_technology)}
            return render(request, 'news/main.html', context)

        # Ловим запрос на сортировку источников
        elif dict(request.POST).get('dropdown'):
            search = []
            for i in dict(request.POST).get('dropdown'):
                search.append(News.objects.filter(name=i))
            context = {'news': search}
            return render(request, 'news/search.html', context)

    # Получаем список источников в категории "Наука"
    list_of_science = []
    for new in News.objects.filter(category__category='Наука'):
        list_of_science.append(new.name)

    # Получаем список источников в категории "Технологии"
    list_of_technology = []
    for new in News.objects.filter(category__category='Технологии'):
        list_of_technology.append(new.name)

    context = {'news': news, 'r_news': r_news, 'list_of_science': set(list_of_science), 'list_of_technology': set(list_of_technology)}
    return render(request, 'news/main.html', context)

# Отображение поста
def post(request, post_id):
    new = News.objects.get(id=post_id)
    r_news = News.objects.order_by('?')
    context = {'new': new, 'r_news': r_news[0:4]}
    return render(request, 'news/post.html', context)