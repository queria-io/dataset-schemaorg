{# schema.org の型の CSV（schemaorg-current-https-types.csv）。取得したままの形 #}

select * from read_csv('data/schemaorg/types.csv', header = true, all_varchar = true)
