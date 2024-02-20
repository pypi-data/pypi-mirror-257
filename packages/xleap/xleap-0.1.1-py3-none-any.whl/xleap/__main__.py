import pandas as pd
from rich.console import Console
from rich.table import Table

from xleap.metrics.base import prompt_length, response_length, response_space_count
from xleap.metrics.evaluate import evaluate
from xleap.metrics.scores import textstat

# from xleap.metrics.abc.nlp import bleu, rouge
# from xleap.metrics.stat import metrics
# from xleap.metrics.toxicity import PromptToxicity, ResponseToxicity

# # from xleap.metrics.nlp.relevance_to_prompt import input_output

# app = typer.Typer()
console = Console()


# @app.command()
def hi():
    # return
    # df = Dataset.from_csv("./data.csv")
    df = pd.read_csv("./data.csv", index_col=0)
    a = [
        "bleu",
        "rouge",
        "prompt.osman",
        "response.osman",
        "prompt.crawford",
        "output_structure",
        "prompt.char_count",
        "prompt.smog_index",
        "response.crawford",
        "prompt.gunning_fog",
        "prompt.letter_count",
        "response.char_count",
        "response.smog_index",
        "prompt.lexicon_count",
        "prompt.text_standard",
        "response.gunning_fog",
        "prompt.gulpease_index",
        "prompt.sentence_count",
        "prompt.syllable_count",
        "response.letter_count",
        "prompt.difficult_words",
        "prompt.monosyllabcount",
        "prompt.polysyllabcount",
        "prompt.szigriszt_pazos",
        "response.lexicon_count",
        "response.text_standard",
        "prompt.fernandez_huerta",
        "prompt.gutierrez_polini",
        "response.gulpease_index",
        "response.sentence_count",
        "response.syllable_count",
        "response.difficult_words",
        "response.monosyllabcount",
        "response.polysyllabcount",
        "response.szigriszt_pazos",
        "prompt.coleman_liau_index",
        "response.fernandez_huerta",
        "response.gutierrez_polini",
        "prompt.flesch_reading_ease",
        "prompt.flesch_kincaid_grade",
        "response.coleman_liau_index",
        "prompt.linsear_write_formula",
        "response.flesch_reading_ease",
        "response.flesch_kincaid_grade",
        "response.linsear_write_formula",
        "prompt.automated_readability_index",
        "prompt.dale_chall_readability_score",
        "response.automated_readability_index",
        "response.dale_chall_readability_score",
        "reasons",
        "faithfulness",
        "answer_relevancy",
        "context_relevancy",
        "context_recall",
        "ground_truths",
        "contexts",
    ]

    df.drop(a, axis=1, inplace=True)

    df.rename(columns={"question": "prompt", "answer": "response"}, inplace=True)

    df: pd.DataFrame = df.loc[range(0, 100)]
    # evaluate(df, [prompt_length] + metrics)
    # evaluate(df, [prompt_length] + metrics)
    evaluate(df, [prompt_length] + textstat)
    evaluate(df, [prompt_length, response_space_count])
    evaluate(df, [prompt_length, response_length])
    evaluate(df, [prompt_length])
    # evaluate(df, [prompt_length] + metrics, force=True)
    evaluate(df, [prompt_length, response_space_count])
    evaluate(df, [prompt_length])
    evaluate(df, [prompt_length, response_length, response_space_count, response_length])

    return df


if __name__ == "__main__":
    """some thing just like this"""
    # typer.run(app)
    r = hi()
    scores = r
    table = Table("Name", "Values")
    # for k, v in scores.items():
    #     v: list[ItemResult]
    #     table.add_row(k, ", ".join([str(ItemResult(*i).value) for i in v]))
    print(r.columns, r)

# a = xleap._client.DataPointCreate(
#     question="Question: What were the temperatures and snowfall amounts during the cold snap in Afghanistan in January 2023, and how many people and livestock were affected?",
#     answer="During the cold snap in Afghanistan in January 2023, temperatures dropped to record lows, reaching as low as -30 degrees Celsius (-22 degrees Fahrenheit) in some regions. The snowfall amounts varied across the country, with some areas experiencing heavy snowfall of up to 2 meters (6.5 feet), while others received lighter snowfall of around 30 centimeters (1 foot).\n\nAs for the number of people and livestock affected, it is estimated that approximately 500,000 people and 1 million livestock were affected by the extreme cold and heavy snowfall. These severe weather conditions caused disruptions in transportation, power outages, and limited access to essential services, leading to significant challenges for the affected population.",
# )
# b = xleap._client.DataPointCreate(
#     question="did any russian player play?",
#     answer="Yes, Russian players participated in Wimbledon 2023.",
#     contexts=[
#         "players, after they were banned from the previous edition due to the Russian invasion of Ukraine.",
#         "Mate Pavić /  Lyudmyla Kichenok def.  Joran Vliegen /  Xu Yifan, 6-4, 6-7(9-11), 6-3",
#         "disrupted by rain.The tournament saw the return of Russian and Belarusian tennis players, after",
#         "The tournament was played on grass courts, with all main draw matches played at the All England",
#     ],
# )


# print(r.scores, "scores", r)


# def main(name: str = "Xleap"):
#     print(f"Hello {name}")

#     client = Xleap()
#     r = client.create_data_point_create(data_point_create=b)
#     print(r)


# metrics = ['prompt.flesch_reading_ease', 'response.flesch_reading_ease', 'bleu', 'meteor', 'rouge', 'relevance_to_prompt']
# for i in a:
#     ...:     b.append(i.result.get('results', {}))

# b=Dataset.from_pandas(pd.DataFrame(data=[i.result.get('results', {}) for i in a]))


# In [77]: for i in a:
#     ...:     b.append(i.result.get('results', {}))


# b =
