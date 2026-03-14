import fs from "fs";
import path from "path";

const filePath = path.join(process.cwd(), "data", "tasks.json");

function readTasks() {
  try {
    const data = fs.readFileSync(filePath, "utf-8");
    return data ? JSON.parse(data) : [];
  } catch {
    return [];
  }
}

function writeTasks(tasks: any[]) {
  fs.writeFileSync(filePath, JSON.stringify(tasks, null, 2));
}

export async function PUT(
  req: Request,
  context: { params: Promise<{ id: string }> }
) {
  const { id } = await context.params;
  const body = await req.json();

  const tasks = readTasks();

  const index = tasks.findIndex((t: any) => String(t.id) === id);

  if (index === -1) {
    return Response.json({ error: "Task not found" }, { status: 404 });
  }

  tasks[index] = {
    ...tasks[index],
    title: body.title,
    description: body.description,
  };

  writeTasks(tasks);

  return Response.json(tasks[index]);
}

export async function DELETE(
  req: Request,
  context: { params: Promise<{ id: string }> }
) {
  const { id } = await context.params;

  const tasks = readTasks();

  const newTasks = tasks.filter((t: any) => String(t.id) !== id);

  writeTasks(newTasks);

  return Response.json({ message: "Task deleted" });
}