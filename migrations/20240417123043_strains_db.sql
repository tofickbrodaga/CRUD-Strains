-- migrate:up
create extension if not exists "uuid-ossp";
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    nickname VARCHAR(50) UNIQUE,
    lastname VARCHAR(50),
    firstname VARCHAR(50)
);

CREATE TABLE strains (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_nickname VARCHAR(50) REFERENCES users(nickname),
    strain_name VARCHAR(50) UNIQUE,
    creation_date DATE
);

CREATE TABLE experiments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    strain_name VARCHAR(50) REFERENCES strains(strain_name), -- Maintain the reference
    start_date DATE,
    end_date DATE,
    growthenvironment VARCHAR(50),
    results TEXT,
    CONSTRAINT unique_strain_name UNIQUE (strain_name)
);

-- migrate:down

