from datetime import datetime
from pony.orm import Database, composite_key, Optional, PrimaryKey, Required, Set


def define_entities(db_entity: Database().Entity) -> None:
    """
    Defines the Bootstrap-Budget schema in the form of class objects for mapping to the database.

    :param db_entity:
    :return: None
    """
    class User(db_entity):
        _table_ = 'USER'

        id = PrimaryKey(int, auto=True)
        last_name = Optional(str, nullable=True)
        first_name = Optional(str, nullable=True)
        middle_name = Optional(str, nullable=True)
        username = Required(str, unique=True)
        address_line_1 = Optional(str, nullable=True)
        address_line_2 = Optional(str, nullable=True)
        city = Optional(str, nullable=True)
        state = Optional(str, nullable=True)
        zipcode = Optional(str, nullable=True)
        email = Optional(str, nullable=True)
        phone_number = Optional(str, nullable=True)
        hash = Required(str)
        created_dt_tm = Required(datetime)
        updated_dt_tm = Required(datetime)
        is_active = Required(bool, default=True)
        accounts = Set('Account')
        configs = Set('Config')
        budgets = Set('Budget')
        budget_items = Set('BudgetItem')
        transactions = Set('Transaction')
        user_budgets = Set('UserBudget')
    """
    CREATE TABLE "USER" (
        "id" INTEGER PRIMARY KEY AUTOINCREMENT,
        "last_name" TEXT,
        "first_name" TEXT,
        "middle_name" TEXT,
        "username" TEXT UNIQUE NOT NULL,
        "address_line_1" TEXT,
        "address_line_2" TEXT,
        "city" TEXT,
        "state" TEXT,
        "zipcode" TEXT,
        "email" TEXT,
        "phone_number" TEXT,
        "hash" TEXT NOT NULL,
        "created_dt_tm" DATETIME NOT NULL,
        "updated_dt_tm" DATETIME NOT NULL,
        "is_active" BOOLEAN NOT NULL
    );
    """

    class Config(db_entity):
        _table_ = 'CONFIG'

        id = PrimaryKey(int, auto=True)
        name = Required(str, unique=True)
        description = Optional(str, nullable=True)
        config_value = Optional(str, nullable=True)
        config_value_type = Required(int, default=0)
        created_dt_tm = Required(datetime)
        updated_dt_tm = Required(datetime)
        is_active = Required(bool, default=True)
        user_id = Required(User)
        composite_key(name, user_id)
    """
    CREATE TABLE "CONFIG" (
        "id" INTEGER PRIMARY KEY AUTOINCREMENT,
        "name" TEXT UNIQUE NOT NULL,
        "description" TEXT,
        "config_value" TEXT,
        "config_value_type" INTEGER NOT NULL,
        "created_dt_tm" DATETIME NOT NULL,
        "updated_dt_tm" DATETIME NOT NULL,
        "is_active" BOOLEAN NOT NULL,
        "user_id" INTEGER NOT NULL REFERENCES "USER" ("id") ON DELETE CASCADE,
        CONSTRAINT "unq_config__name_user_id" UNIQUE ("name", "user_id")
    );
    
    CREATE INDEX "idx_config__user_id" ON "CONFIG" ("user_id");
    """

    class Budget(db_entity):
        _table_ = 'BUDGET'

        id = PrimaryKey(int, auto=True)
        name = Required(str)
        description = Optional(str, nullable=True)
        budget_year = Required(int)
        created_dt_tm = Required(datetime)
        updated_dt_tm = Required(datetime)
        is_active = Required(bool, default=True)
        user_id = Required(User)
        user_budgets = Set('UserBudget')
        composite_key(name, user_id)
    """
    CREATE TABLE "BUDGET" (
        "id" INTEGER PRIMARY KEY AUTOINCREMENT,
        "name" TEXT NOT NULL,
        "description" TEXT,
        "budget_year" INTEGER NOT NULL,
        "created_dt_tm" DATETIME NOT NULL,
        "updated_dt_tm" DATETIME NOT NULL,
        "is_active" BOOLEAN NOT NULL,
        "user_id" INTEGER NOT NULL REFERENCES "USER" ("id") ON DELETE CASCADE,
        CONSTRAINT "unq_budget__name_user_id" UNIQUE ("name", "user_id")
    );
    
    CREATE INDEX "idx_budget__user_id" ON "BUDGET" ("user_id");
    """

    class UserBudget(db_entity):
        _table_ = 'USER_BUDGET'

        id = PrimaryKey(int, auto=True)
        permissions = Required(int)
        created_dt_tm = Required(datetime)
        updated_dt_tm = Required(datetime)
        is_active = Required(bool, default=True)
        user_id = Required(User)
        budget_id = Required(Budget)
    """
    CREATE TABLE "USER_BUDGET" (
        "id" INTEGER PRIMARY KEY AUTOINCREMENT,
        "permissions" INTEGER NOT NULL,
        "created_dt_tm" DATETIME NOT NULL,
        "updated_dt_tm" DATETIME NOT NULL,
        "is_active" BOOLEAN NOT NULL,
        "user_id" INTEGER NOT NULL REFERENCES "USER" ("id") ON DELETE CASCADE,
        "budget_id" INTEGER NOT NULL REFERENCES "BUDGET" ("id") ON DELETE CASCADE
    );
    
    CREATE INDEX "idx_user_budget__budget_id" ON "USER_BUDGET" ("budget_id");
    CREATE INDEX "idx_user_budget__user_id" ON "USER_BUDGET" ("user_id");
    """

    class BudgetItem(db_entity):
        _table_ = 'BUDGET_ITEM'

        id = PrimaryKey(int, auto=True)
        name = Required(str)
        description = Optional(str, nullable=True)
        budget_amount = Required(float, default=0)
        sequence_order = Required(int, default=99)
        created_dt_tm = Required(datetime)
        updated_dt_tm = Required(datetime)
        is_active = Required(bool, default=True)
        user_id = Required(User)
        transactions = Set('Transaction')
        composite_key(name, user_id)
    """
    CREATE TABLE "BUDGET_ITEM" (
        "id" INTEGER PRIMARY KEY AUTOINCREMENT,
        "name" TEXT NOT NULL,
        "description" TEXT,
        "budget_amount" REAL NOT NULL,
        "sequence_order" INTEGER NOT NULL,
        "created_dt_tm" DATETIME NOT NULL,
        "updated_dt_tm" DATETIME NOT NULL,
        "is_active" BOOLEAN NOT NULL,
        "user_id" INTEGER NOT NULL REFERENCES "USER" ("id") ON DELETE CASCADE,
        CONSTRAINT "unq_budget_item__name_user_id" UNIQUE ("name", "user_id")
    );
    
    CREATE INDEX "idx_budget_item__user_id" ON "BUDGET_ITEM" ("user_id");
    """

    class Account(db_entity):
        _table_ = 'ACCOUNT'

        id = PrimaryKey(int, auto=True)
        name = Required(str)
        description = Optional(str, nullable=True)
        account_number = Optional(str, nullable=True)
        account_route_nbr = Optional(str, nullable=True)
        opening_amount = Required(float, default=0)
        created_dt_tm = Required(datetime)
        updated_dt_tm = Required(datetime)
        is_active = Required(bool, default=True)
        user_id = Required(User)
        transactions = Set('Transaction')
        composite_key(name, user_id)
    """
    CREATE TABLE "ACCOUNT" (
        "id" INTEGER PRIMARY KEY AUTOINCREMENT,
        "name" TEXT NOT NULL,
        "description" TEXT,
        "account_number" TEXT,
        "account_route_nbr" TEXT,
        "opening_amount" REAL NOT NULL,
        "created_dt_tm" DATETIME NOT NULL,
        "updated_dt_tm" DATETIME NOT NULL,
        "is_active" BOOLEAN NOT NULL,
        "user_id" INTEGER NOT NULL REFERENCES "USER" ("id") ON DELETE CASCADE,
        CONSTRAINT "unq_account__name_user_id" UNIQUE ("name", "user_id")
    );
    
    CREATE INDEX "idx_account__user_id" ON "ACCOUNT" ("user_id");
    """

    class Transaction(db_entity):
        _table_ = 'TRANSACTION'

        id = PrimaryKey(int, auto=True)
        description = Optional(str, nullable=True)
        amount = Required(float, default=0)
        transaction_dt_tm = Required(datetime)
        note = Optional(str, nullable=True)
        created_dt_tm = Required(datetime)
        updated_dt_tm = Required(datetime, nullable=True)
        is_active = Required(bool, default=True)
        user_id = Required(User)
        account_id = Required(Account)
        budget_item_id = Required(BudgetItem)
    """
    CREATE TABLE "TRANSACTION" (
        "id" INTEGER PRIMARY KEY AUTOINCREMENT,
        "description" TEXT,
        "amount" REAL NOT NULL,
        "transaction_dt_tm" DATETIME NOT NULL,
        "note" TEXT,
        "created_dt_tm" DATETIME NOT NULL,
        "updated_dt_tm" DATETIME,
        "is_active" BOOLEAN NOT NULL,
        "user_id" INTEGER NOT NULL REFERENCES "USER" ("id") ON DELETE CASCADE,
        "account_id" INTEGER NOT NULL REFERENCES "ACCOUNT" ("id") ON DELETE CASCADE,
        "budget_item_id" INTEGER NOT NULL REFERENCES "BUDGET_ITEM" ("id") ON DELETE CASCADE
    );
    
    CREATE INDEX "idx_transaction__account_id" ON "TRANSACTION" ("account_id");
    CREATE INDEX "idx_transaction__budget_item_id" ON "TRANSACTION" ("budget_item_id");
    CREATE INDEX "idx_transaction__user_id" ON "TRANSACTION" ("user_id");
    """
