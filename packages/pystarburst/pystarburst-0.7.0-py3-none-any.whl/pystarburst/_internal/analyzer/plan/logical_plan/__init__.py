#
# Copyright (c) 2022-2023 Starburst Data, Inc. All rights reserved.
#
from enum import Enum
from typing import Optional, Union

from pydantic.fields import Field

from pystarburst._internal.analyzer.base_model import BaseModel
from pystarburst._internal.utils import get_version


class TypeCoercionMode(str, Enum):
    DEFAULT = "DEFAULT"
    LEGACY = "LEGACY"


class LogicalPlan(BaseModel):
    type_coercion_mode: str = Field(TypeCoercionMode.DEFAULT, alias="typeCoercionMode")
    pystarburst_version: Optional[str] = Field(get_version(), alias="pyStarburstVersion")


LogicalPlanUnion = Union[
    # binary
    "Except",
    "Intersect",
    "IntersectAll",
    "Union",
    "UnionAll",
    "Join",
    "UsingJoin",
    # leaf
    "Query",
    "Range",
    "TrinoValues",
    "UnresolvedRelation",
    # table
    "CreateTable",
    "TableDelete",
    "TableMerge",
    "TableUpdate",
    # table_function
    "TableFunctionRelation",
    # unary
    "Aggregate",
    "CreateView",
    "Filter",
    "Limit",
    "Pivot",
    "Project",
    "Unpivot",
    "Sample",
    "Sort",
    "Stack",
]
