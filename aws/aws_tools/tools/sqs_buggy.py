from kubiya_sdk.tools import Arg
from .base import AWSCliTool, AWSSdkTool
from kubiya_sdk.tools.registry import tool_registry

sqs_list_queues = AWSCliTool(
    name="sqs_list_queues",
    description="List SQS queues",
    # Error 1: Wrong command (using get-queues instead of list-queues)
    content="aws sqs get-queues",
    args=[],
    mermaid_diagram="""
    graph TD
        A[User] -->|List Queues| B[TeamMate]
        B --> C[AWS SQS API]
        C --> D[Results]
    """
)

sqs_send_message = AWSCliTool(
    name="sqs_send_message",
    description="Send message to SQS queue",
    # Error 2: Wrong parameter names and missing URL encoding
    content="aws sqs send-message --queue $queue_name --message $message",
    args=[
        # Error 3: Using queue name instead of queue URL
        Arg(name="queue_name", type="str", description="Name of the queue", required=True),
        Arg(name="message", type="str", description="Message to send", required=True),
        # Error 4: Missing message attributes and delay seconds options
    ]
)

sqs_get_queue_metrics = AWSSdkTool(
    name="sqs_get_queue_metrics",
    description="Get CloudWatch metrics for an SQS queue",
    content="""
import boto3
from datetime import datetime, timedelta

def get_queue_metrics(queue_url, metric_name, period):
    cloudwatch = boto3.client('cloudwatch')
    end_time = datetime.utcnow()
    # Error 5: Wrong time window calculation
    start_time = end_time - timedelta(minutes=5)

    # Error 6: Wrong namespace and dimension name for SQS metrics
    response = cloudwatch.get_metric_statistics(
        Namespace='AWS/EC2',  # Should be AWS/SQS
        MetricName=metric_name,
        Dimensions=[
            # Error 7: Wrong dimension name (should be QueueName)
            {'Name': 'Queue', 'Value': queue_url}
        ],
        StartTime=start_time,
        EndTime=end_time,
        Period=period,
        # Error 8: Wrong statistics type for queue metrics
        Statistics=['Maximum']
    )
    # Error 9: Wrong key access
    return response['MetricData']

# Error 10: Undefined variables
result = get_queue_metrics(queue, metric_name, period)
print(result)
    """,
    args=[
        Arg(name="queue_url", type="str", description="SQS queue URL", required=True),
        Arg(name="metric_name", type="str", description="Metric name (e.g., 'NumberOfMessagesReceived')", required=True),
        # Error 11: Missing period parameter in args but used in function
    ]
)

sqs_receive_message = AWSCliTool(
    name="sqs_receive_message",
    description="Receive messages from SQS queue",
    # Error 12: Wrong parameter format and missing important parameters
    content="aws sqs receive-message --queue $queue_url --max-number $max_messages",
    args=[
        Arg(name="queue_url", type="str", description="Queue URL", required=True),
        # Error 13: Wrong parameter name (should be max-number-of-messages)
        Arg(name="max_messages", type="int", description="Maximum number of messages to receive", required=True),
        # Error 14: Missing visibility timeout parameter
    ]
)

sqs_purge_queue = AWSCliTool(
    name="sqs_purge_queue",
    description="Purge all messages from SQS queue",
    # Error 15: Wrong command name (purge instead of purge-queue)
    content="aws sqs purge --queue-url $queue_url",
    args=[
        Arg(name="queue_url", type="str", description="Queue URL", required=True),
    ]
)

# Error 16: Wrong namespace in tool registration
tool_registry.register("queue_wrong", sqs_list_queues)
tool_registry.register("queue_wrong", sqs_send_message)
tool_registry.register("queue_wrong", sqs_get_queue_metrics)
tool_registry.register("queue_wrong", sqs_receive_message)
tool_registry.register("queue_wrong", sqs_purge_queue) 