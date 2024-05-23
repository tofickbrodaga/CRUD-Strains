-- migrate:up

INSERT INTO strains_exp.strains (strain_name, creation_date)
SELECT
    'Strain_' || chr(trunc(65 + random() * 26)::int) || chr(trunc(65 + random() * 26)::int) || '_' || row_number() OVER () || '_' || uuid_generate_v4() AS strain_name,
    '2023-01-01'::DATE + (random() * interval '365 days') AS creation_date
FROM
    generate_series(1, 100000);

-- migrate:down
