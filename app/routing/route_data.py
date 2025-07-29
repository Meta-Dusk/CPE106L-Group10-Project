import flet as ft
import re

from dataclasses import dataclass
from typing import Callable
from enum import Enum

@dataclass
class RouteHandler:
    path: str
    handler: Callable[[ft.Page, ft.RouteChangeEvent], None]
    auth_required: bool = False
    path_regex: re.Pattern = None  # Only for dynamic routes
    param_names: list[str] = None  # Names of params (e.g. ['user_id'])

class PageRoute(Enum):
    LOADING = "/"
    LOGIN = "/login"
    RETRY = "/retry"
    DASHBOARD = "/dashboard"
    GRAPHS = "/dashboard/graphs"
    BOOKING = "/dashboard/booking"
    API_KEY = "/dashboard/api-key"
    PROFILE = "/profile/:user_id"
    OPERATOR = "/profile/op/:user_id"
    SETTINGS = "/profile/settings"
    MAP_VIEW = "/dashboard/mapview"