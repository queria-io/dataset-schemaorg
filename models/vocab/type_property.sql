{# 型が直接持てるプロパティ（プロパティの domainIncludes を 1 行ずつに開いたもの）。
   親の型から受け継ぐプロパティは含まない。 #}

select
    version,
    unnest(string_split(domain, '|')) as type_name,
    name as property_name
from {{ ref('property') }}
where domain is not null
