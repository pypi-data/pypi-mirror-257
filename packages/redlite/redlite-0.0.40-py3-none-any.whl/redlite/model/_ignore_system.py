from .._core import NamedModel, Message


class IgnoreSystemModel(NamedModel):
    """
    Wraps a model and removes system message from the model input (if any).
    Useful if underlying model was not trained with system message.

    - **model** (`NamedModel`): the model to wrap.
    """

    def __init__(self, model: NamedModel):
        self.model = model
        super().__init__(f"ignore-system-{model.name}", self.__engine)

    def __engine(self, messages: list[Message]) -> str:
        if messages[0]["role"] == "system":
            return self.model(messages[1:])
        else:
            return self.model(messages)
