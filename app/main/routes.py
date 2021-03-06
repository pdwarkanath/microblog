from flask import render_template, flash, redirect, request, url_for, g, jsonify, current_app
from app import db
from app.main.forms import EditProfileForm, PostForm, SearchForm
from datetime import datetime
from flask_login import current_user, login_required
from app.models import User, Post
from datetime import datetime
from app.auth.email import send_password_reset_email
from flask_babel import _, get_locale
from google.cloud import translate
from app.translate import translate_text
from app.main import bp


@bp.before_app_request
def before_request():
	if current_user.is_authenticated:
		current_user.last_seen = datetime.utcnow()
		db.session.commit()
		g.search_form = SearchForm()
	g.locale = str(get_locale())

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
	form = PostForm()
	if form.validate_on_submit():
		if 'GOOGLE_APPLICATION_CREDENTIALS' not in current_app.config or not current_app.config['GOOGLE_APPLICATION_CREDENTIALS']:
			language = ''
		else:
			translate_client = translate.Client()
			language = translate_client.detect_language(form.post.data)['language']
			
		post = Post(body = form.post.data, author=current_user)
		post.language = language
		db.session.add(post)
		db.session.commit()
		flash(_('Your post is now live!'))
		return redirect(url_for('main.index'))
	page = request.args.get('page', 1, type = int)
	posts = current_user.followed_posts().paginate(page, current_app.config['POSTS_PER_PAGE'], False)
	if posts.has_next:
		next_url = url_for('main.index', page = posts.next_num)
	else:
		next_url = None
	if posts.has_prev:
		prev_url = url_for('main.index', page = posts.prev_num)
	else:
		prev_url = None
	return render_template('index.html', title=_('Home'), posts = posts.items, form = form, next_url = next_url, prev_url = prev_url)



@bp.route('/user/<username>')
@login_required
def user(username):
	user = User.query.filter_by(username=username).first_or_404()
	page = request.args.get('page', 1, type = int)
	posts = user.posts.order_by(Post.timestamp.desc()).paginate(page, current_app.config['POSTS_PER_PAGE'], False)
	if posts.has_next:
		next_url = url_for('main.user', username = username, page = posts.next_num)
	else:
		next_url = None
	if posts.has_prev:
		prev_url = url_for('main.user', username = username, page = posts.prev_num)
	else:
		prev_url = None
	return render_template('user.html', user=user, posts=posts.items, next_url = next_url, prev_url = prev_url)




@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
	form = EditProfileForm(current_user.username)
	if form.validate_on_submit():
		current_user.username = form.username.data
		current_user.about_me = form.about_me.data
		db.session.commit()
		flash(_('Your changes have been saved.'))
		return redirect(url_for('main.edit_profile'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.about_me.data = current_user.about_me
	return render_template('edit_profile.html', title = _('Edit Profile'), form = form)


@bp.route('/follow/<username>', methods= ['GET', 'POST'])
@login_required
def follow(username):
	user = User.query.filter_by(username = username).first()
	if user is None:
		flash(_('User %(username)s not found.', username = username))
		return redirect(url_for('main.index'))
	if user == current_user:
		flash(_('You cannot follow yourself!'))
		return redirect(url_for('main.user', username=username))
	current_user.follow(user)
	db.session.commit()
	flash(_('You are following %(username)s!', username = username))
	return redirect(url_for('main.user', username=username))


@bp.route('/unfollow/<username>', methods= ['GET', 'POST'])
@login_required
def unfollow(username):
	user = User.query.filter_by(username = username).first()
	if user is None:
		flash(_('User %(username)s not found.', username = username))
		return redirect(url_for('main.index'))
	if user == current_user:
		flash(_('You cannot unfollow yourself!'))
		return redirect(url_for('main.user', username=username))
	current_user.unfollow(user)
	db.session.commit()
	flash(_('You are no longer following %(username)s!', username = username))
	return redirect(url_for('main.user', username=username))

@bp.route('/explore')
@login_required
def explore():
	page = request.args.get('page', 1, type = int)
	posts = Post.query.order_by(Post.timestamp.desc()).paginate(page, current_app.config['POSTS_PER_PAGE'], False)
	if posts.has_next:
		next_url = url_for('main.explore', page = posts.next_num)
	else:
		next_url = None
	if posts.has_prev:
		prev_url = url_for('main.explore', page = posts.prev_num)
	else:
		prev_url = None
	return render_template('index.html', title = _('Explore'), posts = posts.items, next_url = next_url, prev_url = prev_url)

@bp.route('/translate', methods=['POST'])
@login_required
def translate_post():
	return jsonify(translate_text(request.form['text'], request.form['dest_language']))

@bp.route('/search')
@login_required
def search():
	if not g.search_form.validate():
		return redirect(url_for('main.explore'))
	page = request.args.get('page', 1, type=int)
	posts, total = Post.search(g.search_form.q.data, page, current_app.config['POSTS_PER_PAGE'])
	next_url = url_for('main.search', q=g.search_form.q.data, page=page + 1) \
		if total > page * current_app.config['POSTS_PER_PAGE'] else None
	prev_url = url_for('main.search', q=g.search_form.q.data, page=page - 1) \
		if page > 1 else None
	return render_template('search.html', title=_('Search'), posts=posts, next_url=next_url, prev_url=prev_url)
