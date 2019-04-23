const express = require('express');

const router = express.Router();

const userCtrl = require('../controllers/users');
const authHelper = require('../helpers/AuthHelper');

router.get('/users', authHelper.VerifyToken, userCtrl.GetAllUsers);
router.get('/users/:id', authHelper.VerifyToken, userCtrl.GetUserById);
router.get('/users/:username', authHelper.VerifyToken, userCtrl.GetUserByName);

module.exports = router;
