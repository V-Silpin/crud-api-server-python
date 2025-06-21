import Inputpanel from './components/Inputpanel';
import Table from './components/Table';
import { useState, useEffect } from 'react';
import './App.css';
import { fetchCourses, createCourse, updateCourse, deleteCourse } from './api';

function App() {
  const [courses, setCourses] = useState([]);
  const [selectedAction, setSelectedAction] = useState('Read');
  const [selectedCourse, setSelectedCourse] = useState(null);
  const [refresh, setRefresh] = useState(false);

  // Fetch courses on mount and when refresh changes
  useEffect(() => {
    fetchCourses().then(setCourses);
  }, [refresh]);

  // Handler for input panel submit
  const handleSubmit = async (form) => {
    try {
      if (selectedAction === 'Create') {
        await createCourse(form);
      } else if (selectedAction === 'Update') {
        await updateCourse(form.id, form);
      } else if (selectedAction === 'Delete') {
        await deleteCourse(form.id);
      }
      setRefresh((r) => !r); // trigger refresh
    } catch (e) {
      alert('Operation failed: ' + e.message);
    }
  };

  return (
    <>
      {/* App Title */}
      <div className="w-full flex justify-center mb-8 mt-6">
        <h1 className="text-5xl font-extrabold text-blue-700 drop-shadow-lg tracking-wide">ZA CRUD</h1>
      </div>
      <div className="grid grid-cols-3 h-screen bg-gray-100 p-4">
        {/* Action Buttons */}
        <div className="col-span-1 flex flex-col items-center justify-center gap-8">
          {['Create', 'Read', 'Update', 'Delete'].map((action) => {
            const colorMap = {
              Create: 'bg-green-300 text-white border-green-700 hover:bg-green-600',
              Read: 'bg-blue-300 text-white border-blue-700 hover:bg-blue-600',
              Update: 'bg-yellow-300 text-white border-yellow-600 hover:bg-yellow-500',
              Delete: 'bg-red-300 text-white border-red-700 hover:bg-red-600',
            };
            const selectedColor = colorMap[action] + ' scale-105';
            const defaultColor = colorMap[action].replace('bg-', 'bg-opacity-10 bg-').replace('text-white', 'text-' + colorMap[action].split('-')[1] + '-700');
            return (
              <button
                key={action}
                className={`w-48 h-20 text-2xl rounded-3xl font-bold shadow-lg transition-all duration-200 border-4 ${selectedAction === action ? selectedColor : defaultColor}`}
                onClick={() => setSelectedAction(action)}
              >
                {action} Button
              </button>
          );
        })}
        </div>

        {/* Table and Input Panel */}
        <div className='col-span-2 flex flex-col gap-4'>
          <div className="mb-6">
            <Table courses={courses} />
          </div>

          {/* Input panel */}
          <div>
            <Inputpanel onSubmit={handleSubmit} action={selectedAction} course={selectedCourse} />
          </div>
        </div>
      </div>
    </>
  );
}

export default App;
