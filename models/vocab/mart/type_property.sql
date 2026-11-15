{# 型が直接持てるプロパティ（プロパティの domainIncludes を 1 行ずつに開いたもの）。
   親の型から受け継ぐプロパティは含まない。 #}

with properties as (
    select p.*, f.sha256 as source_sha256
    from {{ ref('stg_properties') }} as p
    left join {{ ref('stg_source_file') }} as f on list_contains(f.paths, p.source_path)
    where p.domain is not null
)

select
    v.version,
    unnest(string_split(p.domain, '|')) as type_name,
    p.name as property_name,
    p.source_sha256
from properties as p
cross join {{ ref('stg_version') }} as v
