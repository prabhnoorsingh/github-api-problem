import arrow
import json
import requests
import datetime
from django.db.models import Q
#Local imports
from githubUsers.utils.CommonUtils import whoami
from githubProject.settings import logger
from githubUsers.models import UserDetail, TrackApiUsage


def convert_str_into_datetime(datetime_string):
    """
    Converts datetime in string format to datetime.datetime format.
    """
    arrow_obj = arrow.get(datetime_string)
    tmp_datetime = arrow_obj.datetime
    tmp_datetime = tmp_datetime.replace(tzinfo=None)
    return tmp_datetime


def save_api_count():
    """
    Adds an entry to TrackApiUsage table, whenever user-search API is hit.
    """
    time_stamp = datetime.datetime.now().replace(tzinfo=None)
    save_api_hit_time_stamp = TrackApiUsage(api_usage_date=time_stamp)
    save_api_hit_time_stamp.save()
    if save_api_hit_time_stamp:
        logger.info("search-user API is being hit "+str(save_api_hit_time_stamp.pk)+ " time(s)")
    return True


def get_github_users():
    """
    It first fetches all users using Github fetch users api and then fetches detailed information about each user using
    their user_url..
    """
    list_of_user_data = []
    try:
        users_requested_data = requests.get('https://api.github.com/users')
        time_stamp = datetime.datetime.now().replace(tzinfo=None)
        logger.info("Status code for fetching list of all users is.. "+str(users_requested_data.status_code))
        if users_requested_data.status_code == 200:
            users_data_list = json.loads(users_requested_data.text)
            if users_data_list:
                logger.info("Total users fetched "+str(len(users_data_list)))
                for user_summary in users_data_list:
                    logger.info("Fetching data of id .. "+str(user_summary["id"]))
                    user_detail_data = requests.get(user_summary["url"])
                    logger.info("Status code for fetching list of all users is.. " + str(user_detail_data.status_code))
                    if user_detail_data.status_code == 200:
                        user_data = json.loads(user_detail_data.text)
                        user_data["db_entry_creation_date"] = time_stamp
                        user_data["created_at"] = convert_str_into_datetime(user_data["created_at"])
                        user_data["updated_at"] = convert_str_into_datetime(user_data["updated_at"])
                        list_of_user_data.append(user_data)
                    else:
                        message = "Data could not be fetched from github, due to HTTP error" +str(user_detail_data.status_code)
                        return False, [message]
        else:
            message = "Data could not be fetched from github, due to HTTP error" + str(users_requested_data.status_code)
            return False, [message]

    except ConnectionError as conn_err:
        logger.exception("Exception due to connection err in "+whoami()+","+str(conn_err))
        return False, ["Connection Error has occurred due to which request can not be processed."]
    except Exception as err:
        logger.exception("Exception occurred in function " + whoami() + ", " + str(err))
        return False,  ["Some error has occurred due to which request can not be processed."]
    return True, list_of_user_data


def create_filter_query(type,field_in,repos,location,created,followers,sort,search_term):
    """
    Returns the filtered user data from the database depending upont he input paramters.
    """
    user_detail_queryset = ''
    try:
        user_detail_queryset = UserDetail.objects.all()

        if type:
            user_detail_queryset =user_detail_queryset.filter(type__iexact=type)
        if field_in:
            if field_in=='login':
                user_detail_queryset = user_detail_queryset.filter(login__icontains=search_term)
            elif field_in=='fullname':
                user_detail_queryset = user_detail_queryset.filter(name__icontains=search_term)
            elif field_in=='email':
                user_detail_queryset = user_detail_queryset.filter(email__icontains=search_term)
        else:
            if search_term:
                user_detail_queryset = user_detail_queryset.filter(
                    Q(login__icontains=search_term) | Q(name__icontains=search_term))
        if repos:
            if repos.startswith('>'):
                repos_count = repos[1:]
                user_detail_queryset = user_detail_queryset.filter(public_repos__gt=repos_count)
            elif repos.startswith('<'):
                repos_count = repos[1:]
                user_detail_queryset = user_detail_queryset.filter(public_repos__lt=repos_count)
            elif repos.startswith('>='):
                repos_count = repos[2:]
                user_detail_queryset = user_detail_queryset.filter(public_repos__gte=repos_count)
            elif repos.startswith('<='):
                repos_count = repos[2:]
                user_detail_queryset = user_detail_queryset.filter(public_repos__lte=repos_count)
            elif repos.startswith('*..'):
                repos_count = repos[3:]
                user_detail_queryset = user_detail_queryset.filter(public_repos__lte=repos_count)
            elif repos.endswith('..*'):
                repos_count = repos[:-3]
                user_detail_queryset = user_detail_queryset.filter(public_repos__gte=repos_count)
            elif '..' in repos:
                repos_range=repos.split('..')
                user_detail_queryset = user_detail_queryset.filter(public_repos__gte=repos_range[0],public_repos__lte=repos_range[1])
            else:
                user_detail_queryset = user_detail_queryset.filter(public_repos=repos)

        if location:
            user_detail_queryset = user_detail_queryset.filter(location__iexact=location)
        if created:
            if created.startswith('>'):
                user_detail_queryset = user_detail_queryset.filter(created_at__gt=created[1:])
            elif created.startswith('<'):
                user_detail_queryset = user_detail_queryset.filter(created_at__lt=created[1:])
            elif created.startswith('>='):
                user_detail_queryset = user_detail_queryset.filter(created_at__gte=created[2:])
            elif created.startswith('<='):
                user_detail_queryset = user_detail_queryset.filter(created_at__lte=created[2:])
            elif created.startswith('*..'):
                user_detail_queryset = user_detail_queryset.filter(created_at__lte=created[3:])
            elif created.endswith('..*'):
                user_detail_queryset = user_detail_queryset.filter(created_at__gte=created[:-3])
            elif '..' in created:
                created_range=created.split('..')
                user_detail_queryset = user_detail_queryset.filter(created_at__gte=created_range[0],followers__lte=created_range[1])
            else:
                user_detail_queryset = user_detail_queryset.filter(created_at=created)
        if followers:
            if followers.startswith('>'):
                user_detail_queryset = user_detail_queryset.filter(followers__gt=followers[1:])
            elif followers.startswith('<'):
                user_detail_queryset = user_detail_queryset.filter(followers__lt=followers[1:])
            elif followers.startswith('>='):
                user_detail_queryset = user_detail_queryset.filter(followers__gte=followers[2:])
            elif followers.startswith('<='):
                user_detail_queryset = user_detail_queryset.filter(followers__lte=followers[2:])
            elif followers.startswith('*..'):
                user_detail_queryset = user_detail_queryset.filter(followers__lte=followers[3:])
            elif followers.endswith('..*'):
                user_detail_queryset = user_detail_queryset.filter(followers__gte=followers[:-3])
            elif '..' in followers:
                followers_count=followers.split('..')
                user_detail_queryset = user_detail_queryset.filter(followers__gte=followers_count[0],followers__lte=followers_count[1])
            else:
                user_detail_queryset = user_detail_queryset.filter(followers=followers)

        if sort:
            if 'asc' in sort:
                if 'followers' in sort:
                    user_detail_queryset = user_detail_queryset.order_by('followers')
                elif 'repositories' in sort:
                    user_detail_queryset = user_detail_queryset.order_by('public_repos')
                elif 'joined' in sort:
                    user_detail_queryset = user_detail_queryset.order_by('created_at')
            # default order is 'desc'
            else:
                if 'followers' in sort:
                    user_detail_queryset = user_detail_queryset.order_by('-followers')
                elif 'repositories' in sort:
                    user_detail_queryset = user_detail_queryset.order_by('-public_repos')
                elif 'joined' in sort:
                    user_detail_queryset = user_detail_queryset.order_by('-created_at')

    except Exception as err:
        logger.exception("Exception occurred in function " + whoami() + ", " + str(err))
    return user_detail_queryset

