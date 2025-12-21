from contextvars import ContextVar

# Thread-safe context variable to store the current user_id during a request
user_id_context: ContextVar[int] = ContextVar("user_id_context", default=None)
