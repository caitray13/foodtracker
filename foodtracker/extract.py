from typing import List

from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline

tokenizer = AutoTokenizer.from_pretrained("Dizex/FoodBaseBERT")
model = AutoModelForTokenClassification.from_pretrained("Dizex/FoodBaseBERT")
pipe = pipeline("ner", model=model, tokenizer=tokenizer)


def extract_entity_weights(corpus: str) -> List[float]:
    list_of_words = corpus.split(" ")
    entity_weights = list(filter(lambda x: x.isnumeric(), list_of_words))
    return entity_weights


def extract_entities(corpus: str) -> List[str]:
    def convert_entities_to_list(text, entities: List[dict]) -> List[str]:
        ents = []
        for ent in entities:
            e = {"start": ent["start"], "end": ent["end"], "label": ent["entity_group"]}
            if (
                ents
                and -1 <= ent["start"] - ents[-1]["end"] <= 1
                and ents[-1]["label"] == e["label"]
            ):
                ents[-1]["end"] = e["end"]
                continue
            ents.append(e)

        return [text[e["start"] : e["end"]] for e in ents]

    ner_entity_results = pipe(corpus, aggregation_strategy="simple")
    entities = convert_entities_to_list(corpus, ner_entity_results)
    return entities


def combine_entity_and_weight(entities: List[str], entity_weights: List[float]) -> dict:
    entities_and_weights = dict(map(lambda i, j: (i, j), entities, entity_weights))
    return entities_and_weights


def extract(corpus: str) -> dict:
    entities = extract_entities(corpus)
    entity_weights = extract_entity_weights(corpus)
    entities_and_weights = combine_entity_and_weight(entities, entity_weights)
    return entities_and_weights