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

INSERT INTO users (login, lastname, firstname)
VALUES
    ('user1', 'Doe', 'John'),
    ('user2', 'Smith', 'Alice'),
    ('user3', 'Johnson', 'Bob'),
    ('user4', 'Williams', 'Emily'),
    ('user5', 'Brown', 'Michael'),
     ('user6', 'Jones', 'Emma'),
    ('user7', 'Garcia', 'Daniel');

INSERT INTO strains (strain_name, creation_date)
VALUES
    ('Strain_A', '2023-01-15'),
    ('Strain_B', '2023-02-20'),
    ('Strain_C', '2023-03-25'),
    ('Strain_D', '2023-04-10'),
    ('Strain_E', '2023-05-15'),
    ('Strain_F', '2023-06-20'),
    ('Strain_G', '2023-07-25');

INSERT INTO user_strains (user_id, strain_id)
SELECT u.id, s.id
FROM users u
CROSS JOIN strains s
WHERE u.lastname = 'Doe'
AND s.strain_name IN ('Strain_A', 'Strain_B');


INSERT INTO user_strains (user_id, strain_id)
SELECT u.id, s.id
FROM users u
JOIN strains s
ON s.strain_name = 'Strain_G'
WHERE u.lastname = 'Johnson';


INSERT INTO user_strains (user_id, strain_id)
SELECT u.id, s.id
FROM users u
JOIN strains s
ON s.strain_name = 'Strain_F'
WHERE u.lastname = 'Garcia';

-- migrate:down

