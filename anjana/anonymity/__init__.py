# -*- coding: utf-8 -*-

# Copyright 2024 Spanish National Research Council (CSIC)
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""Python library for applying different anonymity techniques."""

from ._k_anonymity import k_anonymity, k_anonymity_inner, alpha_k_anonymity
from ._l_diversity import l_diversity, entropy_l_diversity, recursive_c_l_diversity
from ._t_closeness import t_closeness
from ._beta_likeness import basic_beta_likeness, enhanced_beta_likeness
from ._delta_disclosure import delta_disclosure

__all__ = [
    "k_anonymity",
    "k_anonymity_inner",
    "alpha_k_anonymity",
    "l_diversity",
    "entropy_l_diversity",
    "recursive_c_l_diversity",
    "t_closeness",
    "basic_beta_likeness",
    "enhanced_beta_likeness",
    "delta_disclosure",
]
