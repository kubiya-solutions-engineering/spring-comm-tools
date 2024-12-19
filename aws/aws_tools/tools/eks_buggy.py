from kubiya_sdk.tools import Arg
from .base import AWSCliTool, AWSSdkTool
from kubiya_sdk.tools.registry import tool_registry

eks_list_clusters = AWSCliTool(
    name="eks_list_clusters",
    description="List EKS clusters",
    # Error 1: Wrong service name (using ecs instead of eks)
    content="aws ecs list-clusters",
    args=[],
    mermaid_diagram="""
    graph TD
        A[User] -->|List Clusters| B[TeamMate]
        B --> C[AWS EKS API]
        C --> D[Results]
    """
)

eks_describe_nodegroup = AWSCliTool(
    name="eks_describe_nodegroup",
    description="Describe EKS nodegroup",
    # Error 2: Wrong parameter names and missing required cluster-name
    content="aws eks describe-nodegroup --nodegroup $nodegroup_name",
    args=[
        # Error 3: Missing required cluster_name argument
        Arg(name="nodegroup_name", type="str", description="Name of the nodegroup", required=True),
    ]
)

eks_get_cluster_metrics = AWSSdkTool(
    name="eks_get_cluster_metrics",
    description="Get CloudWatch metrics for an EKS cluster",
    content="""
import boto3
from datetime import datetime, timedelta

def get_cluster_metrics(cluster_name, metric_name, period):
    cloudwatch = boto3.client('cloudwatch')
    end_time = datetime.utcnow()
    # Error 4: Wrong time window (using minutes instead of hours)
    start_time = end_time - timedelta(minutes=1)

    # Error 5: Wrong namespace and dimensions for EKS metrics
    response = cloudwatch.get_metric_statistics(
        Namespace='AWS/EC2',  # Should be ContainerInsights
        MetricName=metric_name,
        Dimensions=[
            # Error 6: Wrong dimension names
            {'Name': 'ClusterName', 'Value': cluster_name}
        ],
        StartTime=start_time,
        EndTime=end_time,
        # Error 7: Period too short for EKS metrics
        Period=10,
        Statistics=['Average']
    )
    # Error 8: Accessing wrong key in response
    return response['MetricDatapoints']

result = get_cluster_metrics(cluster_name, metric_name, period)
print(result)
    """,
    args=[
        Arg(name="cluster_name", type="str", description="EKS cluster name", required=True),
        Arg(name="metric_name", type="str", description="Metric name (e.g., 'node_cpu_utilization')", required=True),
        Arg(name="period", type="int", description="Period in seconds", required=True),
    ]
)

eks_update_kubeconfig = AWSCliTool(
    name="eks_update_kubeconfig",
    description="Update kubeconfig for EKS cluster",
    # Error 9: Wrong parameter format and missing required parameters
    content="aws eks update-kubeconfig --name=$cluster_name --role-arn=$role",
    args=[
        Arg(name="cluster_name", type="str", description="EKS cluster name", required=True),
        # Error 10: Making role_arn required when it should be optional
        Arg(name="role", type="str", description="IAM role ARN", required=True),
    ]
)

# Error 11: Wrong namespace in tool registration
tool_registry.register("kubernetes", eks_list_clusters)
tool_registry.register("kubernetes", eks_describe_nodegroup)
tool_registry.register("kubernetes", eks_get_cluster_metrics)
tool_registry.register("kubernetes", eks_update_kubeconfig) 