from pydantic import BaseModel, Field, IPvAnyNetwork, AliasChoices


class IPRouteScheme(BaseModel):
    id: str = Field(
        default=None,
        validation_alias=AliasChoices(
            ".id",
            "id",
        ),
        serialization_alias=".id",
    )

    active: bool
    disabled: bool = Field(default=None)
    distance: int = Field(default=None)
    dst_address: IPvAnyNetwork = Field(
        default=None,
        validation_alias=AliasChoices(
            "dst_address",
            "dst-address",
        ),
    )
    dynamic: bool = Field(default=None, exclude=True, frozen=True)
    ecmp: bool = Field(default=None, exclude=True, frozen=True)
    gateway: str = Field(default=None)
    hw_offloaded: bool = Field(default=None, alias="hw-offloaded")
    immediate_gw: str = Field(default=None, alias="immediate-gw")
    inactive: bool = Field(default=None)
    pref_src: str = Field(default=None, alias="immediate-gw")
    routing_table: str = Field(default=None, alias="routing-table")
    scope: int = Field(default=None)
    static: bool = Field(default=None)
    suppress_hw_offload: bool = Field(
        default=None, alias="suppress-hw-offload"
    )
    target_scope: int = Field(default=None, alias="target-scope")

    @staticmethod
    def api_patch(_id=None):
        path = "/rest/ip/route"
        if _id:
            return f"{path}/{_id}"
        return path

    class Config:
        populate_by_name = True


a = [
    {
        ".id": "*80000060",
        "active": "true",
        "disabled": "false",
        "distance": "1",
        "dst-address": "0.0.0.0/0",
        "dynamic": "false",
        "ecmp": "false",
        "gateway": "Shkaver_8",
        "hw-offloaded": "false",
        "immediate-gw": "Shkaver_8",
        "inactive": "false",
        "pref-src": "",
        "routing-table": "Shkaver_8",
        "scope": "30",
        "static": "true",
        "suppress-hw-offload": "false",
        "target-scope": "10",
    }
]
