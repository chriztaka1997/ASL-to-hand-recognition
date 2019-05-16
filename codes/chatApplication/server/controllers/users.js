const httpStatus = require('http-status-codes');
const User = require('../models/userModels');
module.exports = {
  async GetAllUsers(req, res) {
    await User.find({})
      .populate('following.userFollowed')
      .populate('followers.follower')
      .then(result => {
        res.status(httpStatus.OK).json({ message: 'All users', result });
      })
      .catch(err => {
        res.status(httpStatus.INTERNAL_SERVER_ERROR).json({ message: 'Error occured' });
      });
  },

  async GetUserById(req, res) {
    await User.findOne({ _id: req.params.id })
      .populate('following.userFollowed')
      .populate('followers.follower')
      .then(result => {
        res.status(httpStatus.OK).json({ message: 'User by Id', result });
      })
      .catch(err => {
        res.status(httpStatus.INTERNAL_SERVER_ERROR).json({ message: 'Error occured' });
      });
  },

  async GetUserByName(req, res) {
    console.log('randommmm');
    console.log(req.params);
    await User.findOne({ username: req.params.username })
      .populate('following.userFollowed')
      .populate('followers.userFollower')
      .then(result => {
        res.status(httpStatus.OK).json({ message: 'User by username', result });
      })
      .catch(err => {
        res.status(httpStatus.INTERNAL_SERVER_ERROR).json({ message: 'Error occured' });
      });
  }
};
