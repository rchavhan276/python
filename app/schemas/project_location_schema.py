from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID


class ProjectLocationModel(BaseModel):
    id: UUID
    project_id: UUID
    location_id: UUID
    created_at: datetime
    updated_at: datetime


class AddProjectLocationModel(BaseModel):
    project_id: UUID = Field(alias = "projectId")
    location_id: UUID = Field(alias = "locationId")
 