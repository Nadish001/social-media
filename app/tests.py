from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Follow, Posts


class FollowTests(TestCase):
    def setUp(self):
        self.follower = User.objects.create_user(username='follower', password='pass12345')
        self.target = User.objects.create_user(username='target', password='pass12345')
        self.client.force_login(self.follower)

    def test_follow_and_unfollow_updates_profile_counts(self):
        profile_url = reverse('userprofile', kwargs={'username': self.target.username})
        follow_url = reverse('follow_user', kwargs={'username': self.target.username})

        response = self.client.post(follow_url, {'next': profile_url})
        self.assertRedirects(response, profile_url)
        self.assertTrue(Follow.objects.filter(follower=self.follower, following=self.target).exists())

        response = self.client.get(profile_url)
        self.assertEqual(response.context['followers_count'], 1)
        self.assertTrue(response.context['is_following'])
        self.assertContains(response, 'Unfollow')
        self.assertEqual(
            self.client.get(reverse('profile')).context['following_count'],
            1,
        )

        post = Posts.objects.create(user=self.target, title='Target post', post_img='posts/test.jpg')
        post_response = self.client.get(reverse('postview', kwargs={'pid': post.id}))
        self.assertContains(post_response, 'Unfollow')

        self.client.post(follow_url, {'next': profile_url})
        self.assertFalse(Follow.objects.filter(follower=self.follower, following=self.target).exists())
        self.assertEqual(self.client.get(profile_url).context['followers_count'], 0)
        self.assertContains(
            self.client.get(reverse('postview', kwargs={'pid': post.id})),
            'Follow',
        )

    def test_cannot_follow_self(self):
        response = self.client.post(reverse('follow_user', kwargs={'username': self.follower.username}))

        self.assertRedirects(response, reverse('profile'))
        self.assertFalse(Follow.objects.exists())
