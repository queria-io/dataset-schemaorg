select type_name, property_name
from {{ ref('type_property') }}
group by all
having count(*) > 1
