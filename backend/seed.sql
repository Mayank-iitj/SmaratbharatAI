-- SmartBharat AI Mock Seed Data

CREATE TABLE IF NOT EXISTS profiles (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    age INT,
    income DECIMAL(10,2),
    state VARCHAR(100),
    district VARCHAR(100),
    occupation VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS schemes (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    eligibility_criteria TEXT,
    official_link VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS complaints (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    category VARCHAR(100),
    description TEXT,
    status VARCHAR(50) DEFAULT 'Pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert dummy schemes
INSERT INTO schemes (name, description, eligibility_criteria, official_link) VALUES
('PM Kisan Samman Nidhi', 'Income support of Rs. 6000/- per year to all landholding farmer families.', 'Landholding farmers', 'https://pmkisan.gov.in'),
('Stand-Up India Scheme', 'Facilitates bank loans between 10 lakh and 1 Crore to at least one SC/ST borrower and at least one woman borrower.', 'SC/ST or Women entrepreneurs', 'https://www.standupmitra.in')
ON CONFLICT DO NOTHING;

-- Insert a dummy user
INSERT INTO profiles (user_id, name, age, income, state, district, occupation) VALUES
('user_123', 'Rahul Sharma', 32, 450000.00, 'Maharashtra', 'Pune', 'Small Business Owner')
ON CONFLICT (user_id) DO NOTHING;
