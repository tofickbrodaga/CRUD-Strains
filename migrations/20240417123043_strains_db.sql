-- migrate:up
create extension if not exists "uuid-ossp";

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    login VARCHAR(50) UNIQUE,
    lastname VARCHAR(50),
    firstname VARCHAR(50)
);

CREATE TABLE strains (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    strain_name TEXT UNIQUE,
    creation_date DATE
);

CREATE TABLE user_strains (
    user_id UUID REFERENCES users(id),
    strain_id UUID REFERENCES strains(id),
    PRIMARY KEY (user_id, strain_id)
);

CREATE TABLE experiments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    strain_name TEXT REFERENCES strains(strain_name),
    start_date DATE,
    end_date DATE,
    growth_environment VARCHAR(50),
    results TEXT
);

-- migrate:down

