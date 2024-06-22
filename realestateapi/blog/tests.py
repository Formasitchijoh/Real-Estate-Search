import json
from random import randint

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from .models import Post, Tag


class PostTest(APITestCase):
    def setUp(self):
        self.tag1 = Tag.objects.create(title='Django')
        self.tag2 = Tag.objects.create(title='Database')
        self.tag3 = Tag.objects.create(title='Relationship')

    def test_can_create_post(self):
        url = reverse('posts-create')
        data = {
            'title': 'Test Post',
            'body': 'The body of the test post.',
            'tags': [self.tag1.id, self.tag2.id],
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_cannot_create_post_with_non_existent_tags(self):
        url = reverse('posts-create')
        data = {
            'title': 'Test Post',
            'body': 'The body of the test post.',
            'tags': [self.tag1.id, randint(50, 100)],
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_can_get_post(self):
        post = Post.objects.create(
            title='Test Post', body='The body of the test post.')
        post.tags.add(self.tag1)

        url = reverse('posts-get', kwargs={'pk': post.id})

        response = self.client.get(url, format='json')
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data['title'], post.title)
        self.assertEqual(response_data['body'], post.body)
        self.assertEqual(response_data['tags'][0]['id'], self.tag1.id)

    def test_cannot_get_non_existent_post(self):
        url = reverse('posts-get', kwargs={'pk': randint(50, 100)})

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_can_update_post(self):
        post = Post.objects.create(
            title='Test Post', body='The body of the test post.')
        post.tags.set([self.tag1, self.tag3])

        url = reverse('posts-update', kwargs={'pk': post.id})
        data = {
            'title': 'Updated Test Post',
            'body': 'The body of the updated test post.',
            'tags': [self.tag2.id, self.tag3.id],
        }

        response = self.client.put(url, data, format='json')
        response_data = json.loads(response.content)

        post = Post.objects.get(id=post.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data['title'], post.title)
        self.assertEqual(response_data['body'], post.body)
        self.assertEqual(len(response_data['tags']), 2)
        self.assertEqual(response_data['tags'][0]['id'], self.tag2.id)
        self.assertEqual(response_data['tags'][1]['id'], self.tag3.id)

    def test_cannot_update_non_existent_post(self):
        url = reverse('posts-update', kwargs={'pk': randint(50, 100)})
        data = {
            'title': 'Updated Test Post',
            'body': 'The body of the updated test post.',
            'tags': [self.tag2.id, self.tag3.id],
        }

        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_cannot_update_post_with_non_existent_tags(self):
        post = Post.objects.create(
            title='Test Post', body='The body of the test post.')
        post.tags.set([self.tag1, self.tag3])

        url = reverse('posts-update', kwargs={'pk': post.id})
        data = {
            'title': 'Updated Test Post',
            'body': 'The body of the updated test post.',
            'tags': [self.tag2.id, randint(50, 100)],
        }

        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
