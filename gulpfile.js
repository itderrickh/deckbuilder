const gulp = require('gulp');
const concat = require('gulp-concat');
const minify = require('gulp-minify');
const cleanCss = require('gulp-clean-css');
const shell = require('gulp-shell');
const order = require("gulp-order");

gulp.task('pack-js', function () {
	return gulp.src([
			'wwwroot/js/*.js',
			'wwwroot/js/controllers/*.js',
			'wwwroot/js/services/*.js'])
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
	var vendorFiles = [
		'node_modules/jquery/dist/jquery.min.js',
		'node_modules/angular/angular.min.js',
		'node_modules/angular-route/angular-route.min.js',
		'node_modules/angucomplete-alt/dist/angucomplete-alt.min.js',
		'node_modules/angular-cookies/angular-cookies.min.js',
		'node_modules/moment/min/moment.min.js',
		'node_modules/fullcalendar/dist/fullcalendar.min.js',
		'node_modules/angular-ui-calendar/src/calendar.js',
		'node_modules/bootstrap/dist/js/bootstrap.min.js',
		'node_modules/clipboard/dist/clipboard.min.js',
		'node_modules/@fortawesome/fontawesome-free/js/all.min.js',
		'node_modules/ngclipboard/dist/ngclipboard.min.js',
		'node_modules/sweetalert2/dist/sweetalert2.min.js',
		'node_modules/noty/lib/noty.min.js',
		'node_modules/autosize/dist/autosize.min.js'
	];

	return gulp.src(vendorFiles)
		.pipe(order(vendorFiles, { base: './' }))
		.pipe(concat('vendor.js'))
		.pipe(gulp.dest('wwwroot/build/js'));
});

gulp.task('pack-css', function () {
	return gulp.src([
			'node_modules/bootstrap/dist/css/bootstrap.min.css',
			'node_modules/bootstrap/dist/css/bootstrap-grid.min.css',
			'node_modules/fullcalendar/dist/fullcalendar.min.css',
			'node_modules/noty/lib/noty.css',
			'wwwroot/css/*.css'
		])
		.pipe(concat('stylesheet.css'))
		.pipe(cleanCss())
		.pipe(gulp.dest('wwwroot/build/css'));
});

gulp.task('flask', gulp.parallel('pack-js', 'pack-vendor-js', 'pack-css', shell.task(['python -m flask run'])));

gulp.task('default', gulp.series('flask'));