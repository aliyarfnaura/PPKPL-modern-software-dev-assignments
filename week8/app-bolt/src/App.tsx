import { useState } from 'react';
import { TaskList } from './components/TaskList';
import { CreateTask } from './components/CreateTask';
import { EditTask } from './components/EditTask';

type View =
  | { type: 'list' }
  | { type: 'create' }
  | { type: 'edit'; taskId: string };

function App() {
  const [view, setView] = useState<View>({ type: 'list' });

  const handleBackToList = () => {
    setView({ type: 'list' });
  };

  const handleCreateTask = () => {
    setView({ type: 'create' });
  };

  const handleEditTask = (taskId: string) => {
    setView({ type: 'edit', taskId });
  };

  if (view.type === 'create') {
    return (
      <CreateTask
        onBack={handleBackToList}
        onSuccess={handleBackToList}
      />
    );
  }

  if (view.type === 'edit') {
    return (
      <EditTask
        taskId={view.taskId}
        onBack={handleBackToList}
        onSuccess={handleBackToList}
      />
    );
  }

  return (
    <TaskList
      onCreateTask={handleCreateTask}
      onEditTask={handleEditTask}
    />
  );
}

export default App;
