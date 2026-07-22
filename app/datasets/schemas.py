from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class DatasetCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    description: str | None = None


class DatasetItemCreate(BaseModel):
    prompt: str = Field(min_length=1)
    expected_output: str = Field(min_length=1)
    metadata: dict | None = None


class DatasetItemResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )

    id: int
    dataset_id: int
    prompt: str
    expected_output: str
    metadata: dict | None = Field(
        default=None,
        validation_alias="item_metadata",
    )


class DatasetResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None = None
    created_at: datetime
    items: list[DatasetItemResponse] = Field(default_factory=list)