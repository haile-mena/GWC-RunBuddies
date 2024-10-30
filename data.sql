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

-- Table for user preferences/survey responses
CREATE TABLE IF NOT EXISTS user_preferences (
    user_id   int(10) not null PRIMARY KEY,
    age INTEGER,
    gender TEXT,
    running_level TEXT,
    preferred_distance TEXT,
    running_frequency TEXT,
    preferred_time TEXT,
    location TEXT,
    goals TEXT,
    bio TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Table for running preferences
CREATE TABLE IF NOT EXISTS running_preferences (
    user_id   int(10) not null PRIMARY KEY,
    preferred_pace TEXT,
    race_participation BOOLEAN,
    preferred_terrain TEXT,
    group_runs BOOLEAN,
    cross_training TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- existing users
INSERT INTO users (id, username, email, password) VALUES (4262325532, 'johndoe', 'johndoe@gmail.com', 'password')
ON CONFLICT(id) DO UPDATE SET username=excluded.username, email=excluded.email, password=excluded.password;

INSERT INTO users (id, username, email, password) VALUES (3079137588, 'janedoe', 'janedoe@gmail.com', 'password')
ON CONFLICT(id) DO UPDATE SET username=excluded.username, email=excluded.email, password=excluded.password;

-- existing preferences
INSERT INTO preferences (user_id, gender, city, state, exp, pace, mile, terrian, time) VALUES (4262325532, 'male', 'New York', 'NY', 'Beginner', 10, 5, 'Flat', 'Morning')
ON CONFLICT(user_id) DO UPDATE SET gender=excluded.gender, city=excluded.city, state=excluded.state, exp=excluded.exp, pace=excluded.pace, mile=excluded.mile, terrian=excluded.terrian, time=excluded.time;

INSERT INTO preferences (user_id, gender, city, state, exp, pace, mile, terrian, time) VALUES (3079137588, 'female', 'Los Angeles', 'CA', 'Intermediate', 9, 10, 'Hilly', 'Evening')
ON CONFLICT(user_id) DO UPDATE SET gender=excluded.gender, city=excluded.city, state=excluded.state, exp=excluded.exp, pace=excluded.pace, mile=excluded.mile, terrian=excluded.terrian, time=excluded.time;

-- existing user preferences
INSERT INTO user_preferences (user_id, age, gender, running_level, preferred_distance, running_frequency, preferred_time, location, goals, bio) VALUES (4262325532, 25, 'male', 'Beginner', '5K', '3 times a week', 'Morning', 'New York', 'Stay fit', 'I love running in the park')
ON CONFLICT(user_id) DO UPDATE SET age=excluded.age, gender=excluded.gender, running_level=excluded.running_level, preferred_distance=excluded.preferred_distance, running_frequency=excluded.running_frequency, preferred_time=excluded.preferred_time, location=excluded.location, goals=excluded.goals, bio=excluded.bio;

INSERT INTO user_preferences (user_id, age, gender, running_level, preferred_distance, running_frequency, preferred_time, location, goals, bio) VALUES (3079137588, 30, 'female', 'Intermediate', '10K', '4 times a week', 'Evening', 'Los Angeles', 'Train for a marathon', 'Running is my passion')
ON CONFLICT(user_id) DO UPDATE SET age=excluded.age, gender=excluded.gender, running_level=excluded.running_level, preferred_distance=excluded.preferred_distance, running_frequency=excluded.running_frequency, preferred_time=excluded.preferred_time, location=excluded.location, goals=excluded.goals, bio=excluded.bio;

-- existing running preferences
INSERT INTO running_preferences (user_id, preferred_pace, race_participation, preferred_terrain, group_runs, cross_training) VALUES (4262325532, '10 min/mile', 1, 'Flat', 1, 'Yoga')
ON CONFLICT(user_id) DO UPDATE SET preferred_pace=excluded.preferred_pace, race_participation=excluded.race_participation, preferred_terrain=excluded.preferred_terrain, group_runs=excluded.group_runs, cross_training=excluded.cross_training;

INSERT INTO running_preferences (user_id, preferred_pace, race_participation, preferred_terrain, group_runs, cross_training) VALUES (3079137588, '9 min/mile', 0, 'Hilly', 0, 'Pilates')
ON CONFLICT(user_id) DO UPDATE SET preferred_pace=excluded.preferred_pace, race_participation=excluded.race_participation, preferred_terrain=excluded.preferred_terrain, group_runs=excluded.group_runs, cross_training=excluded.cross_training;