(function($){
    class App{
        constructor(camera) {
            this.camera = camera;
            this.main = $('#search');
            this.form = this.main.find('form');
            this.input = this.form.find('.search-input');
            this.cameraBtn = this.form.find('.js-search-camera');
            this.search = this.form.find('.js-search');
            this.view = this.main.find('.search-view');
            this.list = this.view.find('.search-list');
            this.message = this.view.find('.search-message');
            this.registerListener();
            this.view.hide();
        }

        registerListener () {
            this.form.on('submit', this.onSubmit.bind(this));
            this.cameraBtn.on('click', this.onCameraBtn.bind(this));
        }

        onCameraBtn () {
            this.camera.find(this.onCameraFind.bind(this));
        }

        onCameraFind (code) {
            this.input.val(code);
            this.doSearch(code)
        }

        onSubmit (ev) {
            ev.preventDefault();
            var value = this.input.val();
            this.doSearch(value);
            return false;
        }

        doSearch(keyword) {
            $.getJSON(url_config.api.front_search + encodeURIComponent(keyword))
            .then(
                this.handleResult.bind(this),
                this.handleError.bind(this)
                );
        }

        handleResult (response) {
            this.view.show();
            if(response.status == 'ok'){
                if(response.data.length > 0){
                    this.showResult(response.data);
                }else{
                    this.showMessage('Niestety nie znaleźlismy producenta.');
                }
            }else{
                this.showMessage(response.message);
            }
        }

        showMessage (msg) {
            this.message.show().text(msg);
            this.list.empty().hide();
        }

        showResult (items) {
            this.message.hide();
            this.list.show();
            this.list.empty().append(
                $.map(items,  item => {
                    var brands = (item.brands || []).join(', ');
                    return '<li><a href="#">' + item.name + '</a> ' + brands + '</li>';
                })
            );
        }

        handleError () {
            this.showMessage('Problemy z połączeniem');
        }
    };

    class Camera {
        constructor ( ) {
            this.initialized = false;
            this.listeners = [];
            this.viewport = document.querySelector('.search-viewport');
            $('#camera-modal').on('hidden.bs.modal', function (e) {
                Quagga.stop();
            });
        }

        camera_init () {
            this.initialized = true;
            Quagga.init(
                {
                    inputStream : {
                        name : 'Live',
                        type : 'LiveStream',
                        target: this.viewport
                    },
                    decoder : {
                        readers : ['ean_reader'],
                        multiple: false
                    }
                },
                err => {
                    if (err) {
                        return;
                    }
                    this.start();
                }
            );
            Quagga.onDetected(result => {
                this.listeners.forEach( fn => fn(result.codeResult.code));
                this.listeners = [];
                this.stop();
            });
        }

        stop () {
            $('#camera-modal').modal('hide');
        }

        start () {
            $('#camera-modal').modal();
            if(this.initialized){
                Quagga.start();
            }else{
                this.camera_init();
            }
        }

        find (listener) {
            this.listeners.push(listener);
            this.start();
        }
    };
    const camera = new Camera();
    const app= new App(App);

}) (jQuery);
