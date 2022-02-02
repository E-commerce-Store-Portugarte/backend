from rest_framework.routers import Route, SimpleRouter


class ProductRouter(SimpleRouter):

    routes = [
        Route(
            url=r'^{prefix}/$',
            mapping={'get': 'list'},
            name='{basename}-list',
            detail=False,
            initkwargs={}
        ),
        Route(
            url=r'^{prefix}/{lookup}/$',
            mapping={'get': 'get'},
            name='{basename}-detail',
            detail=True,
            initkwargs={}
        ),
    ]


class OrderRouter(SimpleRouter):

    routes = [
        Route(
            url=r'^{prefix}/$',
            mapping={'get': 'list'},
            name='{basename}-list',
            detail=False,
            initkwargs={}
        ),
        Route(
            url=r'^{prefix}/{lookup}/$',
            mapping={'get': 'get'},
            name='{basename}-detail',
            detail=True,
            initkwargs={}
        ),
    ]


class BasketItemRouter(SimpleRouter):

    routes = [
        Route(
            url=r'^{prefix}/$',
            mapping={'get': 'list', 'post': 'create'},
            name='{basename}-list',
            detail=False,
            initkwargs={}
        ),
        Route(
            url=r'^{prefix}/{lookup}/$',
            mapping={'delete': 'delete', 'put': 'put'},
            name='{basename}-update',
            detail=True,
            initkwargs={}
        ),
    ]