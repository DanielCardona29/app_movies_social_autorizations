from typing import Annotated

from pydantic import BaseModel, EmailStr, Field

from src.utils.constants import PASSWORD_REGULAR_EXPRESSION

from ...database.db_consults import (
    CREATE_TABLE_USERS,
    INSERT_USER,
    VALIDATE_IF_TABLE_USERS_EXISTS,
)
from ..db_connect import cursor

PasswordType = Annotated[
    None,
    Field(min_length=8, max_length=20, regex=PASSWORD_REGULAR_EXPRESSION, default="", description="Debe contener al menos una mayúscula, un número y un caracter especial, entre 8 y 20 caracteres"),
]


class user(BaseModel):
    name: str = Field(..., min_length=3, max_length=255)
    email: str = EmailStr
    password: PasswordType
    twitter_id: str = ""
    google_id: str = ""
    facebook_id: str = ""


class dbServices:
    async def createUsersTable(self):
        """Create the table users"""
        cursor.execute(CREATE_TABLE_USERS)
        response_create_table = cursor.fetchall()
        print(response_create_table)
        if response_create_table:
            return True
        return False

    async def validateTableUsersExists(self):
        """Validate if the table users exists and create it if not"""
        try:
            cursor.execute(VALIDATE_IF_TABLE_USERS_EXISTS)
            table_exist = cursor.fetchall()[0]

            if table_exist:
                return True

            return self.createUsersTable()

        except Exception as e:
            print(f"Error on consult users table {e}")
            return False

    def isertUserData(self, data: user):
        """Insert data on the table users"""
        cursor.execute(INSERT_USER, (data.name, data.email, data.password, data.twitter_id, data.google_id, data.facebook_id))
        response_insert_user = cursor.fetchall()
        print(response_insert_user)
        if response_insert_user:
            return True
        return False

    async def writeUser(
        self,
        name: str,
        email: str,
        password: str,
        twitter_id: str,
        google_id: str,
        facebook_id: str,
    ):
        """Write a user on the table users"""

        try:
            # Validate if the table exists before to write the user.
            table_exist = await self.validateTableUsersExists()

            if not table_exist:
                raise Exception("Error: users table not exists and can't be created")

            # tramsform the data to the user model
            data = user(name=name, email=email, password=password, twitter_id=twitter_id, google_id=google_id, facebook_id=facebook_id)
            return self.isertUserData(data)

        except Exception as e:
            print(f"Error on write user {e}")
            return False
