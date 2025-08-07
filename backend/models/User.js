const mongoose = require('mongoose');

const userSchema = new mongoose.Schema({
  name: String,
  email: String,
  password: String,
  resumeText: String,
  skills: [String],
});

// ...existing code...
module.exports = mongoose.model('User', userSchema);
