{# 型が直接持てるプロパティ（プロパティの domainIncludes を 1 行ずつに開いたもの）。
   親の型から受け継ぐプロパティは含まない。 #}

select
    v.version,
    unnest(string_split(p.domain, '|')) as type_name,
    p.name as property_name
from {{ ref('stg_properties') }} as p
cross join {{ ref('stg_version') }} as v
where p.domain is not null
