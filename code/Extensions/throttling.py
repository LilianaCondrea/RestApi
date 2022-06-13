from rest_framework.throttling import UserRateThrottle, AnonRateThrottle


class CreateBlogThrottle(UserRateThrottle):
    rate = '2/hour'
    scope = 'create_blog'


class CreateCommentThrottle(UserRateThrottle):
    rate = '10/hour'
    scope = 'create_blog'


class AuthUserThrottle(UserRateThrottle):
    rate = '100/hour'
    scope = 'auth_user'

class NoneAuthUserThrottle(AnonRateThrottle):
    rate = '20/hour'
    scope = 'none_auth_user'
