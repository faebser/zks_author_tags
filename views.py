from django.http import HttpResponse
from django.http import HttpRequest
from django.template.response import TemplateResponse
from zks.models import ArticleIntro, ArticleTags
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User


def pagination(queryset, parameter, amount, amountSmall, amountThreeCol):
    """

    :param queryset:
    :param parameter:
    :param int amount:
    :param int amountSmall:
    :param int amountThreeCol:
    :return:
    """
    total_amount = amount + amountSmall + amountThreeCol
    if parameter is None:
        return queryset[:amount], queryset[amount:amount + amountSmall], queryset[amountSmall:amountSmall + amountThreeCol], queryset.last().pk
    else:
        for index, item in enumerate(queryset):
            if item.pk == parameter:
                return None, None, queryset[index + 1: index + 1 + amountThreeCol], item.pk


def get_list_from_tag(request, tag):
    """
    This function returns a list of articles for a tag

    :param HttpRequest request:
    :param String tag:
    :return HttpResponse:
    """
    amount = 2
    context = dict()
    parameter = request.GET.get('pagination', None)
    get_parameter = None

    try:
        target_tag = ArticleTags.objects.get(url__iexact=tag)
        articles = target_tag.articleintro_set.all().exclude(placeholder__page__publisher_is_draft=False).order_by('date').exclude(placeholder__page=None)
        onecol, twocol, threecol, get_parameter = pagination(articles, parameter, amount, 4)
    except ObjectDoesNotExist:
        onecol = None
        twocol = None
        threecol = None

    context.update({
        'onecol': onecol,
        'twocol': twocol,
        'threecol': threecol,
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

    amount = 2
    context = dict()
    parameter = request.GET.get('pagination', None)
    get_parameter = None

    try:
        target_user = User.objects.get(first_name__iexact=firstname, last_name__iexact=lastname)
        articles = target_user.articleintro_set.all().exclude(placeholder__page__publisher_is_draft=False).order_by('date').exclude(placeholder__page=None)
        articles, small_articles, get_parameter = pagination(articles, parameter, amount, 40)
    except ObjectDoesNotExist:
        onecol = None
        twocol = None
        threecol = None

    context.update({
        'articles': articles,
        'small-articles': small_articles,
        'pagination': get_parameter
    })

    return TemplateResponse(request, 'tag_author.html', context)