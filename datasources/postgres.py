from enum import Enum
from env.settings import (
    POSTGRES_HOST,
    POSTGRES_PORT,
    POSTGRES_USER,
    POSTGRES_PASSWORD
)


class PostgresDatasources(Enum):
    SAMPLE_POYO_DB = "poyo"
    
    def to_config(self) -> dict:
        return {
            "name": f"postgres_datasource_{self.value}",
            "class_name": "Datasource",
            "execution_engine": {
                "class_name": "SqlAlchemyExecutionEngine",
                "connection_string": \
                    f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}"\
                    f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{self.value}",
            },
            "data_connectors": {
                "default_runtime_data_connector_name": {
                    "class_name": "RuntimeDataConnector",
                    "batch_identifiers": ["default_identifier_name"],
                },
                "default_inferred_data_connector_name": {
                    "class_name": "InferredAssetSqlDataConnector",
                    "include_schema_name": True,
                },
            },
        }
