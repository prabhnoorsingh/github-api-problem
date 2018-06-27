from django.db.models import *


class UserDetail(Model):
    """
    Stores detailed information about each user.
    """
    id = IntegerField(primary_key=True)
    login = CharField(max_length=255)
    node_id = CharField(max_length=255,null=True, blank=True)
    avatar_url = CharField(max_length=255,null=True, blank=True)
    gravatar_id = CharField(max_length=255, null=True, blank=True)
    url = CharField(max_length=255,null=True, blank=True)
    html_url = CharField(max_length=255, null=True, blank=True)
    followers_url = CharField(max_length=255, null=True, blank=True)
    following_url = CharField(max_length=255, null=True, blank=True)
    gists_url = CharField(max_length=255, null=True, blank=True)
    starred_url = CharField(max_length=255, null=True, blank=True)
    subscriptions_url = CharField(max_length=255, null=True, blank=True)
    organizations_url = CharField(max_length=255, null=True, blank=True)
    repos_url = CharField(max_length=255, null=True, blank=True)
    events_url = CharField(max_length=255, null=True, blank=True)
    received_events_url = CharField(max_length=255, null=True, blank=True)
    type = CharField(max_length=255, null=True, blank=True)
    site_admin = BooleanField(blank=True)
    name = CharField(max_length=255, null=True, blank=True)
    company = CharField(max_length=255, null=True, blank=True)
    blog = CharField(max_length=255, null=True, blank=True)
    location = CharField(max_length=255, null=True, blank=True)
    email = CharField(max_length=255, null=True, blank=True)
    hirable = CharField(max_length=255, null=True, blank=True)
    bio = CharField(max_length=255, null=True, blank=True)
    public_repos = CharField(max_length=255, null=True, blank=True)
    public_gists = CharField(max_length=255, null=True, blank=True)
    followers = CharField(max_length=255, null=True, blank=True)
    following = CharField(max_length=255, null=True, blank=True)
    created_at = DateTimeField(null=True, blank=True)
    updated_at = DateTimeField(null=True, blank=True)
    db_entry_creation_date = DateTimeField()
    db_entry_updation_date = DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('db_entry_creation_date',)


class TrackApiUsage(Model):
    """
    Stores hit count of Github user search API.
    """
    search_entry = AutoField(primary_key=True)
    api_usage_date = DateTimeField()


class ApiUsageSummary(TrackApiUsage):
    """
    It is used to provide report of search API calls count in a day, month and year in Admin Panel.
    """
    class Meta:
        proxy = True
        verbose_name = "Search API Usage Summary"
        verbose_name_plural = "Search API Usage Summary"


class UserSummary(UserDetail):
    """
    It is used to provide report of number of users added to database in a day, month and year in Admin Panel.
    """
    class Meta:
        proxy = True
        verbose_name = "User Summary"
        verbose_name_plural = "Users Summary"
