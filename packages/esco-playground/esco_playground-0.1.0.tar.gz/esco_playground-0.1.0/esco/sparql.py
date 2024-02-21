import io

import pandas as pd
from SPARQLWrapper import CSV, SPARQLWrapper

import esco.util


#
# Sparql
#
class SparqlClient:
    def __init__(self, url="http://localhost:18890/sparql"):
        self.url = url
        self.client = SPARQLWrapper(url)
        self.prefixes = {
            "jolux": "http://data.legilux.public.lu/resource/ontology/jolux#",
            "adms": "http://www.w3.org/ns/adms#",
            "skosXl": "http://www.w3.org/2008/05/skos-xl#",
            "owl": "http://www.w3.org/2002/07/owl#",
            "skosxl": "http://www.w3.org/2008/05/skos-xl#",
            "org": "http://www.w3.org/ns/org#",
            "xsd": "http://www.w3.org/2001/XMLSchema#",
            "iso-thes": "http://purl.org/iso25964/skos-thes#",
            "skos": "http://www.w3.org/2004/02/skos/core#",
            "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
            "vocab-adms": "https://www.w3.org/TR/vocab-adms/#",
            "at": "http://publications.europa.eu/ontology/authority/",
            "dct": "http://purl.org/dc/terms/",
            "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
            "esco": "http://data.europa.eu/esco/model#",
            "rov": "http://www.w3.org/ns/regorg#",
            "etms": "http://data.europa.eu/esco/etms/model/#",
            "dcat": "http://www.w3.org/ns/dcat#",
            "euvoc": "http://publications.europa.eu/ontology/euvoc#",
            "prov": "http://www.w3.org/ns/prov#",
            "foaf": "http://xmlns.com/foaf/0.1/",
            "qdr": "http://data.europa.eu/esco/qdr#",
        }

    def query(self, query):
        query = (
            "\n".join([f"PREFIX {k}: <{v}>" for k, v in self.prefixes.items()]) + query
        )
        self.client.setQuery(query)
        self.client.setReturnFormat(CSV)
        results = self.client.query().convert()
        return results

    def load_esco(self, categories=None):
        categories = categories or [
            "http://data.europa.eu/esco/isced-f/06",
            "http://data.europa.eu/esco/skill/243eb885-07c7-4b77-ab9c-827551d83dc4",
            "http://data.europa.eu/esco/skill/b590d4e5-7c62-4b4a-abc2-c270b482e0ce",
        ]

        categories = "\n".join([f"<{uri}>" for uri in categories])

        res = self.query(
            """

            SELECT DISTINCT * WHERE {

            VALUES ?category { """
            + categories
            + """ }

            ?uri a esco:Skill ;
                skos:prefLabel ?label ;
                skos:broaderTransitive* ?category  ;
                esco:skillType _:skillType ;
                iso-thes:status "released"
            .

            _:skillType skos:prefLabel ?skillType .

            OPTIONAL {
                ?uri skos:altLabel ?altLabel .
                ?uri dct:description _:description .

                _:description
                    esco:nodeLiteral ?description;
                    esco:language "en"^^xsd:language
                .
            }

            FILTER (lang(?label) = "en") .
            FILTER(lang(?altLabel) = "en")
            FILTER(lang(?skillType) = "en")
                            }"""
        )
        df = pd.read_csv(io.StringIO(res.decode()))
        return df

    def infer_skills_from_skill(self, skill_uri: str):
        """
        Infer skills from a set of skills.
        """
        query = f"""
        SELECT DISTINCT (?parent AS ?uri) ?label WHERE {{

        ?parent a esco:Skill ;
            skos:prefLabel ?label

        .

        <{skill_uri}> skos:broaderTransitive+ ?parent .

        FILTER (lang(?label) = 'en')
        }}"""

        res = self.query(query)
        df = pd.read_csv(io.StringIO(res.decode()))
        return df.groupby(df.s).agg(lambda x: x.iloc[0]).to_dict(orient="index")

    def load_isco(self, categories=None):
        categories = categories or [  # Defaults to ICT professionals and technicians.
            "http://data.europa.eu/esco/isco/C25",
            "http://data.europa.eu/esco/isco/C35",
        ]

        categories = "\n".join([f"<{uri}>" for uri in categories])

        res = self.query(
            """

        SELECT DISTINCT * WHERE {

        VALUES ?category { """
            + categories
            + """ }

        ?uri a esco:Occupation ;
            skos:prefLabel ?label ;
            esco:relatedEssentialSkill ?s ;
            skos:broaderTransitive* ?category  ;
            iso-thes:status "released"
        .

        # Get current skill labels associated
        #  with the occupation.
        ?s skos:prefLabel ?skill ;
            esco:skillType ?skillType ;
            iso-thes:status "released"
            .
        FILTER (lang(?skill) = "en")

        # If an occupation lacks a description,
        #   don't skip it.
        OPTIONAL {
            ?uri skos:altLabel ?altLabel .
            ?uri dct:description _:description .

            _:description
            esco:nodeLiteral ?description;
            esco:language "en"^^xsd:language
            .
        }

        FILTER (lang(?label) = "en")
        FILTER(lang(?altLabel) = "en")
                        }"""
        )
        df = pd.read_csv(io.StringIO(res.decode()))
        return df

    def load_skills(self):
        df = self.load_esco()
        return esco.util._aggregate_skills(df)

    def load_occupations(self):
        df = self.load_isco()
        return esco.util._aggregate_occupations(df)
