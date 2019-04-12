const express = require('express');

const router = express.Router();

const userCtrl = require('../controllers/users');
const authHelper = require('../helpers/AuthHelper');

router.get('/users', authHelper.VerifyToken, userCtrl.GetAllUsers);

module.exports = router;
