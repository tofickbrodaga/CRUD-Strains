# CRUD-Strains

## Штаммы и пользователи:
- штамм может принадлежать нескольким пользователям
- пользователь может создавать несколько штаммов

Штамм - УИН, наименование, дата создания

Пользователь - логин, фамилия, имя

## Штаммы и эксперименты: 
- штамм может иметь несколько экспериментов
- эксперимент может принадлежать только одному штамму
  
Эксперимент - дата начала, дата конца, среда выращивания, результаты


## Данные для заполнения БД:

Users
```
INSERT INTO users (login, lastname, firstname)
VALUES
    ('user1', 'Doe', 'John'),
    ('user2', 'Smith', 'Alice'),
    ('user3', 'Johnson', 'Bob'),
    ('user4', 'Williams', 'Emily'),
    ('user5', 'Brown', 'Michael'),
     ('user6', 'Jones', 'Emma'),
    ('user7', 'Garcia', 'Daniel');
```
Strains
```
INSERT INTO strains (strain_name, creation_date)
VALUES
    ('Strain_A', '2023-01-15'),
    ('Strain_B', '2023-02-20'),
    ('Strain_C', '2023-03-25'),
    ('Strain_D', '2023-04-10'),
    ('Strain_E', '2023-05-15'),
    ('Strain_F', '2023-06-20'),
    ('Strain_G', '2023-07-25');
```
User to Strains
```
INSERT INTO user_strains (user_id, strain_id)
SELECT u.id, s.id
FROM users u
CROSS JOIN strains s;
```
