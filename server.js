const express = require('express');
const mongoose = require('mongoose');
const session = require('express-session');
const path = require('path');
require('dotenv').config();

const authRoutes = require('./routes/auth');

const app = express();

mongoose.connect(process.env.MONGODB_URI)
  .then(() => console.log('Connected to MongoDB'))
  .catch((err) => console.error('MongoDB connection error:', err));

app.use(express.urlencoded({ extended: true }));
app.use(express.json());

app.use(session({
  secret: process.env.SESSION_SECRET,
  resave: false,
  saveUninitialized: false
}));

app.use('/uploads', express.static(path.join(__dirname, 'uploads')));
app.use(express.static(path.join(__dirname, 'Pages 2')));

app.use(authRoutes);

function requireAuth(req, res, next) {
  if (req.session.userId) return next();
  return res.redirect('/signIn.html');
}

app.get('/landingPage.html', requireAuth, (req, res) => {
  res.sendFile(path.join(__dirname, 'Pages 2', 'landingPage.html'));
});

app.get('/profilePage.html', requireAuth, (req, res) => {
  res.sendFile(path.join(__dirname, 'Pages 2', 'profilePage.html'));
});

app.get('/supportPage.html', (req, res) => {
  res.sendFile(path.join(__dirname, 'Pages 2', 'supportPage.html'));
});

app.get('/', (req, res) => {
  res.redirect('/signIn.html');
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server running on http://localhost:${PORT}`));