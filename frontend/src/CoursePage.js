import React, { useEffect, useState } from 'react';
import './CoursePage.css';
import axios from 'axios';


const BackendDataDisplay = () => {
  const [courseData, setCourseData] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const { data: response } = await axios.get('http://127.0.0.1:8000/api/course_list/');
        setCourseData(response);
      } catch (error) {
        console.error(error.message);
      }
    };

    fetchData();
  }, []);

  if (!courseData) {
    return <div>Loading...</div>;
  }

  return (
    <div className="CoursePage">
      <header className="CoursePage-header">
        {courseData.map((course) => (
          <div className="CourseCards" key={course.id}>
            <h3>Название курса: {course.title}</h3>
            <div>
              <p>Категория: {course.category.category_name}</p>
            </div>
            <p>Описание: {course.content}</p>
            <p>Цена: {course.price}</p>
            <p>ID: {course.id}</p>
          </div>
        ))}
      </header>
    </div>
  );
};

export default BackendDataDisplay;
