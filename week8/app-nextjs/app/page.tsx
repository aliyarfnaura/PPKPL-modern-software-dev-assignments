"use client";

import { useEffect, useState } from "react";

export default function Home() {
  const [tasks, setTasks] = useState<any[]>([]);
  const [title, setTitle] = useState("");
  const [desc, setDesc] = useState("");

  async function loadTasks() {
    try {
      const res = await fetch("/api/tasks");
      const data = await res.json();
      setTasks(data);
    } catch (err) {
      console.error("Failed to load tasks", err);
    }
  }

  async function addTask() {
    if (!title.trim()) {
      alert("Title required");
      return;
    }

    try {
      await fetch("/api/tasks", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          title: title,
          description: desc,
        }),
      });

      setTitle("");
      setDesc("");

      loadTasks();
    } catch (err) {
      console.error("Error adding task", err);
    }
  }

  async function deleteTask(id: number) {
    try {
      await fetch(`/api/tasks/${id}`, {
        method: "DELETE",
      });

      loadTasks();
    } catch (err) {
      console.error("Delete failed", err);
    }
  }

  async function editTask(task: any) {
    const newTitle = prompt("Edit title", task.title);
    const newDesc = prompt("Edit description", task.description);

    if (newTitle === null) return;

    try {
      await fetch(`/api/tasks/${task.id}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          title: newTitle,
          description: newDesc,
        }),
      });

      loadTasks();
    } catch (err) {
      console.error("Edit failed", err);
    }
  }

  useEffect(() => {
    loadTasks();
  }, []);

  return (
    <div className="container">
      <h1>Next.js Task Manager</h1>

      <div className="form">
        <input
          placeholder="Task title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
        />

        <input
          placeholder="Description"
          value={desc}
          onChange={(e) => setDesc(e.target.value)}
        />

        <button onClick={addTask}>Add Task</button>
      </div>

      {tasks.map((task) => (
        <div key={task.id} className="task">
          <b>{task.title}</b>
          <p>{task.description}</p>

          <div className="task-buttons">
            <button onClick={() => editTask(task)}>Edit</button>
            <button onClick={() => deleteTask(task.id)}>Delete</button>
          </div>
        </div>
      ))}
    </div>
  );
}