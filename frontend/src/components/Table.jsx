import React from 'react';

const Table = ({ courses }) => {
  return (
    <div className="overflow-x-auto">
      <table className="min-w-full bg-white rounded shadow">
        <thead>
          <tr>
            <th className="px-4 py-2 border-b">ID</th>
            <th className="px-4 py-2 border-b">Name</th>
            <th className="px-4 py-2 border-b">Description</th>
            <th className="px-4 py-2 border-b">Price</th>
          </tr>
        </thead>
        <tbody>
          {courses.length === 0 ? (
            <tr>
              <td colSpan="4" className="text-center py-4 text-gray-400">No courses available</td>
            </tr>
          ) : (
            courses.map((course) => (
              <tr key={course.id}>
                <td className="px-4 py-2 border-b">{course.id}</td>
                <td className="px-4 py-2 border-b">{course.name}</td>
                <td className="px-4 py-2 border-b">{course.description}</td>
                <td className="px-4 py-2 border-b">{course.price}</td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
};

export default Table;
