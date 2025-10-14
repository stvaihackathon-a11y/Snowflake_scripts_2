--liquibase formatted sql
--changeset vyas:002-create-customer-table
--comment: Create CUSTOMER table for storing customer information

CREATE TABLE CUSTOMER (
    CUSTOMER_ID  NUMBER(10,0) PRIMARY KEY,
    FIRST_NAME   VARCHAR(50) NOT NULL,
    LAST_NAME    VARCHAR(50),
    EMAIL        VARCHAR(100) UNIQUE,
    PHONE        VARCHAR(20),
    CREATED_AT   TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP
);

--rollback DROP TABLE IF EXISTS CUSTOMER;
