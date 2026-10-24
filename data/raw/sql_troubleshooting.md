# SQL Troubleshooting Guide

## Primary Key and Foreign Key Errors
A primary key uniquely identifies each row in a table and cannot contain duplicate or NULL values. A foreign key references a key in another table and enforces referential integrity. Before inserting a child record, verify that the referenced parent record exists.

## JOIN Operations
INNER JOIN returns matching rows from both tables. LEFT JOIN returns every row from the left table and matching rows from the right table. If a query produces duplicate rows, check whether the join columns contain multiple matches.

## NULL Values
SQL NULL represents missing or unknown information. Use IS NULL or IS NOT NULL to test for NULL values. Comparisons such as column = NULL do not work as expected. COALESCE can replace NULL with a fallback value.

## Query Performance
Avoid selecting unnecessary columns. Use indexes on frequently filtered or joined columns when appropriate. Use EXPLAIN to inspect a query execution plan before optimizing a slow query.
