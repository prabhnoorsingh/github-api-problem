from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
#Local imports
from githubProject.settings import logger
from githubUsers.utils import githubData
from githubUsers.users.serializers import *
from githubUsers.utils.CommonUtils import whoami
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Github Users API')


@api_view(['POST', 'PUT'])
def fetch_and_store_all_users(request):
    """
    Fetches all users from Github and inserts them to the database. Incase, user_id is existing in database, it updates
    the user information.
    """
    try:
        logger.info("API "+whoami()+" has been hit !")
        store_api_count = githubData.save_api_count()
        flag, list_of_user_data = githubData.get_github_users()
        if flag:
            if list_of_user_data:
                serializer_list = []
                try:
                    for user_data in list_of_user_data:
                        existing_user = UserDetail.objects.filter(id=user_data["id"]).first()
                        if existing_user:
                            logger.info("User with id "+str(user_data["id"])+"is already existing. So performing an update to existing data.")
                            serializer = UserDetailSerializer(existing_user, data=user_data)
                        else:
                            logger.info("Creating new user")
                            serializer = UserDetailSerializer(data=user_data)
                        if serializer.is_valid():
                            serializer.save()
                            serializer_list.append(serializer.data)
                        else:
                            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                    return Response(data=serializer_list, status=status.HTTP_201_CREATED)
                except Exception as err:
                    logger.info(err)
                    return Response(data="Error occurred while storing user data", status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(data="No user details are present on github", status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data=list_of_user_data[0], status=status.HTTP_400_BAD_REQUEST)
    except Exception as err:
        logger.exception("Exception occurred in API "+ whoami() + ", " +str(err))
        return Response(data="Error occurred while fetch the list of github users", status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def send_filtered_users(request):
    """
    Filters and returns the github users stored in database, depending upon the input parameters.
    :param request: q, type, in, repos, location,created, followers,sort
    :sample request: q=tom&type=user&in=email&repos=>40&sort=followers-asc&followers=>60location=iceland
    """
    try:
        logger.info("API " + whoami() + " has been hit !")
        type = (request.GET.get('type', '')).strip()
        field_in = (request.GET.get('in', '')).strip()
        repos = (request.GET.get('repos', '')).strip()
        location = (request.GET.get('location', '')).strip()
        created = (request.GET.get('created', '')).strip()
        followers = (request.GET.get('followers', '')).strip()
        sort = (request.GET.get('sort', '')).strip()
        search_term = (request.GET.get('q','')).strip()

        user_detail_queryset = githubData.create_filter_query(type,field_in,repos,location,created,followers,sort,search_term)

        if user_detail_queryset:
            serializer = UserDetailSerializer(user_detail_queryset, many=True)
        else:
            return Response(data="Input parameters of the filters are not valid",status=status.HTTP_400_BAD_REQUEST)

        return Response(data=serializer.data, status=status.HTTP_200_OK)
    except Exception as err:
        logger.exception("Exception occurred in API " + whoami() + ", " + str(err))
        return Response(data="Error occurred while fetching the filtered user data from database", status=status.HTTP_400_BAD_REQUEST)
