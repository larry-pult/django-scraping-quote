from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Quote, Author, Tag
from .scraping import scrape_quotes


# Create your views here.
def index(request):
    return HttpResponseRedirect("/quote/")


def quote(request):
    quotes = Quote.objects.all()
    context = {
        "title": "list of all quotes:",
        "quotes": quotes
    }
    return render(request, "web_scraping/quote.html", context=context)


def tag(request):
    tags = Tag.objects.all().order_by("tag")
    context = {
        "tags": tags
    }
    return render(request, "web_scraping/tag.html", context=context)


def author(request):
    authors = Author.objects.all().order_by("author")
    context = {
        "authors": authors
    }
    return render(request, "web_scraping/author.html", context=context)


def quote_by_quote_id(request, quote_id):
    quotes = Quote.objects.get(pk=quote_id)
    context = {
        "title": f"quote #{quote_id}:",
        "quotes": [quotes]
    }
    return render(request, "web_scraping/quote.html", context=context)


def quote_by_tag_id(request, tag_id):
    tag = Tag.objects.get(pk=tag_id)
    quotes = Quote.objects.filter(tags=tag)
    context = {
        "title": f"quotes with tag \"{tag.tag}\":",
        "quotes": quotes
    }
    return render(request, "web_scraping/quote.html", context=context)


def quote_by_author_id(request, author_id):
    author = Author.objects.get(pk=author_id)
    quotes = Quote.objects.filter(author=author)
    context = {
        "title": f"quotes with author \"{author.author}\":",
        "quotes": quotes
    }
    return render(request, "web_scraping/quote.html", context=context)


def run_scraping(request):
    # scrape all quote objects
    quote_list = []
    for page in range(1, 100):
        quotes_in_page = scrape_quotes(page)
        if not quotes_in_page:
            break
        quote_list.extend(quotes_in_page)
    print(quote_list)

    # insert the scraping results into database
    update_scraping_results(quote_list)

    return HttpResponse("Scraping done. Sorry for the wait, I didn't implement async")


def update_scraping_results(quote_list):
    # get all unique authors and tags
    author_set = set()
    tag_set = set()
    for quote_object in quote_list:
        author_set.add(quote_object["author"])
        tag_set.update(quote_object["tags"])

    # insert author objects into database
    for author in author_set:
        if Author.objects.filter(author=author).exists():
            continue

        Author(author=author).save()

    # insert tag objects into database
    for tag in tag_set:
        if Tag.objects.filter(tag=tag).exists():
            continue

        Tag(tag=tag).save()

    # insert quote objects into database
    for quote_object in quote_list:
        if Quote.objects.filter(quote=quote_object["quote"]).exists():
            continue

        new_quote = Quote(quote=quote_object["quote"])
        new_quote.author = Author.objects.get(author=quote_object["author"])

        new_quote.save()
        for tag in quote_object["tags"]:
            new_quote.tags.add(Tag.objects.get(tag=tag))

        new_quote.save()
