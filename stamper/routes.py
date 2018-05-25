def includeme(config):
    config.add_static_view('js', 'static/js', cache_max_age=3600)
    config.add_static_view('css', 'static/css', cache_max_age=3600)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_static_view('dz', 'static/dropzone', cache_max_age=3600)
    config.add_route('add-image', '/api/1.0/add-image')
    config.add_route('image-upload', '/upload')
    config.add_route('login', '/login')
    config.add_route('home', '/')
