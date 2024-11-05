from api.auth.controllers.auth_controller import auth_router
from api.users.controllers.users_controller import users_router

routes = [users_router, auth_router]
