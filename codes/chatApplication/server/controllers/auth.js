const Joi = require('joi');
const HttpStatus = require('http-status-codes');
const User = require('../models/userModels');
const Helpers = require('../helpers/helpers.js');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const dbconfig = require('../config/secret');

module.exports = {
  // Setting restriction for registration/sign up page
  // Function return a promise and we handle it
  async CreateUser(req, res) {
    // Creating object key for Joi
    const schema = Joi.object().keys({
      username: Joi.string()
        .min(5)
        .max(15)
        .required(),
      email: Joi.string()
        .email()
        .required(),
      password: Joi.string()
        .min(3)
        .required(),
      firstname: Joi.string().required(),
      lastname: Joi.string().required()
    });

    // Return result
    // Result.error = = = null -> lead to invalid
    const { error, value } = Joi.validate(req.body, schema);
    if (error && error.details) {
      return res.status(HttpStatus.BAD_REQUEST).json({ message: error.details });
    }

    // Using await help composing task one by one
    // Check if email already exist
    const userEmail = await User.findOne({ email: req.body.email });
    if (userEmail) {
      return res.status(HttpStatus.CONFLICT).json({ message: 'Email already exist' });
    }

    // Check if username already exist
    const userName = await User.findOne({ username: Helpers.firstUppercase(req.body.username) });
    if (userName) {
      return res.status(HttpStatus.CONFLICT).json({ message: 'Username already exist' });
    }

    // Using bcryptjs to encrypt the password
    // Using auto-gen a salt and hash
    return bcrypt.hash(value.password, 16, (err, hash) => {
      // If error hit when hasing, return a Bad_request
      if (err) {
        return res.status(HttpStatus.BAD_REQUEST).json({ message: 'Error hashing password' });
      }
      // Converting all input into a proper format
      const body = {
        username: Helpers.firstUppercase(value.username),
        email: Helpers.lowerCase(value.email),
        password: hash,
        firstname: value.firstname,
        lastname: value.lastname
      };

      // Creating user when all requirement is meeet
      User.create(body)
        .then(user => {
          const token = jwt.sign({ data: user }, dbconfig.secret, {
            expiresIn: 120
          });

          res.status(HttpStatus.CREATED).json({ message: 'User created sucessfully', user, token });
        })
        .catch(err => {
          // If error occur, it's the serverside since all information had been validated.
          res.status(HttpStatus.INTERNAL_SERVER_ERROR).json({ message: 'Error occured' });
        });
    });
  }
};
