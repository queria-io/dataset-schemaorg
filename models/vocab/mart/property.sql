{# schema.org のプロパティに、取ったバージョンの番号と元のファイルを付ける #}

select v.version, p.* exclude (source_path), f.sha256 as source_sha256
from {{ ref('stg_properties') }} as p
cross join {{ ref('stg_version') }} as v
left join {{ ref('stg_source_file') }} as f on list_contains(f.paths, p.source_path)
