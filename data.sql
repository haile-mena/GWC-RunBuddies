DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id        int(10) PRIMARY KEY,
    username  varchar(50) not null,
    email     varchar(50) not null,
    password  varchar(50) not null 
);

DROP TABLE IF EXISTS preferences;
CREATE TABLE preferences (
    user_id   int(10) not null PRIMARY KEY,
    gender    varchar(50) not null,
    city      varchar(50) not null,
    state     varchar(50) not null,
    exp       varchar(50) not null,
    pace      int(50),
    mile      int(50),
    terrian   varchar(50),
    time      varchar(50)
);

-- existing users
INSERT INTO users (id, username, email, password) VALUES (4262325532, 'johndoe', 'johndoe@gmail.com', 'password');
INSERT INTO users (id, username, email, password) VALUES (3079137588, 'janedoe', 'janedoe@gmail.com', 'password');

-- existing preferences
INSERT INTO preferences (user_id, gender, city, state, exp, pace, mile, terrian, time) VALUES (4262325532, 'male', 'New York', 'NY', 'Beginner', 10, 5, 'Flat', 'Morning');
INSERT INTO preferences (user_id, gender, city, state, exp, pace, mile, terrian, time) VALUES (3079137588, 'female', 'Los Angeles', 'CA', 'Intermediate', 9, 10, 'Hilly', 'Evening');