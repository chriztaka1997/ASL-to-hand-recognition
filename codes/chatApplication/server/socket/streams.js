module.exports = function(io) {
  io.on('connectiin', socket => {
    console.log('user connected');
  });
};
