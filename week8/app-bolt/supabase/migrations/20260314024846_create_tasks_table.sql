/*
  # Create tasks table

  1. New Tables
    - `tasks`
      - `id` (uuid, primary key) - Unique identifier for each task
      - `title` (text) - Task title/name
      - `description` (text) - Detailed description of the task
      - `status` (text) - Current status (todo, in_progress, completed)
      - `created_at` (timestamptz) - When the task was created

  2. Security
    - Enable RLS on `tasks` table
    - Add policies for public access (select, insert, update, delete)
    
  3. Notes
    - Status field uses text with check constraint to ensure valid values
    - All fields except description are required
    - Created_at automatically set to current timestamp
*/

CREATE TABLE IF NOT EXISTS tasks (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  title text NOT NULL,
  description text DEFAULT '',
  status text NOT NULL DEFAULT 'todo' CHECK (status IN ('todo', 'in_progress', 'completed')),
  created_at timestamptz DEFAULT now() NOT NULL
);

ALTER TABLE tasks ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Anyone can view tasks"
  ON tasks FOR SELECT
  USING (true);

CREATE POLICY "Anyone can insert tasks"
  ON tasks FOR INSERT
  WITH CHECK (true);

CREATE POLICY "Anyone can update tasks"
  ON tasks FOR UPDATE
  USING (true)
  WITH CHECK (true);

CREATE POLICY "Anyone can delete tasks"
  ON tasks FOR DELETE
  USING (true);