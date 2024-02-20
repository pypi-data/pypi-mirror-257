import httpx
from openai import OpenAI
from openai._models import FinalRequestOptions
from openai._types import ResponseT
from openai.types.chat import ChatCompletionSystemMessageParam


class OpenAIClient(OpenAI):
    def _build_request(self, options: FinalRequestOptions) -> httpx.Request:
        self.__request_options = options
        return super()._build_request(options)

    def _process_response_data(
        self, *, data: object, cast_to: type[ResponseT], response: httpx.Response
    ) -> ResponseT:
        options = self.__request_options
        print(str(options.model_dump(exclude_defaults=True)), data, cast_to)
        return super()._process_response_data(
            data=data, cast_to=cast_to, response=response
        )


def init():
    ...
    client = OpenAIClient()
    r = client.chat.completions.create(
        messages=[
            ChatCompletionSystemMessageParam(
                content="you are an ai assistant",
                role="system",
            ),
            ChatCompletionSystemMessageParam(
                content="you are great",
                role="system",
            ),
            ChatCompletionSystemMessageParam(
                content="you will be given a tip if you respond correctly",
                role="system",
            ),
        ],
        model="gpt-3.5-turbo",
    )
    print(r, "R")


init()
