import operator
from abc import ABC, abstractmethod
from collections import defaultdict, deque
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Any, Dict, Literal, List

import torch
from yaloader import loads

from mllooper import Module, State, ModuleConfig, LooperState
from mllooper.data import DatasetState
from mllooper.logging.messages import ScalarLogMessage


@dataclass
class MetricState(State):
    output: Optional[Any] = None


class Metric(Module, ABC):
    def __init__(self, requires_grad: bool = False,
                 state_name_dataset: Optional[str] = 'dataset_state',
                 state_name_looper: Optional[str] = 'looper_state',
                 state_name_model: Optional[str] = 'model_state',
                 **kwargs):
        super().__init__(**kwargs)
        self.state_name = self.name
        self.requires_grad = requires_grad

        self.state = MetricState()

        self._last_log_time_per_dataset = {}

        self.state_name_dataset: Optional[str] = state_name_dataset
        self.state_name_looper: Optional[str] = state_name_looper
        self.state_name_model: Optional[str] = state_name_model

    def log(self, state: State) -> None:
        """Save last log time per dataset name."""
        try:
            dataset_state: DatasetState = getattr(state, self.state_name_dataset)
        except AttributeError as e:
            self.logger.warning(e)
            return

        dataset_name = dataset_state.name
        now = datetime.now()
        last_log_time = self._last_log_time_per_dataset.get(dataset_name, None)
        if last_log_time and now - last_log_time < self.log_time_delta:
            return

        self._last_log_time = now
        self._last_log_time_per_dataset[dataset_name] = now
        self._log(state)

    def step(self, state: State) -> None:
        dataset_state: DatasetState = getattr(state, self.state_name_dataset)
        self.state.output = None

        with torch.set_grad_enabled(dataset_state.train and self.requires_grad):
            metric_output = self.calculate_metric(state)

        self.state.output = metric_output
        setattr(state, self.state_name, self.state)

    @abstractmethod
    def calculate_metric(self, state: State) -> Any:
        raise NotImplementedError

    def state_dict(self) -> Dict[str, Any]:
        state_dict = super(Metric, self).state_dict()
        state_dict.update(
            requires_grad=self.requires_grad,
            state=self.state
        )
        return state_dict

    def load_state_dict(self, state_dict: Dict[str, Any], strict: bool = True) -> None:
        requires_grad = state_dict.pop('requires_grad')
        state = state_dict.pop('state')

        super(Metric, self).load_state_dict(state_dict)

        self.requires_grad = requires_grad
        self.state = state

    @torch.no_grad()
    def is_better(self, x, y) -> bool:
        """Return True if x is better than y in sense of the metric.

        For every metric every value should be better than None.
        """
        raise NotImplementedError


@loads(None)
class MetricConfig(ModuleConfig):
    requires_grad: bool = False
    state_name_dataset: Optional[str] = 'dataset_state'
    state_name_looper: Optional[str] = 'looper_state'
    state_name_model: Optional[str] = 'model_state'


class ScalarMetric(Metric):
    def __init__(self, reduction: Literal['mean', 'sum'] = 'mean', **kwargs):
        super().__init__(**kwargs)
        self.reduction = reduction

    @abstractmethod
    def calculate_metric(self, state: State) -> torch.Tensor:
        raise NotImplementedError

    def _log(self, state: State) -> None:
        looper_state: LooperState = getattr(state, self.state_name_looper)
        dataset_state: DatasetState = getattr(state, self.state_name_dataset)

        output: torch.Tensor = self.state.output

        self.logger.debug(ScalarLogMessage(
            tag=f"{dataset_state.name}/{self.name}", step=looper_state.total_iteration,
            scalar=float(output.detach().cpu().item())
        ))

    def state_dict(self) -> Dict[str, Any]:
        state_dict = super(ScalarMetric, self).state_dict()
        state_dict.update(
            reduction=self.reduction,
        )
        return state_dict

    def load_state_dict(self, state_dict: Dict[str, Any], strict: bool = True) -> None:
        reduction = state_dict.pop('reduction')

        super(ScalarMetric, self).load_state_dict(state_dict)

        self.reduction = reduction


@loads(None)
class ScalarMetricConfig(MetricConfig):
    reduction: Literal['mean', 'sum'] = 'mean'


@dataclass
class AveragedMetricState(MetricState):
    output: Optional[Any] = None
    average: Optional[Any] = None


class AveragedMetric(ScalarMetric):
    def __init__(self, metric: ScalarMetric, avg_decay: float = 0.995, ignore_nan: bool = True, **kwargs):
        name = kwargs.pop('name')
        name = "Averaged" if name is None else name
        super().__init__(name=f"{name} {metric.name}", **kwargs)
        self.metric = metric
        self.avg_decay = avg_decay
        self.ignore_nan = ignore_nan
        self.state = AveragedMetricState()
        self.average_per_dataset = {}

    def initialise(self, modules: Dict[str, 'Module']) -> None:
        self.metric.initialise(modules)

    def teardown(self, state: State) -> None:
        self.metric.teardown(state)

    def log(self, state: State) -> None:
        super(AveragedMetric, self).log(state)
        self.metric.log(state)

    def _log(self, state: State) -> None:
        looper_state: LooperState = getattr(state, self.state_name_looper)
        dataset_state: DatasetState = getattr(state, self.state_name_dataset)

        dataset_average = self.average_per_dataset.get(dataset_state.name, None)
        if dataset_average is not None:
            self.logger.debug(ScalarLogMessage(
                tag=f"{dataset_state.name}/{self.name}", step=looper_state.total_iteration,
                scalar=float(dataset_average.detach().cpu().item())
            ))

    def step(self, state: State) -> None:
        dataset_state: DatasetState = getattr(state, self.state_name_dataset)
        self.state.output = None
        self.state.average = None

        with torch.set_grad_enabled(dataset_state.train and self.requires_grad):
            metric_output = self.calculate_metric(state)

        self.state.output = metric_output
        # Needed for logging in the metric itself
        self.metric.state.output = metric_output

        with torch.set_grad_enabled(False):
            dataset_average = self.average_per_dataset.get(dataset_state.name, None)
            if not torch.any(torch.isnan(metric_output)) or not self.ignore_nan:
                if dataset_average is None:
                    dataset_average = metric_output.detach()
                else:
                    dataset_average = self.avg_decay * dataset_average + (1.0 - self.avg_decay) * metric_output.detach()
            self.average_per_dataset[dataset_state.name] = dataset_average
            self.state.average = self.average_per_dataset[dataset_state.name]
        setattr(state, self.name, self.state)

    def calculate_metric(self, state: State) -> torch.Tensor:
        return self.metric.calculate_metric(state)

    def state_dict(self) -> Dict[str, Any]:
        state_dict = super(AveragedMetric, self).state_dict()
        state_dict.update(
            metric_state_dict=self.metric.state_dict(),
            avg_decay=self.avg_decay,
            state=self.state
        )
        return state_dict

    def load_state_dict(self, state_dict: Dict[str, Any], strict: bool = True) -> None:
        metric_state_dict = state_dict.pop('metric_state_dict')
        avg_decay = state_dict.pop('avg_decay')
        state = state_dict.pop('state')

        super(AveragedMetric, self).load_state_dict(state_dict)

        self.metric.load_state_dict(metric_state_dict)
        self.avg_decay = avg_decay
        self.state = state

    @torch.no_grad()
    def is_better(self, x, y) -> bool:
        return self.metric.is_better(x, y)


@loads(AveragedMetric)
class AveragedMetricConfig(ScalarMetricConfig):
    metric: ScalarMetricConfig
    avg_decay: float = 0.995
    ignore_nan: bool = True

    def load(self, *args, **kwargs):
        config_data = dict(self)
        config_data['metric'] = config_data['metric'].load()
        return self._loaded_class(**config_data)


@dataclass
class MeanMetricState(MetricState):
    output: Optional[Any] = None
    mean: Optional[Any] = None


class MeanMetric(ScalarMetric):
    def __init__(self, metric: ScalarMetric, ignore_nan: bool = True, **kwargs):
        name = kwargs.pop('name')
        name = "Mean" if name is None else name
        super().__init__(name=f"{name} {metric.name}", **kwargs)
        self.metric = metric
        self.ignore_nan = ignore_nan
        self.state = MeanMetricState()
        self.mean_per_dataset = {}
        self.samples_per_dataset = {}

    def initialise(self, modules: Dict[str, 'Module']) -> None:
        self.metric.initialise(modules)

    def teardown(self, state: State) -> None:
        self.metric.teardown(state)

    def log(self, state: State) -> None:
        super(MeanMetric, self).log(state)
        self.metric.log(state)

    def _log(self, state: State) -> None:
        looper_state: LooperState = getattr(state, self.state_name_looper)
        dataset_state: DatasetState = getattr(state, self.state_name_dataset)

        dataset_mean = self.mean_per_dataset.get(dataset_state.name, None)
        if dataset_mean is not None:
            self.logger.debug(ScalarLogMessage(
                tag=f"{dataset_state.name}/{self.name}", step=looper_state.total_iteration,
                scalar=float(dataset_mean.detach().cpu().item())
            ))

    def step(self, state: State) -> None:
        dataset_state: DatasetState = getattr(state, self.state_name_dataset)
        self.state.output = None
        self.state.mean = None

        with torch.set_grad_enabled(dataset_state.train and self.requires_grad):
            metric_output = self.calculate_metric(state)
        self.state.output = metric_output
        # Needed for logging in the metric itself
        self.metric.state.output = metric_output

        with torch.set_grad_enabled(False):
            dataset_mean = self.mean_per_dataset.get(dataset_state.name, None)
            dataset_sample_count = self.samples_per_dataset.get(dataset_state.name, 0)

            if not torch.any(torch.isnan(metric_output)) or not self.ignore_nan:
                if dataset_mean is None:
                    dataset_mean = metric_output.detach()
                    dataset_sample_count = 1
                else:
                    dataset_mean = (dataset_mean * dataset_sample_count + metric_output.detach()) / (dataset_sample_count+1)
                    dataset_sample_count += 1

            self.mean_per_dataset[dataset_state.name] = dataset_mean
            self.samples_per_dataset[dataset_state.name] = dataset_sample_count

            self.state.mean = self.mean_per_dataset[dataset_state.name]
        setattr(state, self.name, self.state)

    def calculate_metric(self, state: State) -> Any:
        return self.metric.calculate_metric(state)

    def state_dict(self) -> Dict[str, Any]:
        state_dict = super(MeanMetric, self).state_dict()
        state_dict.update(
            metric_state_dict=self.metric.state_dict(),
            state=self.state
        )
        return state_dict

    def load_state_dict(self, state_dict: Dict[str, Any], strict: bool = True) -> None:
        metric_state_dict = state_dict.pop('metric_state_dict')
        state = state_dict.pop('state')

        super(MeanMetric, self).load_state_dict(state_dict)

        self.metric.load_state_dict(metric_state_dict)
        self.state = state

    @torch.no_grad()
    def is_better(self, x, y) -> bool:
        return self.metric.is_better(x, y)


@loads(MeanMetric)
class MeanMetricConfig(ScalarMetricConfig):
    metric: ScalarMetricConfig
    ignore_nan: bool = True

    def load(self, *args, **kwargs):
        config_data = dict(self)
        config_data['metric'] = config_data['metric'].load()
        return self._loaded_class(**config_data)


@dataclass
class RunningMeanMetricState(MetricState):
    output: Optional[Any] = None


class RunningMeanMetric(ScalarMetric):
    def __init__(self, max_len: int, metric: ScalarMetric, ignore_nan: bool = False, **kwargs):
        name = kwargs.pop('name')
        name = "Running Mean" if name is None else name
        super().__init__(name=f"{name} {metric.name}", **kwargs)
        self.max_len = max_len
        self.metric = metric
        self.ignore_nan = ignore_nan
        self.state = RunningMeanMetricState()
        self.deque_per_dataset = defaultdict(lambda: deque(maxlen=self.max_len))

    def initialise(self, modules: Dict[str, 'Module']) -> None:
        self.metric.initialise(modules)

    def teardown(self, state: State) -> None:
        self.metric.teardown(state)

    def log(self, state: State) -> None:
        super(RunningMeanMetric, self).log(state)
        self.metric.log(state)

    def _log(self, state: State) -> None:
        looper_state: LooperState = getattr(state, self.state_name_looper)
        dataset_state: DatasetState = getattr(state, self.state_name_dataset)

        dataset_values: List[torch.Tensor] = list(self.deque_per_dataset[dataset_state.name])
        if dataset_values is not None and len(dataset_values) > 0:
            if self.ignore_nan:
                mean = torch.nanmean(torch.stack(dataset_values).squeeze())
            else:
                mean = torch.mean(torch.stack(dataset_values).squeeze())
            self.logger.debug(ScalarLogMessage(
                tag=f"{dataset_state.name}/{self.name}", step=looper_state.total_iteration,
                scalar=float(mean.detach().cpu().item())
            ))

    def step(self, state: State) -> None:
        dataset_state: DatasetState = getattr(state, self.state_name_dataset)
        self.state.output = None
        self.state.running_mean = None

        with torch.set_grad_enabled(dataset_state.train and self.requires_grad):
            metric_output = self.calculate_metric(state)
        self.state.output = metric_output
        # Needed for logging in the metric itself
        self.metric.state.output = metric_output

        with torch.set_grad_enabled(False):
            dataset_deque = self.deque_per_dataset[dataset_state.name]

            dataset_deque.append(metric_output.detach())

        setattr(state, self.name, self.state)

    def calculate_metric(self, state: State) -> Any:
        return self.metric.calculate_metric(state)

    def state_dict(self) -> Dict[str, Any]:
        state_dict = super(RunningMeanMetric, self).state_dict()
        state_dict.update(
            metric_state_dict=self.metric.state_dict(),
            state=self.state
        )
        return state_dict

    def load_state_dict(self, state_dict: Dict[str, Any], strict: bool = True) -> None:
        metric_state_dict = state_dict.pop('metric_state_dict')
        state = state_dict.pop('state')

        super(RunningMeanMetric, self).load_state_dict(state_dict)

        self.metric.load_state_dict(metric_state_dict)
        self.state = state

    @torch.no_grad()
    def is_better(self, x, y) -> bool:
        return self.metric.is_better(x, y)


@loads(RunningMeanMetric)
class RunningMeanMetricConfig(ScalarMetricConfig):
    max_len: int
    metric: ScalarMetricConfig
    ignore_nan: bool = False

    def load(self, *args, **kwargs):
        config_data = dict(self)
        config_data['metric'] = config_data['metric'].load()
        return self._loaded_class(**config_data)


@dataclass
class MetricListState(State):
    metrics: Dict[str, Any] = field(default_factory=dict)


class MetricList(Module):
    def __init__(self, metrics: List[Metric], **kwargs):
        super().__init__(**kwargs)
        self.metrics = metrics
        self.state = MetricListState()

    def initialise(self, modules: Dict[str, 'Module']) -> None:
        for metric in self.metrics:
            metric.initialise(modules)

    def teardown(self, state: State) -> None:
        for metric in self.metrics:
            metric.teardown(state)

    def log(self, state: State) -> None:
        super(MetricList, self).log(state)
        for metric in self.metrics:
            metric.log(state)

    def step(self, state: State) -> None:
        self.state.metrics = {}

        for metric in self.metrics:
            keys_in_state_before_metric = set(state.__dict__.keys())
            metric.step(state)
            for key in set(state.__dict__.keys()):
                if key in keys_in_state_before_metric:
                    continue
                self.state.metrics[key] = state.__dict__.pop(key)

        setattr(state, 'metrics_state', self.state)

    def state_dict(self) -> Dict[str, Any]:
        state_dict = super(MetricList, self).state_dict()
        state_dict.update(
            metric_state_dicts=[metric.state_dict() for metric in self.metrics],
            state=self.state
        )
        return state_dict

    def load_state_dict(self, state_dict: Dict[str, Any], strict: bool = True) -> None:
        metric_state_dicts = state_dict.pop('metric_state_dicts')
        state = state_dict.pop('state')

        super(MetricList, self).load_state_dict(state_dict)

        for metric, metric_state_dict in zip(self.metrics, metric_state_dicts):
            metric.load_state_dict(metric_state_dict)
        self.state = state

    def is_better(self, x, y) -> bool:
        raise NotImplementedError


@loads(MetricList)
class MetricListConfig(ModuleConfig):
    metrics: List[MetricConfig]

    def load(self, *args, **kwargs):
        config_data = dict(self)
        config_data['metrics'] = [metric_config.load() for metric_config in config_data['metrics']]
        return self._loaded_class(**config_data)


class Loss(ScalarMetric):
    def __init__(self, metrics: List[ScalarMetric], weights: Optional[List[float]] = None,
                 requires_grad: bool = True, state_name_loss: str = 'loss_state', **kwargs):
        if not requires_grad:
            self.logger.warning(f"requires_grad of {self.name} is always set to True.")
        name = kwargs.pop('name')
        name = f"Loss({', '.join(map(operator.attrgetter('name'), metrics))})" if name is None else name
        super().__init__(name=name, requires_grad=True, **kwargs)
        self.state_name = state_name_loss

        self.metrics = metrics
        self.weights = weights
        if self.weights is not None and len(self.metrics) != len(self.weights):
            raise ValueError(f"Metrics and weights have to to of same length.")
        elif self.weights is None:
            self.weights = [1.0 for _ in self.metrics]
        for metric in self.metrics:
            metric.requires_grad = True
        self.state = MetricState()

    def initialise(self, modules: Dict[str, 'Module']) -> None:
        for metric in self.metrics:
            metric.initialise(modules)

    def teardown(self, state: State) -> None:
        for metric in self.metrics:
            metric.teardown(state)

    def log(self, state: State) -> None:
        super(Loss, self).log(state)
        for metric in self.metrics:
            metric.log(state)

    def calculate_metric(self, state: State) -> torch.Tensor:
        output = None
        weight_sum = 0.0
        for metric, weight in zip(self.metrics, self.weights):
            keys_in_state_before_metric = set(state.__dict__.keys())
            metric.step(state)
            for key in set(state.__dict__.keys()):
                if key in keys_in_state_before_metric:
                    continue
                metric_state: MetricState = state.__dict__.pop(key)
                if output is None:
                    output = metric_state.output * weight
                else:
                    output = output + metric_state.output * weight
                weight_sum += weight
        output = output / weight_sum
        return output

    def state_dict(self) -> Dict[str, Any]:
        state_dict = super(Loss, self).state_dict()
        state_dict.update(
            metric_state_dicts=[metric.state_dict() for metric in self.metrics],
            weights=self.weights,
            state=self.state
        )
        return state_dict

    def load_state_dict(self, state_dict: Dict[str, Any], strict: bool = True) -> None:
        metric_state_dicts = state_dict.pop('metric_state_dicts')
        weights = state_dict.pop('weights')
        state = state_dict.pop('state')

        super(Loss, self).load_state_dict(state_dict)

        for metric, metric_state_dict in zip(self.metrics, metric_state_dicts):
            metric.load_state_dict(metric_state_dict)
        self.weights = weights
        self.state = state

    def is_better(self, x, y) -> bool:
        raise NotImplementedError


@loads(Loss)
class LossConfig(MetricConfig):
    requires_grad: bool = True
    metrics: List[ScalarMetricConfig]
    weights: Optional[List[float]] = None
    state_name_loss: str = 'loss_state'

    def load(self, *args, **kwargs):
        config_data = dict(self)
        config_data['metrics'] = [metric_config.load() for metric_config in config_data['metrics']]
        return self._loaded_class(**config_data)
