# coding=utf-8
# Copyright 2017 The Tensor2Tensor Authors.
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

"""Data generators for translation data-sets."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# Dependency imports

from tensor2tensor.data_generators import generator_utils
from tensor2tensor.data_generators import problem
from tensor2tensor.data_generators import text_encoder
from tensor2tensor.data_generators import translate
from tensor2tensor.utils import registry

import tensorflow as tf

FLAGS = tf.flags.FLAGS

# End-of-sentence marker.
EOS = text_encoder.EOS_ID

_ENFR_TRAIN_DATASETS = [
    [
        "https://s3.amazonaws.com/opennmt-trainingdata/baseline-1M-enfr.tgz",
        ("baseline-1M-enfr/baseline-1M_train.en",
         "baseline-1M-enfr/baseline-1M_train.fr")
    ],
    #    [
    #        "http://www.statmt.org/wmt13/training-parallel-commoncrawl.tgz",
    #        ("commoncrawl.fr-en.en", "commoncrawl.fr-en.fr")
    #    ],
    #    [
    #        "http://www.statmt.org/wmt13/training-parallel-europarl-v7.tgz",
    #        ("training/europarl-v7.fr-en.en", "training/europarl-v7.fr-en.fr")
    #    ],
    #    [
    #        "http://www.statmt.org/wmt14/training-parallel-nc-v9.tgz",
    #        ("training/news-commentary-v9.fr-en.en",
    #         "training/news-commentary-v9.fr-en.fr")
    #    ],
    #    [
    #        "http://www.statmt.org/wmt10/training-giga-fren.tar",
    #        ("giga-fren.release2.fixed.en.gz",
    #         "giga-fren.release2.fixed.fr.gz")
    #    ],
    #    [
    #        "http://www.statmt.org/wmt13/training-parallel-un.tgz",
    #        ("un/undoc.2000.fr-en.en", "un/undoc.2000.fr-en.fr")
    #    ],
]
_ENFR_TEST_DATASETS = [
    [
        "https://s3.amazonaws.com/opennmt-trainingdata/baseline-1M-enfr.tgz",
        ("baseline-1M-enfr/baseline-1M_valid.en",
         "baseline-1M-enfr/baseline-1M_valid.fr")
    ],
    #    [
    #        "http://data.statmt.org/wmt17/translation-task/dev.tgz",
    #        ("dev/newstest2013.en", "dev/newstest2013.fr")
    #    ],
]


@registry.register_problem
class TranslateEnfrWmt8k(translate.TranslateProblem):
  """Problem spec for WMT En-Fr translation."""

  @property
  def targeted_vocab_size(self):
    return 2**13  # 8192

  @property
  def vocab_name(self):
    return "vocab.enfr"

  def generator(self, data_dir, tmp_dir, train):
    symbolizer_vocab = generator_utils.get_or_generate_vocab(
        data_dir, tmp_dir, self.vocab_file, self.targeted_vocab_size,
        _ENFR_TRAIN_DATASETS)
    datasets = _ENFR_TRAIN_DATASETS if train else _ENFR_TEST_DATASETS
    tag = "train" if train else "dev"
    data_path = translate.compile_data(tmp_dir, datasets,
                                       "wmt_enfr_tok_%s" % tag)
    return translate.token_generator(data_path + ".lang1", data_path + ".lang2",
                                     symbolizer_vocab, EOS)

  @property
  def input_space_id(self):
    return problem.SpaceID.EN_TOK

  @property
  def target_space_id(self):
    return problem.SpaceID.FR_TOK


@registry.register_problem
class TranslateEnfrWmt32k(TranslateEnfrWmt8k):

  @property
  def targeted_vocab_size(self):
    return 2**15  # 32768


@registry.register_problem
class TranslateEnfrWmtCharacters(translate.TranslateProblem):
  """Problem spec for WMT En-Fr translation."""

  @property
  def is_character_level(self):
    return True

  @property
  def vocab_name(self):
    return "vocab.enfr"

  def generator(self, data_dir, tmp_dir, train):
    character_vocab = text_encoder.ByteTextEncoder()
    datasets = _ENFR_TRAIN_DATASETS if train else _ENFR_TEST_DATASETS
    tag = "train" if train else "dev"
    data_path = translate.compile_data(tmp_dir, datasets,
                                       "wmt_enfr_chr_%s" % tag)
    return translate.character_generator(
        data_path + ".lang1", data_path + ".lang2", character_vocab, EOS)

  @property
  def input_space_id(self):
    return problem.SpaceID.EN_CHR

  @property
  def target_space_id(self):
    return problem.SpaceID.FR_CHR
