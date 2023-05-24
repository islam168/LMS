import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './CorsePage.css'
const BackendDataDisplay = () => {
  const [courseData, setCourseData] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/course_page/1/'); // Replace with your backend API endpoint
        setCourseData(response.data);
      } catch (error) {
        console.error(error);
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
            <div>
            <h1>{courseData.title}</h1>
            <p>{courseData.content}</p>
            {courseData.course_material.map((material) => (
              <div key={material.id}>
                <img src={material.preview} alt={material.name} />
                <p>{material.content}</p>
              </div>
                ))}
            </div>
      </header>
    </div>

  );
};

export default BackendDataDisplay;

