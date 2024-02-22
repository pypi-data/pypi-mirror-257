"""AvroToSQL manager."""

from popsink_transformer.errors import PopsinkTransformerError
from popsink_transformer.avro_to_sql.utils.type_converter import (
    SqlEngine,
    get_avro_to_sql_mapping,
)


class AvroToSQL:
    """AvroToSQL class.

    Note: This class is designed to convert Avro fields into SQL-readable types.
    It does not perform the conversion of entire Avro schemas to SQL queries.
    """

    def __init__(self, from_source: dict, sql_engine: SqlEngine) -> None:
        self.from_source = from_source
        self.sql_engine = sql_engine

    def convert(self) -> str:
        """Convert an avro schema to an SQL schema."""
        self._handle_base_schema_errors()

        sql_fields = []
        for avro_field in self.from_source["fields"]:
            formatted_field = self._format_field(avro_field)
            sql_fields.append(formatted_field)

        sql_schema = ",".join(sql_fields)
        return sql_schema

    def _format_field(self, avro_field: dict) -> dict:
        """Call all the specific methods for field formatting."""
        sql_field = ""
        sql_field = self._unwrap_field(avro_field, sql_field)
        sql_field = self._write_nullable(avro_field, sql_field)
        sql_field = self._format_array(avro_field, sql_field)
        sql_field = self._convert_avro_type_to_sql_type(sql_field)
        sql_field = self._format_record(avro_field, sql_field)
        sql_field = self._format_map(avro_field, sql_field)
        return sql_field

    def _unwrap_field(self, avro_field: dict, sql_field: str):
        """Unwrap avro field."""
        avro_field_type = avro_field["type"]

        if avro_field.get("logicalType"):
            avro_field_type = avro_field["logicalType"]

        if isinstance(avro_field_type, list):
            avro_field_type = [
                value for value in avro_field_type if value != "null"
            ].pop()

        if isinstance(avro_field_type, dict):
            avro_field_type = avro_field_type["type"]

        sql_field = f'`{avro_field["name"]}` {avro_field_type}'
        return sql_field

    def _write_nullable(self, avro_field: dict, sql_field: str):
        """Write the nullable state at the end of the field."""
        if "type" in avro_field:
            avro_field_type = avro_field["type"]

            if isinstance(avro_field_type, dict):
                avro_field_type = avro_field_type.get("type")

            if avro_field_type != "record":
                if (
                    not isinstance(avro_field["type"], list)
                    and avro_field["type"] != "record"
                ):
                    sql_field += " NOT NULL"
        return sql_field

    def _format_array(self, avro_field: dict, sql_field: str):
        """Format array fields."""
        if "array" in sql_field:
            if self.sql_engine is SqlEngine.POSTGRES:
                sql_field = sql_field.replace(
                    "array", f"{avro_field['type']['items']} ARRAY"
                )
            if self.sql_engine is SqlEngine.FLINK:
                sql_field = sql_field.replace(
                    "array", f"ARRAY<{avro_field['type']['items']}>"
                )
        return sql_field

    def _format_map(self, avro_field: dict, sql_field: str):
        """Format map fields."""
        if "map" in sql_field:
            if self.sql_engine is SqlEngine.POSTGRES:
                sql_field = sql_field.replace("map", "JSON")

            if self.sql_engine is SqlEngine.FLINK:
                map_type = avro_field["type"]["values"].upper()
                sql_field = sql_field.replace(
                    "map", f"MAP<{map_type}, {map_type}>"
                )
        return sql_field

    def _format_record(self, avro_field: dict, sql_field: str):
        """Format record fields."""
        if "record" in sql_field:
            if self.sql_engine is SqlEngine.POSTGRES:
                sql_field = sql_field.replace("record", "JSON")

            if self.sql_engine is SqlEngine.FLINK:
                nested_fields = avro_field.get(
                    "fields", avro_field["type"]["fields"]
                )

                field_header = []
                for field in nested_fields:
                    formatted_field = self._format_field(field)
                    field_header.append(formatted_field)

                header = ", ".join(field_header)
                sql_field = sql_field.replace("record", f"ROW<{header}>")

                field_body = []
                record_name = avro_field["name"]
                for field in nested_fields:
                    field_name = field["name"]
                    line = f"`{field_name}` AS `{record_name}`.`{field_name}`"
                    field_body.append(line)

                body = ",".join(field_body)
                sql_field += f",{body}"
        return sql_field

    def _convert_avro_type_to_sql_type(self, sql_field: str):
        """Convert avro type to SQL type.

        We replace the avro type with one space before to not mistake it with
        the name of the field.

        Example: '`date` date'
        """

        for avro_type, sql_type in get_avro_to_sql_mapping(
            self.sql_engine
        ).items():
            if avro_type in sql_field:
                sql_field = sql_field.replace(f" {avro_type}", f" {sql_type}")
                if self.sql_engine is SqlEngine.FLINK:
                    sql_field = sql_field.replace(
                        f"<{avro_type}>", f"<{sql_type}>"
                    )
        return sql_field

    def _handle_base_schema_errors(self) -> None:
        """Handle base schema errors."""
        self._raise_error_if_schema_is_empty()
        self._raise_error_if_no_record()
        self._raise_error_if_no_fields_key()
        self._raise_error_if_fields_key_is_not_a_list()

    def _raise_error_if_no_record(self) -> None:
        """Raise error if 'record' type is not found."""
        if self.from_source.get("type") != "record":
            raise PopsinkTransformerError("The base type should be a 'record'")

    def _raise_error_if_no_fields_key(self) -> None:
        """Raise error if 'fields' key is missing."""
        if "fields" not in self.from_source:
            raise PopsinkTransformerError(
                "Missing 'fields' key on base schema"
            )

    def _raise_error_if_schema_is_empty(self) -> None:
        """Raise error if the avro schema is empty."""
        if not self.from_source:
            raise PopsinkTransformerError(
                "Expecting value: line 1 column 1 (char 0)"
            )

    def _raise_error_if_fields_key_is_not_a_list(self) -> None:
        """Raise error if the 'fields' key is not a list."""
        if not isinstance(self.from_source.get("fields"), list):
            raise PopsinkTransformerError("The 'fields' key should be a list")
