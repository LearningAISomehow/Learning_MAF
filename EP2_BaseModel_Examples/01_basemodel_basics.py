"""EP2: understand BaseModel before connecting an LLM.

Install: python -m pip install pydantic==2.13.4
Run:     python 01_basemodel_basics.py

All input data in this file is written by hand for teaching.
This example does not call an LLM or write to a database.
"""

import json
from typing import Literal

from pydantic import BaseModel, Field, ValidationError


# 1. Define the shape of one answer. BaseModel comes from Pydantic.
class MemoryDecision(BaseModel):
    memory_type: Literal["profile", "preference", "event", "none"]
    memory_key: str
    memory_value: str = Field(
        description=(
            "For a preference, extract only the activity or preference "
            "explicitly stated by the user. Do not add details."
        )
    )


def main() -> None:
    # 2. Turn JSON text into a validated Python object.
    # This is a hand-written sample, not a live model response.
    sample_json = (
        '{"memory_type": "preference", "memory_key": "likes", '
        '"memory_value": "gardening"}'
    )
    decision = MemoryDecision.model_validate_json(sample_json)
    print("1. JSON text -> Python object")
    print("Object type:", type(decision).__name__)
    print("Field access:", decision.memory_value)

    # 3. Use the fields in ordinary application code.
    if decision.memory_type == "preference":
        print("Preference ready for application code:", decision.memory_value)
    print("As a dictionary:", decision.model_dump())
    print("As JSON text:", decision.model_dump_json())

    # 4. The schema describes the answer's structure, not an actual answer.
    schema = MemoryDecision.model_json_schema()
    print("\n2. JSON Schema")
    print(json.dumps(schema, indent=2))

    # Field(description=...) adds guidance. It does not supply a default.
    print("\n3. A description does not make a field optional")
    try:
        MemoryDecision(memory_type="preference", memory_key="likes")
    except ValidationError as error:
        print("Missing memory_value rejected:", error.errors()[0]["msg"])

    # 5. Literal allows only the listed category values.
    print("\n4. An invalid category is rejected")
    try:
        MemoryDecision.model_validate(
            {
                "memory_type": "important",
                "memory_key": "likes",
                "memory_value": "gardening",
            }
        )
    except ValidationError as error:
        print("Rejected:", error.errors()[0]["msg"])

    # 6. A structurally valid answer can still have the wrong meaning.
    # We deliberately replace gardening with skydiving to show the boundary.
    wrong_meaning = MemoryDecision.model_validate(
        {
            "memory_type": "preference",
            "memory_key": "likes",
            "memory_value": "skydiving",
        }
    )
    print("\n5. Valid structure does not guarantee correct meaning")
    print("Original message: I like gardening.")
    print("This passes validation:", wrong_meaning.model_dump_json())
    print("But skydiving was not stated in the original message.")


if __name__ == "__main__":
    main()
