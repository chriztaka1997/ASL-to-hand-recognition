const jwt = require('jsonwebtoken');
const HttpStatus = require('http-status-codes');
const dbConfig = require('../config/secret');

module.exports = {
  VerifyToken: (req, res, next) => {
    // Check if token is in the cookie
    // auth.js send the token to the cookie
    // we catching it here
    if (!req.headers.Authorization) {
      return res.status(HttpStatus.UNAUTHORIZED).json({ message: 'No authorization' });
    }
    const token = req.cookies.auth || req.headers.Authorization.split(' ')[1];
    if (!token) {
      return res.status(HttpStatus.FORBIDDEN).json({ message: 'No token provided' });
    }

    return jwt.verify(token, dbConfig.secret, (err, decoded) => {
      if (err) {
        if (err.expiredAt < new Date()) {
          return res.status(HttpStatus.INTERNAL_SERVER_ERROR).json({
            message: 'Token has expired. Please loging again',
            token: null
          });
        }
        next();
      }
      req.user = decoded.data;
      next();
    });
  }
};
