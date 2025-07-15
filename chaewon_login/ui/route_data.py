import flet as ft

from dataclasses import dataclass
from typing import Callable
from enum import Enum

@dataclass
class RouteHandler:
    path: str
    handler: Callable[[ft.Page, ft.RouteChangeEvent], None]
    auth_required: bool = False
    
class PageRoute(Enum):
    LOADING = "/"
    LOGIN = "/login"
    RETRY = "/retry"
    DASHBOARD = "/dashboard"