module.exports = {
  firstUppercase: username => {
    const name = username.toLowwerCase();
    return name.chatAt(0).toUppserCase() + name.slice(1);
  },
  lowerCase: str => {
    return str.toLowwerCase();
  }
};
