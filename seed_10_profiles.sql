-- ============================================================
-- DriftDater Seed Data (FIXED FOR CURRENT MODELS)
-- ============================================================

BEGIN;

-- ============================================================
-- USERS
-- ============================================================

INSERT INTO users (
    first_name, last_name, username, dob,
    looking_for, password_hash, email, gender, has_changed_dob
) VALUES
('Aaliya',  'Thompson',  'aaliya_t',   '1996-03-14', 'Men',
 'pbkdf2:sha256:1000000$v4jMwguNvlBLFEzS$206532695a6b1fa408e4849cba1cce130a16f2e8689b397e1eee47570dacc97d', 'aaliya.thompson@email.com', 'Female', false),
('Marcus',  'Reid',      'marcus_r',   '1993-07-22', 'Women',
 'pbkdf2:sha256:1000000$v4jMwguNvlBLFEzS$206532695a6b1fa408e4849cba1cce130a16f2e8689b397e1eee47570dacc97d', 'marcus.reid@email.com', 'Male', false),

('Simone',  'Clarke',    'simone_c',   '1998-11-05', 'Everyone',
 'pbkdf2:sha256:1000000$v4jMwguNvlBLFEzS$206532695a6b1fa408e4849cba1cce130a16f2e8689b397e1eee47570dacc97d', 'simone.clarke@email.com', 'Female', false),

('Devonte', 'Brown',     'devonte_b',  '1995-01-30', 'Women',
 'pbkdf2:sha256:1000000$v4jMwguNvlBLFEzS$206532695a6b1fa408e4849cba1cce130a16f2e8689b397e1eee47570dacc97d', 'devonte.brown@email.com', 'Male', false),

('Priya',   'Nair',      'priya_n',    '1997-06-18', 'Men',
 'pbkdf2:sha256:1000000$v4jMwguNvlBLFEzS$206532695a6b1fa408e4849cba1cce130a16f2e8689b397e1eee47570dacc97d', 'priya.nair@email.com', 'Female', false),

('Jordan',  'Francis',   'jordan_f',   '1994-09-09', 'Everyone',
 'pbkdf2:sha256:1000000$v4jMwguNvlBLFEzS$206532695a6b1fa408e4849cba1cce130a16f2e8689b397e1eee47570dacc97d', 'jordan.francis@email.com', 'Non-binary', false),

('Kezia',   'Morgan',    'kezia_m',    '1999-04-25', 'Men',
 'pbkdf2:sha256:1000000$v4jMwguNvlBLFEzS$206532695a6b1fa408e4849cba1cce130a16f2e8689b397e1eee47570dacc97d', 'kezia.morgan@email.com', 'Female', false),

('Liam',    'Hutchinson','liam_h',     '1992-12-03', 'Women',
 'pbkdf2:sha256:1000000$v4jMwguNvlBLFEzS$206532695a6b1fa408e4849cba1cce130a16f2e8689b397e1eee47570dacc97d', 'liam.hutchinson@email.com', 'Male', false),

('Nadia',   'Levy',      'nadia_l',    '2000-08-17', 'Everyone',
 'pbkdf2:sha256:1000000$v4jMwguNvlBLFEzS$206532695a6b1fa408e4849cba1cce130a16f2e8689b397e1eee47570dacc97d', 'nadia.levy@email.com', 'Female', false),

('Tyrese',  'Campbell',  'tyrese_c',   '1991-02-11', 'Women',
 'pbkdf2:sha256:1000000$v4jMwguNvlBLFEzS$206532695a6b1fa408e4849cba1cce130a16f2e8689b397e1eee47570dacc97d', 'tyrese.campbell@email.com', 'Male', false);

-- ============================================================
-- PROFILES
-- ============================================================

INSERT INTO profile (
    user_id, visibility, education, photo_url, bio, location, interests
)
SELECT u.user_id, v.visibility, v.education, v.photo_url, v.bio, v.location, v.interests
FROM users u
JOIN (VALUES
  ('aaliya_t',   'Public',  'Bachelors', 'https://i.pravatar.cc/300?u=1',
   'Food lover, explorer of Kingston cafés.', 'Kingston, Jamaica', 'Cooking, Travel, Music'),

  ('marcus_r',   'Public',  'Masters', 'https://i.pravatar.cc/300?u=2',
   'Dev by day, chef by night.', 'Montego Bay, Jamaica', 'Tech, Fitness, Music'),

  ('simone_c',   'Public',  'Bachelors', 'https://i.pravatar.cc/300?u=3',
   'Film camera enthusiast.', 'Kingston, Jamaica', 'Art, Photography, Film'),

  ('devonte_b',  'Public',  'High School', 'https://i.pravatar.cc/300?u=4',
   'Gym + football lifestyle.', 'Portmore, Jamaica', 'Sports, Fitness, Travel'),

  ('priya_n',    'Public',  'PhD', 'https://i.pravatar.cc/300?u=5',
   'Research + coffee debates.', 'Kingston, Jamaica', 'Reading, Travel, Cooking'),

  ('jordan_f',   'Public',  'Bachelors', 'https://i.pravatar.cc/300?u=6',
   'Designer + plant parent.', 'Ocho Rios, Jamaica', 'Art, Film, Pets'),

  ('kezia_m',    'Public',  'Masters', 'https://i.pravatar.cc/300?u=7',
   'Salsa dancer & marketer.', 'Kingston, Jamaica', 'Music, Socializing, Fashion'),

  ('liam_h',     'Public',  'Bachelors', 'https://i.pravatar.cc/300?u=8',
   'Architect obsessed with coffee.', 'Spanish Town, Jamaica', 'Art, Travel, Reading'),

  ('nadia_l',    'Private', 'Bachelors', 'https://i.pravatar.cc/300?u=9',
   'Med student, always overthinking.', 'Kingston, Jamaica', 'Fitness, Reading, Film'),

  ('tyrese_c',   'Public',  'Masters', 'https://i.pravatar.cc/300?u=10',
   'Producer + vinyl collector.', 'Mandeville, Jamaica', 'Music, Gaming, Tech')
) AS v(username, visibility, education, photo_url, bio, location, interests)
ON u.username = v.username;

-- ============================================================
-- PREFERENCES
-- ============================================================

INSERT INTO preferences (
    user_id, gender_pref, education_pref, religion_pref, age_min, age_max
)
SELECT u.user_id, v.gender_pref, v.education_pref, v.religion_pref, v.age_min, v.age_max
FROM users u
JOIN (VALUES
  ('aaliya_t',   'Male',     'Bachelors', 'Open', 22, 35),
  ('marcus_r',   'Female',   'Bachelors', 'Christian', 22, 32),
  ('simone_c',   'Everyone', 'Bachelors', 'Open', 20, 35),
  ('devonte_b',  'Female',   'High School','Open', 20, 30),
  ('priya_n',    'Male',     'Masters', 'Open', 25, 38),
  ('jordan_f',   'Everyone', 'Bachelors', 'Agnostic', 22, 35),
  ('kezia_m',    'Male',     'Bachelors', 'Christian', 24, 36),
  ('liam_h',     'Female',   'Bachelors', 'Open', 24, 38),
  ('nadia_l',    'Everyone', 'Masters', 'Open', 22, 32),
  ('tyrese_c',   'Female',   'Bachelors', 'Open', 22, 35)
) AS v(username, gender_pref, education_pref, religion_pref, age_min, age_max)
ON u.username = v.username;

COMMIT;