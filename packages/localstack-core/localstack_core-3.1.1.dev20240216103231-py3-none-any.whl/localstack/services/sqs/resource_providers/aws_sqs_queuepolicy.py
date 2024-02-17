# LocalStack Resource Provider Scaffolding v2
from __future__ import annotations

import json
from pathlib import Path
from typing import Optional, TypedDict

import localstack.services.cloudformation.provider_utils as util
from localstack.services.cloudformation.resource_provider import (
    OperationStatus,
    ProgressEvent,
    ResourceProvider,
    ResourceRequest,
)


class SQSQueuePolicyProperties(TypedDict):
    PolicyDocument: Optional[dict]
    Queues: Optional[list[str]]
    Id: Optional[str]


REPEATED_INVOCATION = "repeated_invocation"


class SQSQueuePolicyProvider(ResourceProvider[SQSQueuePolicyProperties]):
    TYPE = "AWS::SQS::QueuePolicy"  # Autogenerated. Don't change
    SCHEMA = util.get_schema_path(Path(__file__))  # Autogenerated. Don't change

    def create(
        self,
        request: ResourceRequest[SQSQueuePolicyProperties],
    ) -> ProgressEvent[SQSQueuePolicyProperties]:
        """
        Create a new resource.

        Primary identifier fields:
          - /properties/Id

        Required properties:
          - PolicyDocument
          - Queues

        Read-only properties:
          - /properties/Id

        """
        model = request.desired_state
        sqs = request.aws_client_factory.sqs
        for queue in model.get("Queues", []):
            policy = json.dumps(model["PolicyDocument"])
            sqs.set_queue_attributes(QueueUrl=queue, Attributes={"Policy": policy})

        physical_resource_id = util.generate_default_name(
            stack_name=request.stack_name, logical_resource_id=request.logical_resource_id
        )
        model["Id"] = physical_resource_id

        return ProgressEvent(
            status=OperationStatus.SUCCESS,
            resource_model=model,
            custom_context=request.custom_context,
        )

    def read(
        self,
        request: ResourceRequest[SQSQueuePolicyProperties],
    ) -> ProgressEvent[SQSQueuePolicyProperties]:
        """
        Fetch resource information
        """
        raise NotImplementedError

    def delete(
        self,
        request: ResourceRequest[SQSQueuePolicyProperties],
    ) -> ProgressEvent[SQSQueuePolicyProperties]:
        """
        Delete a resource
        """
        sqs = request.aws_client_factory.sqs
        for queue in request.previous_state["Queues"]:
            try:
                sqs.set_queue_attributes(QueueUrl=queue, Attributes={"Policy": ""})

            except sqs.exceptions.QueueDoesNotExist:
                return ProgressEvent(status=OperationStatus.FAILED, resource_model={})

        return ProgressEvent(
            status=OperationStatus.SUCCESS,
            resource_model={},
        )

    def update(
        self,
        request: ResourceRequest[SQSQueuePolicyProperties],
    ) -> ProgressEvent[SQSQueuePolicyProperties]:
        """
        Update a resource
        """
        raise NotImplementedError
