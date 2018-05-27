def post_liked(request, slug):
    return 'liked_posts' in request.session and slug in request.session['liked_posts']
