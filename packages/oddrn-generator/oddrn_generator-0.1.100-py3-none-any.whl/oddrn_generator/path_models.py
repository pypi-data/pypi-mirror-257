from typing import Optional

from pydantic import BaseModel, Field, FilePath

from oddrn_generator.exceptions import (
    EmptyPathValueException,
    PathDoesntExistException,
    WrongPathOrderException,
)


class BasePathsModel(BaseModel):
    class Config:
        dependencies_map = {}
        data_source_path = None
        allows_null = []
        extra = "forbid"
        allow_population_by_field_name = True

    def __validate_path(self, field) -> None:
        for deps in reversed(self.__config__.dependencies_map[field]):
            deps_value = getattr(self, deps, None)
            # allow dependency null if it is in allow_null list
            if deps_value is None and deps in self.__config__.allows_null:
                return
            if not deps_value:
                raise WrongPathOrderException(
                    f"'{field}' can not be without '{deps}' attribute"
                )

    def validate_all_paths(self) -> None:
        for field in self.__fields_set__:
            self.__validate_path(field)

    def get_dependency(self, field) -> tuple:
        dependency = self.__config__.dependencies_map.get(field)
        if not dependency:
            raise PathDoesntExistException(f"Path '{field}' doesn't exist in generator")
        return dependency

    def check_if_path_is_set(self, path: str) -> None:
        if not getattr(self, path, None):
            raise EmptyPathValueException(f"Path '{path}' is not set up")

    def set_path_value(self, path: str, value: str) -> None:
        setattr(self, path, value)
        self.__validate_path(path)

    @property
    def data_source_path(self):
        return self.__config__.data_source_path


class PostgresqlPathsModel(BasePathsModel):
    databases: str
    schemas: Optional[str]
    tables: Optional[str]
    views: Optional[str]
    tables_columns: Optional[str] = Field(alias="columns")
    views_columns: Optional[str] = Field(alias="columns")
    relationships: Optional[str]

    class Config:
        dependencies_map = {
            "databases": ("databases",),
            "schemas": ("databases", "schemas"),
            "tables": ("databases", "schemas", "tables"),
            "views": ("databases", "schemas", "views"),
            "tables_columns": ("databases", "schemas", "tables", "tables_columns"),
            "views_columns": ("databases", "schemas", "views", "views_columns"),
            "relationships": ("databases", "schemas", "tables", "relationships"),
        }
        data_source_path = "databases"


class MysqlPathsModel(BasePathsModel):
    databases: str
    tables: Optional[str]
    views: Optional[str]
    tables_columns: Optional[str] = Field(alias="columns")
    views_columns: Optional[str] = Field(alias="columns")

    class Config:
        dependencies_map = {
            "databases": ("databases",),
            "tables": ("databases", "tables"),
            "views": ("databases", "views"),
            "tables_columns": ("databases", "tables", "tables_columns"),
            "views_columns": ("databases", "views", "views_columns"),
        }
        data_source_path = "databases"


class KafkaPathsModel(BasePathsModel):
    topics: Optional[str]

    class Config:
        dependencies_map = {"topics": ("topics",)}


class KafkaConnectorPathsModel(BasePathsModel):
    connectors: str

    class Config:
        dependencies_map = {"connectors": ("connectors",)}


class GluePathsModel(BasePathsModel):
    databases: Optional[str]
    tables: Optional[str]
    columns: Optional[str]
    owners: Optional[str]
    jobs: Optional[str]
    runs: Optional[str]

    class Config:
        dependencies_map = {
            "databases": ("databases",),
            "tables": ("databases", "tables"),
            "columns": ("databases", "tables", "columns"),
            "owners": ("owners",),
            "jobs": ("jobs",),
            "runs": ("jobs", "runs"),
        }


class SnowflakePathsModel(BasePathsModel):
    databases: str
    schemas: Optional[str]
    tables: Optional[str]
    views: Optional[str]
    tables_columns: Optional[str] = Field(alias="columns")
    views_columns: Optional[str] = Field(alias="columns")
    pipes: Optional[str]
    relationships: Optional[str]

    class Config:
        dependencies_map = {
            "databases": ("databases",),
            "schemas": ("databases", "schemas"),
            "tables": ("databases", "schemas", "tables"),
            "views": ("databases", "schemas", "views"),
            "tables_columns": ("databases", "schemas", "tables", "tables_columns"),
            "views_columns": ("databases", "schemas", "views", "views_columns"),
            "pipes": ("pipes",),
            "relationships": ("databases", "schemas", "tables", "relationships"),
        }
        data_source_path = "databases"


class AirflowPathsModel(BasePathsModel):
    dags: Optional[str]
    tasks: Optional[str]
    runs: Optional[str]

    class Config:
        dependencies_map = {
            "dags": ("dags",),
            "tasks": ("dags", "tasks"),
            "runs": ("dags", "tasks", "runs"),
        }


class HivePathsModel(BasePathsModel):
    databases: Optional[str]
    tables: Optional[str]
    views: Optional[str]
    tables_columns: Optional[str] = Field(alias="columns")
    views_columns: Optional[str] = Field(alias="columns")
    owners: Optional[str]

    class Config:
        dependencies_map = {
            "databases": ("databases",),
            "tables": ("databases", "tables"),
            "views": ("databases", "views"),
            "tables_columns": ("databases", "tables", "tables_columns"),
            "views_columns": ("databases", "views", "views_columns"),
            "owners": ("owners",),
        }
        data_source_path = "databases"


class ElasticSearchPathsModel(BasePathsModel):
    templates: Optional[str]
    streams: Optional[str]
    indices: Optional[str]
    fields: Optional[str]
    indices_fields: Optional[str] = Field(alias="fields")
    templates_fields: Optional[str] = Field(alias="fields")

    class Config:
        dependencies_map = {
            "indices": ("indices",),
            "indices_fields": ("indices", "indices_fields"),
            "streams": ("streams",),
            "templates": ("templates",),
            "templates_fields": ("templates", "templates_fields"),
        }


class FeastPathsModel(BasePathsModel):
    featureviews: Optional[str]
    features: Optional[str]
    subfeatures: Optional[str]

    class Config:
        dependencies_map = {
            "featureviews": ("featureviews",),
            "features": ("featureviews", "features"),
            "subfeatures": ("featureviews", "features", "subfeatures"),
        }


class DynamodbPathsModel(BasePathsModel):
    tables: Optional[str]
    columns: Optional[str]

    class Config:
        dependencies_map = {"tables": ("tables",), "columns": ("tables", "columns")}


class OdbcPathsModel(BasePathsModel):
    databases: str
    schemas: Optional[str]
    tables: Optional[str]
    views: Optional[str]
    tables_columns: Optional[str] = Field(alias="columns")
    views_columns: Optional[str] = Field(alias="columns")

    class Config:
        dependencies_map = {
            "databases": ("databases",),
            "schemas": ("databases", "schemas"),
            "tables": ("databases", "schemas", "tables"),
            "views": ("databases", "schemas", "views"),
            "tables_columns": ("databases", "schemas", "tables", "tables_columns"),
            "views_columns": ("databases", "schemas", "views", "views_columns"),
        }
        data_source_path = "databases"


class MssqlPathsModel(BasePathsModel):
    databases: str
    schemas: Optional[str]
    tables: Optional[str]
    views: Optional[str]
    tables_columns: Optional[str] = Field(alias="columns")
    views_columns: Optional[str] = Field(alias="columns")

    class Config:
        dependencies_map = {
            "databases": ("databases",),
            "schemas": ("databases", "schemas"),
            "tables": ("databases", "schemas", "tables"),
            "views": ("databases", "schemas", "views"),
            "tables_columns": ("databases", "schemas", "tables", "tables_columns"),
            "views_columns": ("databases", "schemas", "views", "views_columns"),
        }
        data_source_path = "databases"


class OraclePathsModel(BasePathsModel):
    schemas: str
    databases: Optional[str]
    tables: Optional[str]
    views: Optional[str]
    columns: Optional[str]
    tables_columns: Optional[str] = Field(alias="columns")
    views_columns: Optional[str] = Field(alias="columns")

    class Config:
        dependencies_map = {
            "schemas": ("schemas",),
            "databases": ("schemas", "databases"),
            "tables": ("schemas", "databases", "tables"),
            "views": ("schemas", "databases", "views"),
            "tables_columns": ("schemas", "databases", "tables", "tables_columns"),
            "views_columns": ("schemas", "databases", "views", "views_columns"),
        }
        data_source_path = "databases"


class RedshiftPathsModel(BasePathsModel):
    databases: str
    schemas: Optional[str]
    tables: Optional[str]
    views: Optional[str]
    tables_columns: Optional[str] = Field(alias="columns")
    views_columns: Optional[str] = Field(alias="columns")

    class Config:
        dependencies_map = {
            "databases": ("databases",),
            "schemas": ("databases", "schemas"),
            "tables": ("databases", "schemas", "tables"),
            "views": ("databases", "schemas", "views"),
            "tables_columns": ("databases", "schemas", "tables", "tables_columns"),
            "views_columns": ("databases", "schemas", "views", "views_columns"),
        }
        data_source_path = "databases"


class ClickHousePathsModel(BasePathsModel):
    databases: str
    tables: Optional[str]
    views: Optional[str]
    tables_columns: Optional[str] = Field(alias="columns")
    views_columns: Optional[str] = Field(alias="columns")

    class Config:
        dependencies_map = {
            "databases": ("databases",),
            "tables": ("databases", "tables"),
            "views": ("databases", "views"),
            "tables_columns": ("databases", "tables", "tables_columns"),
            "views_columns": ("databases", "views", "views_columns"),
        }
        data_source_path = "databases"


class AthenaPathsModel(BasePathsModel):
    catalogs: Optional[str]
    databases: Optional[str]
    tables: Optional[str]
    views: Optional[str]
    tables_columns: Optional[str] = Field(alias="columns")
    views_columns: Optional[str] = Field(alias="columns")

    class Config:
        dependencies_map = {
            "catalogs": ("catalogs",),
            "databases": ("catalogs", "databases"),
            "tables": ("catalogs", "databases", "tables"),
            "views": ("catalogs", "databases", "views"),
            "tables_columns": ("catalogs", "databases", "tables", "tables_columns"),
            "views_columns": ("catalogs", "databases", "views", "views_columns"),
        }


class QuicksightPathsModel(BasePathsModel):
    datasets: Optional[str]
    analyses: Optional[str]
    dashboards: Optional[str]
    data_sources: Optional[str]

    class Config:
        dependencies_map = {
            "datasets": ("datasets",),
            "analyses": ("analyses",),
            "dashboards": ("dashboards",),
            "data_sources": ("data_sources",),
        }


class DbtPathsModel(BasePathsModel):
    databases: Optional[str]
    schemas: Optional[str]
    tables: Optional[str]
    views: Optional[str]
    tables_columns: Optional[str] = Field(alias="columns")
    views_columns: Optional[str] = Field(alias="columns")
    tests: Optional[str]
    runs: Optional[str]
    models: Optional[str]
    seeds: Optional[str]

    class Config:
        dependencies_map = {
            "databases": ("databases",),
            "schemas": ("databases", "schemas"),
            "tables": ("databases", "schemas", "tables"),
            "views": ("databases", "schemas", "views"),
            "tables_columns": ("databases", "schemas", "tables", "tables_columns"),
            "views_columns": ("databases", "schemas", "views", "views_columns"),
            "tests": ("databases", "tests"),
            "runs": ("databases", "tests", "runs"),
            "models": ("models",),
            "seeds": ("seeds",),
        }


class PrefectPathsModel(BasePathsModel):
    flows: str
    tasks: Optional[str]
    runs: Optional[str]

    class Config:
        dependencies_map = {
            "flows": ("flows",),
            "tasks": ("flows", "tasks"),
            "runs": ("flows", "tasks", "runs"),
        }


class TableauPathsModel(BasePathsModel):
    sites: str
    databases: Optional[str]
    schemas: Optional[str]
    tables: Optional[str]
    columns: Optional[str]
    workbooks: Optional[str]
    sheets: Optional[str]

    class Config:
        dependencies_map = {
            "sites": ("sites",),
            "databases": ("sites", "databases"),
            "schemas": ("sites", "databases", "schemas"),
            "tables": ("sites", "databases", "schemas", "tables"),
            "columns": ("sites", "databases", "schemas", "tables", "columns"),
            "workbooks": ("sites", "workbooks"),
            "sheets": ("sites", "workbooks", "sheets"),
        }
        data_source_path = "sites"
        allows_null = ["schemas"]


class Neo4jPathsModel(BasePathsModel):
    databases: str
    nodes: Optional[str]
    fields: Optional[str]

    class Config:
        dependencies_map = {
            "databases": ("databases",),
            "nodes": ("databases", "nodes"),
            "fields": ("databases", "nodes", "fields"),
        }
        data_source_path = "databases"


class S3PathsModel(BasePathsModel):
    buckets: Optional[str]
    keys: Optional[str]
    columns: Optional[str]

    class Config:
        dependencies_map = {
            "buckets": ("buckets",),
            "keys": ("buckets", "keys"),
            "columns": ("buckets", "keys", "columns"),
        }
        data_source_path = "buckets"


class S3CustomPathsModel(BasePathsModel):
    buckets: Optional[str]
    keys: Optional[str]
    columns: Optional[str]

    class Config:
        dependencies_map = {
            "buckets": ("buckets",),
            "keys": ("buckets", "keys"),
            "columns": ("buckets", "keys", "columns"),
        }
        data_source_path = "buckets"


class CassandraPathsModel(BasePathsModel):
    keyspaces: str
    tables: Optional[str]
    views: Optional[str]
    columns: Optional[str]
    tables_columns: Optional[str] = Field(alias="columns")
    views_columns: Optional[str] = Field(alias="columns")

    class Config:
        dependencies_map = {
            "keyspaces": ("keyspaces",),
            "tables": ("keyspaces", "tables"),
            "views": ("keyspaces", "views"),
            "tables_columns": ("keyspaces", "tables", "tables_columns"),
            "views_columns": ("keyspaces", "views", "views_columns"),
        }
        data_source_path = "keyspaces"


class SagemakerPathsModel(BasePathsModel):
    experiments: Optional[str]
    trials: Optional[str]
    jobs: Optional[str]
    artifacts: Optional[str]

    class Config:
        dependencies_map = {
            "experiments": ("experiments",),
            "trials": ("experiments", "trials"),
            "jobs": ("experiments", "trials", "jobs"),
            "artifacts": ("experiments", "trials", "artifacts"),
        }


class KubeflowPathsModel(BasePathsModel):
    pipelines: Optional[str]
    experiments: Optional[str]
    runs: Optional[str]

    class Config:
        dependencies_map = {
            "pipelines": ("pipelines",),
            "experiments": ("experiments",),
            "runs": ("experiments", "runs"),
        }


class TarantoolPathsModel(BasePathsModel):
    spaces: Optional[str]
    columns: Optional[str]

    class Config:
        dependencies_map = {"spaces": ("spaces",), "columns": ("spaces", "columns")}


class KinesisPathsModel(BasePathsModel):
    streams: Optional[str]
    shards: Optional[str]
    data_records: Optional[str]

    class Config:
        dependencies_map = {
            "streams": ("streams",),
            "shards": ("streams", "shards"),
            "data_records": ("streams", "shards", "data_records"),
        }


class MongoPathsModel(BasePathsModel):
    databases: str
    collections: Optional[str]
    columns: Optional[str]

    class Config:
        dependencies_map = {
            "databases": ("databases",),
            "collections": ("databases", "collections"),
            "columns": ("databases", "collections", "columns"),
        }
        data_source_path = "databases"


class VerticaPathsModel(BasePathsModel):
    databases: str
    schemas: Optional[str]
    tables: Optional[str]
    views: Optional[str]
    tables_columns: Optional[str] = Field(alias="columns")
    views_columns: Optional[str] = Field(alias="columns")

    class Config:
        dependencies_map = {
            "databases": ("databases",),
            "schemas": ("databases", "schemas"),
            "tables": ("databases", "schemas", "tables"),
            "views": ("databases", "schemas", "views"),
            "tables_columns": ("databases", "schemas", "tables", "tables_columns"),
            "views_columns": ("databases", "schemas", "views", "views_columns"),
        }
        data_source_path = "databases"


class PrestoPathsModel(BasePathsModel):
    catalogs: Optional[str]
    schemas: Optional[str]
    tables: Optional[str]
    columns: Optional[str]

    class Config:
        dependencies_map = {
            "catalogs": ("catalogs",),
            "schemas": ("catalogs", "schemas"),
            "tables": ("catalogs", "schemas", "tables"),
            "columns": ("catalogs", "schemas", "tables", "columns"),
        }
        # data_source_path = "databases"


class SupersetPathsModel(BasePathsModel):
    databases: Optional[str]
    datasets: Optional[str]
    columns: Optional[str]
    dashboards: Optional[str]
    charts: Optional[str]

    class Config:
        dependencies_map = {
            "databases": ("databases",),
            "datasets": ("databases", "datasets"),
            "columns": ("databases", "datasets", "columns"),
            "charts": ("charts",),
            "dashboards": ("dashboards",),
        }


class CubeJsPathModel(BasePathsModel):
    cubes: str = ""

    class Config:
        dependencies_map = {"cubes": ("cubes",)}


class MetabasePathModel(BasePathsModel):
    collections: str = ""
    dashboards: Optional[str]
    cards: Optional[str]

    class Config:
        dependencies_map = {
            "collections": ("collections",),
            "dashboards": ("collections", "dashboards"),
            "cards": ("collections", "cards"),
        }


class DmsPathsModel(BasePathsModel):
    tasks: Optional[str]
    runs: Optional[str]

    class Config:
        dependencies_map = {"tasks": ("tasks",), "runs": ("tasks", "runs")}


class PowerBiPathModel(BasePathsModel):
    datasets: Optional[str]
    dashboards: Optional[str]

    class Config:
        dependencies_map = {
            "datasets": ("datasets",),
            "dashboards": ("dashboards",),
        }


class RedashPathsModel(BasePathsModel):
    queries: Optional[str]
    dashboards: Optional[str]

    class Config:
        dependencies_map = {
            "queries": ("queries",),
            "dashboards": ("dashboards",),
            "jobs": ("jobs",),
        }


class AirbytePathsModel(BasePathsModel):
    connections: Optional[str]

    class Config:
        dependencies_map = {
            "connections": ("connections",),
        }


class FilesystemPathModel(BasePathsModel):
    path: Optional[str]
    fields: Optional[str]

    class Config:
        dependencies_map = {"path": ("path",), "fields": ("path", "fields")}


class GreatExpectationsPathsModel(BasePathsModel):
    suites: Optional[str]
    types: Optional[str]
    runs: Optional[str]

    class Config:
        dependencies_map = {
            "suites": ("suites",),
            "types": ("suites", "types"),
            "runs": ("suites", "types", "runs"),
        }


class DatabricksLakehousePathModel(BasePathsModel):
    databases: Optional[str]
    tables: Optional[str]
    columns: Optional[str]

    class Config:
        dependencies_map = {
            "databases": ("databases",),
            "tables": ("databases", "tables"),
            "columns": ("databases", "tables", "columns"),
        }


class DatabricksUnityCatalogPathModel(BasePathsModel):
    catalogs: Optional[str]
    schemas: Optional[str]
    tables: Optional[str]
    columns: Optional[str]

    class Config:
        dependencies_map = {
            "catalogs": ("catalogs",),
            "schemas": ("catalogs", "schemas"),
            "tables": ("catalogs", "schemas", "tables"),
            "columns": ("catalogs", "schemas", "tables", "columns"),
        }


class DatabricksFeatureStorePathModel(BasePathsModel):
    databases: Optional[str]
    tables: Optional[str]
    columns: Optional[str]

    class Config:
        dependencies_map = {
            "databases": ("databases",),
            "tables": ("databases", "tables"),
            "columns": ("databases", "tables", "columns"),
        }


class SingleStorePathsModel(BasePathsModel):
    databases: str
    tables: Optional[str]
    views: Optional[str]
    tables_columns: Optional[str] = Field(alias="columns")
    views_columns: Optional[str] = Field(alias="columns")

    class Config:
        dependencies_map = {
            "databases": ("databases",),
            "tables": ("databases", "tables"),
            "views": ("databases", "views"),
            "tables_columns": ("databases", "tables", "tables_columns"),
            "views_columns": ("databases", "views", "views_columns"),
        }
        data_source_path = "databases"


class AzureSQLPathsModel(BasePathsModel):
    databases: str
    schemas: Optional[str]
    tables: Optional[str]
    views: Optional[str]
    columns: Optional[str]
    tables_columns: Optional[str] = Field(alias="columns")
    views_columns: Optional[str] = Field(alias="columns")

    class Config:
        dependencies_map = {
            "databases": ("databases",),
            "schemas": ("databases", "schemas"),
            "tables": ("databases", "schemas", "tables"),
            "views": ("databases", "schemas", "views"),
            "tables_columns": ("databases", "schemas", "tables", "tables_columns"),
            "views_columns": ("databases", "schemas", "views", "views_columns"),
        }
        data_source_path = "databases"


class FivetranPathsModel(BasePathsModel):
    transformers: Optional[str]

    class Config:
        dependencies_map = {
            "transformers": ("transformers",),
        }


class LambdaPathsModel(BasePathsModel):
    functions: Optional[str]

    class Config:
        dependencies_map = {
            "functions": ("functions",),
        }


class CouchbasePathsModel(BasePathsModel):
    buckets: str
    scopes: Optional[str]
    collections: Optional[str]
    columns: Optional[str]

    class Config:
        dependencies_map = {
            "buckets": ("buckets",),
            "scopes": ("buckets", "scopes"),
            "collections": ("buckets", "scopes", "collections"),
            "columns": ("buckets", "scopes", "collections", "columns"),
        }
        data_source_path = "buckets"


class SQLitePathsModel(BasePathsModel):
    path: Optional[FilePath]
    tables: Optional[str]
    views: Optional[str]
    columns: Optional[str]
    tables_columns: Optional[str] = Field(alias="columns")
    views_columns: Optional[str] = Field(alias="columns")

    class Config:
        dependencies_map = {
            "path": ("path",),
            "tables": ("path", "tables"),
            "views": ("path", "views"),
            "tables_columns": ("path", "tables", "tables_columns"),
            "views_columns": ("path", "views", "views_columns"),
        }
        data_source_path = "path"


class BigTablePathsModel(BasePathsModel):
    instances: Optional[str]
    tables: Optional[str]
    columns: Optional[str]

    class Config:
        dependencies_map = {
            "instances": ("instances",),
            "tables": ("instances", "tables"),
            "columns": ("instances", "tables", "columns"),
        }


class DuckDBPathsModel(BasePathsModel):
    catalogs: Optional[str]
    schemas: Optional[str]
    tables: Optional[str]
    columns: Optional[str]

    class Config:
        dependencies_map = {
            "catalogs": ("catalogs",),
            "schemas": ("catalogs", "schemas"),
            "tables": ("catalogs", "schemas", "tables"),
            "columns": ("catalogs", "schemas", "tables", "columns"),
        }


class GCSPathsModel(BasePathsModel):
    buckets: Optional[str]
    keys: Optional[str]
    columns: Optional[str]

    class Config:
        dependencies_map = {
            "buckets": ("buckets",),
            "keys": ("buckets", "keys"),
            "columns": ("buckets", "keys", "columns"),
        }


class BlobPathsModel(BasePathsModel):
    keys: Optional[str]
    columns: Optional[str]

    class Config:
        dependencies_map = {
            "keys": ("keys",),
            "columns": (
                "keys",
                "columns",
            ),
        }


class BigQueryStoragePathsModel(BasePathsModel):
    datasets: Optional[str]
    tables: Optional[str]
    columns: Optional[str]

    class Config:
        dependencies_map = {
            "datasets": ("datasets",),
            "tables": ("datasets", "tables"),
            "columns": ("datasets", "tables", "columns"),
        }


class CKANPathsModel(BasePathsModel):
    organizations: Optional[str]
    groups: Optional[str]
    datasets: Optional[str]
    resources: Optional[str]
    fields: Optional[str]

    class Config:
        dependencies_map = {
            "organizations": ("organizations",),
            "groups": ("groups",),
            "datasets": ("organizations", "datasets"),
            "resources": ("organizations", "datasets", "resources"),
            "fields": ("organizations", "datasets", "resources", "fields"),
        }


class AzureDataFactoryPathsModel(BasePathsModel):
    factories: Optional[str]
    datasets: Optional[str]
    pipelines: Optional[str]
    pipelines: Optional[str]
    pipelines_runs: Optional[str]
    activities: Optional[str]
    activities_runs: Optional[str]

    class Config:
        dependencies_map = {
            "factories": ("factories",),
            "datasets": ("factories", "datasets"),
            "pipelines": ("factories", "pipelines"),
            "pipelines_runs": ("factories", "pipelines", "pipelines_runs"),
            "activities": ("factories", "pipelines", "activities"),
            "activities_runs": (
                "factories",
                "pipelines",
                "activities",
                "activities_runs",
            ),
        }


class ApiPathsModel(BasePathsModel):
    resources: Optional[str]
    fields: Optional[str]

    class Config:
        dependencies_map = {
            "resources": ("resources",),
            "fields": ("resources", "fields"),
        }
