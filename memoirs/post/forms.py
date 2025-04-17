from django import forms
from .models import Category, TagPost, Post


class AddPostForm(forms.ModelForm):
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), label="Категория", empty_label="Категория не выбрана", widget=forms.Select)
    tags = forms.ModelMultipleChoiceField(queryset=TagPost.objects.all(), required=False, label="Теги", widget=forms.CheckboxSelectMultiple(attrs={'class': 'checkbox-container'}))

    class Meta:
        model = Post
        fields = ['title', 'content', 'images', 'is_published', 'cat', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'class': 'form-input', 'rows': 5}),
        }


class UploadFileForm(forms.Form):
    file = forms.ImageField(label="Файл")
