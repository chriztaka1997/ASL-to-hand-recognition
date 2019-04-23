const HttpStatus = require('http-status-codes');
const User = require('../models/userModels');

module.exports = {
  FollowUser(req, res) {
    const followUser = async () => {
      await User.updateOne(
        {
          _id: req.user._id,
          // ne is stand for not equal
          'following.userFollowed': { $ne: req.body.userFollowed }
        },
        {
          $push: {
            following: {
              userFollowed: req.body.userFollowed
            }
          }
        }
      );

      await User.updateOne(
        {
          // Weird logic right here. CAUTION!!!
          _id: req.body.userFollowed,
          // ne is stand for not equal
          'following.userFollower': { $ne: req.user._id }
        },
        {
          $push: {
            followers: {
              userFollower: req.user._id
            }
          }
        }
      );
    };

    followUser()
      .then(() => {
        res.status(HttpStatus.OK).json({ message: 'User is followed' });
      })
      .catch(err => {
        res.status(HttpStatus.INTERNAL_SERVER_ERROR).json({ message: 'Error occured in adding friend' });
      });
  }
};
