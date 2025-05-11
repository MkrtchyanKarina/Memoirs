from django import forms
from .models import Category, TagPost, Post, Comment


class AddPostForm(forms.ModelForm):
    """ Форма для добавления поста
    title: заголовок (обязательное поле)
    content: одержимое поста (необязательное)
    images: изображение (необязательное)
    is_published: статус статьи - опубликована/черновик (обязательное, по-умолчанию DRAFT/False)
    cat: категория (обязательное)
    tags: теги (необязательное)
    """
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), label="Категория", empty_label="Категория не выбрана", widget=forms.Select)
    tags = forms.ModelMultipleChoiceField(queryset=TagPost.objects.all(), required=False, label="Теги", widget=forms.CheckboxSelectMultiple(attrs={'class': 'checkbox-container'}))

    class Meta:
        model = Post
        fields = ['title', 'content', 'images', 'is_published', 'cat', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'class': 'form-input', 'rows': 5}),
        }


class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']


class SearchPostForm(forms.Form):
    query = forms.CharField(label='Поиск', max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-input'}))
    title = forms.CharField(label='Поиск по заголовку', max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-input'}))
    content = forms.CharField(label='Поиск по тексту', max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-input'}))
    author = forms.CharField(label='Поиск по автору', max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-input'}))
