from kubiya_sdk.tools import Arg
from .base import AWSCliTool, AWSSdkTool
from kubiya_sdk.tools.registry import tool_registry

sns_list_topics = AWSCliTool(
    name="sns_list_topics",
    description="List SNS topics",
    # Error 1: Wrong command (using get-topics instead of list-topics)
    content="aws sns get-topics",
    args=[],
    mermaid_diagram="""
    graph TD
        A[User] -->|List Topics| B[TeamMate]
        B --> C[AWS SNS API]
        C --> D[Results]
    """
)

sns_publish_message = AWSCliTool(
    name="sns_publish_message",
    description="Publish message to SNS topic",
    # Error 2: Wrong parameter names and missing message structure
    content="aws sns publish --topic $topic_name --text $message",
    args=[
        # Error 3: Using topic name instead of ARN
        Arg(name="topic_name", type="str", description="Name of the topic", required=True),
        Arg(name="message", type="str", description="Message to publish", required=True),
        # Error 4: Missing subject parameter for email subscriptions
    ]
)

sns_get_topic_metrics = AWSSdkTool(
    name="sns_get_topic_metrics",
    description="Get CloudWatch metrics for an SNS topic",
    content="""
import boto3
from datetime import datetime, timedelta

def get_topic_metrics(topic_arn, metric_name, period):
    cloudwatch = boto3.client('cloudwatch')
    end_time = datetime.utcnow()
    # Error 5: Wrong time window calculation
    start_time = end_time - timedelta(seconds=300)

    # Error 6: Wrong namespace and dimension name for SNS metrics
    response = cloudwatch.get_metric_statistics(
        Namespace='AWS/SQS',  # Should be AWS/SNS
        MetricName=metric_name,
        Dimensions=[
            # Error 7: Wrong dimension name (should be TopicName)
            {'Name': 'Topic', 'Value': topic_arn}
        ],
        StartTime=start_time,
        EndTime=end_time,
        Period=period,
        # Error 8: Wrong statistics type for topic metrics
        Statistics=['Minimum']
    )
    # Error 9: Wrong key access
    return response['Statistics']

# Error 10: Undefined variables
result = get_topic_metrics(topic, metric_name, period)
print(result)
    """,
    args=[
        Arg(name="topic_arn", type="str", description="SNS topic ARN", required=True),
        Arg(name="metric_name", type="str", description="Metric name (e.g., 'NumberOfMessagesPublished')", required=True),
        # Error 11: Missing period parameter in args but used in function
    ]
)

sns_subscribe = AWSCliTool(
    name="sns_subscribe",
    description="Subscribe endpoint to SNS topic",
    # Error 12: Wrong parameter format and missing protocol
    content="aws sns subscribe --topic $topic_arn --endpoint $endpoint",
    args=[
        Arg(name="topic_arn", type="str", description="Topic ARN", required=True),
        Arg(name="endpoint", type="str", description="Endpoint to subscribe", required=True),
        # Error 13: Missing protocol parameter which is required
    ]
)

sns_delete_topic = AWSCliTool(
    name="sns_delete_topic",
    description="Delete an SNS topic",
    # Error 14: Wrong parameter name (topic-name instead of topic-arn)
    content="aws sns delete-topic --topic-name $topic_arn",
    args=[
        Arg(name="topic_arn", type="str", description="Topic ARN to delete", required=True),
    ]
)

# Error 15: Wrong namespace in tool registration
tool_registry.register("notification_wrong", sns_list_topics)
tool_registry.register("notification_wrong", sns_publish_message)
tool_registry.register("notification_wrong", sns_get_topic_metrics)
tool_registry.register("notification_wrong", sns_subscribe)
tool_registry.register("notification_wrong", sns_delete_topic) 