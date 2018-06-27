import datetime
from rest_framework import serializers
#Local imports
from githubUsers.models import UserDetail


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetail
        fields = '__all__'

    def create(self, validated_data):
        """
        Create and return a new `UserDetail` instance, given the validated data.
        """
        return UserDetail.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `UserDetail` instance, given the validated data.
        """
        time_stamp = datetime.datetime.now().replace(tzinfo=None)
        instance.id = validated_data.get('id', instance.id)
        instance.login = validated_data.get('login', instance.login)
        instance.node_id = validated_data.get('node_id', instance.node_id)
        instance.avatar_url = validated_data.get('avatar_url', instance.avatar_url)
        instance.gravatar_id = validated_data.get('gravatar_id', instance.gravatar_id)
        instance.url = validated_data.get('url', instance.url)
        instance.html_url = validated_data.get('html_url', instance.html_url)
        instance.followers_url = validated_data.get('followers_url', instance.followers_url)
        instance.following_url = validated_data.get('following_url', instance.following_url)
        instance.gists_url = validated_data.get('gists_url', instance.gists_url)
        instance.starred_url = validated_data.get('starred_url', instance.starred_url)
        instance.subscriptions_url = validated_data.get('node_id', instance.subscriptions_url)
        instance.organizations_url = validated_data.get('node_id', instance.organizations_url)
        instance.repos_url = validated_data.get('node_id', instance.repos_url)
        instance.events_url = validated_data.get('created', instance.events_url)
        instance.received_events_url = validated_data.get('created', instance.received_events_url)
        instance.type = validated_data.get('created', instance.type)
        instance.site_admin = validated_data.get('created', instance.site_admin)
        instance.name = validated_data.get('name', instance.name)
        instance.site_admin = validated_data.get('created', instance.site_admin)
        instance.company = validated_data.get('company', instance.company)
        instance.blog = validated_data.get('blog', instance.blog)
        instance.location = validated_data.get('location', instance.location)
        instance.email = validated_data.get('email', instance.email)
        instance.hirable = validated_data.get('hirable', instance.hirable)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.public_repos = validated_data.get('public_repos', instance.public_repos)
        instance.public_gists = validated_data.get('public_gists', instance.public_gists)
        instance.followers = validated_data.get('followers', instance.followers)
        instance.following = validated_data.get('following', instance.following)
        instance.created_at = validated_data.get('created_at', instance.created_at)
        instance.updated_at = validated_data.get('updated_at', instance.updated_at)
        instance.db_entry_updation_date = time_stamp
        instance.save()
        return instance
