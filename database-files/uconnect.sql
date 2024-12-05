SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

DROP DATABASE IF EXISTS `uconnect`;
CREATE DATABASE IF NOT EXISTS `uconnect`;
USE `uconnect`;


CREATE TABLE IF NOT EXISTS `User`
(
    `UserID` INT PRIMARY KEY AUTO_INCREMENT,
    `FirstName`  VARCHAR(50)         NOT NULL,
    `LastName`   VARCHAR(50)         NOT NULL,
    `Email`      VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS `Advisor`
(
    `AdvisorID`  INT PRIMARY KEY AUTO_INCREMENT,
    `UserID`     INT,
    `FirstName`  VARCHAR(50)         NOT NULL,
    `LastName`   VARCHAR(50)         NOT NULL,
    `College`    VARCHAR(100),
    `Department` VARCHAR(100),
    `Email`      VARCHAR(100) UNIQUE NOT NULL,
    `Phone`      VARCHAR(15),
    `IsActive`   BOOLEAN DEFAULT TRUE,
    `LastLogin`  DATETIME DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (`UserID`) REFERENCES User(`UserID`)
);

CREATE TABLE IF NOT EXISTS `Student`
(
    `StudentID`   INT PRIMARY KEY AUTO_INCREMENT,
    `UserID`     INT,
    `FirstName`   VARCHAR(50)         NOT NULL,
    `LastName`    VARCHAR(50)         NOT NULL,
    `Username`    VARCHAR(50) UNIQUE  NOT NULL,
    `College`     VARCHAR(100),
    `Major`       VARCHAR(100),
    `Year`        INT,
    `Email`       VARCHAR(100) UNIQUE NOT NULL,
    `AdvisorID`   INT,
    `MentorID`    INT,
    `Num_Coops`   INT DEFAULT 0,
    `CoopStatus`  VARCHAR(50),
    `CoopPositionID` INT,
    `LastLogin`   DATETIME DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,
    `IsActive`    BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (`UserID`) REFERENCES `User`(`UserID`),
    FOREIGN KEY (`MentorID`) REFERENCES `Student`(`StudentID`)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (`AdvisorID`) REFERENCES `Advisor`(`AdvisorID`)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS `Company`
(
    `CompanyID` INT PRIMARY KEY AUTO_INCREMENT,
    `Name`      VARCHAR(100) NOT NULL,
    `Location`  VARCHAR(100),
    `Industry`  VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS `Company_Worked`
(
    `CompanyID` INT,
    `UserID` INT,
    PRIMARY KEY (`CompanyID`, `UserID`),
    FOREIGN KEY (`CompanyID`) REFERENCES `Company`(`CompanyID`)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (`UserID`) REFERENCES `User`(`UserID`)
        ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS `Position`
(
    `PositionID`  INT PRIMARY KEY AUTO_INCREMENT,
    `Name`        VARCHAR(100) NOT NULL,
    `Description` TEXT,
    `IsCoop`      BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS `Positions_Offered`
(
    `CompanyID` INT,
    `PositionID` INT,
    PRIMARY KEY (`CompanyID`, `PositionID`),
    FOREIGN KEY (`CompanyID`) REFERENCES `Company`(`CompanyID`)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (`PositionID`) REFERENCES `Position`(`PositionID`)
        ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS `Company_Recruiter`
(
    `RecruiterID` INT PRIMARY KEY AUTO_INCREMENT,
    `LastName`    VARCHAR(50)         NOT NULL,
    `FirstName`   VARCHAR(50)         NOT NULL,
    `Email`       VARCHAR(100) UNIQUE NOT NULL,
    `Position`    VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS `Recruiters_List`
(
    `CompanyID` INT,
    `RecruiterID` INT,
    PRIMARY KEY (`CompanyID`, `RecruiterID`),
    FOREIGN KEY (`CompanyID`) REFERENCES `Company`(`CompanyID`)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (`RecruiterID`) REFERENCES `Company_Recruiter`(`RecruiterID`)
        ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS `Alumnus`
(
    `AlumnusID`       INT PRIMARY KEY `AUTO_INCREMENT`,
    `UserID`          INT,
    `FirstName`       VARCHAR(50)         NOT NULL,
    `LastName`        VARCHAR(50)         NOT NULL,
    `College`         VARCHAR(100),
    `Major`           VARCHAR(100),
    `Email`           VARCHAR(100) UNIQUE NOT NULL,
    `Num_Coops`       INT     DEFAULT 0,
    `CurrentCompany`  VARCHAR(100),
    `CurrentPosition` VARCHAR(100),
    `LastLogin`       DATETIME DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,
    IsActive        BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (`UserID`) REFERENCES `User`(`UserID`)
);

CREATE TABLE IF NOT EXISTS `Alumni_Mentors`
(
    `StudentID` INT,
    `AlumnusID` INT,
    PRIMARY KEY (`StudentID`, `AlumnusID`),
    FOREIGN KEY (`StudentID`) REFERENCES `Student`(`StudentID`)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (`AlumnusID`) REFERENCES `Alumnus`(`AlumnusID`)
        ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS `Post`
(
    `PostID`      INT AUTO_INCREMENT PRIMARY KEY,
    `AuthorID`    INT,
    `Title`       VARCHAR(100)                        NOT NULL,
    `Slug`        VARCHAR(100) UNIQUE                 NOT NULL,
    `Content`     TEXT,
    `CreatedAt`   DATETIME  DEFAULT CURRENT_TIMESTAMP NOT NULL,
    `UpdatedAt`   TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `PublishedAt` DATETIME,
    FOREIGN KEY (`AuthorID`) REFERENCES `User`(`UserID`)
        ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS `Posts_Made`
(
    `AlumnusID` INT,
    `PostID` INT,
    PRIMARY KEY (`PostID`, `AlumnusID`),
    FOREIGN KEY (`PostID`) REFERENCES `Post`(`PostID`)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (`AlumnusID`) REFERENCES `Alumnus`(`AlumnusID`)
        ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS `Post_Comment`
(
    `CommentID`   INT AUTO_INCREMENT PRIMARY KEY,
    `AuthorID`    INT,
    `Content`     TEXT,
    `PublishedAt` DATETIME,
    `CreatedAt`   DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`AuthorID`) REFERENCES `User`(`UserID`)
        ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Comments_Made
(
    `PostID` INT,
    `CommentID` INT,
    PRIMARY KEY (`PostID`, `CommentID`),
    FOREIGN KEY (`PostID`) REFERENCES `Post`(`PostID`)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (`CommentID`) REFERENCES `Post_Comment`(`CommentID`)
        ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS `Courses`
(
    `CoursesID`     INT PRIMARY KEY AUTO_INCREMENT,
    `Name`          VARCHAR(100) NOT NULL,
    `Professor`     VARCHAR(100),
    `Description`   TEXT,
    `AverageRating` DECIMAL(3, 2) DEFAULT 0,
    `IsActive`      BOOLEAN       DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS `Courses_Taken`
(
    `UserID` INT,
    `CoursesID` INT,
    PRIMARY KEY (`UserID`, `CoursesID`),
    FOREIGN KEY (`UserID`) REFERENCES `User`(`UserID`)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (`CoursesID`) REFERENCES `Courses`(`CoursesID`)
        ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS `Review`
(
    `ReviewID` INT PRIMARY KEY AUTO_INCREMENT,
    `Name` VARCHAR(50) NOT NULL,
    `AuthorID` INT,
    `Title`    VARCHAR(100),
    `Rating`   DECIMAL(3, 2),
    `Content`  TEXT,
    FOREIGN KEY (`AuthorID`) REFERENCES `User`(`UserID`)
        ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS `Reviews_Made`
(
    `CoursesID` INT,
    `ReviewID` INT,
    PRIMARY KEY (`ReviewID`, `CoursesID`),
    FOREIGN KEY (`ReviewID`) REFERENCES `Review`(`ReviewID`)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (`CoursesID`) REFERENCES `Courses`(`CoursesID`)
        ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS `User_Admin`
(
    `AdminID`    INT PRIMARY KEY AUTO_INCREMENT,
    `UserID`     INT,
    `FirstName`  VARCHAR(50)         NOT NULL,
    `LastName`   VARCHAR(50)         NOT NULL,
    `Email`      VARCHAR(100) UNIQUE NOT NULL,
    `IsActive`   BOOLEAN  DEFAULT TRUE,
    `LastLogin`  DATETIME,
    `CreateDate` DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`UserID`) REFERENCES `User`(`UserID`)
);

CREATE TABLE IF NOT EXISTS `Reports`
(
    `ReportID`    INT PRIMARY KEY AUTO_INCREMENT,
    `UserReported` INT NOT NULL,
    `AnsweredBy`  INT,
    `Status`      VARCHAR(50) DEFAULT 'pending',
    `Reason`      TEXT,
    `ReportDate`  DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`UserReported`) REFERENCES `User`(`UserID`)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY (`AnsweredBy`) REFERENCES `User_Admin`(`AdminID`)
        ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS `Reports_Made`
(
    `UserID` INT,
    `ReportID` INT,
    PRIMARY KEY (`UserID`, `ReportID`),
    FOREIGN KEY (`UserID`) REFERENCES `User`(`UserID`)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (`ReportID`) REFERENCES `Reports`(`ReportID`)
        ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS To_Manage
(
    `ReportID` INT,
    `AdminID`  INT,
    PRIMARY KEY (`AdminID`, `ReportID`),
    FOREIGN KEY (`AdminID`) REFERENCES `User_Admin`(`AdminID`)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (`ReportID`) REFERENCES `Reports`(`ReportID`)
        ON UPDATE CASCADE ON DELETE CASCADE
);