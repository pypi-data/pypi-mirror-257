# Copyright Open Logistics Foundation
#
# Licensed under the Open Logistics Foundation License 1.3.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: OLFL-1.3

"""
Definition of the Config that is used to configure the models of the
mlcvzoo_tf_classification package.
"""
import logging
from typing import List, Optional, Union

import related
from attr import define
from config_builder import BaseConfigClass
from mlcvzoo_base.api.configuration import InferenceConfig as APIInferenceConfig
from mlcvzoo_base.api.configuration import ModelConfiguration
from mlcvzoo_base.configuration.annotation_handler_config import AnnotationHandlerConfig
from mlcvzoo_base.configuration.class_mapping_config import ClassMappingConfig
from mlcvzoo_base.configuration.reduction_mapping_config import ReductionMappingConfig

from .const import LossTypes, OptimizerTypes

logger = logging.getLogger(__name__)


@define
class NetConfig(BaseConfigClass):
    """
    Here the base parameters for the model configuration are extracted.
    """

    __related_strict__ = True

    model_path: str = related.StringField()

    build_custom_net: bool = related.BooleanField()

    input_shape: List[int] = related.SequenceField(cls=int)

    save_weights_only: Optional[bool] = related.BooleanField(
        required=False, default=True
    )

    def check_values(self) -> bool:
        success: bool = True

        if self.input_shape is not None:
            success = success and len(self.input_shape) == 3
            if not success:
                logger.error(
                    "\nCheck for attribute 'input_shape' failed\n"
                    "condition: len(input_shape) == 3, found input_shape=%s"
                    % self.input_shape
                )

        return success


@define
class InferenceConfig(APIInferenceConfig):
    """
    Parameters for tensorflow model inference.
    """

    __related_strict__ = True

    top: Optional[int] = related.IntegerField(required=False, default=None)
    # TODO: Refactor the NetConfig to use this checkpoint_path attribute instead of the
    #       model_path
    checkpoint_path: str = ""
    config_path: Optional[str] = None
    score_threshold: Optional[float] = related.FloatField(required=False, default=None)  # type: ignore

    reduction_class_mapping: Optional[ReductionMappingConfig] = related.ChildField(
        cls=ReductionMappingConfig, required=False, default=None
    )

    def check_values(self) -> bool:
        success: bool = True

        if self.top is not None:
            success = success and self.top >= 1
            if not success:
                logger.error(
                    "\nCheck for attribute 'top' failed\n"
                    "condition: top >= 1, found top=%s" % self.top
                )

        if self.score_threshold is not None:
            success = success and 0.0 <= self.score_threshold <= 1.0
            if not success:
                logger.error(
                    "\nCheck for attribute 'top' failed\n"
                    "condition: 0.0 <= score_threshold <= 1.0, found score_threshold=%s"
                    % self.score_threshold
                )

        return success


@define
class FlowFromDirectoryConfig(BaseConfigClass):
    """
    Here the parameters for the training data are extracted, when it
    is available in a directory.
    """

    __related_strict__ = True

    directory: str = related.StringField(default="")


@define
class FlowFromDataframeConfig(BaseConfigClass):
    """
    Here the parameters for the training data are extracted, when it
    is available in a specific file.
    """

    __related_strict__ = True

    ann_file_list: List[str] = related.SequenceField(cls=str)
    annotation_handler_config_path: str = related.StringField(default="")
    annotation_handler_config: Optional[AnnotationHandlerConfig] = related.ChildField(
        cls=AnnotationHandlerConfig, required=False, default=None
    )


@define
class GeneratorConfig(BaseConfigClass):
    """
    Here the parameter for data source is extracted. Note that we have
    exclusive options here.
    """

    __related_strict__ = True

    @property
    def _mutual_attributes(self) -> List[str]:
        return ["flow_from_directory", "flow_from_dataframe"]

    # mutually exclusive fields
    flow_from_directory: Optional[FlowFromDirectoryConfig] = related.ChildField(
        cls=FlowFromDirectoryConfig, default=None, required=False
    )

    flow_from_dataframe: Optional[FlowFromDataframeConfig] = related.ChildField(
        cls=FlowFromDataframeConfig, default=None, required=False
    )


@define
class ModelCheckpointConfig(BaseConfigClass):
    """
    Here the parameters for ModelCheckpoint callback are extracted.
    The parameters follow the definition of tensorflow. For detailed
    information on how to set the parameters have a look at their documentation:
    https://www.tensorflow.org/api_docs/python/tf/keras/callbacks/ModelCheckpoint

    Note that the parameter save_weights_only is listed under NetConfig class.
    """

    __related_strict__ = True

    # specify directory where to store trained models
    work_dir: str = related.StringField()

    monitor: Optional[str] = related.StringField(required=False, default="val_loss")
    verbose: Optional[int] = related.IntegerField(required=False, default=1)
    save_best_only: Optional[bool] = related.BooleanField(required=False, default=False)
    mode: Optional[str] = related.StringField(required=False, default="auto")
    save_freq: Optional[Union[str, int]] = related.StringField(
        required=False, default="epoch"
    )
    initial_value_threshold: Optional[float] = related.FloatField(
        required=False, default=None
    )

    def check_values(self) -> bool:
        return self.verbose in [0, 1] and self.mode in ["auto", "min", "max"]


@define
class TrainConfig(BaseConfigClass):
    """
    Here the parameters for the data generators and training hyper-parameters
    are extracted.
    """

    __related_strict__ = True

    batch_size: int = related.IntegerField()
    epochs: int = related.IntegerField()

    metrics: List[str] = related.SequenceField(cls=str)

    rotation_range: int = related.IntegerField()
    horizontal_flip: bool = related.BooleanField()
    zoom_range: float = related.FloatField()
    rescale: bool = related.BooleanField()

    train_generator_config: GeneratorConfig = related.ChildField(cls=GeneratorConfig)
    val_generator_config: GeneratorConfig = related.ChildField(cls=GeneratorConfig)
    test_generator_config: GeneratorConfig = related.ChildField(cls=GeneratorConfig)

    model_checkpoint_config: ModelCheckpointConfig = related.ChildField(
        cls=ModelCheckpointConfig
    )

    featurewise_center: Optional[bool] = related.BooleanField(
        required=False, default=False
    )
    featurewise_std_normalization: Optional[bool] = related.BooleanField(
        required=False, default=False
    )
    vertical_flip: Optional[bool] = related.BooleanField(required=False, default=True)
    width_shift_range: Optional[float] = related.FloatField(required=False, default=0.2)
    height_shift_range: Optional[float] = related.FloatField(
        required=False, default=0.2
    )

    seed: Optional[int] = related.IntegerField(required=False, default=None)

    color_mode: str = related.StringField(default="rgb")
    shuffle: bool = related.BooleanField(default=False)

    # specify a directory where to store augmented images
    save_to_dir: Optional[str] = related.StringField(required=False, default=None)
    save_prefix: Optional[str] = related.StringField(required=False, default="")
    save_format: Optional[str] = related.StringField(required=False, default="png")
    follow_links: Optional[bool] = related.BooleanField(required=False, default=False)
    interpolation: Optional[str] = related.StringField(
        required=False, default="nearest"
    )

    loss: str = related.StringField(default=LossTypes.CATEGORICAL_CROSSENTROPY)
    optimizer: str = related.StringField(default=OptimizerTypes.ADAM)
    learning_rate: float = related.FloatField(default=0.001)
    # momentum optional for training
    momentum: Optional[float] = related.FloatField(default=0.9)

    def check_values(self) -> bool:
        return (
            self.optimizer
            in OptimizerTypes.get_values_as_list(class_type=OptimizerTypes)
            and self.loss in LossTypes.get_values_as_list(class_type=LossTypes)
            and self.color_mode in ["grayscale", "rgb", "rgba"]
            and self.save_format in ["png", "jpeg"]
            and self.interpolation in ["nearest", "bilinear", "bicubic"]
        )


@define
class Config(ModelConfiguration):
    """
    Here the parameter groups are extracted and the respective detailed
    config classes as listed above are called.
    """

    net_config: NetConfig = related.ChildField(cls=NetConfig)

    class_mapping: ClassMappingConfig = related.ChildField(ClassMappingConfig)

    inference_config: InferenceConfig = related.ChildField(cls=InferenceConfig)

    train_config: TrainConfig = related.ChildField(cls=TrainConfig)
