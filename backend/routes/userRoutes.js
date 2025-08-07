const  express = require('express');
const  User = require('../models/User.js');

const router = express.Router();

router.post('/register', async (req, res) => {
  const { name, email, password } = req.body;
  const user = new User({ name, email, password });
  await user.save();
  res.json({ message: 'User registered', user });
});

router.post('/login', async (req, res) => {
  const { email, password } = req.body;
  const user = await User.findOne({ email, password });
  if (!user) return res.status(401).json({ message: 'Invalid credentials' });
  res.json({ message: 'Login successful', user });
});

router.post('/uploadResume', async (req, res) => {
  const { userId, resumeText } = req.body;
  const skills = extractSkills(resumeText); // Mock function
  const user = await User.findByIdAndUpdate(userId, { resumeText, skills });
  res.json({ message: 'Resume uploaded', user });
});

function extractSkills(resume) {
  const keywords = ['JavaScript', 'React', 'Node.js', 'MongoDB', 'Python'];
  return keywords.filter(skill => resume.includes(skill));
}

module.exports = router;

