--liquibase formatted sql
--changeset vyas:001-create-department-table
--comment: Create DEPARTMENT table for storing department details

CREATE TABLE DEPARTMENT (
    DEPT_ID      NUMBER(10,0) PRIMARY KEY,
    DEPT_NAME    VARCHAR(100) NOT NULL UNIQUE,
    LOCATION     VARCHAR(100)
);

--rollback DROP TABLE IF EXISTS DEPARTMENT;
