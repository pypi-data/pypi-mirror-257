# LocalStack Resource Provider Scaffolding v2
from __future__ import annotations

from pathlib import Path
from typing import Optional, TypedDict

import localstack.services.cloudformation.provider_utils as util
from localstack.services.cloudformation.resource_provider import (
    OperationStatus,
    ProgressEvent,
    ResourceProvider,
    ResourceRequest,
)


class LogsSubscriptionFilterProperties(TypedDict):
    DestinationArn: Optional[str]
    FilterPattern: Optional[str]
    LogGroupName: Optional[str]
    Distribution: Optional[str]
    FilterName: Optional[str]
    RoleArn: Optional[str]


REPEATED_INVOCATION = "repeated_invocation"


class LogsSubscriptionFilterProvider(ResourceProvider[LogsSubscriptionFilterProperties]):
    TYPE = "AWS::Logs::SubscriptionFilter"  # Autogenerated. Don't change
    SCHEMA = util.get_schema_path(Path(__file__))  # Autogenerated. Don't change

    def create(
        self,
        request: ResourceRequest[LogsSubscriptionFilterProperties],
    ) -> ProgressEvent[LogsSubscriptionFilterProperties]:
        """
        Create a new resource.

        Primary identifier fields:
          - /properties/FilterName
          - /properties/LogGroupName

        Required properties:
          - DestinationArn
          - FilterPattern
          - LogGroupName

        Create-only properties:
          - /properties/FilterName
          - /properties/LogGroupName



        IAM permissions required:
          - iam:PassRole
          - logs:PutSubscriptionFilter
          - logs:DescribeSubscriptionFilters

        """
        model = request.desired_state
        logs = request.aws_client_factory.logs

        logs.put_subscription_filter(
            logGroupName=model["LogGroupName"],
            filterName=model["LogGroupName"],
            filterPattern=model["FilterPattern"],
            destinationArn=model["DestinationArn"],
        )

        return ProgressEvent(
            status=OperationStatus.SUCCESS,
            resource_model=model,
            custom_context=request.custom_context,
        )

    def read(
        self,
        request: ResourceRequest[LogsSubscriptionFilterProperties],
    ) -> ProgressEvent[LogsSubscriptionFilterProperties]:
        """
        Fetch resource information

        IAM permissions required:
          - logs:DescribeSubscriptionFilters
        """
        raise NotImplementedError

    def delete(
        self,
        request: ResourceRequest[LogsSubscriptionFilterProperties],
    ) -> ProgressEvent[LogsSubscriptionFilterProperties]:
        """
        Delete a resource

        IAM permissions required:
          - logs:DeleteSubscriptionFilter
        """
        model = request.desired_state
        logs = request.aws_client_factory.logs

        logs.delete_subscription_filter(
            logGroupName=model["LogGroupName"],
            filterName=model["LogGroupName"],
        )

        return ProgressEvent(
            status=OperationStatus.SUCCESS,
            resource_model=model,
            custom_context=request.custom_context,
        )

    def update(
        self,
        request: ResourceRequest[LogsSubscriptionFilterProperties],
    ) -> ProgressEvent[LogsSubscriptionFilterProperties]:
        """
        Update a resource

        IAM permissions required:
          - logs:PutSubscriptionFilter
          - logs:DescribeSubscriptionFilters
        """
        raise NotImplementedError
