from dataclasses import dataclass, field

TABLE_CREATE_STEM = "create table if not exists"
TABLE_DROP_STEM = "drop table if exists"
TABLE_INSERT_INTO_STEM = "insert into"


Schema = dict[str, str]


@dataclass
class Table:
    """Class describing a generic PostgreSQL table.
    Contains utilities that help with creation and deletion of tables.
    """

    name: str
    schema: Schema
    primary_key_column: str = ""
    not_null_cols: list[str] = field(default_factory=list)

    def _get_schema_str(self) -> str:
        """Returns the table schema in string form"""
        return ", ".join(
            [
                f"{column_name} {column_type}"
                for column_name, column_type in self.schema.items()
            ]
        )

    def _get_on_conflict_do_nothing_str(self) -> str:
        """Creates ON CONFLICT DO NOTHING statements for INSERT queries

        :return: ON CONFLICT DO NOTHING statement
        :rtype: str
        """
        return f"on conflict ({self.primary_key_column}) do nothing"

    def _get_constraint_pk(self) -> str:
        """Returns a string that can be used to add PRIMARY KEY constraints

        :return: string that can be used to add PRIMARY KEY constraints
        :rtype: str
        """
        if not self.primary_key_column:
            return ""

        return f"primary key ({self.primary_key_column})"

    @property
    def schema_str(self) -> str:
        return self._get_schema_str()

    @property
    def primary_key_str(self) -> str:
        return self._get_constraint_pk()

    def _get_columns_str(self) -> str:
        """Returns the table columns in string form"""
        return ", ".join(column_name for column_name in self.schema)

    def get_insert_query(self) -> str:
        """Returns an insert table query for use in psycopg2 execute calls"""
        columns = self._get_columns_str()
        value_placeholders = ", ".join(["%s" for _ in range(len(self.schema))])
        on_conflict_str = self._get_on_conflict_do_nothing_str()
        return f"{TABLE_INSERT_INTO_STEM} {self.name} ({columns}) values ({value_placeholders}) {on_conflict_str}"

    def get_create_table_query(self) -> str:
        """Returns a create table query"""
        query = f"{TABLE_CREATE_STEM} {self.name}"
        query += f" ({self.schema_str}"

        if self.primary_key_column:
            query += f", {self.primary_key_str}"

        query += ")"
        return query

    def get_drop_table_query(self) -> str:
        """Returns a drop table query"""
        return f"{TABLE_DROP_STEM} {self.name}"
