const express = require('express');

const router = express.Router();

const messageCtrl = require('../controllers/message');
const authHelper = require('../helpers/AuthHelper');

router.post('/chat-messages/:senderId/:receiverId', authHelper.VerifyToken, messageCtrl.SendMessage);

module.exports = router;
