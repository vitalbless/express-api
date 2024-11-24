const createError = require('http-errors');
const express = require('express');
const path = require('path');
const cookieParser = require('cookie-parser');
const logger = require('morgan');
const fs = require('fs');
const cors = require('cors');
require('dotenv').config();

const app = express();

app.use(cors());
app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());

// Убираем настройку для view engine, так как она не нужна для серверных ошибок
// app.set('view engine', 'ejs');

// Главная страница
app.get('/', (req, res) => {
  res.send('Hello World');
});

// Убираем настройку для favicon.ico
app.get('/favicon.ico', (req, res) => res.status(204).end());

// Раздача статических файлов из папки 'uploads'
app.use('uploads', express.static('uploads'));

app.use('/api', require('./routes'));

// Проверка и создание папки 'uploads'
if (!fs.existsSync('uploads')) {
  fs.mkdirSync('uploads');
}

// catch 404 and forward to error handler
app.use(function (req, res, next) {
  next(createError(404));
});

// error handler
app.use(function (err, req, res, next) {
  // Логирование ошибки в консоль
  console.error(`Error: ${err.message}`);
  console.error(err.stack);

  // Отправка стандартного ответа 500, без рендеринга страницы
  res.status(err.status || 500).send('Server error');
});

module.exports = app;
