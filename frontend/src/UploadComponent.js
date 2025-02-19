import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState('');
  const [image, setImage] = useState('');
  const [image2, setImage2] = useState('');
  const [colors, setColors] = useState([]);
  const [percents, setPercents] = useState([]);
  const [clothes, setClothes] = useState([]);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('imageUpload', file);

    try {
      const response = await axios.post('/api/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setMessage(response.data.message);
      setImage(response.data.image);
      setImage2(response.data.image2);
      setColors(response.data.colors);
      setPercents(response.data.percents);
      setClothes(response.data.clothes);
    } catch (error) {
      console.error('Error uploading file:', error);
    }
  };

  return (
    <div>
      <h1>Upload Image</h1>
      <form onSubmit={handleSubmit}>
        <input type="file" onChange={handleFileChange} />
        <button type="submit">Upload</button>
      </form>
      {message && <p>{message}</p>}
      {image && <img src={image} alt="Uploaded" />}
      {image2 && <img src={image2} alt="Segmented" />}
      <ul>
        {colors.map((color, index) => (
          <li key={index}>Color: {color}</li>
        ))}
        {percents.map((percent, index) => (
          <li key={index}>Percent: {percent}</li>
        ))}
      </ul>
      <h2>Clothes</h2>
      <ul>
        {clothes.map((item, index) => (
          <li key={index}>
            <img src={item.img} alt={item.type} />
            <p>Type: {item.type}</p>
            <p>Colors: {item.colors.join(', ')}</p>
            <p>Percents: {item.percemnts.join(', ')}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;