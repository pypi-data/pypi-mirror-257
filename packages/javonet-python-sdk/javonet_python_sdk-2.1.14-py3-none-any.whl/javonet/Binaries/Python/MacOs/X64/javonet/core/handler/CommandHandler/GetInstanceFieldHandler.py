from javonet.core.handler.CommandHandler.AbstractCommandHandler import *


class GetInstanceFieldHandler(AbstractCommandHandler):

    def __init__(self):
        self._required_parameters_count = 2

    def process(self, command):
        try:
            if len(command.payload) != self._required_parameters_count:
                raise Exception("GetInstanceFieldHandler parameters mismatch!")
            clazz = command.payload[0]
            field = command.payload[1]
            return getattr(clazz, field)
        except Exception as e:
            exc_type, exc_value = type(e), e
            new_exc = exc_type(exc_value).with_traceback(e.__traceback__)
            raise new_exc from None

