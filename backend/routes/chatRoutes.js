const express= require('express');
const dotenv= require('dotenv');
const axios = require('axios');

dotenv.config();
const router = express.Router();

router.post('/careerbot', async (req, res) => {
  const { message } = req.body;

  try {
    const openaiResponse = await axios.post(
      'https://api.openai.com/v1/chat/completions',
      {
        model: 'gpt-3.5-turbo',
        messages: [
          { role: 'system', content: 'You are a helpful career advisor AI assistant.' },
          { role: 'user', content: message }
        ]
      },
      {
        headers: {
          'Authorization': `Bearer ${process.env.OPENAI_API_KEY}`,
          'Content-Type': 'application/json'
        }
      }
    );

    const reply = openaiResponse.data.choices[0].message.content;
    res.json({ reply });
  } catch (error) {
    console.error(error.response?.data || error.message);
    res.status(500).json({ error: 'OpenAI API Error' });
  }
});

module.exports = router;
