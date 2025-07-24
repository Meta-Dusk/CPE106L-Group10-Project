import flet as ft

from dataclasses import dataclass
from typing import Callable
from enum import Enum

@dataclass
class RouteHandler:
    path: str
    handler: Callable[[ft.Page, ft.RouteChangeEvent], None]
    auth_required: bool = False

# Used only for static routes, and type-safety.
class PageRoute(Enum):
    LOADING = "/"
    LOGIN = "/login"
    RETRY = "/retry"
    DASHBOARD = "/dashboard"
    GRAPHS = "/dashboard/graphs"
    BOOKING = "/dashboard/booking"
    API_KEY = "/dashboard/api-key"