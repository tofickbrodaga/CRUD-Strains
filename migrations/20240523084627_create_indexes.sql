-- migrate:up
create index strains_creation_idx on strains_exp.strains using btree(creation_date);

create extension pg_trgm;
create index strains_name_trgm_idx on strains_exp.strains using gist(strain_name gist_trgm_ops);
-- migrate:down