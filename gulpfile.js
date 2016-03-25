"use strict";
var fs = require('fs'),
    path = require('path'),
    gulp = require('gulp'),
    $ = require('gulp-load-plugins')(),
    browserSync = require('browser-sync').create(),
    livereload = browserSync.stream,
    json = JSON.parse(fs.readFileSync('./package.json'));

var config = (function () {
    var appName = json.name;

    var path = {
        bower: './bower_components/',
        assets: './' + appName + '/assets',
        static: './' + appName + '/static'
    };

    return {
        path: path,
        scss: {
            input: path.assets + '/scss/style.scss',
            include: [
                path.bower + '/bootstrap-sass/assets/stylesheets',
                path.bower + '/font-awesome/scss',
                path.assets + '/scss/'
            ],
            output: path.static + "/css",
            watch: [
                path.assets + '/scss/**.scss'
            ]
        },
        icons: {
            input: [
                path.bower + '/font-awesome/fonts/**.*'
            ],
            output: path.static + "/fonts"
        },
        script: {
            input: [
                path.bower + '/jquery/dist/jquery.js',
                path.bower + '/bootstrap-sass/assets/javascripts/bootstrap.js',
                path.bower + '/mousetrap/mousetrap.js',
                path.assets + '/js/*.js'
            ],
            output: path.static + "/js/script.js",
            watch: [
                path.assets + '/js/*.js'
            ]
        }
    };
}());

gulp.task('server', function () {
    browserSync.init({
        proxy: 'localhost:8000'
    });
});

gulp.task('bower', function () {
    return $.bower(config.path.bower);
});

gulp.task('icons', function () {
    return gulp.src(config.icons.input)
        .pipe(gulp.dest(config.icons.output));
});

gulp.task('js', function () {
    var directory = path.dirname(config.script.output);
    var filename = path.basename(config.script.output);
    return gulp.src(config.script.input)
        .pipe($.concat(filename))
        .pipe(gulp.dest(directory))
        .pipe(livereload())
        .pipe($.uglify())
        .pipe($.rename({extname: '.min.js'}))
        .pipe(gulp.dest(directory))
        .pipe(livereload());
});

gulp.task('scss', function () {
    return $.rubySass(
        config.scss.input,
        {
            style: 'expanded',
            loadPath: config.scss.include,
            sourcemap: true
        }
    )
        .pipe($.autoprefixer("last 1 version", "> 1%", "ie 8", "ie 7"))
        .pipe(gulp.dest(config.scss.output))
        .pipe(livereload())
        .pipe($.rename({extname: '.min.css'}))
        .pipe($.cleanCss())
        .pipe(gulp.dest(config.scss.output))
        .pipe(livereload());
});

// Rerun the task when a file changes
gulp.task('watch', function () {
    config.scss.watch.forEach(function (path) {
        gulp.watch(path, ['scss']);
    });
    config.script.watch.forEach(function (path) {
        gulp.watch(path, ['js']);
    });
});

gulp.task('default', ['bower', 'icons', 'js', 'scss', 'watch']);
