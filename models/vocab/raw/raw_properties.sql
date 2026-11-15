{# schema.org のプロパティの CSV（schemaorg-current-https-properties.csv）。取得したままの形 #}

select * from read_csv('data/schemaorg/properties.csv', header = true, all_varchar = true, filename = true)
