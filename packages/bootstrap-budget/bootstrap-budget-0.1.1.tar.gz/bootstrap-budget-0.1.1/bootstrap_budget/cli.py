import click
import csv
import os
import secrets

from bootstrap_budget import __version__, sample_data, schema
from datetime import datetime
from pony.orm import Database, db_session, select
from werkzeug.security import generate_password_hash

# Pony needs the current working directory in order to place the database outside of site_packages
CURRENT_WORKING_DIRECTORY = os.getcwd()


def get_db() -> Database().Entity | None:
    """
    Gets a connection to the Bootstrap Budget database (if exists).

    :return: A SQLite connection to the Bootstrap Database. If the database does not exist, None is returned.
    """
    if os.path.exists('bootstrap_budget.db'):
        db = Database()
        schema.define_entities(db.Entity)
        db.bind(provider='sqlite', filename=f'{CURRENT_WORKING_DIRECTORY}\\bootstrap_budget.db')
        db.generate_mapping()

        return db
    else:
        return None


@db_session
def create_admin_account(db: Database().Entity) -> None:
    """
    Creates the admin account on the USER table.

    :return: None
    """
    admin_passwd = click.prompt(text='Enter admin password', type=str, default='admin',
                                show_default=True, hide_input=True)

    # Generate password hash and salt
    hashed_password = generate_password_hash(admin_passwd)

    try:
        admin = db.User(username='admin',
                        hash=hashed_password,
                        created_dt_tm=datetime.now(),
                        updated_dt_tm=datetime.now())
        click.echo('The Bootstrap Budget admin account has been created.')
    except Exception as e:
        # TODO: Find a better solution for handling this exception
        click.echo(e)


def create_config_file() -> None:
    """
    Creates a config file with a generated SECRET_KEY value for Flask.

    :return: None
    """
    secret_key = secrets.token_urlsafe(32)

    # Create the Flask instance directory
    os.makedirs('instance', exist_ok=True)

    with open('instance/bootstrap_config.py', 'w', ) as f:
        f.write(f"SECRET_KEY = '{secret_key}'")

    click.echo("The Bootstrap configuration file has been created.")


@db_session
def reset_admin_password(db: Database().Entity) -> None:
    """
    Resets the admin account password.

    :return: None
    """
    admin_passwd = click.prompt(text='Enter admin password', type=str, default='admin',
                                show_default=True, hide_input=True)

    # Generate password hash and salt
    hashed_password = generate_password_hash(admin_passwd)

    try:
        admin = db.User.get(username='admin')
        admin.hash = hashed_password
        click.echo('The Bootstrap Budget admin password has been reset.')
    except Exception as e:
        # TODO: Find a better solution for handling this exception
        click.echo(e)


@db_session
def create_basic_user(db: Database().Entity) -> str:
    """
    Creates a basic user (meets required fields) for the purposes of testing.

    :return: A User entity object record.
    """
    username: str | None = None

    while username is None:
        username = click.prompt(text='Enter new username', type=str, default=None)

        if username is None:
            continue

        user = db.User.get(username=username)

        if user is not None:
            click.echo('The username entered already exists. Please choose a different username.')
            exit(1)

        user_password: str = click.prompt(text=f'Enter password for {username}', type=str, default=f'{username}',
                                          show_default=True, hide_input=True)

        # Generate password hash and salt
        hashed_password = generate_password_hash(user_password)

        try:
            user = db.User(username=username,
                           hash=hashed_password,
                           created_dt_tm=datetime.now(),
                           updated_dt_tm=datetime.now())
            click.echo(f'The user "{username}" has been created.')
        except Exception as e:
            # TODO: Find a better solution for handling this exception
            click.echo(e)

    return username


@db_session
def create_sample_data(db: Database().Entity, user: str) -> None:
    """
    Creates a basic user (meets required fields) for the purposes of testing.

    :return: The user_id of the newly inserted user.
    """
    # Gather sample data
    sample_data_path = sample_data.__file__
    sample_data_dir = os.path.dirname(sample_data_path)

    budget_csv_path: str = f'{sample_data_dir}\\budget.csv'
    budget_item_csv_path: str = f'{sample_data_dir}\\budget_item.csv'
    account_csv_path: str = f'{sample_data_dir}\\account.csv'
    transaction_csv_path: str = f'{sample_data_dir}\\transaction.csv'

    user = db.User.get(username=user)

    # Insert BUDGET records
    with open(budget_csv_path, mode='r') as csv_file:
        budget_csv = csv.DictReader(csv_file)

        for budget in budget_csv:
            db.Budget(name=budget['name'],
                      description=budget['description'],
                      budget_year=int(budget['budget_year']),
                      created_dt_tm=datetime.now(),
                      updated_dt_tm=datetime.now(),
                      user_id=user.id)

    # Insert BUDGET_ITEM records
    with open(budget_item_csv_path, mode='r') as csv_file:
        budget_item_csv = csv.DictReader(csv_file)

        for budget_item in budget_item_csv:
            db.BudgetItem(name=budget_item['name'],
                          description=budget_item['description'],
                          budget_amount=float(budget_item['budget_amount']),
                          sequence_order=int(budget_item['sequence_order']),
                          created_dt_tm=datetime.now(),
                          updated_dt_tm=datetime.now(),
                          user_id=user.id)

    # Insert ACCOUNT records
    with open(account_csv_path, mode='r') as csv_file:
        account_csv = csv.DictReader(csv_file)

        for account in account_csv:
            db.Account(name=account['name'],
                       description=account['description'],
                       account_number=account['account_number'],
                       account_route_nbr=account['account_route_nbr'],
                       opening_amount=float(account['opening_amount']),
                       created_dt_tm=datetime.now(),
                       updated_dt_tm=datetime.now(),
                       user_id=user.id)

    # Retrieve ACCOUNT and BUDGET_ITEM records as a lookup dictionaries
    # TODO: Find a better way to address looking up foreign key value
    # TODO: There should be a way to query dynamically with Pony
    accounts_lookup: dict = {}
    budget_items_lookup: dict = {}

    accounts = select(a for a in db.Account if a.user_id == user)
    for account in accounts:
        accounts_lookup[account.name] = account.id

    budget_items = select(bi for bi in db.BudgetItem if bi.user_id == user)
    for budget_item in budget_items:
        budget_items_lookup[budget_item.name] = budget_item.id

    # Insert TRANSACTION records
    with open(transaction_csv_path, mode='r') as csv_file:
        transaction_csv = csv.DictReader(csv_file)

        for transaction in transaction_csv:
            db.Transaction(description=transaction['description'],
                           amount=float(transaction['amount']),
                           transaction_dt_tm=datetime.fromisoformat(transaction['transaction_dt_tm']),
                           note=transaction['note'],
                           account_id=accounts_lookup[transaction['account_name']],
                           budget_item_id=budget_items_lookup[transaction['budget_item_name']],
                           created_dt_tm=datetime.now(),
                           updated_dt_tm=datetime.now(),
                           user_id=user.id)

    click.echo('Sample data has been successfully inserted.')


@click.command()
@click.option('--version', is_flag=True, help='Returns the current version of Bootstrap Budget installed.')
@click.option('--setup', is_flag=True, help='Creates the database schema, admin user, and base config.')
@click.option('--reset-admin', is_flag=True, help='Reset admin password.')
@click.option('--reset-bootstrap', is_flag=True, help='Reset your Bootstrap-Budget install (start over).')
@click.option('--backup', is_flag=True, help='Backup all tables to CSV (password-protected zip file).')
def bootstrap(version: bool, setup: bool, reset_admin: bool, reset_bootstrap: bool, backup: bool) -> None:
    """
    The Bootstrap Budget command-line interface utility. Used for initial setup, reset, and backing up data.

    :param version: Returns the current version of Bootstrap Budget installed.
    :param setup: Creates the database schema, admin user, and base config.
    :param reset_admin: Reset admin password.
    :param reset_bootstrap: Reset your Bootstrap-Budget install (start over).
    :param backup: Backup all tables to CSV (password-protected zip file).
    :return: None
    """
    if version:
        click.echo(f'bootstrap-budget v{__version__}')
    else:
        db = get_db()

        if db is not None:
            if reset_bootstrap:
                if click.confirm('Resetting Bootstrap Budget means deleting all of your data and starting over. '
                                 'Are you sure you want to do this?'):
                    db.drop_all_tables(with_all_data=True)
                    db.create_tables()
                    click.echo('The Bootstrap Budget schema has been recreated.')
                    create_admin_account(db)
                    create_config_file()
                    click.echo('Your Boostrap Budget install has been completely reset!')
            elif reset_admin:
                if click.confirm('You are about to reset your admin account. Are you sure you want to do this?'):
                    reset_admin_password(db)
            elif backup:
                # TODO: Complete the backup feature
                click.echo('This does nothing right now, sorry :(')
            else:
                click.echo('Your Boostrap Budget setup is already complete!')
        else:
            if setup:
                db = Database()
                schema.define_entities(db.Entity)
                db.bind(provider='sqlite', filename=f'{CURRENT_WORKING_DIRECTORY}\\bootstrap_budget.db', create_db=True)
                db.generate_mapping(create_tables=True)
                click.echo('The Bootstrap Budget schema has been created.')
                create_admin_account(db)
                create_config_file()
                click.echo('Your Boostrap Budget setup is complete!')
            else:
                click.echo('The Bootstrap Budget database has not been created. Run --setup first.')


@click.command('bootstrap-test')
@click.option('--create-user', is_flag=True, help='Creates a basic user for testing purposes.')
@click.option('--create-sample', is_flag=True, help='Inserts test user with sample data set.')
def bootstrap_test(create_user: bool, create_sample: bool) -> None:
    """
    The Bootstrap Budget TEST command-line interface utility. Used for setting up test users and sample data.

    :param create_user: Creates a basic user for testing purposes.
    :param create_sample: Inserts sample data set with test user.
    :return: None
    """
    db = get_db()

    if get_db() is not None:
        if create_user:
            create_basic_user(db)
        elif create_sample:
            username = create_basic_user(db)
            create_sample_data(db, username)
    else:
        click.echo('The Bootstrap Budget database has not been created. Run --setup first.')


if __name__ == '__main__':
    pass
