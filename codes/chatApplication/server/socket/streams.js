module.exports = function(io) {
  io.on('connection', socket => {
    socket.on('refresh', data => {
      // Can look up more into emit documentation of Socket Io
      // this will emit to all client
      io.emit('refreshPage', {});
    });
  });
};
