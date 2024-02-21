# Copyright 2024 Sergio Nava Muñoz and Mario Graff Guerrero

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import numpy as np
from CompStats.measurements import CI
from CompStats.bootstrap import StatisticSamples


def test_CI():
    """Test confidence interval"""

    statistic = StatisticSamples(num_samples=26, n_jobs=-1)
    pop = np.r_[3, 4, 5, 2, 4]
    samples = statistic(pop)
    low, high = CI(samples)
    mean = pop.mean()
    assert low < mean < high