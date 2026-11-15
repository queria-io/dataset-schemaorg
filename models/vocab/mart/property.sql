{# schema.org のプロパティに、取ったバージョンの番号を付ける #}

select v.version, p.*
from {{ ref('stg_properties') }} as p
cross join {{ ref('stg_version') }} as v
