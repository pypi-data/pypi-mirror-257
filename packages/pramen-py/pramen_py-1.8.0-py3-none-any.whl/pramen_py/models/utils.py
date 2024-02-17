#  Copyright 2022 ABSA Group Limited
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.


from typing import List

from pramen_py.models import MetastoreTable, TableFormat


def get_metastore_table(
    table_name: str,
    tables: List[MetastoreTable],
) -> MetastoreTable:
    def filter_func(table: MetastoreTable) -> bool:
        return table.name == table_name

    try:
        return next(filter(filter_func, tables))
    except StopIteration as err:
        raise KeyError(
            f"Table {table_name} missed in the config. "
            f"Available tables are:\n"
            f"{chr(10).join(t.name for t in tables)}"
        ) from err


def get_table_format_by_value(value: str) -> TableFormat:
    if value in TableFormat._value2member_map_:
        return TableFormat(value)
    else:
        raise Exception(f"Table format {value} is not supported by pramen-py")
