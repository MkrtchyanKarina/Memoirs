from django.test import TestCase
from .models import Post, Category, TagPost


class PostModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.cat1 = Category.objects.create(name="Новости", slug="news")

    def test_categories_and_posts(self):
        post = Post.objects.create(title="new post", is_published=Post.Status.PUBLISHED, cat=Category.objects.get(pk=1))

        self.assertLessEqual(post.is_published, 1)
        self.assertLessEqual(post.title, "new post")
        self.assertLessEqual(post.content, "")
        self.assertLessEqual(self.cat1.posts.count(), 1)

    def test_tags_and_posts(self):
        tag = TagPost.objects.create(tag="Музыка", slug="music")
        post = Post.objects.create(title="new post", is_published=Post.Status.PUBLISHED, cat=Category.objects.get(pk=1))
        post.tags.set = TagPost.objects.get(tag="Музыка")
        self.assertLessEqual(post.tags.count(), 1)
        self.assertLessEqual(tag.tags.count(), 1)

