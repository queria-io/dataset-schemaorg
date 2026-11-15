{# schema.org の型に、取ったバージョンの番号と元のファイルを付ける #}

select v.version, t.* exclude (source_path), f.sha256 as source_sha256
from {{ ref('stg_types') }} as t
cross join {{ ref('stg_version') }} as v
left join {{ ref('stg_source_file') }} as f on list_contains(f.paths, t.source_path)
