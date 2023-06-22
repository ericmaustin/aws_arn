from __future__ import annotations

from typing import Optional, Tuple, List
from dataclasses import dataclass


class MalformedArnError(Exception):
    def __init__(self, arn_str):
        self.arn_str = arn_str

    def __str__(self):
        return f'malformed arn string: {self.arn_str}'


@dataclass(frozen=True)
class AwsArn:
    """
    AwsArn dataclass contains the arn parts and the original arn string
    """
    partition: str
    service: str
    region: Optional[str]
    account_id: Optional[str]
    resource: str
    resource_type: Optional[str] = None
    resource_id: Optional[str] = None

    def update(self, **kwargs) -> AwsArn:
        for k, v in kwargs.items():
            self.__setattr__(k, v)
        return self

    def clone(
            self,
            partition: Optional[str] = None,
            service: Optional[str] = None,
            region: Optional[str] = None,
            account_id: Optional[str] = None,
            resource: Optional[str] = None,
            resource_type: Optional[str] = None,
            resource_id: Optional[str] = None,
    ) -> AwsArn:
        """
        Clone the AwsArn object with optional new values
        :return: a new AwsArn object
        """
        return AwsArn(
            partition=partition or self.partition,
            service=service or self.service,
            region=region or self.region,
            account_id=account_id or self.account_id,
            resource=resource or self.resource,
            resource_type=resource_type or self.resource_type,
            resource_id=resource_id or self.resource_id,
        )

    def __str__(self):
        return f"arn:{self.partition}:{self.service}:{self.region}:{self.account_id}:{self.resource}"

    @classmethod
    def parse(cls, arn: str) -> AwsArn:
        return parse_arn(arn)


def parse_arn(arn: str) -> AwsArn:
    """ parse the arn string into an AwsArn object """
    if not arn.startswith("arn:"):
        raise MalformedArnError(arn)

    arn_parts = arn.split(":", 5)

    if len(arn_parts) < 6:
        raise MalformedArnError(arn)

    arn_dict = {
        "partition": arn_parts[1],
        "service": arn_parts[2],
        "region": arn_parts[3] if arn_parts[3] != "" else None,
        "account_id": arn_parts[4] if arn_parts[4] != "" else None,
        "resource": arn_parts[5],
        "resource_type": None,
        "resource_id": None,
    }

    if "/" not in arn_dict["resource"] and ":" not in arn_dict["resource"]:
        arn_dict["resource_id"] = arn_dict["resource"]
        return AwsArn(**arn_dict)

    resource_type, resource_id = _parse_resource(arn_dict["resource"])
    arn_dict["resource_type"] = resource_type
    arn_dict["resource_id"] = resource_id

    return AwsArn(**arn_dict)


def _parse_resource(resource) -> Tuple[Optional[str], str]:
    resource_type = None

    first_separator_index = -1
    for idx, c in enumerate(resource):
        if c in (':', '/'):
            first_separator_index = idx
            break

    if first_separator_index != -1:
        resource_type = resource[:first_separator_index]
        resource_id = resource[first_separator_index + 1:]
    else:
        resource_id = resource

    return resource_type, resource_id
