USE [master];
GO

CREATE DATABASE [my_library]
go

CREATE LOGIN [library_user]
WITH PASSWORD = N'pass123', -- LOGIN PASSWORD
CHECK_EXPIRATION = OFF,
CHECK_POLICY = OFF;
GO

USE [my_library];
GO

CREATE USER [library_user] FOR LOGIN [library_user];
GO

ALTER ROLE [db_datareader] ADD MEMBER [library_user];
ALTER ROLE [db_datawriter] ADD MEMBER [library_user];
GO