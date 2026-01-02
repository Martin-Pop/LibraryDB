from flask import Blueprint, render_template, request, redirect, url_for, flash

from src.service_container import author_service
from src.utils import parse_db_exception

authors_bp = Blueprint('authors', __name__, url_prefix='/authors')


@authors_bp.route('/')
def list_authors():

    page = request.args.get('page', 1, type=int)
    limit = 10
    offset = (page - 1) * limit

    authors_list = author_service.get_authors(offset, limit)

    rows = []
    for author in authors_list:
        rows.append({
            'id': author.id,
            'data_values': [author.id, author.name, author.nationality]
        })

    has_next = len(authors_list) == limit

    return render_template(
        'list.html',
        title="Authors",
        entity_name='authors',
        headers=['ID', 'Name', 'Nationality'],
        rows=rows,
        page=page,
        has_next=has_next
    )


@authors_bp.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    try:
        success = author_service.remove_author(id)
        if success:
            flash('Author was deleted.', 'success')
        else:
            flash('Error while deleting.', 'error')
    except Exception as e:
        flash('Error deleting author: ' + parse_db_exception(e), 'error')

    return redirect(url_for('authors.list_authors'))


@authors_bp.route('/create', methods=['GET', 'POST'])
def create():

    if request.method == 'POST':

        name = request.form.get('name')
        nationality = request.form.get('nationality')

        try:
            author_service.add_new_author(name, nationality)
            flash('Author created successfully.', 'success')
            return redirect(url_for('authors.list_authors'))

        except Exception as e:
            flash('Error creating author: ' + parse_db_exception(e), 'error')
            author = {'name' : name, 'nationality': nationality}
            return render_template('author_form.html', title="Create Author", author=author)

    # GET
    return render_template('author_form.html', title="Create Author", author=None)


@authors_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):

    author = author_service.get_by_id(id)
    if not author:
        flash('Author was not found', 'error')
        return redirect(url_for('authors.list_authors'))

    if request.method == 'POST':

        name = request.form.get('name')
        nationality = request.form.get('nationality')

        try:
            success = author_service.update_author(id, name, nationality)
            if success:
                flash('Author updated successfully.', 'success')
            else:
                flash('Error while updating.', 'error')
            return redirect(url_for('authors.list_authors'))

        except Exception as e:
            flash('Error updating author: ' + parse_db_exception(e), 'error')

    return render_template('author_form.html', title="Edit Author", author=author)