{# schema.org の型に、取ったバージョンの番号を付ける #}

select v.version, t.*
from {{ ref('stg_types') }} as t
cross join {{ ref('stg_version') }} as v
