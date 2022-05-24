from rest_framework.throttling import UserRateThrottle


class CreateBlogThrottle(UserRateThrottle):
    rate = '2/hour'
    scope = 'create_blog'
    message = 'You can only create 3 blog per day'


class CreateCommentThrottle(UserRateThrottle):
    rate = '10/hour'
    scope = 'create_blog'
    message = 'You can only create 3 comments per day.'
