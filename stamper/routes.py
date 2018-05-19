def includeme(config):
    config.add_static_view('js', 'static/js', cache_max_age=3600)
    config.add_static_view('css', 'static/css', cache_max_age=3600)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
