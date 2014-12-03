''' API calls with respect to users and authentication '''
from urllib2 import HTTPError
from urllib import urlencode
import copy
import json
from lib.util import DottableDict

from django.conf import settings
from django.utils.translation import ugettext as _

from .json_object import JsonParser as JP
from . import user_models, gradebook_models, organization_models, workgroup_models, course_models
from .json_requests import GET, POST, PUT, DELETE
from .api_error import api_error_protect, ERROR_CODE_MESSAGES
from .group_models import GroupInfo

AUTH_API = getattr(settings, 'AUTH_API', 'api/server/sessions')
USER_API = getattr(settings, 'USER_API', 'api/server/users')
GROUP_API = getattr(settings, 'GROUP_API', 'api/server/groups')

USER_ROLES = DottableDict(
    STAFF='staff',
    INSTRUCTOR='instructor',
    OBSERVER='observer',
    TA='assistant',
)

VALID_USER_KEYS = ["email", "first_name", "last_name", "full_name", "city", "country",
                   "username", "level_of_education", "password", "gender", "title", "is_active", "avatar_url"]


def _clean_user_keys(user_hash):
    return {user_key: user_hash[user_key] for user_key in VALID_USER_KEYS if user_key in user_hash}


@api_error_protect
def authenticate(username, password):
    ''' authenticate to the API server '''
    data = {
        "username": username,
        "password": password
    }
    response = POST(
        '{}/{}/'.format(settings.API_SERVER_ADDRESS, AUTH_API),
        data
    )
    return JP.from_json(response.read(), user_models.AuthenticationResponse)


@api_error_protect
def get_user(user_id):
    ''' get specified user '''
    # NB - trailing slash causes only a small amount of fields to get output
    # get extended fields as well if not including trailing slash
    response = GET(
        '{}/{}/{}'.format(
            settings.API_SERVER_ADDRESS, USER_API, user_id
        )
    )
    return JP.from_json(response.read(), user_models.UserResponse)


@api_error_protect
def get_user_dict(user_id):
    ''' get specified user as a dict'''
    # NB - trailing slash causes only a small amount of fields to get output
    # get extended fields as well if not including trailing slash
    response = GET(
        '{}/{}/{}/'.format(
            settings.API_SERVER_ADDRESS, USER_API, user_id
        )
    )
    return json.loads(response.read())


@api_error_protect
def get_users(fields=[], *args, **kwargs):
    ''' get all users that meet filter criteria'''
    request_fields = ['id', 'email', 'username']
    request_fields.extend(fields)
    qs_params = {
        "page_size": 0,
        "fields": ",".join(request_fields),
    }

    for karg in kwargs:
        if isinstance(kwargs[karg], list):
            qs_params[karg] = ",".join(kwargs[karg])
        else:
            qs_params[karg] = kwargs[karg]

    response = GET(
        '{}/{}?{}'.format(
            settings.API_SERVER_ADDRESS,
            USER_API,
            urlencode(qs_params)
        )
    )
    return JP.from_json(response.read(), user_models.UserResponse)


@api_error_protect
def delete_session(session_key):
    ''' delete associated openedx session '''
    DELETE(
        '{}/{}/{}'.format(
            settings.API_SERVER_ADDRESS,
            AUTH_API,
            session_key
        )
    )


@api_error_protect
def register_user(user_hash):
    ''' register the given user within the openedx server '''
    response = POST(
        '{}/{}'.format(settings.API_SERVER_ADDRESS, USER_API),
        _clean_user_keys(user_hash)
    )
    return JP.from_json(response.read())


@api_error_protect
def _update_user(user_id, user_hash):
    ''' update the given user's information within the openedx server '''
    response = POST(
        '{}/{}/{}'.format(settings.API_SERVER_ADDRESS, USER_API, user_id),
        user_hash
    )
    return JP.from_json(response.read())


@api_error_protect
def update_user_information(user_id, user_hash):
    ''' update the given user's information within the openedx server '''
    return _update_user(user_id, _clean_user_keys(user_hash))


@api_error_protect
def activate_user(user_id):
    ''' activate the given user on the openedx server '''
    return _update_user(user_id, {"is_active": True})


@api_error_protect
def get_user_courses(user_id):
    ''' get the user's summary for their courses '''
    response = GET(
        '{}/{}/{}/courses'.format(
            settings.API_SERVER_ADDRESS,
            USER_API,
            user_id
        )
    )
    courses = JP.from_json(response.read(), course_models.Course)

    return courses


@api_error_protect
def get_user_roles(user_id):
    ''' get a list of user roles '''
    response = GET(
        '{}/{}/{}/roles?page_size=0'.format(
            settings.API_SERVER_ADDRESS,
            USER_API,
            user_id,
        )
    )
    return JP.from_json(response.read())


@api_error_protect
def add_user_role(user_id, course_id, role):
    ''' add role for course, roles are 'instructor' and 'assistant' '''
    data = {
        'course_id': course_id,
        'role': role
    }
    response = POST(
        '{}/{}/{}/roles'.format(
            settings.API_SERVER_ADDRESS,
            USER_API,
            user_id,
        ),
        data
    )
    return JP.from_json(response.read())


@api_error_protect
def update_user_roles(user_id, role_list):
    ''' update roles, where role_list is a list of dictionaries containing course_id & role '''
    response = PUT(
        '{}/{}/{}/roles'.format(
            settings.API_SERVER_ADDRESS,
            USER_API,
            user_id,
        ),
        role_list
    )
    return JP.from_json(response.read())


@api_error_protect
def delete_user_role(user_id, course_id, role):
    response = DELETE(
        '{}/{}/{}/roles/{}/courses/{}'.format(
            settings.API_SERVER_ADDRESS,
            USER_API,
            user_id,
            role,
            course_id
        )
    )

    return (response.code == 204)


@api_error_protect
def get_user_groups(user_id, group_type=None, group_object=GroupInfo, *args, **kwargs):
    ''' get the groups in which this user is a member '''
    qs_params = {}
    qs_params.update(kwargs)

    if group_type:
        qs_params["type"] = group_type

    url = '{}/{}/{}/groups'.format(
        settings.API_SERVER_ADDRESS,
        USER_API,
        user_id,
    )

    if len(qs_params.keys()) > 0:
        url += "?{}".format(urlencode(qs_params))

    response = GET(url)

    groups_json = json.loads(response.read())

    return JP.from_dictionary(groups_json["groups"], group_object)


@api_error_protect
def enroll_user_in_course(user_id, course_id):
    ''' enrolls the user summary in the given course '''
    data = {"course_id": course_id}
    response = POST(
        '{}/{}/{}/courses'.format(
            settings.API_SERVER_ADDRESS,
            USER_API,
            user_id
        ),
        data
    )

    courses = JP.from_json(response.read(), course_models.Course)


@api_error_protect
def unenroll_user_from_course(user_id, course_id):
    ''' unenroll a User from a Course (inactivates the enrollment) '''
    response = DELETE(
        '{}/{}/{}/courses/{}'.format(
            settings.API_SERVER_ADDRESS,
            USER_API,
            user_id,
            course_id
        )
    )
    return (response.code == 204)


@api_error_protect
def get_user_course_detail(user_id, course_id):
    ''' get details for the user for this course'''
    response = GET(
        '{}/{}/{}/courses/{}'.format(
            settings.API_SERVER_ADDRESS,
            USER_API,
            user_id,
            course_id
        )
    )

    return JP.from_json(response.read(), user_models.UserCourseStatus)


@api_error_protect
def get_user_gradebook(user_id, course_id, gradebook_model=gradebook_models.Gradebook):
    ''' get grades for the user for this course'''
    response = GET(
        '{}/{}/{}/courses/{}/grades'.format(
            settings.API_SERVER_ADDRESS,
            USER_API,
            user_id,
            course_id
        )
    )

    return JP.from_json(response.read(), gradebook_model)


@api_error_protect
def set_user_bookmark(user_id, course_id, chapter_id, sequential_id, page_id):
    '''
    Let the openedx server know the most recently visited page
    Can also provide a None value for chapter_id, then it just sets the page
    within the sequential_id
    '''

    data = {"positions":
            [
                {
                    "parent_content_id": course_id,
                    "child_content_id": chapter_id,
                },
                {
                    "parent_content_id": chapter_id,
                    "child_content_id": sequential_id,
                },
                {
                    "parent_content_id": sequential_id,
                    "child_content_id": page_id,
                },
            ]
            }

    response = POST(
        '{}/{}/{}/courses/{}'.format(
            settings.API_SERVER_ADDRESS,
            USER_API,
            user_id,
            course_id
        ),
        data
    )

    return JP.from_json(response.read())


@api_error_protect
def is_user_in_group(user_id, group_id):
    ''' checks group membership '''
    try:
        response = GET(
            '{}/{}/{}/users/{}'.format(
                settings.API_SERVER_ADDRESS,
                GROUP_API,
                group_id,
                user_id,
            )
        )
    except HTTPError, e:
        if e.code == 404:
            return False
        else:
            raise e

    return (response.code == 200)


@api_error_protect
def set_user_preferences(user_id, preference_dictionary):
    ''' sets users preferences information '''
    response = POST(
        '{}/{}/{}/preferences'.format(
            settings.API_SERVER_ADDRESS,
            USER_API,
            user_id,
        ),
        preference_dictionary
    )

    return True


@api_error_protect
def delete_user_preference(user_id, preference_key):
    ''' sets users preferences information '''
    DELETE(
        '{}/{}/{}/preferences/{}'.format(
            settings.API_SERVER_ADDRESS,
            USER_API,
            user_id,
            preference_key
        )
    )

    return True


@api_error_protect
def get_user_preferences(user_id):
    ''' sets users preferences information '''
    response = GET(
        '{}/{}/{}/preferences'.format(
            settings.API_SERVER_ADDRESS,
            USER_API,
            user_id,
        ),
    )

    # Note that we return plain dictionary here - makes more sense 'cos we set a dictionary
    return json.loads(response.read())


@api_error_protect
def get_user_organizations(user_id, organization_object=organization_models.Organization):
    ''' return organizations with which the user is associated '''
    response = GET(
        '{}/{}/{}/organizations/?page_size=0'.format(
            settings.API_SERVER_ADDRESS,
            USER_API,
            user_id,
        )
    )

    return JP.from_json(response.read(), organization_object)


@api_error_protect
def get_user_workgroups(user_id, course_id=None, workgroup_object=workgroup_models.Workgroup):
    ''' return organizations with which the user is associated '''
    qs_params = {"page_size": 0}
    if course_id:
        qs_params["course_id"] = course_id

    url = '{}/{}/{}/workgroups/?{}'.format(
        settings.API_SERVER_ADDRESS,
        USER_API,
        user_id,
        urlencode(qs_params),
    )

    response = GET(url)
    return JP.from_json(response.read(), workgroup_object)


@api_error_protect
def get_users_city_metrics():
    ''' return users by sity metrics'''

    response = GET(
        '{}/{}/metrics/cities/?page_size=0'.format(
            settings.API_SERVER_ADDRESS,
            USER_API,
        )
    )

    return JP.from_json(response.read(), user_models.CityList)


@api_error_protect
def get_course_social_metrics(user_id, course_id):
    ''' fetch social metrics for course '''

    response = GET(
        '{}/{}/{}/courses/{}/metrics/social/'.format(
            settings.API_SERVER_ADDRESS,
            USER_API,
            user_id,
            course_id,
        )
    )

    return JP.from_json(response.read())

USER_ERROR_CODE_MESSAGES = {
    "update_user_information": {
        409: _(("User with matching username "
                "or email already exists")),
    },
    "authenticate": {
        403: _("User account not activated"),
        401: _("Username or password invalid"),
        404: _("Username or password invalid"),
    },
    "register_user": {
        409: _("Username or email already registered"),
    },
}
ERROR_CODE_MESSAGES.update(USER_ERROR_CODE_MESSAGES)