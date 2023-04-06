from django.forms import (
    ModelForm,
    CharField,
    TextInput,
    ModelChoiceField,
    ModelMultipleChoiceField,
)

from quotes.models import (
    Tag,
    Author,
    Quote,
    User,
)


class TagForm(ModelForm):
    name = CharField(min_length=3, max_length=25, required=True, widget=TextInput())

    class Meta:
        model = Tag
        fields = ['name']


class QuoteForm(ModelForm):
    author = ModelChoiceField(queryset=Author.objects.none())  # noqa
    tags = ModelMultipleChoiceField(queryset=Tag.objects.none())  # noqa

    class Meta:
        model = Quote
        fields = ['quote', 'author', 'tags']

    def __init__(self, user: User, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['author'].queryset = Author.objects.filter(user=user)  # noqa
        self.fields['tags'].queryset = Tag.objects.all()  # noqa


class AuthorForm(ModelForm):
    class Meta:
        model = Author
        fields = ['fullname', 'born_date', 'born_location', 'description']
