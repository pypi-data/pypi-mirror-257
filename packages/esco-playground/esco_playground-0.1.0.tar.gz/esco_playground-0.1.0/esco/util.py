import pandas as pd


def _aggregate_skills(df):
    """
    Aggregate skills by uri.
    Concatenate the values label, altLabel and description in the `text` column separated by "; "

    """
    skills = df.groupby("uri").agg(
        {
            "label": lambda x: x.iloc[0],
            "altLabel": lambda x: list(set(x)),
            "description": lambda x: x.iloc[0],
            "skillType": lambda x: x.iloc[0],
        }
    )
    # Add a lowercase text field for semantic search.
    skills["text"] = skills.apply(
        lambda x: "; ".join([x.label] + x.altLabel + [x.description]).lower(), axis=1
    )
    # .. and a set of all the labels for each skill.

    skills["allLabel"] = skills.apply(
        lambda x: {t.lower() for t in x.altLabel} | {x.label.lower()}, axis=1
    )
    return skills


def _aggregate_occupations(df):
    """
    Aggregate occupations by uri.
    """
    o = df.groupby("uri").apply(
        lambda x: pd.Series(
            {
                "label": x.label.iloc[0],
                "altLabel": list(set(x.altLabel)),
                "description": x.description.iloc[0],
                "skill": list(set(x.skill.values)),
                "skill_": list(set(x[x.skillType.str.endswith("skill")].skill.values)),
                "knowledge_": list(
                    set(x[x.skillType.str.endswith("knowledge")].skill.values)
                ),
                "s": list(set(x.s.values)),
            }
        )
    )
    # Add a lowercase text field for semantic search.
    o["text"] = o.apply(
        lambda x: "; ".join([x.label] + x.altLabel + [x.description]).lower(), axis=1
    )
    # .. and a set of all the labels for each skill.

    o["allLabel"] = o.apply(
        lambda x: {t.lower() for t in x.altLabel} | {x.label.lower()}, axis=1
    )
    return o
