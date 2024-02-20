from typing import List, Text, Type

from belfry_python_anvil.api_resources.base import BaseModel


def get_payload_attrs(payload_model: Type[BaseModel]) -> List[Text]:
    return list(payload_model.model_fields.keys())
