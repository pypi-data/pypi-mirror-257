from __future__ import annotations


from pydantic import (
    BaseModel,
    Field,
    field_validator,
    IPvAnyAddress,
    AliasChoices,
)


class L2TPClientScheme(BaseModel):
    id: str = Field(
        default=None,
        validation_alias=AliasChoices(
            ".id",
            "id",
        ),
        serialization_alias=".id",
    )
    add_default_route: bool = Field(
        default=False,
        validation_alias=AliasChoices(
            "add-default-route",
            "add_default_route",
        ),
        serialization_alias="add-default-route",
    )
    allow: list = Field(default=[])

    allow_fast_path: bool = Field(
        default=False,
        validation_alias=AliasChoices(
            "allow-fast-path",
            "allow_fast_path",
        ),
        serialization_alias="allow-fast-path",
    )
    comment: str = Field(default="")

    connect_to: IPvAnyAddress | str = Field(
        default=None,
        validation_alias=AliasChoices(
            "connect-to",
            "connect_to",
        ),
        serialization_alias="connect-to",
    )

    dial_on_demand: bool = Field(
        default=False,
        validation_alias=AliasChoices(
            "dial-on-demand",
            "dial_on_demand",
        ),
        serialization_alias="dial-on-demand",
    )

    disabled: bool = Field(default=False)

    ipsec_secret: str = Field(
        default="",
        validation_alias=AliasChoices(
            "ipsec-secret",
            "ipsec_secret",
        ),
        serialization_alias="ipsec-secret",
    )

    keepalive_timeout: int = Field(
        default=60,
        validation_alias=AliasChoices(
            "keepalive-timeout",
            "keepalive_timeout",
        ),
        serialization_alias="keepalive-timeout",
    )
    l2tp_proto_version: str = Field(
        default="l2tpv2",
        validation_alias=AliasChoices(
            "l2tp-proto-version",
            "l2tp_proto_version",
        ),
        serialization_alias="l2tp-proto-version",
    )
    l2tpv3_digest_hash: str = Field(
        default="md5",
        validation_alias=AliasChoices(
            "l2tpv3-digest-hash",
            "l2tpv3_digest_hash",
        ),
        serialization_alias="l2tpv3-digest-hash",
    )
    max_mru: int = Field(
        default=1450,
        validation_alias=AliasChoices(
            "max-mru",
            "max_mru",
        ),
        serialization_alias="max-mru",
    )
    max_mtu: int = Field(
        default=1450,
        validation_alias=AliasChoices(
            "max-mtu",
            "max_mtu",
        ),
        serialization_alias="max-mtu",
    )
    mrru: str = Field(default="disabled")
    name: str

    password: str
    profile: str = Field(default="default-encryption")
    running: bool = Field(
        default=None,
        exclude=True,
        frozen=True,
    )
    use_ipsec: bool = Field(
        default=False,
        validation_alias=AliasChoices(
            "use-ipsec",
            "use_ipsec",
        ),
        serialization_alias="use-ipsec",
    )
    use_peer_dns: str = Field(
        default="no",
        validation_alias=AliasChoices(
            "use-peer-dns",
            "use_peer_dns",
        ),
        serialization_alias="use-peer-dns",
    )
    user: str = Field(default="")

    @field_validator("allow", mode="before")
    def allow_validate(cls, allow) -> list:
        if isinstance(allow, str):
            return allow.split(",")
        else:
            return allow

    @staticmethod
    def api_patch(_id=None):
        path = "/rest/interface/l2tp-client"
        if _id:
            return f"{path}/{_id}"
        return path

    class Config:
        populate_by_name = True
        json_encoders = {
            list: lambda v: ",".join(v),  # преобразовать списки в строку
            int: lambda v: str(v),  # преобразовать числа в строку
            bool: lambda v: v,  # только так работает
        }
