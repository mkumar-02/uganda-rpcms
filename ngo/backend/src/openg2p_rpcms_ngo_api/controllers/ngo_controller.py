import logging
from typing import Optional

from openg2p_fastapi_common.controller import BaseController

from ..config import Settings
from ..errors import NgoNotFoundError
from ..schemas import (
    LocationCreate,
    LocationListResponse,
    LocationResponse,
    MouCreate,
    MouListResponse,
    MouResponse,
    MouSignRequest,
    NgoListResponse,
    NgoResponse,
    NgoUpdate,
)
from ..services import LocationService, MouService, NgoService

_config = Settings.get_config()
_logger = logging.getLogger(_config.logging_default_logger_name)


class NgoController(BaseController):
    """Staff APIs for partner master records, MoUs, and locations."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ngos = NgoService.get_component()
        self.mous = MouService.get_component()
        self.locations = LocationService.get_component()
        self.router.tags += ["Partners"]

        self.router.add_api_route(
            "/ngos",
            self.list_ngos,
            methods=["GET"],
            responses={200: {"model": NgoListResponse}},
        )
        self.router.add_api_route(
            "/ngos/{ngo_id}",
            self.get_ngo,
            methods=["GET"],
            responses={200: {"model": NgoResponse}},
        )
        self.router.add_api_route(
            "/ngos/{ngo_id}",
            self.update_ngo,
            methods=["PATCH"],
            responses={200: {"model": NgoResponse}},
        )
        self.router.add_api_route(
            "/ngos/{ngo_id}/mous",
            self.list_mous,
            methods=["GET"],
            responses={200: {"model": MouListResponse}},
        )
        self.router.add_api_route(
            "/ngos/{ngo_id}/mous",
            self.create_mou,
            methods=["POST"],
            responses={200: {"model": MouResponse}},
        )
        self.router.add_api_route(
            "/mous/{mou_id}/sign",
            self.sign_mou,
            methods=["POST"],
            responses={200: {"model": MouResponse}},
        )
        self.router.add_api_route(
            "/ngos/{ngo_id}/locations",
            self.list_locations,
            methods=["GET"],
            responses={200: {"model": LocationListResponse}},
        )
        self.router.add_api_route(
            "/ngos/{ngo_id}/locations",
            self.create_location,
            methods=["POST"],
            responses={200: {"model": LocationResponse}},
        )
        self.router.add_api_route(
            "/locations/{location_id}",
            self.delete_location,
            methods=["DELETE"],
            responses={200: {"model": dict}},
        )

    async def list_ngos(self, status: Optional[str] = None):
        rows = await self.ngos.list_ngos(status=status)
        return NgoListResponse(
            count=len(rows), ngos=[NgoResponse.model_validate(r) for r in rows]
        )

    async def get_ngo(self, ngo_id: str):
        ngo = await self.ngos.get(ngo_id)
        if not ngo:
            raise NgoNotFoundError(ngo_id)
        return NgoResponse.model_validate(ngo)

    async def update_ngo(self, ngo_id: str, body: NgoUpdate):
        ngo = await self.ngos.update(ngo_id, body)
        return NgoResponse.model_validate(ngo)

    async def list_mous(self, ngo_id: str):
        rows = await self.mous.list_for_ngo(ngo_id)
        return MouListResponse(
            count=len(rows), mous=[MouResponse.model_validate(r) for r in rows]
        )

    async def create_mou(self, ngo_id: str, body: MouCreate):
        mou = await self.mous.create(ngo_id, body)
        return MouResponse.model_validate(mou)

    async def sign_mou(self, mou_id: str, body: MouSignRequest = None):
        mou = await self.mous.mark_signed(mou_id, body or MouSignRequest())
        return MouResponse.model_validate(mou)

    async def list_locations(self, ngo_id: str):
        rows = await self.locations.list_for_ngo(ngo_id)
        return LocationListResponse(
            count=len(rows),
            locations=[LocationResponse.model_validate(r) for r in rows],
        )

    async def create_location(self, ngo_id: str, body: LocationCreate):
        loc = await self.locations.create(ngo_id, body)
        return LocationResponse.model_validate(loc)

    async def delete_location(self, location_id: str):
        await self.locations.delete(location_id)
        return {"deleted": location_id}
