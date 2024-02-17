# Generated by ariadne-codegen
# Source: schema.graphql

from datetime import datetime
from typing import Any, List, Optional
from uuid import UUID

from pydantic import Field

from .base_model import BaseModel
from .enums import (
    Element,
    MemUnits,
    ModuleInstanceStatus,
    ModuleInstanceTarget,
    Order,
    TopologyVersion,
)


class ArgumentInput(BaseModel):
    id: Optional[UUID] = None
    name: Optional[str] = None
    tags: Optional[List[str]] = None
    value: Optional[Any] = None


class CreateExperimentInput(BaseModel):
    name: str
    data: "ExperimentDataInput"
    project_id: Any
    smol_id: Any
    protein_id: Any
    tags: List[str]


class CreateProjectInput(BaseModel):
    name: str
    tags: List[str]


class CreateProteinConformerInput(BaseModel):
    name: Optional[str] = None
    project_id: Any
    protein_id: Any
    structure_id: Any
    tags: List[str]


class CreateProteinInput(BaseModel):
    name: str
    sequence: str
    project_id: Any
    protein_id: Optional[Any] = None
    tags: List[str]


class CreateSmolConformerInput(BaseModel):
    name: Optional[str] = None
    smol_id: Any
    smol_tautomer_id: Any
    structure_id: Any
    project_id: Any
    tags: List[str]


class CreateSmolInput(BaseModel):
    name: str
    data: "SmolDataInput"
    project_id: Any
    tags: List[str]


class CreateSmolTautomerInput(BaseModel):
    name: Optional[str] = None
    data: "SmolTautomerDataInput"
    smol_id: Any
    project_id: Any
    tags: List[str]


class CreateStructureInput(BaseModel):
    name: str
    topology: "TopologyInput"
    project_id: Any
    trajectory_id: Optional[Any] = None
    tags: List[str]


class DateTimeFilter(BaseModel):
    eq: Optional[datetime] = None
    ne: Optional[datetime] = None
    gt: Optional[datetime] = None
    ge: Optional[datetime] = None
    lt: Optional[datetime] = None
    le: Optional[datetime] = None


class EntityFilterBy(BaseModel):
    and_: Optional[List["EntityFilterBy"]] = Field(alias="and", default=None)
    or_: Optional[List["EntityFilterBy"]] = Field(alias="or", default=None)
    not_: Optional["EntityFilterBy"] = Field(alias="not", default=None)
    id: Optional["UuidFilter"] = None
    created_at: Optional["DateTimeFilter"] = None
    updated_at: Optional["DateTimeFilter"] = None
    deleted_at: Optional["DateTimeFilter"] = None
    tags: Optional["TagFilter"] = None


class EntitySortBy(BaseModel):
    id: Optional[Order] = None
    created_at: Optional[Order] = None
    updated_at: Optional[Order] = None
    deleted_at: Optional[Order] = None


class ExperimentDataInput(BaseModel):
    unit: str
    measure: str
    value: float
    assay: str


class ExperimentFilterBy(BaseModel):
    and_: Optional[List["ExperimentFilterBy"]] = Field(alias="and", default=None)
    or_: Optional[List["ExperimentFilterBy"]] = Field(alias="or", default=None)
    not_: Optional["ExperimentFilterBy"] = Field(alias="not", default=None)
    id: Optional["UuidFilter"] = None
    created_at: Optional["DateTimeFilter"] = None
    updated_at: Optional["DateTimeFilter"] = None
    deleted_at: Optional["DateTimeFilter"] = None
    tags: Optional["TagFilter"] = None
    project_id: Optional["UuidFilter"] = None


class ExperimentSortBy(BaseModel):
    id: Optional[Order] = None
    created_at: Optional[Order] = None
    updated_at: Optional[Order] = None
    deleted_at: Optional[Order] = None


class ModuleInput(BaseModel):
    path: str
    tags: Optional[List[str]] = None
    tests: List["TestCase"]


class ModuleInstanceInput(BaseModel):
    path: str
    args: List["ArgumentInput"]
    name: Optional[str] = None
    target: Optional[ModuleInstanceTarget] = None
    resources: Optional["ModuleInstanceResourcesInput"] = None
    tags: Optional[List[str]] = None
    out_tags: Optional[List[Optional[List[str]]]] = None
    out_names: Optional[List[Optional[str]]] = None
    end: Optional[bool] = None


class ModuleInstanceResourcesInput(BaseModel):
    gpus: Optional[int] = None
    gpu_mem: Optional[int] = None
    gpu_mem_units: Optional[MemUnits] = None
    cpus: Optional[int] = None
    nodes: Optional[int] = None
    mem: Optional[int] = None
    mem_units: Optional[MemUnits] = None
    storage: Optional[int] = None
    storage_units: Optional[MemUnits] = None
    walltime: Optional[int] = None
    storage_mounts: Optional[List[str]] = None


class ProjectFilterBy(BaseModel):
    and_: Optional[List["ProjectFilterBy"]] = Field(alias="and", default=None)
    or_: Optional[List["ProjectFilterBy"]] = Field(alias="or", default=None)
    not_: Optional["ProjectFilterBy"] = Field(alias="not", default=None)
    id: Optional["UuidFilter"] = None
    created_at: Optional["DateTimeFilter"] = None
    updated_at: Optional["DateTimeFilter"] = None
    deleted_at: Optional["DateTimeFilter"] = None
    tags: Optional["TagFilter"] = None


class ProjectSortBy(BaseModel):
    id: Optional[Order] = None
    created_at: Optional[Order] = None
    updated_at: Optional[Order] = None
    deleted_at: Optional[Order] = None


class ProteinConformerFilterBy(BaseModel):
    and_: Optional[List["ProteinConformerFilterBy"]] = Field(alias="and", default=None)
    or_: Optional[List["ProteinConformerFilterBy"]] = Field(alias="or", default=None)
    not_: Optional["ProteinConformerFilterBy"] = Field(alias="not", default=None)
    id: Optional["UuidFilter"] = None
    created_at: Optional["DateTimeFilter"] = None
    updated_at: Optional["DateTimeFilter"] = None
    deleted_at: Optional["DateTimeFilter"] = None
    tags: Optional["TagFilter"] = None
    project_id: Optional["UuidFilter"] = None


class ProteinConformerSortBy(BaseModel):
    id: Optional[Order] = None
    created_at: Optional[Order] = None
    updated_at: Optional[Order] = None
    deleted_at: Optional[Order] = None


class ProteinFilterBy(BaseModel):
    and_: Optional[List["ProteinFilterBy"]] = Field(alias="and", default=None)
    or_: Optional[List["ProteinFilterBy"]] = Field(alias="or", default=None)
    not_: Optional["ProteinFilterBy"] = Field(alias="not", default=None)
    id: Optional["UuidFilter"] = None
    created_at: Optional["DateTimeFilter"] = None
    updated_at: Optional["DateTimeFilter"] = None
    deleted_at: Optional["DateTimeFilter"] = None
    tags: Optional["TagFilter"] = None
    project_id: Optional["UuidFilter"] = None


class ProteinSortBy(BaseModel):
    id: Optional[Order] = None
    created_at: Optional[Order] = None
    updated_at: Optional[Order] = None
    deleted_at: Optional[Order] = None


class RawEntityInput(BaseModel):
    data: Optional[Any] = None
    tags: List[str]


class ResourceUtilizationInput(BaseModel):
    module_instance_id: UUID = Field(alias="moduleInstanceId")
    gpu: Optional[float] = None
    mem: Optional[float] = None
    storage: float
    walltime: float
    cputime: float
    inodes: float
    sus: Optional[int] = None


class SmolConformerFilterBy(BaseModel):
    and_: Optional[List["SmolConformerFilterBy"]] = Field(alias="and", default=None)
    or_: Optional[List["SmolConformerFilterBy"]] = Field(alias="or", default=None)
    not_: Optional["SmolConformerFilterBy"] = Field(alias="not", default=None)
    id: Optional["UuidFilter"] = None
    created_at: Optional["DateTimeFilter"] = None
    updated_at: Optional["DateTimeFilter"] = None
    deleted_at: Optional["DateTimeFilter"] = None
    tags: Optional["TagFilter"] = None
    project_id: Optional["UuidFilter"] = None


class SmolConformerSortBy(BaseModel):
    id: Optional[Order] = None
    created_at: Optional[Order] = None
    updated_at: Optional[Order] = None
    deleted_at: Optional[Order] = None


class SmolDataInput(BaseModel):
    smi: Optional[str] = None
    inchi: str


class SmolFilterBy(BaseModel):
    and_: Optional[List["SmolFilterBy"]] = Field(alias="and", default=None)
    or_: Optional[List["SmolFilterBy"]] = Field(alias="or", default=None)
    not_: Optional["SmolFilterBy"] = Field(alias="not", default=None)
    id: Optional["UuidFilter"] = None
    created_at: Optional["DateTimeFilter"] = None
    updated_at: Optional["DateTimeFilter"] = None
    deleted_at: Optional["DateTimeFilter"] = None
    tags: Optional["TagFilter"] = None
    project_id: Optional["UuidFilter"] = None
    smol_name: Optional["StringFilter"] = None


class SmolSortBy(BaseModel):
    id: Optional[Order] = None
    created_at: Optional[Order] = None
    updated_at: Optional[Order] = None
    deleted_at: Optional[Order] = None


class SmolTautomerDataInput(BaseModel):
    inchi: str


class SmolTautomerFilterBy(BaseModel):
    and_: Optional[List["SmolTautomerFilterBy"]] = Field(alias="and", default=None)
    or_: Optional[List["SmolTautomerFilterBy"]] = Field(alias="or", default=None)
    not_: Optional["SmolTautomerFilterBy"] = Field(alias="not", default=None)
    id: Optional["UuidFilter"] = None
    created_at: Optional["DateTimeFilter"] = None
    updated_at: Optional["DateTimeFilter"] = None
    deleted_at: Optional["DateTimeFilter"] = None
    tags: Optional["TagFilter"] = None
    project_id: Optional["UuidFilter"] = None


class SmolTautomerSortBy(BaseModel):
    id: Optional[Order] = None
    created_at: Optional[Order] = None
    updated_at: Optional[Order] = None
    deleted_at: Optional[Order] = None


class StringFilter(BaseModel):
    eq: Optional[str] = None
    ne: Optional[str] = None
    gt: Optional[str] = None
    ge: Optional[str] = None
    lt: Optional[str] = None
    le: Optional[str] = None
    like: Optional[str] = None
    in_: Optional[List[str]] = Field(alias="in", default=None)
    not_in: Optional[List[str]] = None


class StructureFilterBy(BaseModel):
    and_: Optional[List["StructureFilterBy"]] = Field(alias="and", default=None)
    or_: Optional[List["StructureFilterBy"]] = Field(alias="or", default=None)
    not_: Optional["StructureFilterBy"] = Field(alias="not", default=None)
    id: Optional["UuidFilter"] = None
    created_at: Optional["DateTimeFilter"] = None
    updated_at: Optional["DateTimeFilter"] = None
    deleted_at: Optional["DateTimeFilter"] = None
    tags: Optional["TagFilter"] = None
    project_id: Optional["UuidFilter"] = None


class StructureSortBy(BaseModel):
    id: Optional[Order] = None
    created_at: Optional[Order] = None
    updated_at: Optional[Order] = None
    deleted_at: Optional[Order] = None


class TagFilter(BaseModel):
    all: Optional[List[str]] = None
    any: Optional[List[str]] = None


class TestCase(BaseModel):
    args: List["ArgumentInput"]
    target: ModuleInstanceTarget
    resources: Optional["ModuleInstanceResourcesInput"] = None
    tags: Optional[List[str]] = None


class TokenFilterBy(BaseModel):
    and_: Optional[List["TokenFilterBy"]] = Field(alias="and", default=None)
    or_: Optional[List["TokenFilterBy"]] = Field(alias="or", default=None)
    not_: Optional["TokenFilterBy"] = Field(alias="not", default=None)
    id: Optional["UuidFilter"] = None
    created_at: Optional["DateTimeFilter"] = None
    updated_at: Optional["DateTimeFilter"] = None
    deleted_at: Optional["DateTimeFilter"] = None
    tags: Optional["TagFilter"] = None


class TokenSortBy(BaseModel):
    id: Optional[Order] = None
    created_at: Optional[Order] = None
    updated_at: Optional[Order] = None
    deleted_at: Optional[Order] = None


class TopologyInput(BaseModel):
    version: Optional[TopologyVersion] = None
    symbols: List[Element]
    geometry: List[float]
    velocities: Optional[List[float]] = None
    connectivity: Optional[List[Any]] = None
    formal_charges: Optional[List[int]] = None
    atom_charges: Optional[List[int]] = None
    partial_charges: Optional[List[float]] = None
    labels: Optional[List[str]] = None
    atom_labels: Optional[List[str]] = None
    fragments: Optional[List[List[int]]] = None
    fragment_formal_charges: Optional[List[int]] = None
    fragment_charges: Optional[List[int]] = None
    fragment_partial_charges: Optional[List[float]] = None
    fragment_multiplicities: Optional[List[int]] = None
    alts: Optional[List[Any]] = None


class UpdateModuleInstanceInput(BaseModel):
    id: UUID
    path: Optional[str] = None
    ins: Optional[List["ArgumentInput"]] = None
    outs: Optional[List["ArgumentInput"]] = None
    target: Optional[ModuleInstanceTarget] = None
    status: Optional[ModuleInstanceStatus] = None
    resources: Optional["ModuleInstanceResourcesInput"] = None
    tags: Optional[List[str]] = None


class UuidFilter(BaseModel):
    eq: Optional[Any] = None
    ne: Optional[Any] = None
    in_: Optional[List[Any]] = Field(alias="in", default=None)
