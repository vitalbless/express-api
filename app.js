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
app.set('view engine', 'ejs');

// Раздача статических файлов из папки 'uploads'
app.use('uploads', express.static('uploads'));

app.use('/api', require('./routes'));

// Проверка и создание папки 'uploads', если её нет
if (!fs.existsSync('uploads')) {
  fs.mkdirSync('uploads');
}

// catch 404 and forward to error handler
app.use(function (req, res, next) {
  next(createError(404));
});

// error handler
app.use(function (err, req, res, next) {
  // Логируем ошибку в консоль
  console.error(err.stack);

  // Устанавливаем локальные переменные для ошибки
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};

  // Отправляем ответ с ошибкой в браузер
  res.status(err.status || 500);
  if (req.app.get('env') === 'development') {
    // В режиме разработки показываем стек ошибки
    res.render('error', { error: err.stack });
  } else {
    // В продакшн-среде показываем только общее сообщение
    res.render('error', { error: 'Something went wrong!' });
  }
});

module.exports = app;
