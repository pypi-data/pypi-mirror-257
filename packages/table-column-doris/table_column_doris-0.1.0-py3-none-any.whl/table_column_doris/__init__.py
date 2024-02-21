import re
import typing as t

import sqlparse

__version__ = "0.1.0"

DEFAULT_TYPE_LENGTH = {
    "char": [255],
    "varchar": [65533],
    "string": [1048576],
    "decimal": [9, 0],
    "decimalv3": [9, 0],
    "datetime": [0],
    "datetimev2": [0],
}


class DDLColumn:
    """A column in a table from ddl.

    Attributes:
        col (str): The full column definition.
        name (str): The name of the column.
        type_ (str): The type of the column, with length.
        base_type (str): The base type of the column, without length.
    """

    def __init__(self, col_tokens: t.List[str]):
        self.col_tokens = col_tokens
        self.name = col_tokens[0].lower().strip('"`')
        self.type_ = ""
        self.base_type = ""

        # extract type and base_type
        find_type_len = False
        type_has_parenthesis = False
        for token in col_tokens[1:]:
            if token == " ":
                continue

            if self.base_type == "":
                self.type_ = token.lower()
                self.base_type = self.type_.split("(")[0].strip()

                # the parenthesis is not closed or not found, like `id decimal  (6,`
                # continue to find the type length.
                type_has_parenthesis = "(" in token
                if not type_has_parenthesis or ")" not in token:
                    find_type_len = True

                continue

            type_has_parenthesis = type_has_parenthesis or "(" in token

            if find_type_len and type_has_parenthesis:
                self.type_ += token.strip().lower()
                if ")" in token:
                    break
            else:
                break

    @property
    def col(self) -> str:
        # Only quote if original col name is quoted.
        col_name = self.name
        if self.col_tokens[0].startswith(("`", '"')):
            col_name = f"`{self.name}`"

        return sqlparse.format(
            "".join([col_name] + self.col_tokens[1:]), strip_whitespace=True
        )

    @property
    def col_not_null(self) -> str:
        col = self.col

        if len(re.findall(r"not\s+null", col, re.IGNORECASE)) > 0:
            return col

        return re.sub(r"(?i)\snull\s", " not null ", col)

    def type_length(self) -> t.Optional[t.List[int]]:
        """Get the length of the type, like [200] in varchar(200), [2, 1] in decimal(2, 1).
        Return default length if the type has no length.
        """

        if self.base_type not in DEFAULT_TYPE_LENGTH:
            return []

        default_type_len = DEFAULT_TYPE_LENGTH[self.base_type]
        if "(" not in self.type_:
            return default_type_len

        type_len = list(map(int, self.type_.split("(")[1].split(")")[0].split(",")))
        missing_len = len(default_type_len) - len(type_len)
        if missing_len > 0:
            # fill with default
            return type_len + default_type_len[-missing_len:]

        return type_len

    def __str__(self):
        return self.col

    def __repr__(self) -> str:
        return self.col


# db -> [table -> [col]]
def get_db_table_columns(sql: str) -> t.Dict[str, t.Dict[str, t.List[DDLColumn]]]:
    """Get columns of a table from a create table statement."""
    sql = sqlparse.format(sql, strip_comments=True)

    dbs: t.Dict[str, t.Dict[str, t.List[DDLColumn]]] = {}
    for parsed in sqlparse.parse(sql):
        if not _is_create_table_stmt(parsed):
            continue

        db = ""
        table = str(
            parsed.token_matching(lambda t: isinstance(t, sqlparse.sql.Identifier), 0)
        ).replace("`", "")
        if "." in table:
            db = table.split(".", maxsplit=1)[0]
            table = table.split(".")[1]

        if db not in dbs:
            dbs[db] = {}

        # extract the parenthesis which holds column definitions
        dbs[db][table] = _extract_definitions(parsed.flatten())

    return dbs


def _extract_definitions(token_list) -> t.List[DDLColumn]:
    """
    Return a list of column definitions,
    Each item has two parts, the first is the column name, the second is the column meta.

    Example returns:
        {'db':
            {'table': [
                ['id', 'integer primary key'],
                ['title', 'varchar(200) not null'],
                ['description', 'text']
             ]}}
    """

    # assumes that token_list is a parenthesis
    definitions = []
    tmp: t.List[str] = []
    par_level = 0
    for token in token_list:
        if token.is_whitespace:
            if len(tmp) > 0:
                tmp.append(" ")
        elif token.match(sqlparse.tokens.Punctuation, "("):
            par_level += 1
            if par_level > 1:
                tmp.append(token.value)
        elif token.match(sqlparse.tokens.Punctuation, ")"):
            if par_level == 1:
                break
            par_level -= 1
            tmp.append(token.value)
        elif token.match(sqlparse.tokens.Punctuation, ","):
            # at the middle of a column definition, like `id decimal(6, 6)`
            if par_level > 1:
                tmp.append(token.value)
                continue

            # at the end of a column definition, like `id integer,`
            if tmp and not tmp[0].lower() == "index":
                definitions.append(DDLColumn(tmp))
            tmp = []
        elif par_level > 0:
            tmp.append(token.value)

    if tmp and not tmp[0].lower() == "index":
        definitions.append(DDLColumn(tmp))

    return definitions


def _is_create_table_stmt(stmt) -> bool:
    if stmt.get_type() != "CREATE":
        return False

    for token in stmt:
        if token.ttype is not sqlparse.tokens.Keyword:
            continue
        if token.value.lower() == "table":
            return True

    return False
