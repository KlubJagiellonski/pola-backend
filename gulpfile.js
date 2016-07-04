"use strict";
var fs = require('fs'),
    path = require('path'),
    merge = require('merge-stream'),
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
        static: './' + appName + '/static',
        template: './' + appName + '/templates'
    };

    return {
        path: path,
        scss: {
            input: [
                path.assets + '/scss/style.scss',
                path.assets + '/scss/landing.scss',
            ],
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
        script: {
            input: {
                backend: [
                    path.bower + '/jquery/dist/jquery.js',
                    path.bower + '/bootstrap-sass/assets/javascripts/bootstrap.js',
                    path.bower + '/mousetrap/mousetrap.js',
                    path.bower + "/microplugin/src/microplugin.js", 
                    path.bower + "/sifter/sifter.js", 
                    path.bower + "/selectize/dist/js/selectize.js", 
                    path.assets + '/js/*.js'
                ],
                landing: [
                    path.bower + "/jquery/dist/jquery.js",
                    path.bower + "/bootstrap-sass/assets/javascripts/bootstrap/transition.js",
                    path.bower + "/bootstrap-sass/assets/javascripts/bootstrap/modal.js",
                    path.assets + "/js/landing/*.js"
                ]
            },
            output: path.static + "/js/",
            watch: [
                path.assets + '/js/*.js'
            ]
        },
        icons: {
            input: [
                path.bower + '/font-awesome/fonts/**.*'
            ],
            output: path.static + "/fonts"
        },
        images: {
            input: path.assets + "/images/*",
            output: path.static + "/images/"
        },
        symbols: {
            input: path.assets + "/svg/*.svg",
            output: path.static + "/symbols.svg",
            watch: path.assets + "/svg/*.svg"
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
    var streams = merge();
    for(var name in config.script.input){
        var filename = name + '.js';
        var stream = gulp.src(config.script.input[name])
            .pipe($.concat(filename))
            .pipe(gulp.dest(config.script.output))
            .pipe(livereload())
            .pipe($.uglify())
            .pipe($.rename({extname: '.min.js'}))
            .pipe(gulp.dest(config.script.output))
            .pipe(livereload());
        streams.add(stream);
    };
    return streams;
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

gulp.task("images", function () {
    return gulp.src(config.images.input)
        .pipe($.imagemin())
        .pipe(gulp.dest(config.images.output));
});

gulp.task("symbols", function () {
    return gulp
        .src(config.symbols.input)
        .pipe($.svgmin(function (file) {
            var prefix = path.basename(file.relative, path.extname(file.relative));
            return {
                plugins: [{
                    cleanupIDs: {
                        prefix: prefix + "-",
                        minify: true
                    }
                }]
            };
        }))
        .pipe($.svgstore())
        .pipe($.rename(path.basename(config.symbols.output)))
        .pipe(gulp.dest(path.dirname(config.symbols.output)));
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

gulp.task('build', ['bower', 'icons', 'images', 'js', 'scss']);

gulp.task('default', ['server', 'build', 'watch']);
