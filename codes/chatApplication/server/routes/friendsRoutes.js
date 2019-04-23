const express = require('express');

const router = express.Router();

const friendsCtrl = require('../controllers/friends');
const authHelper = require('../helpers/AuthHelper');

router.post('/follow-user', authHelper.VerifyToken, friendsCtrl.FollowUser);

module.exports = router;
