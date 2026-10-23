{# schema.org のプロパティ。pipelines/schemaorg.py が最新の版の schemaorg-current-https-properties.csv を取る。
   snake_case_name は Queria の列名にするときの形（postalCode → postal_code）。 #}

select
    (select trim(content) from read_text('data/schemaorg/version.txt')) as version,
    label as name,
    id as uri,
    lower(regexp_replace(label, '([a-z0-9])([A-Z])', '\1_\2', 'g')) as snake_case_name,
    {{ plain_text('comment') }} as description,
    {{ schemaorg_names('domainIncludes') }} as domain,
    {{ schemaorg_names('rangeIncludes') }} as range,
    {{ schemaorg_names('subPropertyOf') }} as parent,
    nullif(equivalentProperty, '') as equivalent_property,
    {{ schemaorg_names('inverseOf') }} as inverse_of,
    {{ schemaorg_names('supersededBy') }} as superseded_by
from read_csv('data/schemaorg/properties.csv', header = true, all_varchar = true)
