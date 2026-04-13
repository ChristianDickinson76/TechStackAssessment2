const express = require('express');
const bcrypt = require('bcryptjs');
const multer = require('multer');
const path = require('path');
const fs = require('fs');
const User = require('../models/User');

const router = express.Router();

const uploadDir = path.join(__dirname, '..', 'uploads');
if (!fs.existsSync(uploadDir)) {
  fs.mkdirSync(uploadDir);
}

const storage = multer.diskStorage({
  destination: (req, file, cb) => cb(null, uploadDir),
  filename: (req, file, cb) => {
    cb(null, Date.now() + path.extname(file.originalname));
  }
});

const upload = multer({ storage });

router.post('/signup', upload.single('profileImage'), async (req, res) => {
  try {
    const {
      fullname,
      username,
      password,
      confirmPassword,
      dob,
      email,
      pronouns,
      phone,
      interests
    } = req.body;

    if (password !== confirmPassword) {
      return res.status(400).send('Passwords do not match');
    }

    const existingUser = await User.findOne({
      $or: [{ username }, { email }]
    });

    if (existingUser) {
      return res.status(400).send('Username or email already exists');
    }

    const hashedPassword = await bcrypt.hash(password, 10);

    const interestsArray = Array.isArray(interests)
      ? interests
      : interests
        ? [interests]
        : [];

    const newUser = await User.create({
      fullname,
      username,
      password: hashedPassword,
      dob,
      email,
      pronouns,
      phone,
      interests: interestsArray,
      profileImage: req.file ? `/uploads/${req.file.filename}` : ''
    });

    req.session.userId = newUser._id;
    res.redirect('/landingPage.html');
  } catch (error) {
    console.error(error);
    res.status(500).send('Signup failed');
  }
});

router.post('/signin', async (req, res) => {
  try {
    const { username, password } = req.body;

    const user = await User.findOne({ username });
    if (!user) {
      return res.status(401).send('Invalid username or password');
    }

    const validPassword = await bcrypt.compare(password, user.password);
    if (!validPassword) {
      return res.status(401).send('Invalid username or password');
    }

    req.session.userId = user._id;
    res.redirect('/landingPage.html');
  } catch (error) {
    console.error(error);
    res.status(500).send('Signin failed');
  }
});

router.get('/logout', (req, res) => {
  req.session.destroy(() => {
    res.redirect('/signIn.html');
  });
});

module.exports = router;