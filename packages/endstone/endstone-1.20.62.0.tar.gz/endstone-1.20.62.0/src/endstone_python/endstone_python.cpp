// Copyright (c) 2023, The Endstone Project. (https://endstone.dev) All Rights Reserved.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#include <pybind11/pybind11.h>

#include "endstone/detail/python.h"

namespace endstone::detail {

PYBIND11_MODULE(endstone_python, m)  // NOLINT(*-use-anonymous-namespace)
{
    def_color_format(m);
    def_logger(m);
    def_plugin(m);
    def_plugin_description(m);
    def_plugin_loader(m);
    def_plugin_manager(m);
    def_server(m);
}

}  // namespace endstone::detail
