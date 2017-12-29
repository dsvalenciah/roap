from apistar import Include
from apistar.frameworks.wsgi import WSGIApp as App

from user_routes import user_routes
from publication_routes import publication_routes

ROUTES = [
    Include('/back/users', user_routes),
    Include('/back/publications', publication_routes),
]

app = App(routes=ROUTES)
