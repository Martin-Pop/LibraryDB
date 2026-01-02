from flask import Blueprint, render_template, request, redirect, url_for, flash
from src.service_container import title_service, author_service

title_bp = Blueprint('titles', __name__, url_prefix='/titles')

@title_bp.route('/')
def list_titles():

    page = request.args.get('page', 1, type=int)
    limit = 10
    offset = (page - 1) * limit

    titles_list = title_service.get_titles(offset, limit)

    rows = []
    for title in titles_list:
        rows.append({
            'id': title.id,
            'data_values': [
                title.id, title.title, title.author.name, title.isbn,
                title.page_count, title.price, title.description
            ]
        })

    has_next = len(titles_list) == limit

    return render_template(
        'list.html',
        title="Titles",
        entity_name='titles',
        headers=['ID', 'Title' ,'Author Name', 'ISBN', 'Page Count', 'Price', 'Description'],
        rows=rows,
        page=page,
        has_next=has_next
    )


@title_bp.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    try:
        success = title_service.remove_title(id)
        if success:
            flash('Title was removed.', 'success')
        else:
            flash('Error while deleting.', 'error')
    except Exception as e:
        flash(str(e), 'error')

    return redirect(url_for('titles.list_titles'))


@title_bp.route('/create', methods=['GET', 'POST'])
def create():

    if request.method == 'POST':
        title = request.form.get('title')
        isbn = request.form.get('isbn')
        page_count = request.form.get('page_count')
        price = request.form.get('price')
        description = request.form.get('description')

        author_name = request.form.get('author_name')

        try:
            page_count = int(page_count) if page_count else None
            price = float(price)

            success = title_service.add_new_title(author_name, title, isbn, page_count, price, description)
            if success:
                flash('New title was added.', 'success')
            else:
                flash('Error while adding new title.', 'error')
            return redirect(url_for('titles.list_titles'))

        except Exception as e:
            flash(str(e), 'error')
            title_data = {
                'title': title,
                'isbn': isbn if isbn else '',
                'page_count': page_count,
                'price': price,
                'description': description if description else '',
                'author_name': author_name
            }

            return render_template('title_form.html', title="Create Title", item=title_data)

    return render_template('title_form.html', title="Create Title", item=None)


@title_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):

    title_obj = title_service.get_by_id(id)
    if not title_obj:
        flash('Title was not found', 'error')
        return redirect(url_for('titles.list_titles'))

    if request.method == 'POST':

        title = request.form.get('title')
        isbn = request.form.get('isbn')
        page_count = request.form.get('page_count')
        price = request.form.get('price')
        description = request.form.get('description')

        author_name = request.form.get('author_name')

        try:
            page_count = int(page_count) if page_count else None
            price = float(price)

            success = title_service.update_title(id, author_name, title, isbn, page_count, price, description)
            if success:
                flash('Title updated.', 'success')
            else:
                flash('Error while updating title.', 'error')
            return redirect(url_for('titles.list_titles'))

        except Exception as e:
            flash(str(e), 'error')

    title_data = {
        'title': title_obj.title,
        'isbn': title_obj.isbn if title_obj.isbn else '',
        'page_count': title_obj.page_count,
        'price': title_obj.price,
        'description': title_obj.description if title_obj.description else '',
        'author_name': title_obj.author.name,
    }
    return render_template('title_form.html', title="Create Title", item=title_data)