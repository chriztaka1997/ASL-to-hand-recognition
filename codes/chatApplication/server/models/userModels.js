// Act as a format for user object passing in
const mongoose = require('mongoose');

const userSchema = mongoose.Schema({
  username: { type: String },
  email: { type: String },
  password: { type: String },
  firstname: { type: String },
  lastname: { type: String },
  posts: [
    {
      postId: { type: mongoose.Schema.Types.ObjectId, ref: 'Post' },
      post: { type: String }
    }
  ],
  following: [{ userFollowed: { type: mongoose.Schema.Types.ObjectId, ref: 'User' } }],
  followers: [{ userFollower: { type: mongoose.Schema.Types.ObjectId, ref: 'User' } }]
});

module.exports = mongoose.model('User', userSchema);
