from typing import Any, List, Literal, Optional
from uuid import UUID, uuid4

import httpx
from pydantic import BaseModel, ConfigDict, Field


class Retry(BaseModel):
    backoff_millisecs: int
    max_tries: int


class FailureStrategy(BaseModel):
    retry: Retry


class BeamTask(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: UUID = Field(default_factory=uuid4)
    from_: str = Field(alias='from')
    to: List[str]
    body: str
    failure_strategy: FailureStrategy | Literal["discard"]
    ttl: str
    metadata: Optional[Any] = None

BeamWorkStatus = Literal["claimed", "succeeded", "tempfailed", "permfailed"]

class BeamResult(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    task: UUID
    from_: str = Field(alias='from')
    to: List[str]
    body: str
    status: BeamWorkStatus
    metadata: Optional[Any] = None


class BeamClient:
    def __init__(self, app_id, beam_apikey, beam_proxy_url):
        self.base_url = beam_proxy_url
        self.app_id = app_id
        self.client = httpx.AsyncClient(headers={"Authorization": f"ApiKey {app_id} {beam_apikey}"})

    async def post_beam_task(self, task: BeamTask):
        pass

    async def get_beam_tasks(self) -> list[BeamTask]:
        return []

    async def answer_task(self, task: BeamTask, body: str, workstatus: BeamWorkStatus = "succeeded", metadata: Optional[Any] = None):
        pass

    async def get_task_results(self, task_id: UUID) -> list[BeamResult]:
        return []
