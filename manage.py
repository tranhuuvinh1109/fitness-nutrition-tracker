import unittest
import os

import click
import coverage
from passlib.hash import pbkdf2_sha256
from sqlalchemy import text

from app.db import db
from app.models import (
    UserModel
)


@click.option(
    "--pattern", default="tests_*.py", help="Test search pattern", required=False
)
def cov(pattern):
    """
    Run the unit tests with coverage
    """
    cov = coverage.coverage(branch=True, include="app/*")
    cov.start()
    tests = unittest.TestLoader().discover("tests", pattern=pattern)
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        cov.stop()
        cov.save()
        print("Coverage Summary:")
        cov.report()
        cov.erase()
        return 0
    return 1


@click.option(
    "--pattern", default="tests_*.py", help="Test search pattern", required=False
)
def cov_html(pattern):
    """
    Run the unit tests with coverage and generate an HTML report.
    """
    cov = coverage.coverage(branch=True, include="app/*")
    cov.start()

    tests = unittest.TestLoader().discover("tests", pattern=pattern)
    result = unittest.TextTestRunner(verbosity=2).run(tests)

    if result.wasSuccessful():
        cov.stop()
        cov.save()

        print("Coverage Summary:")
        cov.report()
        cov.html_report(directory="report/htmlcov")
        cov.erase()
        return 0

    return 1


@click.option("--pattern", default="tests_*.py", help="Test pattern", required=False)
def tests(pattern):
    """
    Run the tests without code coverage
    """
    tests = unittest.TestLoader().discover("tests", pattern=pattern)
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


def create_db():
    """
    Create Database.
    """
    db.create_all()
    db.session.commit()


def reset_db():
    """
    Reset Database.
    """
    # Drop old role/permission tables first (if they exist)
    # These tables may have foreign key constraints
    try:
        db.session.execute(text("DROP TABLE IF EXISTS user_role CASCADE"))
        db.session.execute(text("DROP TABLE IF EXISTS role_permission CASCADE"))
        db.session.execute(text("DROP TABLE IF EXISTS role CASCADE"))
        db.session.execute(text("DROP TABLE IF EXISTS permission CASCADE"))
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Note: Some old tables may not exist: {e}")
    
    # Now drop all tables defined in models
    db.drop_all()
    db.create_all()
    db.session.commit()


def drop_db():
    """
    Drop Database.
    """
    # Drop old role/permission tables first (if they exist)
    try:
        db.session.execute(db.text("DROP TABLE IF EXISTS user_role CASCADE"))
        db.session.execute(db.text("DROP TABLE IF EXISTS role_permission CASCADE"))
        db.session.execute(db.text("DROP TABLE IF EXISTS role CASCADE"))
        db.session.execute(db.text("DROP TABLE IF EXISTS permission CASCADE"))
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Note: Some old tables may not exist: {e}")
    
    # Now drop all tables defined in models
    db.drop_all()
    db.session.commit()


def init_db_user():
    # Users are created with default role=2 (regular user)
    # Admin users should have role=1
    pass


def create_user_admin(username="admin"):
    """
    Create User Admin.
    """
    admin = UserModel.query.filter_by(username=username).first()

    if admin is None:
        print("user-admin is not created before!")
        init_db_user()
    else:
        print("user-admin is created!")


@click.argument("filename")
def run_migration(filename):
    """
    Run a specific SQL migration file from migrations folder.
    Usage: flask run-migration migration_update_chat_message.sql
    """
    migrations_dir = os.path.join(os.path.dirname(__file__), "migrations")
    file_path = os.path.join(migrations_dir, filename)
    
    if not os.path.exists(file_path):
        click.echo(f"Error: File {file_path} not found!", err=True)
        return 1
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        click.echo(f"Running migration: {filename}")
        # Execute SQL file
        db.session.execute(text(sql_content))
        db.session.commit()
        click.echo(f"✓ Migration {filename} completed successfully!")
        return 0
    except Exception as e:
        db.session.rollback()
        click.echo(f"✗ Error running migration: {str(e)}", err=True)
        return 1


def init_app(app):
    if app.config["APP_ENV"] == "production":
        commands = [create_db, reset_db, drop_db, run_migration]
    else:
        commands = [
            create_db,
            reset_db,
            drop_db,
            cov_html,
            cov,
            run_migration,
        ]

    for command in commands:
        app.cli.add_command(app.cli.command()(command))
