{# schema.org の型 #}

select
    label as name,
    id as uri,
    {{ plain_text('comment') }} as description,
    {{ schemaorg_names('subTypeOf') }} as parent,
    {{ schemaorg_names('enumerationtype') }} as enumeration_type,
    nullif(equivalentClass, '') as equivalent_class,
    {{ schemaorg_names('supersededBy') }} as superseded_by,
    filename as source_path
from {{ ref('raw_types') }}
