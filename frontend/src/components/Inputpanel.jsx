import React, { useState } from 'react';

const Inputpanel = ({ onSubmit, action, course }) => {
  const [form, setForm] = useState({
    id: '',
    name: '',
    description: '',
    price: ''
  });

  React.useEffect(() => {
    if (course) {
      setForm(course);
    }
  }, [course]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (onSubmit) onSubmit(form);
  };

  // Color map for button
  const colorMap = {
    Create: 'bg-green-300 text-white border-green-700 hover:bg-green-600',
    Read: 'bg-blue-300 text-white border-blue-700 hover:bg-blue-600',
    Update: 'bg-yellow-300 text-white border-yellow-600 hover:bg-yellow-500',
    Delete: 'bg-red-300 text-white border-red-700 hover:bg-red-600',
  };
  const btnColor = colorMap[action] || 'bg-blue-300 text-white border-blue-700 hover:bg-blue-600';

  return (
    <div className="bg-white p-6 rounded shadow w-full max-w-lg mx-auto">
      <h2 className="text-xl font-bold mb-4">Course Input Panel</h2>
      <form className="flex flex-col gap-4" onSubmit={handleSubmit}>
        <input
          type="number"
          name="id"
          value={form.id}
          onChange={handleChange}
          placeholder="ID"
          className="border rounded px-3 py-2"
        />
        <input
          type="text"
          name="name"
          value={form.name}
          onChange={handleChange}
          placeholder="Name"
          className="border rounded px-3 py-2"
        />
        <input
          type="text"
          name="description"
          value={form.description}
          onChange={handleChange}
          placeholder="Description"
          className="border rounded px-3 py-2"
        />
        <input
          type="number"
          name="price"
          value={form.price}
          onChange={handleChange}
          placeholder="Price"
          className="border rounded px-3 py-2"
        />
        <button
          type="submit"
          className={`mt-2 text-2xl rounded-3xl font-bold shadow-lg transition-all duration-200 border-4 h-16 ${btnColor}`}
        >
          {action || 'Submit'}
        </button>
      </form>
    </div>
  );
};

export default Inputpanel;
