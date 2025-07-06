import random
from .models import Quote
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from .forms import QuoteForm


def random_quote(request):
    quotes = list(Quote.objects.all())
    weights = [quote.weight for quote in quotes]
    selected_quote = random.choices(quotes, weights=weights, k=1)[0]
    selected_quote.views += 1
    selected_quote.save()
    return render(request, 'random_quote.html', {'quote': selected_quote})


def like_quote(request, quote_id):
    quote = get_object_or_404(Quote, id=quote_id)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'like':
            quote.likes += 1
        elif action == 'dislike':
            quote.dislikes += 1
        quote.save()

    return render(request, 'random_quote.html', {'quote': quote})


def top_quotes(request):
    sort_by = request.GET.get('sort', 'likes')
    if sort_by == 'dislikes':
        order_field = '-dislikes'
    elif sort_by == 'views':
        order_field = '-views'
    else:
        order_field = '-likes'
    quotes = Quote.objects.all().order_by(order_field)[:10]
    context = {
        'quotes': quotes,
        'current_sort': sort_by,
    }
    return render(request, 'top_quotes.html', context)


def add_quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('random_quote')
    else:
        form = QuoteForm()

    return render(request, 'add_quote.html', {'form': form})
