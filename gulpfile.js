const gulp = require('gulp');
const concat = require('gulp-concat');
const minify = require('gulp-minify');
const cleanCss = require('gulp-clean-css');
const shell = require('gulp-shell');
const order = require("gulp-order");

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

gulp.task('pack-vendor-js', function () {
	return gulp.src('wwwroot/lib/js/*.js')
		.pipe(order([
			'wwwroot/lib/js/jquery-3.3.1.min.js',
			'wwwroot/lib/js/angular.min.js',
			'wwwroot/lib/js/angular-route.js',
			'wwwroot/lib/js/angucomplete-alt.min.js',
			//'wwwroot/lib/js/spin.js',
			//'wwwroot/lib/js/angular-spinner.min.js',
			'wwwroot/lib/js/bootstrap.min.js',
			'wwwroot/lib/js/clipboard.min.js',
			'wwwroot/lib/js/fontawesome-all.min.js',
			'wwwroot/lib/js/ngclipboard.min.js',
			'wwwroot/lib/js/sweetalert2.min.js',
			'wwwroot/lib/js/autosize.min.js'
		], { base: './' }))
		.pipe(concat('vendor.js'))
		.pipe(gulp.dest('wwwroot/build/js'));
});

gulp.task('pack-css', function () {
	return gulp.src(['wwwroot/lib/css/bootstrap.base.min.css', 'wwwroot/lib/css/bootstrap-grid.min.css', 'wwwroot/css/*.css'])
		.pipe(concat('stylesheet.css'))
		.pipe(cleanCss())
		.pipe(gulp.dest('wwwroot/build/css'));
});

gulp.task('flask', ['pack-js', 'pack-vendor-js', 'pack-css'], shell.task(['python -m flask run']));

gulp.task('default', ['flask']);