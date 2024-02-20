import copy
import datetime
from enum import Enum
from typing import Union

from aws_cdk import Duration
from aws_cdk.aws_sqs import Queue
from constructs import Construct
from infraflow.cdk.events import Event
from infraflow.cdk.lambdas import LambdaContext


class PROCESSOR_TYPE(Enum):
    LAMBDA_PYTHON = 1
    ECS_DOCKER = 2

class ProcessorConfig:
    type: PROCESSOR_TYPE
    def __init__(self, type: PROCESSOR_TYPE)
        self.type = type

class LambdaPythonProcessorConfig(ProcessorConfig):
    def __init__(self, handler: str, timeout: Union[Duration, datetime.timedelta, int], max_concurrency: int = None, batch_size=1) -> None:
        super().__init__(PROCESSOR_TYPE.LAMBDA_PYTHON)
        self.batch_size = batch_size
        self.timeout = timeout
        self.handler = handler
        self.max_concurrency = max_concurrency


class EcsDockerProcessorConfig(ProcessorConfig):
    def __init__(self):
        super().__init__(PROCESSOR_TYPE.ECS_DOCKER)

class ExpressDefaultDlqProcessor(Construct):
    def __init__(
            self,
            scope: Construct,
            construct_id: str,
            event: Event,
            lambda_context: LambdaContext,
            default_processor: ProcessorConfig=None,
            express_processor: ProcessorConfig=None,
            retry_processor: ProcessorConfig=None,
            dead_letter_processor: ProcessorConfig=None
    ) -> None:
        super().__init__(scope, construct_id)
        self.lambda_context = lambda_context
        self.express_event = copy.copy(event).express_only()
        self.default_event = copy.copy(event).non_express()
        self.default_processor = default_processor
        self.express_processor = express_processor
        self.retry_processor = retry_processor
        self.dead_letter_processor = dead_letter_processor

    def resources(self):
        if isinstance(self.dead_letter_processor, LambdaPythonProcessorConfig):
            dead_letter_processor = copy.copy(self.dead_letter_processor)
            dead_letter_processor.max_concurrency = 0
            dlq = self.create_lambda_processor(dead_letter_processor, 'DeadLetter')
        elif isinstance(self.retry_processor, EcsDockerProcessorConfig):
            dlq = Queue(self, 'DeadLetterQueue')
        else:
            dlq = None

        if isinstance(self.express_processor, LambdaPythonProcessorConfig):
            express_qf = self.create_lambda_processor(self.express_processor, 'Express', dlq=dlq)
            self.express_event.subscribe(express_qf)
        elif isinstance(self.express_processor, EcsDockerProcessorConfig):
            queue = Queue(self, 'ExpressQueue')
            self.express_event.subscribe(queue)

        if isinstance(self.default_processor, LambdaPythonProcessorConfig):
            default_qf = self.create_lambda_processor(self.default_processor, 'Default', dlq=dlq)
            self.default_event.subscribe(default_qf)
        elif isinstance(self.default_processor, EcsDockerProcessorConfig):
            queue = Queue(self, 'DefaultQueue')
            self.default_event.subscribe(queue)


        if isinstance(self.retry_processor, LambdaPythonProcessorConfig):
            retry_qf = self.create_lambda_processor(self.retry_processor, 'Retry', dlq=dlq)
        elif isinstance(self.retry_processor, EcsDockerProcessorConfig):
            queue = Queue(self, 'RetryQueue')


    def create_lambda_processor(self, processor_config: LambdaPythonProcessorConfig, suffix, dlq):
        return self.lambda_context.queued_function(
            processor_config.handler,
            timeout=processor_config.timeout,
            max_concurrency=processor_config.max_concurrency,
            batch_size=processor_config.batch_size,
            suffix=suffix,
            dead_letter_queue=dlq
        )