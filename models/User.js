const mongoose = require('mongoose');

const userSchema = new mongoose.Schema({
  fullname: { type: String, required: true },
  username: { type: String, required: true, unique: true },
  password: { type: String, required: true },
  dob: { type: String },
  email: { type: String, required: true, unique: true },
  pronouns: { type: String },
  phone: { type: String },
  interests: [{ type: String }],
  profileImage: { type: String }
}, { timestamps: true });

module.exports = mongoose.model('User', userSchema);