import logging
import functools
import asyncio
import os

logger = logging.getLogger(__name__)

class AuditBase:
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        for name, method in cls.__dict__.items():
            if callable(method):
                if asyncio.iscoroutinefunction(method):
                    setattr(cls, name, audit_async(method))
                else:
                    if name == "__init__":
                        cls = audit_init(cls)
                    else:
                        setattr(cls, name, audit(method))

def audit_init(cls):
    original_init = cls.__init__

    @functools.wraps(original_init)
    def wrapper(self, *args, **kwargs):
        logger.debug(f"{cls.__name__}.__init__ called with args: {args}, kwargs: {kwargs}")
        original_init(self, *args, **kwargs)

    cls.__init__ = wrapper
    return cls

def get_extra(func):
    audit_func_path = f"{func.__module__}.{func.__qualname__}"
    audit_filename = os.path.basename(func.__code__.co_filename)  # Añadir esta línea
    audit_lineno = func.__code__.co_firstlineno  # Añadir esta línea
    extra={"audit_func_path": audit_func_path, "audit_filename": audit_filename, "audit_lineno": audit_lineno}
    return extra

def audit(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            extra = get_extra(func)
            logger.debug(f"Called with args: {args}, kwargs: {kwargs}", extra=extra)
            result = func(*args, **kwargs)
            logger.debug(f"Returned: {result}", extra=extra)
            return result
        except Exception as e:
            logger.exception(f"Exception in {func.__module__}.{func.__qualname__}: {e}")
            raise

    return wrapper

def audit_async(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            extra = get_extra(func)
            logger.debug(f"{func.__module__}.{func.__qualname__} called with args: {args}, kwargs: {kwargs}", extra=extra)
            result = await func(*args, **kwargs)
            logger.debug(f"{func.__module__}.{func.__qualname__} returned: {result}", extra=extra)
            return result
        except Exception as e:
            logger.exception(f"Exception in {func.__module__}.{func.__qualname__}: {e}")
            raise

    return wrapper

def audit_async_task(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            extra = get_extra(func)
            logger.debug(f"{func.__module__}.{func.__qualname__} called with args: {args}, kwargs: {kwargs}", extra=extra)
            result = await asyncio.create_task(func(*args, **kwargs))
            logger.debug(f"{func.__module__}.{func.__qualname__} returned: {result}")
            return result
        except Exception as e:
            logger.exception(f"Exception in {func.__module__}.{func.__qualname__}: {e}", extra=extra)
            raise

    return wrapper
