from flask import Blueprint, render_template, request, redirect, url_for, flash
from src.service_container import customer_service
from src.utils import parse_db_exception
import csv

customer_bp = Blueprint('customers', __name__, url_prefix='/customers')

@customer_bp.route('/')
def list_customers():

    page = request.args.get('page', 1, type=int)
    limit = 10
    offset = (page - 1) * limit

    customers_list = customer_service.get_customers(offset, limit)

    rows = []
    for customer in customers_list:
        rows.append({
            'id': customer.id,
            'data_values': [
                customer.id, customer.code, customer.first_name,
                customer.last_name, customer.email, customer.is_active,
                customer.registered_on.replace(microsecond=0)
            ]
        })

    has_next = len(customers_list) == limit

    return render_template(
        'list.html',
        title="Customers",
        entity_name='customers',
        headers=['ID', 'Code', 'First name', 'Last name', 'Email', 'Is active', 'Registered on'],
        rows=rows,
        page=page,
        has_next=has_next
    )


@customer_bp.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    try:
        success = customer_service.remove_customer(id)
        if success:
            flash('Customer was removed.', 'success')
        else:
            flash('Error while deleting.', 'error')
    except Exception as e:
        flash('Error deleting customer: ' + parse_db_exception(e), 'error')

    return redirect(url_for('customers.list_customers'))


@customer_bp.route('/create', methods=['GET', 'POST'])
def create():

    if request.method == 'POST':

        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        is_active = True if request.form.get('active') else False
        try:
            success =  customer_service.register_customer(first_name, last_name, email, is_active)
            if success:
                flash('New customer was added.', 'success')
            else:
                flash('Error while adding new customer.', 'error')
            return redirect(url_for('customers.list_customers'))

        except Exception as e:
            flash('Error creating customer: ' + parse_db_exception(e), 'error')
            customer = {'first_name' : first_name, 'last_name': last_name, "email":email, 'is_active': is_active}
            return render_template('customer_form.html', title="Create Customer", customer=customer)

    return render_template('customer_form.html', title="Create Customer", customer=None)


@customer_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):

    customer = customer_service.get_by_id(id)
    if not customer:
        flash('Customer was not found', 'error')
        return redirect(url_for('customers.list_customers'))

    if request.method == 'POST':

        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')

        try:
            is_active = True if request.form.get('active') else False
            success = customer_service.update_customer(id, first_name, last_name, email, is_active)
            if success:
                flash('Customer updated successfully.', 'success')
            else:
                flash('Error while updating.', 'error')
            return redirect(url_for('customers.list_customers'))

        except Exception as e:
            flash('Error editing customer: ' + parse_db_exception(e), 'error')

    return render_template('customer_form.html', title="Edit Customer", customer=customer)

@customer_bp.route('/bulk-add', methods=['GET', 'POST'])
def bulk_add():

    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file found.', 'error')
            return redirect(request.url)

        file = request.files.get('file')
        if not file:
            flash('No file selected.', 'error')
            return redirect(request.url)

        has_header = request.form.get('has_header') is not None

        try:
            csv_text = file.read().decode('utf-8')
            csv_lines = csv_text.splitlines()
            csv_reader = csv.reader(csv_lines, delimiter=',')

            lines_effected = customer_service.bulk_csv_add(csv_reader, has_header)
            if lines_effected > 0:
                flash(f'Bulk import successful. (lines effected{lines_effected})', 'success')
            else:
                flash(f'Bulk import failed, probably empty csv', 'error')
            return redirect(url_for('customers.list_customers'))

        except Exception as e:
            flash('Error editing customer: ' + parse_db_exception(e), 'error')

    return render_template('import_form.html', title="Bulk Add Customers", back_url=url_for('customers.list_customers'))