# coding=utf-8
# Copyright 2022 The HuggingFace Team. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import TYPE_CHECKING

from transformers.utils import _LazyModule


_import_structure = {
    "base": ["OnnxConfig", "OnnxConfigWithLoss", "OnnxConfigWithPast", "OnnxSeq2SeqConfigWithPast"],
    "config": ["TextDecoderOnnxConfig", "TextEncoderOnnxConfig", "TextSeq2SeqOnnxConfig"],
    "convert": [
        "export",
        "export_models",
        "validate_model_outputs",
        "validate_models_outputs",
        "onnx_export_from_model",
    ],
    "utils": [
        "get_decoder_models_for_export",
        "get_encoder_decoder_models_for_export",
        "get_stable_diffusion_models_for_export",
        "MODEL_TYPES_REQUIRING_POSITION_IDS",
    ],
    "__main__": ["main_export"],
}

if TYPE_CHECKING:
    from .base import OnnxConfig, OnnxConfigWithLoss, OnnxConfigWithPast, OnnxSeq2SeqConfigWithPast  # noqa
    from .config import TextDecoderOnnxConfig, TextEncoderOnnxConfig, TextSeq2SeqOnnxConfig  # noqa
    from .convert import (
        export,
        export_models,
        validate_model_outputs,
        validate_models_outputs,
        onnx_export_from_model,
    )  # noqa
    from .utils import (
        get_decoder_models_for_export,
        get_encoder_decoder_models_for_export,
        get_stable_diffusion_models_for_export,
        MODEL_TYPES_REQUIRING_POSITION_IDS,
    )
    from .__main__ import main_export
else:
    import sys

    sys.modules[__name__] = _LazyModule(
        __name__,
        globals()["__file__"],
        _import_structure,
        module_spec=__spec__,
    )
