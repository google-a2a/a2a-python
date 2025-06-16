"""A2A Pydantic Base Model with shared configuration."""

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_snake


class A2ABaseModel(BaseModel):
    """Base model for all A2A types with shared configuration."""

    model_config = ConfigDict(
        alias_generator=to_snake,
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )
