# Philote-Python
#
# Copyright 2022-2024 Christopher A. Lupp
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
#
#
# This work has been cleared for public release, distribution unlimited, case
# number: AFRL-2023-5713.
#
# The views expressed are those of the authors and do not reflect the
# official guidance or position of the United States Government, the
# Department of Defense or of the United States Air Force.
#
# Statement from DoD: The Appearance of external hyperlinks does not
# constitute endorsement by the United States Department of Defense (DoD) of
# the linked websites, of the information, products, or services contained
# therein. The DoD does not exercise any editorial, security, or other
# control over the information you may find at these locations.
import grpc
import openmdao.api as om
import philote_mdo.openmdao as pmom


# this script should be run with the corresponding NPSS server
prob = om.Problem()
model = prob.model

model.add_subsystem(
    "NPSS",
    pmom.RemoteExplicitComponent(channel=grpc.insecure_channel("localhost:50051")),
    promotes=["*"],
)

prob.setup()
prob.final_setup()

prob.model.list_inputs()

#prob["Alt_DES"] = 30000.
#prob["MN_DES"] = 0.7
prob.run_model()

prob.model.list_outputs()

#print(prob["Fn_SLS"])
