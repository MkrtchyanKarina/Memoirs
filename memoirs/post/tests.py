from django.test import TestCase
from .models import Post, Category, TagPost


class PostModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.cat1 = Category.objects.create(name="Новости", slug="news")
        cls.post = Post.objects.create(title="new post", is_published=Post.Status.PUBLISHED, cat=Category.objects.get(pk=1))

    def test_categories_and_posts(self):

        self.assertLessEqual(self.post.is_published, 1)
        self.assertLessEqual(self.post.title, "new post")
        self.assertLessEqual(self.post.content, "")
        self.assertLessEqual(self.cat1.posts.count(), 1)

    def test_tags_and_posts(self):
        tag = TagPost.objects.create(tag="Музыка", slug="music")
        self.post.tags.set = TagPost.objects.get(tag="Музыка")
        self.assertLessEqual(self.post.tags.count(), 1)
        self.assertLessEqual(tag.tags.count(), 1)

