import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './CorsePage.css';

const BackendDataDisplay = () => {
  const [courseData, setCourseData] = useState(null);
  const [updatedTitle, setUpdatedTitle] = useState('');
  const [updatedContent, setUpdatedContent] = useState('');

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:8000/api/course/1/'); // Замените на свой API-эндпоинт
      setCourseData(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  const handleButtonClick = async () => {
    try {
      const updatedData = {
        title: updatedTitle,
        content: updatedContent,
      };

      const response = await axios.put('http://127.0.0.1:8000/api/course/1/', updatedData); // Замените на свой API-эндпоинт и данные
      setCourseData(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  if (!courseData) {
    return <div>Loading...</div>;
  }

  return (
    <div className="CoursePage">
      <header className="CoursePage-header">
        <div>
          <h1>{courseData.title}</h1>
          <input
            type="text"
            value={updatedTitle}
            onChange={(e) => setUpdatedTitle(e.target.value)}
          />
          <p>{courseData.content}</p>
          <textarea
            value={updatedContent}
            onChange={(e) => setUpdatedContent(e.target.value)}
          ></textarea>
          <div key={courseData.category.id}>
            <h3>{courseData.category.category_name}</h3>
          </div>
          <h3>{courseData.price}</h3>
        </div>
        <button onClick={handleButtonClick}>Send Data</button>
      </header>
    </div>
  );
};

export default BackendDataDisplay;
