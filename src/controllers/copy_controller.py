from flask import Blueprint, render_template, request, redirect, url_for, flash
from src.service_container import copy_service
from src.models.entities import CopyStatus

copy_bp = Blueprint('copies', __name__, url_prefix='/copies')

@copy_bp.route('/')
def list_copies():

    page = request.args.get('page', 1, type=int)
    limit = 10
    offset = (page - 1) * limit

    copies_list = copy_service.get_copies(offset, limit)

    rows = []
    for copy in copies_list:
        rows.append({
            'id': copy.id,
            'data_values': [
                copy.id, copy.title.title, copy.code,
                copy.location, copy.status.value
            ]
        })

    has_next = len(copies_list) == limit

    return render_template(
        'list.html',
        title="Copies",
        entity_name='copies',
        headers=['ID', 'Title', 'Code', 'Location', 'Status'],
        rows=rows,
        page=page,
        has_next=has_next
    )


@copy_bp.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    try:
        success = copy_service.remove_copy(id)
        if success:
            flash('Customer was removed.', 'success')
        else:
            flash('Error while deleting.', 'error')
    except Exception as e:
        flash(str(e), 'error')

    return redirect(url_for('customers.list_customers'))


@copy_bp.route('/create', methods=['GET', 'POST'])
def create():

    if request.method == 'POST':

        title = request.form.get('title')
        code = request.form.get('code')
        location = request.form.get('location')
        status = request.form.get('status')

        try:
            status_enum = CopyStatus(status)
            success =  copy_service.add_new_copy(title, code, location, status_enum)
            if success:
                flash('New copy was added.', 'success')
            else:
                flash('Error while adding new copy.', 'error')
            return redirect(url_for('copies.list_copies'))

        except Exception as e:
            flash(str(e), 'error')
            copy = {'title': title, 'code': code, 'location': location, 'status': status}
            return render_template('copy_form.html', title="Create Copy", copy=copy, statuses=CopyStatus)

    return render_template('copy_form.html', title="Create Copy", copy=None, statuses=CopyStatus)


@copy_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):

    copy = copy_service.get_by_id(id)
    if not copy:
        flash('Copy was not found', 'error')
        return redirect(url_for('copies.list_copies'))

    if request.method == 'POST':

        title = request.form.get('title')
        code = request.form.get('code')
        location = request.form.get('location')
        status = request.form.get('status')

        try:
            status_enum = CopyStatus(status)
            success = copy_service.update_copy(copy.id, title, code, location, status_enum)
            if success:
                flash('Copy updated successfully.', 'success')
            else:
                flash('Error while updating.', 'error')
            return redirect(url_for('copies.list_copies'))

        except Exception as e:
            flash(str(e), 'error')

    copy_values = {
        'title': copy.title.title,
        'code': copy.code,
        'location': copy.location,
        'status': copy.status.value
    }
    return render_template('copy_form.html', title="Edit Copies", copy=copy_values, statuses=CopyStatus)