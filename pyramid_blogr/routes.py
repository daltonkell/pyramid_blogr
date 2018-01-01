def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    # the following routes map URLs to view code using a simple pattern
    # matching language. Our application will conist of a few sections:
    # - index page (listing all of our blog entries);
    # - a sign in/sign out page for authentication;
    # - a way to create and edit blog posts
    config.add_route('blog', '/blog/{id:\d+}/{slug}')
    # the bracketed code is dynamic, and is replaced with whatever we want
    # here, the two dynamic parts mean that 1. the route will only match
    # digits (that's the :\d+) and 2. a string pattern
    # e.g. /blog/156/Some-blog-entry
    config.add_route('blog_action', '/blog/{action}',
                     factory='pyramid_blogr.security.BlogRecordFactory')
    # ^ this route is needed for our authentication
    config.add_route('auth', '/sign/{action}')
    config.add_route('register', '/register')
