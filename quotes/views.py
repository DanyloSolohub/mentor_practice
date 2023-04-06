from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.db import IntegrityError
from django.db.models import Count
from django.views.generic import UpdateView, DeleteView, View
from django.core.paginator import Paginator
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from quotes.models import Tag, Author, Quote
from quotes.forms import QuoteForm, TagForm, AuthorForm
from quotes.service.scrape_quotes import scrape_quotes


class AuthorUpdateView(UpdateView):
    model = Author
    fields = ['fullname', 'born_date', 'born_location', 'description']
    template_name = 'quote/edit_author.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        return obj if obj.user == self.request.user else Http404()

    def get_success_url(self):
        return reverse_lazy('quote:author', kwargs={'author': self.object.fullname})


class QuoteUpdateView(UpdateView):
    model = Quote
    fields = ['quote', 'author', 'tags']
    success_url = reverse_lazy('quote:index')
    template_name = 'quote/edit_quote.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        return obj if obj.user == self.request.user else Http404()

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url

        return self.success_url


class QuoteRemoveView(DeleteView):
    model = Quote
    success_url = reverse_lazy('quote:index')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        return obj if obj.user == self.request.user else Http404()

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url

        return redirect('quote:index')


class QuoteView(View):
    quotes_per_page = 10
    template_get = 'quote/quotes.html'
    template_add = 'quote/add_quote.html'
    form_class = QuoteForm
    model = Quote

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'GET':
            if 'add' in request.path:
                return self.get_form(request)
            elif 'scrape' in request.path:
                return self.scrape(request)

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        match kwargs:
            case {'tag': tag}:
                quotes = self.model.objects.filter(tags__name=tag).order_by('-id')  # noqa
            case _:
                quotes = self.model.objects.all().order_by('-id')  # noqa

        top_tags = Tag.objects.annotate(num_quotes=Count('quote')).order_by('-num_quotes')[:10]  # noqa

        paginator = Paginator(quotes, self.quotes_per_page)

        context = {
            'page_obj': paginator.get_page(request.GET.get('page')),
            'user': request.user,
            'top_tags': top_tags,
            'by_tag': kwargs.get('tag'),
        }
        return render(request, self.template_get, context)

    @method_decorator(login_required)
    def scrape(self, request):
        scrape_quotes(request.user)
        return redirect('quote:index')

    @method_decorator(login_required)
    def get_form(self, request):
        return render(request, self.template_add, {'form': self.form_class(request.user)})

    @method_decorator(login_required)
    def post(self, request):
        form = self.form_class(request.user, request.POST)

        if not form.is_valid():
            return render(request, self.template_add, {'form': form})

        try:
            new_quote = form.save(commit=False)
            new_quote.user = request.user

            new_quote.save()
            form.save_m2m()

        except IntegrityError as e:
            if 'unique constraint "quote of username"' in str(e):
                form.add_error('quote', "This quote already exists. Please add a new quote.")

            return render(request, self.template_add, {'form': form})

        return redirect('quote:index')


class AuthorView(View):
    template_get = 'quote/author.html'
    template_add = 'quote/add_author.html'
    form_class = AuthorForm
    model = Author

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'GET' and 'add' in request.path:
            return self.get_form(request)

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, author: str):
        context = {
            "author": self.model.objects.get(fullname=author),  # noqa
            "user": request.user,
        }
        return render(request, self.template_get, context)

    @method_decorator(login_required)
    def get_form(self, request):
        return render(request, self.template_add, {'form': self.form_class()})

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if not form.is_valid():
            return render(request, self.template_add, {'form': form})

        try:
            new_author = form.save(commit=False)
            new_author.user = request.user
            new_author.save()
        except IntegrityError as e:
            if 'unique constraint "author of username"' in str(e):
                form.add_error("fullname", "Error!!!")

            return render(request, self.template_add, {'form': form})

        return redirect(to='quote:index')


class TagView(View):
    template_name = 'quote/add_tags.html'
    form_class = TagForm
    model = Tag

    @method_decorator(login_required)
    def get(self, request):
        return render(request, self.template_name, {'form': self.form_class()})

    @method_decorator(login_required)
    def post(self, request):
        form = self.form_class(request.POST)

        if not form.is_valid():
            return render(request, self.template_name, {'form': form})

        tag = form.save(commit=False)
        tag.user = request.user
        tag.save()
        return redirect(to='quote:index')
