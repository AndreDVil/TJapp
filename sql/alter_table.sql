/* Alter table to include is_deleted to enable soft deleting */

ALTER TABLE trades ADD COLUMN is_deleted BOOLEAN DEFAULT FALSE;
