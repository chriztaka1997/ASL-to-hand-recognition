const express = require('express');

const router = express.Router();

const messageCtrl = require('../controllers/message');
const authHelper = require('../helpers/AuthHelper');

router.get('/chat-messages/:sender_Id/:receiver_Id', authHelper.VerifyToken, messageCtrl.GetAllMessages);
router.post('/chat-messages/:sender_Id/:receiver_Id', authHelper.VerifyToken, messageCtrl.SendMessage);

module.exports = router;
