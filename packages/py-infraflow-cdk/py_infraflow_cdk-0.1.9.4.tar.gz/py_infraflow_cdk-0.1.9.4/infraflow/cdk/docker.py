import copy

from aws_cdk import aws_ecs as ecs
from aws_cdk import aws_ecs_patterns as ecs_patterns
from aws_cdk import aws_ecr_assets as assets
from aws_cdk.aws_ec2 import SubnetSelection, SubnetType
from aws_cdk.aws_ecs import Cluster

from infraflow.cdk import ServiceStageStack
from infraflow.cdk.sg.patterns import SecurityGroupTarget


class ContainerSize:
    def __init__(self, cpu: int = 256, memory_limit_mib: int = 512):
        self.memory_limit_mib = memory_limit_mib
        self.cpu = cpu


class ContainerImage:
    def __init__(
            self,
            path=None,
            ecr_image=None,
    ):
        self.ecr_image = ecr_image
        self.path = path


class EcsCluster:
    def __init__(self, scope: ServiceStageStack, cluster_name: str, subnet_type: SubnetType = SubnetType.PRIVATE_WITH_EGRESS):
        self.subnet_type = subnet_type
        self.scope = scope
        vpc = self.scope.env.vpc

        self.cluster = ecs.Cluster(self.scope, cluster_name, vpc=vpc)

    def service(self,
                name,
                image: ContainerImage,
                command: str = None,
                count=1,
                size: ContainerSize = ContainerSize(),
                environment: dict[str, str] = {}
                ):
        environment = {**self.scope.env.environment_vars, **environment}
        if image.path:
            image_asset = assets.DockerImageAsset(self.scope, f"{name}_image", directory=image.path)
            local_image = ecs.ContainerImage.from_docker_image_asset(image_asset)
        else:
            local_image = None

        return ecs_patterns.ApplicationLoadBalancedFargateService(
            self.scope, f"{name}_service",
            cluster=self.cluster,  # Required
            cpu=size.cpu,  # Default is 256
            desired_count=count,  # Default is 1
            listener_port=80,
            task_image_options=ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
                image=ecs.ContainerImage.from_registry(image.ecr_image) if image.ecr_image else local_image if image.path else None,
                container_name=f"{name}_task",
                container_port=80,
                environment=environment,
                command=command
            ),
            security_groups=[
                self.scope.security_groups.get_group(target=SecurityGroupTarget(
                    self.cluster,
                    id=name,
                    cdk_type=Cluster,
                    infraflow_pattern=self,
                ))
            ],
            task_subnets=SubnetSelection(subnets=self.scope.env.service_subnets(self.subnet_type)),
            memory_limit_mib=size.memory_limit_mib,  # Default is 512
            public_load_balancer=True
        )  # Default is True


def add_queue_environment_variables(
        environment: dict[str, str],
        queue,
        retry=None,
        dlq=None
) -> dict[str, str]:
    environment = copy.copy(environment)
    environment['SQS_QUEUE'] = retry
    environment['SQS_RETRY_QUEUE'] = retry
    environment['SQS_DEAD_LETTER_QUEUE'] = dlq
    return environment