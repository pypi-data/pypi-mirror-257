import logging
from pathlib import Path
from typing import List

import pandas as pd

log = logging.getLogger(__name__)


NS_MAP = {
    "esco:": "http://data.europa.eu/esco/skill/",
    "par-tec:": "http://par-tec.it/esco/skill/",
}


def to_curie(uri: str):
    for k, v in NS_MAP.items():
        if uri.startswith(v):
            return uri.replace(v, k)
    raise ValueError(f"Unknown prefix for {uri}")


def from_curie(curie: str):
    if curie.startswith(("http://", "https://")):
        return curie
    for k, v in NS_MAP.items():
        if curie.startswith(k):
            return curie.replace(k, v)
    raise ValueError(f"Unknown prefix for {curie}")


def _load_resource(name, index="uri") -> pd.DataFrame:
    ret = pd.read_json(Path(__file__).parent / f"{name}", orient="record")
    return ret.set_index(index)


def load_table(table) -> pd.DataFrame:
    """Load the skills from the JSON file."""
    tables = {
        "skills": "esco_s.json.gz",
        "occupations": "esco_o.json.gz",
    }
    if table not in tables:
        raise ValueError(f"Unknown table {table}")
    df = _load_resource(tables[table])
    df.allLabel = df.allLabel.apply(set)
    return df


class LocalDB:
    """
    A preliminary implementation of an ESCO database
    based on pandas and local Qdrant database for
    supporting text and neural search.

    Data is loaded from the JSON file distributed within
    the package.

    TODO: implement interfaces with Qdrant and Virtuoso.
    """

    def __init__(
        self,
        vector_idx=None,
        vector_idx_config: dict = None,
    ):
        log.info("Loading the skills from the JSON file")
        self.skills = load_table("skills")
        self.vector_idx = vector_idx
        self.vector_idx_config = vector_idx_config

        if vector_idx and vector_idx_config:
            raise ValueError("Cannot specify both vector_idx and vector_idx_config")

        if vector_idx_config:
            try:
                from esco.vector import VectorDB

                self.vector_idx = VectorDB(
                    skills=self.skills,
                    force_recreate=False,
                    config=vector_idx_config,
                )
            except ImportError:
                log.warning(
                    "Could not load Qdrant and langchain database. Maybe you need to `pip install .[langchain]`?"
                )
                self.vector_idx = None

    def validate(self):
        """Validate the coherence between self.skills and self.vector_idx."""
        if not self.vector_idx:
            return True
        vector_idx_count = self.vector_idx.qdrant.client.count(
            collection_name=self.vector_idx.config["collection_name"]
        ).count
        skills_count = self.skills.shape[0]
        if vector_idx_count != skills_count:
            raise ValueError(
                f"Skills and vector index have different number of entries: {skills_count} vs {vector_idx_count}"
            )

        return True

    def create_vector_idx(self, vector_idx_config: dict = None):
        from esco.vector import VectorDB

        if vector_idx_config:
            self.vector_idx_config = vector_idx_config
        if self.vector_idx:
            self.vector_idx.qdrant.client.close()

        self.vector_idx = VectorDB(
            skills=self.skills,
            force_recreate=True,
            config=self.vector_idx_config,
        )

    @staticmethod
    def load_skills():
        return load_table("skills")

    @staticmethod
    def load_occupations():
        return load_table("occupations")

    def get_label(self, uri_or_curie: str):
        uri = from_curie(uri_or_curie)
        return self.skills[self.skills.index == uri]["label"].iloc[0]

    def get(self, uri_or_curie: str):
        uri = from_curie(uri_or_curie)
        return self.skills[self.skills.index == uri].iloc[0].to_dict()

    def search_products(self, products: List[str]) -> List[dict]:
        """
        @return a dict of skills related to a set of product labels.
        """
        products = {p.lower() for p in products}
        ret = self.skills[
            self.skills.apply(lambda x: bool(x.allLabel & products), axis=1)
        ]
        return ret[["label"]].reset_index().to_dict(orient="records")

    def search_neural(self, text: str, **params) -> List[dict]:
        """
        @param text: the text to search for.
        @param params: additional parameters to pass to the neural database.
            Currently supported:
            - k: the number of entries to retrieve
            - score_threshold: the score threshold
        @return a dict of skills related to a set of product labels.
        """
        if not self.vector_idx:
            raise NotImplementedError("Vector database not loaded")
        return self.vector_idx.search(text, **params)

    def close(self):
        if self.vector_idx:
            self.vector_idx.close()
