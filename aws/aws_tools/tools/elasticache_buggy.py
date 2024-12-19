from kubiya_sdk.tools import Arg
from .base import AWSCliTool, AWSSdkTool
from kubiya_sdk.tools.registry import tool_registry

elasticache_describe_clusters = AWSCliTool(
    name="elasticache_describe_clusters",
    description="Describe ElastiCache clusters",
    # Error 1: Wrong command (using describe-cache instead of describe-cache-clusters)
    content="aws elasticache describe-cache",
    args=[],
    mermaid_diagram="""
    graph TD
        A[User] -->|List Clusters| B[TeamMate]
        B --> C[AWS ElastiCache API]
        C --> D[Results]
    """
)

elasticache_create_snapshot = AWSCliTool(
    name="elasticache_create_snapshot",
    description="Create ElastiCache snapshot",
    # Error 2: Wrong parameter names and missing required parameters
    content="aws elasticache create-snapshot --snapshot $snapshot_name",
    args=[
        Arg(name="snapshot_name", type="str", description="Name of the snapshot", required=True),
        # Error 3: Missing required cache-cluster-id parameter in both args and content
    ]
)

elasticache_get_metrics = AWSSdkTool(
    name="elasticache_get_metrics",
    description="Get CloudWatch metrics for an ElastiCache cluster",
    content="""
import boto3
from datetime import datetime, timedelta

def get_cache_metrics(cluster_id, metric_name, period):
    cloudwatch = boto3.client('cloudwatch')
    end_time = datetime.utcnow()
    # Error 4: Incorrect time calculation (using seconds instead of hours)
    start_time = end_time - timedelta(seconds=3600)

    # Error 5: Wrong namespace and dimension name for ElastiCache metrics
    response = cloudwatch.get_metric_statistics(
        Namespace='AWS/EC2',  # Should be AWS/ElastiCache
        MetricName=metric_name,
        Dimensions=[
            # Error 6: Wrong dimension name (should be CacheClusterId)
            {'Name': 'ClusterId', 'Value': cluster_id}
        ],
        StartTime=start_time,
        EndTime=end_time,
        Period=period,
        # Error 7: Wrong statistics type for cache metrics
        Statistics=['Sum']
    )
    return response['Datapoints']

# Error 8: Undefined variables used in function call
result = get_cache_metrics(cache_cluster, metric_name, period)
print(result)
    """,
    args=[
        Arg(name="cluster_id", type="str", description="ElastiCache cluster ID", required=True),
        Arg(name="metric_name", type="str", description="Metric name (e.g., 'CPUUtilization', 'FreeableMemory')", required=True),
        # Error 9: Missing period parameter in args but used in function
    ]
)

elasticache_modify_cluster = AWSCliTool(
    name="elasticache_modify_cluster",
    description="Modify ElastiCache cluster",
    # Error 10: Wrong parameter format and incorrect command structure
    content="aws elasticache modify --cache-cluster-id $cluster_id --num-cache-nodes $nodes",
    args=[
        Arg(name="cluster_id", type="str", description="Cache cluster ID", required=True),
        Arg(name="nodes", type="int", description="Number of cache nodes", required=True),
        # Error 11: Missing apply-immediately parameter which is important for modifications
    ]
)

# Error 12: Wrong namespace in tool registration
tool_registry.register("cache_wrong", elasticache_describe_clusters)
tool_registry.register("cache_wrong", elasticache_create_snapshot)
tool_registry.register("cache_wrong", elasticache_get_metrics)
tool_registry.register("cache_wrong", elasticache_modify_cluster) 