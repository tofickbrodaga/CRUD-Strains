-- migrate:up
CREATE TABLE users (
    id UUID PRIMARY KEY,
    login VARCHAR(50),
    lastname VARCHAR(50),
    firstname VARCHAR(50)
);

CREATE TABLE strains (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users,
    strain_name VARCHAR(50),
    creation_date DATE
);

CREATE TABLE experiments (
    id UUID PRIMARY KEY,
    strain_id UUID REFERENCES strains,
    start_date DATE,
    end_date DATE,
    growthenvironment VARCHAR(50),
    results TEXT
);

-- migrate:down

