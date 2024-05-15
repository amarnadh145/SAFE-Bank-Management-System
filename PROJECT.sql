
CREATE TABLE das_account (
    a_number BIGINT PRIMARY KEY NOT NULL COMMENT 'ACCOUNT NUMBER',
    a_name   VARCHAR(20) NOT NULL COMMENT 'ACCOUNT NAME',
    a_date   DATETIME NOT NULL COMMENT 'ACCOUNT OPENING DATE',
    a_type   VARCHAR(2) NOT NULL COMMENT 'TYPE OF THE ACCOUNT',
    cust_id  BIGINT NOT NULL
);
ALTER TABLE das_account
    ADD CONSTRAINT ch_inh_das_account CHECK ( a_type IN ( 'C', 'L', 'S') );

CREATE TABLE das_check (
    a_number  BIGINT PRIMARY KEY NOT NULL COMMENT 'ACCOUNT NUMBER',
    c_scharge DECIMAL(7, 2) NOT NULL COMMENT 'SERVICE CHARGE OF CHECKING ACCOUNT'
);


CREATE TABLE das_cust (
    cust_id       BIGINT PRIMARY KEY AUTO_INCREMENT NOT NULL COMMENT 'CUSTOMER IDENTIFICATION NUMBER',
    cust_fname    VARCHAR(30) NOT NULL COMMENT 'CUSTOMER''S FIRST NAME',
    cust_lname    VARCHAR(30) NOT NULL COMMENT 'CUSTOMER LAST NAME',
    cust_email    VARCHAR(30) NOT NULL COMMENT 'CUSTOMER EMAIL ADDRESS',
    cust_password VARCHAR(70) NOT NULL COMMENT 'CUSTOMER PASSWORD',
    cust_street   VARCHAR(30) NOT NULL COMMENT 'CUSTOMER STREET NAME',
    cust_city     VARCHAR(30) NOT NULL COMMENT 'CUSTOMER CITY NAME',
    cust_state    VARCHAR(30) NOT NULL COMMENT 'CUSTOMER STATE NAME',
    cust_country  VARCHAR(30) NOT NULL COMMENT 'CUSTOMER COUNTRY NAME',
    cust_zip      BIGINT NOT NULL COMMENT 'CUSTOMER ZIP CODE'
);


CREATE TABLE das_home (
    a_number    BIGINT PRIMARY KEY NOT NULL COMMENT 'ACCOUNT NUMBER',
    h_builtyear DATETIME NOT NULL COMMENT 'BUILT DATE OF HOME',
    h_iacnumber BIGINT NOT NULL COMMENT 'INSURANCE ACCOUNT NUMBER OF HOME',
    h_iname     VARCHAR(30) NOT NULL COMMENT 'INSURANCE COMPANY NAME OF HOME',
    h_iprem     DECIMAL(7, 2) NOT NULL COMMENT 'MONTHLY INSURANCE PREMIUM OF HOME',
    h_istreet   VARCHAR(30) NOT NULL COMMENT 'INSURANCE COMPANY STREET NAME', 
    h_icity     VARCHAR(30) NOT NULL COMMENT 'INSURANCE COMPANY CITY NAME', 
    h_istate    VARCHAR(30) NOT NULL COMMENT 'INSURANCE COMPANY STATE NAME', 
    h_izip      VARCHAR(30) NOT NULL COMMENT 'INSURANCE COMPANY ZIP CODE'
);


CREATE TABLE das_loan (
    a_number   BIGINT PRIMARY KEY NOT NULL COMMENT 'ACCOUNT NUMBER',
    l_lrate    DECIMAL(3, 2) NOT NULL COMMENT 'LOAN RATE OF ACCOUNT',
    l_lamount  DECIMAL(7, 2) NOT NULL COMMENT 'TOTAL LOAN AMOUNT ',
    l_lmonths  INT NOT NULL COMMENT 'DURATION OF THE LOAN IN MONTHS',
    l_lpayment DECIMAL(7, 2) NOT NULL COMMENT 'MONTHLY PAYMENT OF LOAN',
    l_type     CHAR(2) NOT NULL COMMENT 'TYPE OF LOAN ACCOUNT'
);

ALTER TABLE das_loan
    ADD CONSTRAINT ch_inh_das_loan CHECK ( l_type IN ( 'H', 'ST' ) );



CREATE TABLE das_savings (
    a_number BIGINT PRIMARY KEY NOT NULL COMMENT 'ACCOUNT NUMBER',
    s_irate  DECIMAL(3, 2) NOT NULL COMMENT 'INTEREST RATE OF SAVINGS ACCOUNT'
);


CREATE TABLE das_student (
    a_number     BIGINT PRIMARY KEY NOT NULL COMMENT 'ACCOUNT NUMBER',
    s_id         BIGINT NOT NULL COMMENT 'STUDENT IDENTIFICATION NUMBER',
    s_status     VARCHAR(30) NOT NULL COMMENT 'GRAD OR UNDER GRAD STATUS OF THE STUDENT',
    s_exgraddate DATETIME NOT NULL COMMENT 'EXPECTED GRADUATION DATE OF THE STUDENT',
    univ_id      INT NOT NULL
);


CREATE TABLE das_univ (
    univ_id   INT PRIMARY KEY AUTO_INCREMENT NOT NULL COMMENT 'UNIVERSITY ID NUMBER',
    univ_name VARCHAR(30) NOT NULL COMMENT 'UNIVERSITY NAME'
);



ALTER TABLE das_account
    ADD CONSTRAINT das_account_das_cust_fk FOREIGN KEY ( cust_id )
        REFERENCES das_cust ( cust_id );

ALTER TABLE das_check
    ADD CONSTRAINT das_check_das_account_fk FOREIGN KEY ( a_number )
        REFERENCES das_account ( a_number );

ALTER TABLE das_home
    ADD CONSTRAINT das_home_das_loan_fk FOREIGN KEY ( a_number )
        REFERENCES das_loan ( a_number );

ALTER TABLE das_loan
    ADD CONSTRAINT das_loan_das_account_fk FOREIGN KEY ( a_number )
        REFERENCES das_account ( a_number );

ALTER TABLE das_savings
    ADD CONSTRAINT das_savings_das_account_fk FOREIGN KEY ( a_number )
        REFERENCES das_account ( a_number );

ALTER TABLE das_student
    ADD CONSTRAINT das_student_das_loan_fk FOREIGN KEY ( a_number )
        REFERENCES das_loan ( a_number );

ALTER TABLE das_student
    ADD CONSTRAINT das_student_das_univ_fk FOREIGN KEY ( univ_id )
        REFERENCES das_univ ( univ_id );

CREATE TABLE das_employee (
    emp_mail     VARCHAR(30) PRIMARY KEY NOT NULL COMMENT 'EMPLOYEE EMAIL ADDRESS',
    emp_password VARCHAR(70) NOT NULL COMMENT 'EMPLOYEE PASSWORD'
);

-- SQLINES LICENSE FOR EVALUATION USE ONLY
DROP TRIGGER IF EXISTS arc_fkarc_9_das_check;

DELIMITER //

CREATE TRIGGER arc_fkarc_9_das_check BEFORE
    INSERT ON das_check
    FOR EACH ROW
BEGIN
DECLARE d VARCHAR(2);
    SELECT
        a.a_type
    INTO d
    FROM
        das_account a
    WHERE
        a.a_number = new.a_number;

    IF ( d IS NULL OR d <> 'C' ) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'FK DAS_CHECK_DAS_ACCOUNT_FK in Table DAS_CHECK violates Arc constraint on Table DAS_ACCOUNT - discriminator column A_TYPE doesn''t have value ''C''';
    END IF;
END;
//
DELIMITER ;
DELIMITER //

CREATE TRIGGER arc_fkarc_9_das_check BEFORE
    UPDATE ON das_check
    FOR EACH ROW
BEGIN
DECLARE d VARCHAR(2);
    SELECT
        a.a_type
    INTO d
    FROM
        das_account a
    WHERE
        a.a_number = new.a_number;

    IF ( d IS NULL OR d <> 'C' ) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'FK DAS_CHECK_DAS_ACCOUNT_FK in Table DAS_CHECK violates Arc constraint on Table DAS_ACCOUNT - discriminator column A_TYPE doesn''t have value ''C''';
    END IF;
END;
//
DELIMITER ;




-- SQLINES LICENSE FOR EVALUATION USE ONLY
DROP TRIGGER IF EXISTS arc_fkarc_9_das_savings;

DELIMITER //
CREATE TRIGGER arc_fkarc_9_das_savings BEFORE
    INSERT ON das_savings
    FOR EACH ROW
BEGIN
DECLARE d VARCHAR(2);
    SELECT
        a.a_type
    INTO d
    FROM
        das_account a
    WHERE
        a.a_number = new.a_number;

    IF ( d IS NULL OR d <> 'S' ) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT ='FK DAS_SAVINGS_DAS_ACCOUNT_FK in Table DAS_SAVINGS violates Arc constraint on Table DAS_ACCOUNT - discriminator column A_TYPE doesn''t have value ''S''';
    END IF;
END;
//
DELIMITER ;
DELIMITER //
CREATE TRIGGER arc_fkarc_9_das_savings BEFORE
    UPDATE ON das_savings
    FOR EACH ROW
BEGIN
DECLARE d VARCHAR(2);
    SELECT
        a.a_type
    INTO d
    FROM
        das_account a
    WHERE
        a.a_number = new.a_number;

    IF ( d IS NULL OR d <> 'S' ) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT ='FK DAS_SAVINGS_DAS_ACCOUNT_FK in Table DAS_SAVINGS violates Arc constraint on Table DAS_ACCOUNT - discriminator column A_TYPE doesn''t have value ''S''';
    END IF;
END;
//
DELIMITER ;



-- SQLINES LICENSE FOR EVALUATION USE ONLY
DROP TRIGGER IF EXISTS arc_fkarc_9_das_loan;

DELIMITER //
CREATE TRIGGER arc_fkarc_9_das_loan BEFORE
    INSERT ON das_loan
    FOR EACH ROW
BEGIN
DECLARE d VARCHAR(2);
    SELECT
        a.a_type
    INTO d
    FROM
        das_account a
    WHERE
        a.a_number = new.a_number;

    IF ( d IS NULL OR d <> 'L' ) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT ='FK DAS_LOAN_DAS_ACCOUNT_FK in Table DAS_LOAN violates Arc constraint on Table DAS_ACCOUNT - discriminator column A_TYPE doesn''t have value ''L''';
    END IF;
END;
//
DELIMITER ;
DELIMITER //
CREATE TRIGGER arc_fkarc_9_das_loan BEFORE
    UPDATE ON das_loan
    FOR EACH ROW
BEGIN
DECLARE d VARCHAR(2);
    SELECT
        a.a_type
    INTO d
    FROM
        das_account a
    WHERE
        a.a_number = new.a_number;

    IF ( d IS NULL OR d <> 'L' ) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT ='FK DAS_LOAN_DAS_ACCOUNT_FK in Table DAS_LOAN violates Arc constraint on Table DAS_ACCOUNT - discriminator column A_TYPE doesn''t have value ''L''';
    END IF;
END;
//
DELIMITER ;



-- SQLINES LICENSE FOR EVALUATION USE ONLY
DROP TRIGGER IF EXISTS arc_fkarc_8_das_home;

DELIMITER //
CREATE TRIGGER arc_fkarc_8_das_home BEFORE
    INSERT ON das_home
    FOR EACH ROW
BEGIN
DECLARE d CHAR(2);
    SELECT
        a.l_type
    INTO d
    FROM
        das_loan a
    WHERE
        a.a_number = new.a_number;

    IF ( d IS NULL OR d <> 'H' ) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT ='FK DAS_HOME_DAS_LOAN_FK in Table DAS_HOME violates Arc constraint on Table DAS_LOAN - discriminator column L_TYPE doesn''t have value ''H''';
    END IF;
END;
//
DELIMITER ;
DELIMITER //
CREATE TRIGGER arc_fkarc_8_das_home BEFORE
    UPDATE ON das_home
    FOR EACH ROW
BEGIN
DECLARE d CHAR(2);
    SELECT
        a.l_type
    INTO d
    FROM
        das_loan a
    WHERE
        a.a_number = new.a_number;

    IF ( d IS NULL OR d <> 'H' ) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT ='FK DAS_HOME_DAS_LOAN_FK in Table DAS_HOME violates Arc constraint on Table DAS_LOAN - discriminator column L_TYPE doesn''t have value ''H''';
    END IF;
END;
//
DELIMITER ;



-- SQLINES LICENSE FOR EVALUATION USE ONLY
DROP TRIGGER IF EXISTS arc_fkarc_8_das_student;

DELIMITER //
CREATE TRIGGER arc_fkarc_8_das_student BEFORE
    INSERT ON das_student
    FOR EACH ROW
BEGIN
DECLARE d CHAR(2);
    SELECT
        a.l_type
    INTO d
    FROM
        das_loan a
    WHERE
        a.a_number = new.a_number;

    IF ( d IS NULL OR d <> 'ST' ) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT ='FK DAS_STUDENT_DAS_LOAN_FK in Table DAS_STUDENT violates Arc constraint on Table DAS_LOAN - discriminator column L_TYPE doesn''t have value ''ST''';
    END IF;
END;
//
DELIMITER ;
DELIMITER //
CREATE TRIGGER arc_fkarc_8_das_student BEFORE
    UPDATE ON das_student
    FOR EACH ROW
BEGIN
DECLARE d CHAR(2);
    SELECT
        a.l_type
    INTO d
    FROM
        das_loan a
    WHERE
        a.a_number = new.a_number;

    IF ( d IS NULL OR d <> 'ST' ) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT ='FK DAS_STUDENT_DAS_LOAN_FK in Table DAS_STUDENT violates Arc constraint on Table DAS_LOAN - discriminator column L_TYPE doesn''t have value ''ST''';
    END IF;
END;
//
DELIMITER ;

DELIMITER //
CREATE PROCEDURE updateCSCharge(IN new_cscharge DECIMAL(5,2))
BEGIN
    UPDATE DAS_CHECK SET C_SCHARGE = new_cscharge;
END//
DELIMITER ;

DELIMITER //
CREATE PROCEDURE updateSIRate(IN new_sirate DECIMAL(5,2))
BEGIN
    UPDATE DAS_SAVINGS SET S_IRATE = new_sirate;
END//
DELIMITER ;

DELIMITER //
CREATE PROCEDURE updateLIRate(IN new_llrate DECIMAL(5,2))
BEGIN
    UPDATE DAS_loan SET L_LRATE = new_llrate;
END//
DELIMITER ;

