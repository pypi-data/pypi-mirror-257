import copy
import datetime
from enum import Enum
from typing import Union

from aws_cdk import Duration
from aws_cdk.aws_sqs import Queue
from constructs import Construct

from infraflow.cdk.docker import EcsCluster, add_queue_environment_variables, ContainerSize, ContainerImage
from infraflow.cdk.events import Event
from infraflow.cdk.lambdas import LambdaContext


class PROCESSOR_TYPE(Enum):
    LAMBDA_PYTHON = 1
    ECS_DOCKER = 2

class ProcessorConfig:
    type: PROCESSOR_TYPE
    def __init__(
        self,
        type: PROCESSOR_TYPE,
        retry_self=False,
        # retry_default=False,
    ):
        # self.retry_default = retry_default
        self.retry_self = retry_self
        self.type = type


class LambdaPythonProcessorConfig(ProcessorConfig):
    def __init__(self, handler: str, timeout: Union[Duration, datetime.timedelta, int], max_concurrency: int = None, batch_size=1) -> None:
        super().__init__(PROCESSOR_TYPE.LAMBDA_PYTHON)
        self.batch_size = batch_size
        self.timeout = timeout
        self.handler = handler
        self.max_concurrency = max_concurrency


class EcsDockerProcessorConfig(ProcessorConfig):
    def __init__(
            self,
            image: ContainerImage,
            command: str,
            count: int = 1,
            size: ContainerSize = ContainerSize(),
            batch_size: int = 50,
            max_retries: int = 0,
            environment: dict[str, str] = {}
    ):
        """
        Initializes an instance of the class.

        :param path: The path of the code with the docker file.
        :param command: The command to execute on the docker container.
        :param ecr_image: The ECR image to use for processing.
        :param count: The number of container instances to create for processing.
        :param cpu: The CPU units to allocate for each instance.
        :param memory_limit_mib: The memory limit in MiB for each instance.
        :param max_coroutines: The maximum number of coroutines to use for processing.
        :param max_retries: The maximum number of retries for failed tasks.
        :param environment: Additional environment variables to set.

        """
        super().__init__(PROCESSOR_TYPE.ECS_DOCKER)
        self.size = size
        self.image = image
        self.memory_limit_mib = size.memory_limit_mib
        self.cpu = size.cpu
        self.count = count
        self.max_coroutines = batch_size
        self.max_retries = max_retries
        self.environment = copy.copy(environment)
        self.environment['BATCH_SIZE'] = str(batch_size)
        self.environment['MAX_RETRIES'] = str(max_retries)
        self.command = command


class DualPriorityResilientProcessor(Construct):
    def __init__(
            self,
            scope: Construct,
            construct_id: str,
            event: Event,
            lambda_context: LambdaContext,
            ecs_cluster: EcsCluster,
            default_processor: ProcessorConfig=None,
            express_processor: ProcessorConfig=None,
            # retry_processor: ProcessorConfig=None,
            dead_letter_processor: ProcessorConfig=None
    ) -> None:
        super().__init__(scope, construct_id)
        self.name = construct_id
        self.ecs_cluster = ecs_cluster
        self.lambda_context = lambda_context
        self.express_event = copy.copy(event).express_only() if express_processor else None
        self.default_event = copy.copy(event).non_express() if express_processor else copy.copy(event)
        self.default_processor = default_processor
        self.express_processor = express_processor
        # self.retry_processor = retry_processor
        self.dead_letter_processor = dead_letter_processor

    def create_resources(self):
        if isinstance(self.dead_letter_processor, LambdaPythonProcessorConfig):
            dead_letter_processor = copy.copy(self.dead_letter_processor)
            dead_letter_processor.max_concurrency = 0
            dlq = self.create_lambda_processor(dead_letter_processor, 'DeadLetter')
        elif isinstance(self.dead_letter_processor, EcsDockerProcessorConfig):
            dlq = Queue(self, 'DeadLetterQueue')
        else:
            dlq = None

        # if isinstance(self.retry_processor, LambdaPythonProcessorConfig):
        #     retry_qf = self.create_lambda_processor(self.retry_processor, 'Retry', dlq=dlq)
        #     retry_queue = retry_qf.queue
        # elif isinstance(self.retry_processor, EcsDockerProcessorConfig):
        #     retry_queue = Queue(self, 'RetryQueue')
        # else:
        #     retry_queue = None

        if isinstance(self.default_processor, LambdaPythonProcessorConfig):
            default_qf = self.create_lambda_processor(self.default_processor, 'Default', dlq=dlq)
            self.default_event.subscribe(default_qf)
        elif isinstance(self.default_processor, EcsDockerProcessorConfig):
            queue, service = self.create_ecs_processor(self.default_processor, 'Default')
            self.default_event.subscribe(queue)

        if isinstance(self.express_processor, LambdaPythonProcessorConfig):
            express_qf = self.create_lambda_processor(self.express_processor, 'Express', dlq=dlq)
            self.express_event.subscribe(express_qf)
        elif isinstance(self.express_processor, EcsDockerProcessorConfig):
            queue, service = self.create_ecs_processor(self.express_processor, 'Express')
            self.express_event.subscribe(queue)

    def create_lambda_processor(self, processor_config: LambdaPythonProcessorConfig, suffix, dlq):
        return self.lambda_context.queued_function(
            processor_config.handler,
            timeout=processor_config.timeout,
            max_concurrency=processor_config.max_concurrency,
            batch_size=processor_config.batch_size,
            suffix=suffix,
            dead_letter_queue=dlq
        )

    def create_ecs_processor(self, processor_config: EcsDockerProcessorConfig, suffix, retry_url, dlq_url):
        queue = Queue(self, suffix+'Queue', dead_letter_queue=dlq_url)
        add_queue_environment_variables(
            processor_config.environment,
            queue=queue.queue_url,
            retry=retry_url or (queue.queue_url if processor_config.retry_self else None),
            dlq=dlq_url
        )
        return queue, self.ecs_cluster.service(
            name=self.name+suffix,
            environment={**self.ecs_cluster.scope.env.environment_vars, **processor_config.environment},
            count=processor_config,
            size=processor_config.size,
            image=processor_config.image,
            command=processor_config.command
        )