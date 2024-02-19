import shadpy
from ... import handlers


class OnMessageUpdates:
    def on_message_updates(
            self: "shadpy.Client",
            *args, **kwargs,
    ):
        def MetaHandler(func):
            self.add_handler(func, handlers.MessageUpdates(*args, **kwargs))
            return func
        return MetaHandler