// api.js
// Functions to interact with the backend API for CRUD operations

const BASE_URL = 'http://localhost:8000/items/';

export async function fetchCourses() {
  try {
    const response = await fetch(BASE_URL);
    if (!response.ok) {
      throw new Error('Failed to fetch courses');
    }
    return await response.json();
  } catch (error) {
    console.error('Error fetching courses:', error);
    return [];
  }
}

export async function createCourse(course) {
  try {
    const response = await fetch(BASE_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(course),
    });
    if (!response.ok) {
      throw new Error('Failed to create course');
    }
    return await response.json();
  } catch (error) {
    console.error('Error creating course:', error);
    throw error;
  }
}

export async function updateCourse(id, course) {
  try {
    const response = await fetch(`${BASE_URL}${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(course),
    });
    if (!response.ok) {
      throw new Error('Failed to update course');
    }
    return await response.json();
  } catch (error) {
    console.error('Error updating course:', error);
    throw error;
  }
}

export async function deleteCourse(id) {
  try {
    const response = await fetch(`${BASE_URL}${id}`, {
      method: 'DELETE',
    });
    if (!response.ok) {
      throw new Error('Failed to delete course');
    }
    return await response.json();
  } catch (error) {
    console.error('Error deleting course:', error);
    throw error;
  }
}
