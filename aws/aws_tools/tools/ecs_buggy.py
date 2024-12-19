from kubiya_sdk.tools import Arg
from .base import AWSCliTool, AWSSdkTool
from kubiya_sdk.tools.registry import tool_registry

ecs_list_clusters = AWSCliTool(
    name="ecs_list_clusters",
    description="List ECS clusters",
    # Error 1: Wrong command (using describe instead of list-clusters)
    content="aws ecs describe-clusters",
    args=[],
    mermaid_diagram="""
    graph TD
        A[User] -->|List ECS Clusters| B[TeamMate]
        B --> C[AWS ECS API]
        C --> D[Results]
    """
)

ecs_describe_tasks = AWSCliTool(
    name="ecs_describe_tasks",
    description="Describe ECS tasks",
    # Error 2: Missing required --cluster parameter and wrong parameter name for tasks
    content="aws ecs describe-tasks --task-id $task_ids",
    args=[
        Arg(name="task_ids", type="str", description="Task IDs to describe", required=True),
    ]
)

ecs_get_service_metrics = AWSSdkTool(
    name="ecs_get_service_metrics",
    description="Get CloudWatch metrics for an ECS service",
    content="""
import boto3
from datetime import datetime, timedelta

def get_service_metrics(cluster_name, service_name, metric_name, period):
    cloudwatch = boto3.client('cloudwatch')
    end_time = datetime.utcnow()
    # Error 3: Wrong time calculation (using days instead of hours)
    start_time = end_time - timedelta(days=1)

    # Error 4: Wrong namespace and dimension name for ECS metrics
    response = cloudwatch.get_metric_statistics(
        Namespace='AWS/EC2',
        MetricName=metric_name,
        Dimensions=[{'Name': 'ServiceName', 'Value': service_name}],
        StartTime=start_time,
        EndTime=end_time,
        Period=period,
        Statistics=['Average']
    )
    return response['Datapoints']

result = get_service_metrics(cluster_name, service_name, metric_name, period)
print(result)
    """,
    args=[
        Arg(name="cluster_name", type="str", description="ECS cluster name", required=True),
        Arg(name="service_name", type="str", description="ECS service name", required=True),
        Arg(name="metric_name", type="str", description="Metric name (e.g., 'CPUUtilization', 'MemoryUtilization')", required=True),
        Arg(name="period", type="int", description="Period in seconds", required=True),
    ]
)

ecs_run_task = AWSCliTool(
    name="ecs_run_task",
    description="Run an ECS task",
    # Error 5: Missing required parameters and wrong parameter names
    content="aws ecs run-task --task $task_definition",
    args=[
        Arg(name="task_definition", type="str", description="Task definition name", required=True),
    ]
)

# Error 6: Registering tools with wrong namespace
tool_registry.register("ecs_wrong", ecs_list_clusters)
tool_registry.register("ecs_wrong", ecs_describe_tasks)
tool_registry.register("ecs_wrong", ecs_get_service_metrics)
tool_registry.register("ecs_wrong", ecs_run_task) 