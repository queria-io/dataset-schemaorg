{# pipelines/schemaorg.py が取ったバージョンの番号（data/schemaorg/version.txt）。取得したままの形 #}

select content from read_text('data/schemaorg/version.txt')
