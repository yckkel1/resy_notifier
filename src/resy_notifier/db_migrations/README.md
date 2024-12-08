# Database Migrations

This folder contains SQL scripts for documenting and archiving the database schema and table structures used in the `resy_notifier` project. These scripts are not executed directly by the application but serve as a reference for managing and maintaining the database.

## Folder Contents

1. **`schema.sql`**
    - Defines the schema (`resy`) used in the project.
    - Example:
      ```sql
      CREATE SCHEMA IF NOT EXISTS resy;
      ```

2. **`table.sql`**
    - Defines the structure of the `api_keys` table, used to store API keys.
    - Includes the `migrations` table for tracking database changes (optional future feature).
    - Example:
      ```sql
      CREATE TABLE IF NOT EXISTS resy.api_keys (
          id INT AUTO_INCREMENT PRIMARY KEY,
          key VARCHAR(255) NOT NULL,
          effective_date DATETIME NOT NULL,
          terminated_date DATETIME NULL,
          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      );
      ```

## Purpose

These files provide:
- **Documentation**: Archive the database schema and table definitions for reference.
- **Future Use**: Serve as a foundation for database migrations or updates.
- **Version Control**: Keep track of all changes to the database structure via Git.

## Usage

1. **Creating or Updating the Database**:
    - Use a database management tool like DbVisualizer to execute the SQL scripts.

2. **Steps**:
    - Open `schema.sql` in DbVisualizer or your MySQL client to create the schema.
    - Execute `table.sql` to create or update the `api_keys` table.

3. **Maintaining Updates**:
    - For new changes, update `data.sql`.

## Notes

- **Execution**:
    - These files are not executed programmatically in Python. All SQL queries run via DbVisualizer or your preferred MySQL client.
- **Case Sensitivity**:
    - On Windows, MySQL table names are case-insensitive by default. Refer to MySQL documentation if you require case-sensitive table names.
