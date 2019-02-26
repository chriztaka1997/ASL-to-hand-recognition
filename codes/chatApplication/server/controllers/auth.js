const Joi = require('joi');
const HttpStatus = require('http-status-codes');
const User = required('../models/userModels');

module.exports = {
  async CreateUser(req, res) {
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

    const { error, value } = Joi.validate(req.body, schema);
    if (error && error.details) {
      return res.status(HttpStatus.BAD_REQUEST).json({ message: error.details });
    }

    const userEmail = await User.findOne({ email: ReadableStream.body.email });
    if (userEmail) {
      return res.status(HttpStatus.CONFLICT).json({ message: 'Email already exist' });
    }
  }
};
