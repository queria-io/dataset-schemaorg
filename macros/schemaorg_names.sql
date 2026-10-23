{# "https://schema.org/A, https://schema.org/B" を "A|B" にする。schema.org の外の URI はそのまま残す #}
{% macro schemaorg_names(column) -%}
    nullif(replace(replace({{ column }}, 'https://schema.org/', ''), ', ', '|'), '')
{%- endmacro %}

{# 説明文に入っている HTML のリンクや強調を落とす #}
{% macro plain_text(column) -%}
    nullif(trim(regexp_replace({{ column }}, '<[^>]+>', '', 'g')), '')
{%- endmacro %}
