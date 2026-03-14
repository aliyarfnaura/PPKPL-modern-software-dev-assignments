# Week 8 Write-up
Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## Instructions

Fill out all of the `TODO`s in this file.

## Submission Details

Name: **Aliya Raffa Naura Ayu** \
SUNet ID: **N/A** \
Citations: **AI tools used for assistance: Bolt AI**

This assignment took me about **3 hours** hours to do. 


## App Concept 
```
The application built for this assignment is a Task Manager designed to help users manage simple daily tasks. The application allows users to create, view, update, and delete tasks through a simple and intuitive interface.

The main goal of the app is to provide a minimal yet functional productivity tool that demonstrates core web application concepts such as CRUD operations, persistence, basic validation, and frontend–backend interaction.

Across all three implementations, the core features remain the same:
- Create a new task with a title and description
- View a list of existing tasks
- Edit tasks when updates are needed
- Delete tasks that are no longer relevant
- Display tasks in a clean and simple UI

Each version of the application uses a different technology stack to explore how modern development tools and frameworks approach building similar functionality.
```


## Version #1 Description
```
APP DETAILS:
===============
Folder name: app-flask
AI app generation platform: None
Tech Stack: Flask + Python + Vanilla JavaScript + HTML/CSS
Persistence: SQLite database
Frameworks/Libraries Used: 
- Flask
- Flask-CORS
- SQLAlchemy
- Vanilla JavaScript
- HTML / CSS

(Optional but recommended) Screenshots of core flows:
Task list view, create task form, edit task, and delete task interactions.

REFLECTIONS:
===============
a. Issues encountered per stack and how you resolved them: 
The Flask version required setting up the backend API manually, including defining database models and implementing REST endpoints for CRUD operations. One challenge was ensuring that the frontend JavaScript correctly communicated with the Flask backend using fetch requests.

Another issue involved configuring the database connection and initializing the SQLite database using SQLAlchemy. This was resolved by properly setting the database URI and ensuring the database tables were created during application startup.

b. Prompting (e.g. what required additional guidance; what worked poorly/wel): 
The Flask version required setting up the backend API manually, including defining database models and implementing REST endpoints for CRUD operations. One challenge was ensuring that the frontend JavaScript correctly communicated with the Flask backend using fetch requests.

Another issue involved configuring the database connection and initializing the SQLite database using SQLAlchemy. This was resolved by properly setting the database URI and ensuring the database tables were created during application startup.

c. Approximate time-to-first-run and time-to-feature metrics:
Since this version was mostly implemented manually, prompting was not heavily used. However, AI tools such as Warp helped accelerate development by assisting with debugging and suggesting improvements for API structure and error handling.

The AI suggestions were especially helpful for organizing the Flask routes and improving validation logic.
```

## Version #2 Description
```
APP DETAILS:
===============
Folder name: app-nextjs
AI app generation platform: None
Tech Stack: Next.js + React + Node.js
Persistence: JSON file-based storage
Frameworks/Libraries Used: 
- Next.js (App Router)
- React
- Node.js
- CSS modules / global CSS

(Optional but recommended) Screenshots of core flows:
Task list interface, create task form, edit modal/prompt, delete button functionality.

REFLECTIONS:
===============
a. Issues encountered per stack and how you resolved them: 
The main challenge in the Next.js implementation involved correctly implementing API routes using the App Router structure. Handling dynamic route parameters for editing and deleting tasks required adjusting the API route configuration.

Another issue involved parsing JSON data from the file-based storage. If the JSON file was empty, the application would throw parsing errors. This was resolved by adding safe error handling to return an empty array when no tasks were stored.

b. Prompting (e.g. what required additional guidance; what worked poorly/wel): 
The main challenge in the Next.js implementation involved correctly implementing API routes using the App Router structure. Handling dynamic route parameters for editing and deleting tasks required adjusting the API route configuration.

Another issue involved parsing JSON data from the file-based storage. If the JSON file was empty, the application would throw parsing errors. This was resolved by adding safe error handling to return an empty array when no tasks were stored.

c. Approximate time-to-first-run and time-to-feature metrics: 
AI tools were helpful for generating example CRUD endpoints and improving the React component logic. Prompting worked well for generating boilerplate code for API routes and state management in React.

However, some generated solutions required manual adjustments to match the Next.js App Router architecture.
```

## Version #3 Description
```
APP DETAILS:
===============
Folder name: app-bolt
AI app generation platform: Bolt.new
Tech Stack: React + Vite + Tailwind CSS
Persistence: Originally designed to use Supabase, but for local execution the application runs with local state.
Frameworks/Libraries Used: 
- React
- Vite
- Tailwind CSS
- Bolt AI App Generator

(Optional but recommended) Screenshots of core flows:
Dashboard UI, create task button, task list view, and edit/delete interactions.

REFLECTIONS:
===============
a. Issues encountered per stack and how you resolved them
The Bolt-generated application initially expected a Supabase backend configuration. When running the application locally, this caused fetch errors because the required environment variables and backend services were not configured.

This issue was resolved by providing placeholder environment variables and adjusting the application to run locally without requiring a live Supabase connection.

Another issue involved exporting the generated code from Bolt, since the platform does not directly provide a download button. The project was exported via GitHub and then integrated into the assignment folder structure.

b. Prompting (e.g. what required additional guidance; what worked poorly/wel): 
The Bolt-generated application initially expected a Supabase backend configuration. When running the application locally, this caused fetch errors because the required environment variables and backend services were not configured.

This issue was resolved by providing placeholder environment variables and adjusting the application to run locally without requiring a live Supabase connection.

Another issue involved exporting the generated code from Bolt, since the platform does not directly provide a download button. The project was exported via GitHub and then integrated into the assignment folder structure.

c. Approximate time-to-first-run and time-to-feature metrics: 
Bolt worked very well for quickly generating a complete UI and project structure from a simple prompt. The initial prompt describing a task manager application produced a functional interface with task creation and editing flows.

However, some additional adjustments were required to ensure the application could run locally without relying on external services such as Supabase.

Overall, prompting was effective for generating the initial application structure but still required developer intervention for configuration and debugging.
```
