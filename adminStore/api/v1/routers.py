from rest_framework.routers import Route, SimpleRouter


class ProductRouter(SimpleRouter):

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
            mapping={'get': 'get'},
            name='{basename}-get',
            detail=False,
            initkwargs={}
        ),
        Route(
            url=r'^{prefix}/{lookup}/change/$',
            mapping={'put': 'update'},
            name='{basename}-update',
            detail=False,
            initkwargs={}
        ),
        Route(
            url=r'^{prefix}/{lookup}/delete/$',
            mapping={'delete': 'delete'},
            name='{basename}-delete',
            detail=False,
            initkwargs={}
        ),
    ]
