import fs from "fs";
import path from "path";

const filePath = path.join(process.cwd(), "data", "tasks.json");

function readTasks() {
  const data = fs.readFileSync(filePath, "utf-8");
  return JSON.parse(data);
}

function writeTasks(tasks: any) {
  fs.writeFileSync(filePath, JSON.stringify(tasks, null, 2));
}

export async function GET() {
  const tasks = readTasks();
  return Response.json(tasks);
}

export async function POST(req: Request) {
  const tasks = readTasks();
  const body = await req.json();

  if (!body.title) {
    return Response.json({ error: "Title required" }, { status: 400 });
  }

  const newTask = {
    id: Date.now(),
    title: body.title,
    description: body.description || "",
  };

  tasks.push(newTask);
  writeTasks(tasks);

  return Response.json(newTask);
}