var gulp = require('gulp');
var concat = require('gulp-concat');
var minify = require('gulp-minify');
var cleanCss = require('gulp-clean-css');
var shell = require('gulp-shell');

gulp.task('pack-js', function () {
	return gulp.src(['wwwroot/js/*.js', 'wwwroot/js/controllers/*.js', 'wwwroot/js/services/*.js'])
		.pipe(concat('bundle.js'))
		.pipe(minify({
			ext: {
				min: '.js'
			},
			noSource: true
		}))
		.pipe(gulp.dest('wwwroot/build/js'));
});

gulp.task('pack-css', function () {
	return gulp.src(['wwwroot/css/*.css'])
		.pipe(concat('stylesheet.css'))
		.pipe(cleanCss())
		.pipe(gulp.dest('wwwroot/build/css'));
});

gulp.task('flask', shell.task(['flask run']));

gulp.task('default', ['pack-js', 'pack-css', 'flask']);