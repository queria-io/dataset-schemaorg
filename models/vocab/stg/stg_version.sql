select trim(content) as version
from {{ ref('raw_version') }}
