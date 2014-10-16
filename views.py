from django.http import HttpResponse
from django.http import HttpRequest
from django.template.response import TemplateResponse
from zks.models import ArticleIntro, ArticleTags
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User


def pagination(queryset, parameter, amount):
    """

    :param queryset:
    :param parameter:
    :return:
    """
    if parameter is None:
        return queryset[:amount], queryset.last().pk
    else:
        for index, item in enumerate(queryset):
            if item.pk == parameter:
                return queryset[index + 1: index + 1 + amount], item.pk


def get_list_from_tag(request, tag):
    """
    This function returns a list of articles for a tag

    :param HttpRequest request:
    :param String tag:
    :return HttpResponse:
    """
    amount = 10
    context = dict()
    parameter = request.GET.get('pagination', None)
    get_parameter = None

    try:
        target_tag = ArticleTags.objects.get(name__iexact=tag)
        articles = target_tag.articleintro_set.all().exclude(placeholder__page__publisher_is_draft=False).order_by('date')
        articles, get_parameter = pagination(articles, parameter, amount)
    except ObjectDoesNotExist:
        articles = None

    context.update({
        'articles': articles,
        'pagination': get_parameter
    })

    return TemplateResponse(request, 'tag_author.html', context)


def get_list_from_author(request, firstname, lastname):
    """
    Returns a list of articles for a author

    :param HttpRequest request:
    :param string firstname:
    :param string lastname:
    :return HttpResponse:
    """

    amount = 10
    context = dict()
    parameter = request.GET.get('pagination', None)
    get_parameter = None

    try:
        target_user = User.objects.get(first_name__iexact=firstname, last_name__iexact=lastname)
        articles = target_user.articleintro_set.all().exclude(placeholder__page__publisher_is_draft=False).order_by('date')
        articles, get_parameter = pagination(articles, parameter, amount)
    except ObjectDoesNotExist:
        articles = None

    context.update({
        'articles': articles,
        'pagination': get_parameter
    })

    return TemplateResponse(request, 'tag_author.html', context)