const API = "http://127.0.0.1:5000/tasks";

async function loadTasks() {

    const res = await fetch(API);
    const tasks = await res.json();

    const list = document.getElementById("taskList");
    list.innerHTML = "";

    tasks.forEach(task => {

        const li = document.createElement("li");

        li.innerHTML = `
        <strong>${task.title}</strong>
        <p>${task.description || ""}</p>
        <span>Status: ${task.status}</span>
        `;

        // EDIT BUTTON
        const edit = document.createElement("button");
        edit.innerText = "Edit";
        edit.onclick = () => editTask(task);

        // DELETE BUTTON
        const del = document.createElement("button");
        del.innerText = "Delete";
        del.onclick = () => deleteTask(task.id);

        // COMPLETE BUTTON
        const complete = document.createElement("button");
        complete.innerText = "Complete";
        complete.onclick = () => completeTask(task.id);

        li.appendChild(edit);
        li.appendChild(complete);
        li.appendChild(del);

        list.appendChild(li);
    });

}

async function addTask(){

    const title = document.getElementById("title").value;
    const description = document.getElementById("description").value;

    if(!title){
        alert("Title is required");
        return;
    }

    await fetch(API,{
        method:"POST",
        headers:{
            "Content-Type":"application/json"
        },
        body:JSON.stringify({
            title,
            description
        })
    });

    document.getElementById("title").value = "";
    document.getElementById("description").value = "";

    loadTasks();
}

async function editTask(task){

    const newTitle = prompt("Edit title:", task.title);
    const newDescription = prompt("Edit description:", task.description);

    if(!newTitle){
        alert("Title cannot be empty");
        return;
    }

    await fetch(`${API}/${task.id}`,{
        method:"PUT",
        headers:{
            "Content-Type":"application/json"
        },
        body:JSON.stringify({
            title:newTitle,
            description:newDescription
        })
    });

    loadTasks();
}

async function completeTask(id){

    await fetch(`${API}/${id}`,{
        method:"PUT",
        headers:{
            "Content-Type":"application/json"
        },
        body:JSON.stringify({
            status:"completed"
        })
    });

    loadTasks();
}

async function deleteTask(id){

    await fetch(`${API}/${id}`,{
        method:"DELETE"
    });

    loadTasks();
}

loadTasks();