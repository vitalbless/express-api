const jwt = require('jsonwebtoken');

const authenticateToken = (req, res, next) => {
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1];
  if (!token) {
    return res.status(401).json({ error: 'Unauthorized' });
  }
  //передаем токен дальше ключ для расшифровки токен и каллбек , в каллбек функции неважно как написаны аргументы важно на каком месте , на 1 месте должна быть переменная для ошибки
  jwt.verify(token, process.env.SECRET_KEY, (err, user) => {
    if (err) {
      return res.status(403).json({ error: 'Invalid token' });
    }
    req.user = user;
    next();
  });
};
module.exports = { authenticateToken };
