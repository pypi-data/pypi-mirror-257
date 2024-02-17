ORIGIN_WS_NAME = "origin"
MAIN_WS_NAME = "main"
LIVE_WS_NAME = "live"
SNAPSHOT_WS_NAME = "snapshot"

ENABLED_TABLE_FUNCTIONS = {"generateRandom", "null", "numbers", "numbers_mt", "values", "zeros", "zeros_mt"}

ENABLED_SYSTEM_TABLES = {
    "functions",
    "numbers",
    "numbers_mt",
    "one",
}

RESERVED_DATABASE_NAMES = {
    "tinybird",
    "system",
    "public",
    "default",
    "main",
    ORIGIN_WS_NAME,
    MAIN_WS_NAME,
    LIVE_WS_NAME,
    SNAPSHOT_WS_NAME,
    "_temporary_and_external_tables",
}

# Expect this to not be a complete list of all CH Reserved keywords.

SQL_KEYWORDS = {
    # Clickhouse/src/Client/Suggest.cpp
    "add",
    "admin",
    "after",
    "alias",
    "all",
    "alter",
    "and",
    "any",
    "array",
    "as",
    "asc",
    "async",
    "attach",
    "between",
    "by",
    "case",
    "check",
    "clear",
    "cluster",
    "collate",
    "column",
    "copy",
    "create",
    "cross",
    "database",
    "databases",
    "deduplicate",
    "default",
    "desc",
    "describe",
    "detach",
    "distinct",
    "drop",
    "else",
    "end",
    "engine",
    "except",
    "exists",
    "fetch",
    "final",
    "for",
    "format",
    "freeze",
    "from",
    "full",
    "global",
    "grant",
    "group",
    "having",
    "host",
    "identified",
    "if",
    "ilike",
    "in",
    "inner",
    "insert",
    "interval",
    "into",
    "ip",
    "join",
    "key",
    "kill",
    "left",
    "like",
    "limit",
    "limits",
    "local",
    "materialized",
    "modify",
    "name",
    "not",
    "on",
    "only",
    "optimize",
    "option",
    "or",
    "order",
    "outer",
    "outfile",
    "part",
    "partition",
    "permissive",
    "policy",
    "populate",
    "prewhere",
    "primary",
    "processlist",
    "profile",
    "project",
    "query",
    "quota",
    "randomized",
    "readonly",
    "regexp",
    "rename",
    "replace",
    "restrictive",
    "revoke",
    "right",
    "role",
    "row",
    "sample",
    "select",
    "set",
    "settings",
    "show",
    "sync",
    "table",
    "tables",
    "temporary",
    "test",
    "then",
    "to",
    "totals",
    "tracking",
    "truncate",
    "union",
    "use",
    "user",
    "using",
    "values",
    "view",
    "when",
    "where",
    "with",
    "writable"
    # Extra keywords that were added here but don't come from CH source code
    "anti",
    "asof",
    "cube",
    "explain",
    "file",
    "fill",
    "max",
    "min",
    "null",
    "rollout",
    "semi",
    "step",
    "ties",
    "variable",
}

FORBIDDEN_SQL_KEYWORDS = {
    "add",
    "after",
    "all",
    "and",
    "any",
    "array",
    "as",
    "asc",
    "between",
    "by",
    "case",
    "collate",
    "cross",
    "default",
    "desc",
    "distinct",
    "else",
    "end",
    "exists",
    "from",
    "full",
    "global",
    "group",
    "having",
    "if",
    "ilike",
    "in",
    "inner",
    "insert",
    "interval",
    "into",
    "join",
    "left",
    "like",
    "limit",
    "limits",
    "materialized",
    "not",
    "on",
    "or",
    "order",
    "outer",
    "prewhere",
    "right",
    "sample",
    "select",
    "then",
    "to",
    "totals",
    "union",
    "using",
    "where",
    "with",
    # Extra keywords that were added here but don't come from CH source code
    "anti",
    "asof",
    "cube",
    "max",
    "min",
    "null",
    "semi",
}

CH_SETTINGS_JOIN_ALGORITHM_HASH = "hash"  # uses 'hash' by default, https://clickhouse.com/docs/en/operations/settings/settings/#settings-join_algorithm
CH_SETTINGS_JOIN_ALGORITHM_AUTO = "auto,hash"
