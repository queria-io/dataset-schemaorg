{# schema.org の型。pipelines/schemaorg.py が最新の版の schemaorg-current-https-types.csv を取る #}

select
    (select trim(content) from read_text('data/schemaorg/version.txt')) as version,
    label as name,
    id as uri,
    {{ plain_text('comment') }} as description,
    {{ schemaorg_names('subTypeOf') }} as parent,
    {{ schemaorg_names('enumerationtype') }} as enumeration_type,
    nullif(equivalentClass, '') as equivalent_class,
    {{ schemaorg_names('supersededBy') }} as superseded_by
from read_csv('data/schemaorg/types.csv', header = true, all_varchar = true)
