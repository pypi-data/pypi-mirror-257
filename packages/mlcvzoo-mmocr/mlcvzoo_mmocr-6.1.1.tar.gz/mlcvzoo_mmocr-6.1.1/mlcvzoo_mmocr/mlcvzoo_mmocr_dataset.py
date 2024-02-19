# Copyright Open Logistics Foundation
#
# Licensed under the Open Logistics Foundation License 1.3.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: OLFL-1.3

"""
Module for providing the possibility to train a mmocr
model on data that is provided by the annotation handler
of the MLCVZoo. This is realized by extending the 'DATASETS'
registry of mmocr (mmdetection).
"""

import logging
import os
from typing import Any, Dict, List, Optional

from mlcvzoo_base.api.data.annotation import BaseAnnotation
from mlcvzoo_base.configuration.annotation_handler_config import AnnotationHandlerConfig
from mlcvzoo_base.configuration.class_mapping_config import ClassMappingConfig
from mlcvzoo_base.data_preparation.annotation_handler import AnnotationHandler
from mmengine.config import Config
from mmengine.dataset import BaseDataset
from mmocr.registry import DATASETS
from related import to_model

logger = logging.getLogger(__name__)


@DATASETS.register_module()
class MLCVZooMMOCRDataset(BaseDataset):
    """
    Implementation of a custom dataset. It follows the instructions given by:
    https://mmdetection.readthedocs.io/en/dev-3.x/advanced_guides/customize_dataset.html

    We followed an example and created our own dataset class
    which has to be compatible to the class "BaseDataset"
    of the mmengine framework.

    Annotation format required from mmengine.dataset.base_dataset.BaseDataset:
    .. code-block:: none

        {
            "metainfo":
            {
              "dataset_type": "test_dataset",
              "task_name": "test_task"
            },
            "data_list":
            [
              {
                "img_path": "test_img.jpg",
                "height": 604,
                "width": 640,
                "instances":
                [
                  {
                    "bbox": [0, 0, 10, 20],
                    "bbox_label": 1,
                    "mask": [[0,0],[0,10],[10,20],[20,0]],
                    "extra_anns": [1,2,3]
                  },
                  {
                    "bbox": [10, 10, 110, 120],
                    "bbox_label": 2,
                    "mask": [[10,10],[10,110],[110,120],[120,10]],
                    "extra_anns": [4,5,6]
                  }
                ]
              },
            ]
        }

    """

    def __init__(
        self,
        *args: Any,
        annotation_handler_config: Optional[Config] = None,
        class_mapping_config: Optional[Config] = None,
        **kwargs: Any
    ) -> None:
        self.annotations: List[BaseAnnotation] = []
        self.CLASSES: List[str] = []

        if annotation_handler_config is not None:
            # Set annotation handler configuration from given annotation handler config
            configuration = to_model(AnnotationHandlerConfig, annotation_handler_config)
            # Set class mapping configuration from given class mapping config
            if class_mapping_config is not None:
                configuration.class_mapping = to_model(
                    ClassMappingConfig, class_mapping_config
                )
            # Create annotation handler, if no class mapping config was given,
            # assume it is part of the config file
            annotation_handler = AnnotationHandler(
                configuration=configuration,
            )
            # Load annotations and model classes from annotation handler
            self.annotations = annotation_handler.parse_training_annotations()
            self.CLASSES = annotation_handler.mapper.get_model_class_names()

        BaseDataset.__init__(self, *args, **kwargs)

    def load_data_list(self) -> List[Dict[str, Any]]:
        data_list: List[Dict[str, Any]] = []

        # TODO: Handle ignore flag if present in kwargs
        for img_id, annotation in enumerate(self.annotations):
            if not os.path.isfile(annotation.image_path):
                logger.debug(
                    "Skip annotation with path='%s' since image='%s' does not exist"
                    % (annotation.annotation_path, annotation.image_path)
                )
                continue

            instances: List[Dict[str, Any]] = []
            # Segmentation training - train with masks and bounding boxes
            for segmentation in annotation.segmentations:
                if segmentation.box is None:
                    box = segmentation.to_bounding_box().box
                else:
                    box = segmentation.box

                instances.append(
                    {
                        "ignore_flag": 0,
                        "ignore": 0,
                        "bbox_label": segmentation.class_id,
                        "bbox": box.to_list(dst_type=float),
                        "mask": segmentation.to_list(dst_type=float),
                        "polygon": segmentation.to_list(dst_type=float)[0],
                    }
                )

            data_list.append(
                {
                    "img_path": annotation.image_path,
                    "img_id": img_id,
                    # TODO: How to prepare for panoptic segmentation?
                    "seg_map_path": None,
                    "height": annotation.get_height(),
                    "width": annotation.get_width(),
                    "instances": instances,
                }
            )

        return data_list
