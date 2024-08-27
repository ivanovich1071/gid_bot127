from .logger import logger
from .storage import init_db

# Экспортируем утилиты для легкого доступа к ним в других частях проекта
__all__ = ["logger", "init_db"]
