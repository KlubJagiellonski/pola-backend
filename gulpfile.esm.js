import gulp from 'gulp';
import sourcemaps from 'gulp-sourcemaps';
import cssnano from 'gulp-cssnano';
import autoprefixer from 'gulp-autoprefixer';
import rename from 'gulp-rename';
import concat from 'gulp-concat';
import terser from 'gulp-terser';

const sass = require('gulp-sass')(require('sass'));

const path = {
    assets: './pola/assets',
    static: './pola/static',
    template: './pola/templates'
};

export function buildStyles() {
    return gulp.src(`${path.assets}/scss/style.scss`)
        .pipe(sourcemaps.init())
        .pipe(sass({
            includePaths: [
                './node_modules/bootstrap-sass/assets/stylesheets/',
                './node_modules/font-awesome/scss/',
            ]
        }).on('error', sass.logError))
        .pipe(autoprefixer())
        .pipe(gulp.dest(`${path.static}/css`))
        .pipe(rename({extname: '.min.css'}))
        .pipe(cssnano())
        .pipe(sourcemaps.write())
        .pipe(gulp.dest(`${path.static}/css`))
}

export function buildScripts() {
    return gulp.src([
        './node_modules/jquery/dist/jquery.js',
        './node_modules/bootstrap-sass/assets/javascripts/bootstrap.js',
        './node_modules/mousetrap/mousetrap.js',
        `${path.assets}/js/*.js`
    ])
        .pipe(sourcemaps.init())
        .pipe(concat('backend.js'))
        .pipe(gulp.dest(`${path.static}/js/`))
        .pipe(terser())
        .pipe(rename({extname: '.min.js'}))
        .pipe(sourcemaps.write())
        .pipe(gulp.dest(`${path.static}/js/`));
}

export function copyFonts() {
    return gulp.src('./node_modules/font-awesome/fonts/**.*')
        .pipe(gulp.dest(`${path.static}/fonts`))
}

export function watch() {
    gulp.watch(`${path.assets}/scss/**.scss`, ['buildStyles']);
    gulp.watch(`${path.assets}/js/**.js`, ['buildScripts']);
}

export default gulp.parallel(
    buildStyles,
    buildScripts,
    copyFonts
)
