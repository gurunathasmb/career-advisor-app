import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [file, setFile] = useState(null);
  const [skills, setSkills] = useState([]);
  const [jobs, setJobs] = useState([]);

  const handleUpload = async () => {
    const formData = new FormData();
    formData.append('resume', file);
    const res = await axios.post('http://localhost:5000/api/resume/upload', formData);
    setSkills(res.data.skills);
    const rec = await axios.post('http://localhost:5000/api/recommend', { skills: res.data.skills });
    setJobs(rec.data.recommendedJobs);
  };

  return (
    <div className="p-4">
      <h1 className="text-2xl mb-4">Career Advisor</h1>
      <input type="file" onChange={e => setFile(e.target.files[0])} />
      <button onClick={handleUpload} className="ml-2 p-2 bg-blue-500 text-white">Upload</button>
      <div className="mt-4">
        <h2 className="text-xl">Extracted Skills:</h2>
        <ul>{skills.map((s, i) => <li key={i}>{s}</li>)}</ul>
        <h2 className="text-xl mt-4">Recommended Jobs:</h2>
        <ul>{jobs.map((j, i) => <li key={i}>{j}</li>)}</ul>
      </div>
    </div>
  );
}

export default App;
