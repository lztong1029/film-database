-- =========================================
-- Create Database
-- =========================================
CREATE DATABASE IF NOT EXISTS filmdb
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_unicode_ci;

USE filmdb;

-- =========================================
-- 1. Core Tables
-- =========================================

-- Movies table
CREATE TABLE Movies (
    movieId VARCHAR(20) PRIMARY KEY,
    primaryTitle VARCHAR(255),
    originalTitle VARCHAR(255),
    titleType VARCHAR(50),
    startYear INT,
    runtimeMinutes INT,
    releaseYear INT
);

-- Studio table
CREATE TABLE Studio (
    studioId INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    country VARCHAR(255),
    city VARCHAR(255),
    foundedYear INT
);

-- Award table
CREATE TABLE Award (
    awardId INT AUTO_INCREMENT PRIMARY KEY,
    awardName VARCHAR(255)
);

-- Genre table
CREATE TABLE Genre (
    genreId INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) UNIQUE
);

-- User table (synthetic)
CREATE TABLE User (
    userId INT AUTO_INCREMENT PRIMARY KEY,
    userName VARCHAR(255)
);

-- People table
CREATE TABLE People (
    pId VARCHAR(20) PRIMARY KEY,
    primaryName VARCHAR(255),
    birthYear INT,
    deathYear INT,
    primaryProfession VARCHAR(255),
    currentStudioId INT,
    FOREIGN KEY (currentStudioId) REFERENCES Studio(studioId)
);

-- =========================================
-- 2. Subtype Tables (ISA: Actor / Director / Writer)
-- =========================================

CREATE TABLE Actor (
    actorId VARCHAR(20) PRIMARY KEY,
    number_of_fans INT DEFAULT 0,
    FOREIGN KEY (actorId) REFERENCES People(pId)
);

CREATE TABLE Director (
    directorId VARCHAR(20) PRIMARY KEY,
    directing_style VARCHAR(255),
    best_known_movieId VARCHAR(20),
    FOREIGN KEY (directorId) REFERENCES People(pId),
    FOREIGN KEY (best_known_movieId) REFERENCES Movies(movieId)
);

CREATE TABLE Writer (
    writerId VARCHAR(20) PRIMARY KEY,
    writing_style VARCHAR(255),
    best_known_movieId VARCHAR(20),
    FOREIGN KEY (writerId) REFERENCES People(pId),
    FOREIGN KEY (best_known_movieId) REFERENCES Movies(movieId)
);

-- =========================================
-- 3. Review Table
-- =========================================

CREATE TABLE Review (
    reviewId INT AUTO_INCREMENT PRIMARY KEY,
    userId INT,
    movieId VARCHAR(20),
    post_time DATETIME,
    content TEXT,
    rating INT CHECK (rating >= 1 AND rating <= 10),
    FOREIGN KEY (userId) REFERENCES User(userId),
    FOREIGN KEY (movieId) REFERENCES Movies(movieId)
);

-- =========================================
-- 4. Relationship Tables (Join Tables)
-- =========================================

-- Movie–Genre
CREATE TABLE Has_Genre (
    movieId VARCHAR(20),
    genreId INT,
    PRIMARY KEY (movieId, genreId),
    FOREIGN KEY (movieId) REFERENCES Movies(movieId),
    FOREIGN KEY (genreId) REFERENCES Genre(genreId)
);

-- Movie–Studio
CREATE TABLE Produced_By (
    movieId VARCHAR(20),
    studioId INT,
    PRIMARY KEY (movieId, studioId),
    FOREIGN KEY (movieId) REFERENCES Movies(movieId),
    FOREIGN KEY (studioId) REFERENCES Studio(studioId)
);

-- Movie–Award
CREATE TABLE Wins_Award (
    movieId VARCHAR(20),
    awardId INT,
    year INT,
    PRIMARY KEY (movieId, awardId),
    FOREIGN KEY (movieId) REFERENCES Movies(movieId),
    FOREIGN KEY (awardId) REFERENCES Award(awardId)
);

-- User–Favorite–Movie
CREATE TABLE Favorites (
    userId INT,
    movieId VARCHAR(20),
    PRIMARY KEY (userId, movieId),
    FOREIGN KEY (userId) REFERENCES User(userId),
    FOREIGN KEY (movieId) REFERENCES Movies(movieId)
);

-- Actor–ActsIn–Movie
CREATE TABLE Acts_In (
    movieId VARCHAR(20),
    actorId VARCHAR(20),
    PRIMARY KEY (movieId, actorId),
    FOREIGN KEY (movieId) REFERENCES Movies(movieId),
    FOREIGN KEY (actorId) REFERENCES Actor(actorId)
);

-- Director–Directs–Movie
CREATE TABLE Directs (
    movieId VARCHAR(20),
    directorId VARCHAR(20),
    PRIMARY KEY (movieId, directorId),
    FOREIGN KEY (movieId) REFERENCES Movies(movieId),
    FOREIGN KEY (directorId) REFERENCES Director(directorId)
);

-- Writer–Writes–Movie
CREATE TABLE Writes_Script_For (
    movieId VARCHAR(20),
    writerId VARCHAR(20),
    PRIMARY KEY (movieId, writerId),
    FOREIGN KEY (movieId) REFERENCES Movies(movieId),
    FOREIGN KEY (writerId) REFERENCES Writer(writerId)
);