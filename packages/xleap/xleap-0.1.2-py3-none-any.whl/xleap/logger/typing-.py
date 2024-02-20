from dataclasses import dataclass


class MissingAttribute(ValueError):
    @classmethod
    def build(cls, name: str, *args: list[str]):
        return MissingAttribute(
            f"{', '.join(args[:-1])} and {args[-1]} are required for {name}"
        )


@dataclass
class DataPoint:
    prompt: str
    response: str
    # a list of context strings
    context: list[str] | None
    # a list of ground truth answer strings
    answer: list[str] | None

    def answer_accuracy(self):
        if not self.prompt or not self.response or not self.answer:
            raise MissingAttribute.build(
                "answer_accuracy", "prompt, response, answer".split(", ")
            )

    def answer_relevancy(self):
        if not self.prompt or not self.response:
            raise MissingAttribute.build(
                "answer_relevancy", "prompt, response".split(", ")
            )

    def answer_groundedness(self):
        if not self.prompt or not self.response or not self.context:
            raise MissingAttribute.build(
                "answer_groundedness", "prompt, response, context".split(", ")
            )
