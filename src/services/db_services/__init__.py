from typing import Annotated, Optional

from pydantic import BaseModel, EmailStr, Field, field_validator

from src.utils.constants import PASSWORD_REGULAR_EXPRESSION

from ...database.db_consults import (
    CREATE_TABLE_USERS,
    INSERT_USER,
    VALIDATE_IF_USER_EXIST,
    VALIDATE_IF_X_TABLE_EXIST,
)
from ..db_connect import conn

PasswordType = Annotated[
    None,
    Field(
        min_length=8,
        max_length=20,
        pattern=PASSWORD_REGULAR_EXPRESSION,
        default="",
        description="Debe contener al menos una mayúscula, un número y un caracter especial, entre 8 y 20 caracteres",
    ),
]


class user(BaseModel):
    name: str = Field(..., min_length=3, max_length=255)
    email: str = EmailStr
    password: Optional[str] = None
    twitter_id: Optional[str] = None
    google_id: Optional[str] = None
    facebook_id: Optional[str] = None

    @field_validator("password", "twitter_id", "google_id", "facebook_id", mode="before")
    @classmethod
    def convert_empty_string_to_none(cls, v):
        return v or ""


class twitterUser(user):
    twitter_id: str


class dbServices:
    """Class to manage the db services
    METHODS: runModifyConsult, runSelectConsult, createUsersTable, validateTableUsersExists, isertUserData, writeUser

      runModifyConsult: Execute a consult that modify the db\n
      runSelectConsult: Execute a consult that return data\n
      createUsersTable: Create the table users\n
      validateTableUsersExists: Validate if the table users exists and create it if not\n
      isertUserData: Insert data on the table users\n
      writeUser: Write a user on the table users\n
    """

    # this method is used to modify the db
    def runModifyConsult(self, consult, data=None):
        """Execute a consult that modify the db
        Valids: CREATE, INSERT, UPDATE, DELETE\n
        return True if the consult was executed successfully\n
        returns an exception if the consult was not executed successfully
        """
        try:
            cursor = conn.cursor()
            cursor.execute(consult, data)
            # save changes
            conn.commit()
            cursor.close()
            # return True if the consult was executed successfully
            return True
        except Exception as e:
            # Sontimg went wrong with the consult
            raise e

    def runSelectConsult(self, consult, data=None):
        """Execute a consult that return data
        Valids: SELECT
         return the data if the consult was executed successfully\n
         returns true if not data was found but the consult was executed successfullys\n
         returns an exception if the consult was not executed successfully
        """
        try:
            cursor = conn.cursor()
            cursor.execute(consult, data)
            response = cursor.fetchall()
            cursor.close()
            if response:
                return response
            return True
        except Exception as e:
            raise e

    def createTable(self, data=None):
        """Creates a user table if not exists
        return True if the table was created successfully\n
        returns an exception if the table was not created successfully
        """
        response_create_table = self.runModifyConsult(CREATE_TABLE_USERS, data)
        if response_create_table:
            return True
        return False

    def validateIfExist(self, consult, data=None):
        """
        Validates if the table users exists and create it if not
        return True if the table exists\n
        returns an exception if the table was not created successfully
        """
        try:
            table_exist = self.runSelectConsult(consult, data)[0]
            if table_exist[0]:
                return True
            return self.createTable(data=data)

        except Exception as e:
            print(f"Error on consult users table {e}")
            return False

    def isertUserData(self, data: user):
        """Insert one user data on the table users
        return True if the user was inserted successfully\n
        returns an exception if the user was not inserted successfully
        """
        response_insert_user = self.runModifyConsult(
            INSERT_USER, (data.name, data.email, data.password, data.twitter_id, data.google_id, data.facebook_id)
        )
        print(response_insert_user)
        if response_insert_user:
            return True
        return False

    def writeUser(
        self,
        name: str,
        email: str,
        password: str = None,
        twitter_id: str = None,
        google_id: str = None,
        facebook_id: str = None,
    ):
        """start all the process to write a user on the table users
        return True if the user was written successfully\n
        returns an exception if the user was not written successfully
        """
        try:
            # Validate if the table exists before to write the user.
            table_exist = self.validateIfExist(VALIDATE_IF_X_TABLE_EXIST, ("users",))
            if not table_exist:
                raise Exception("Error: users table not exists and can't be created")
            # tramsform the data to the user model
            data = user(
                name=name,
                email=email,
                password=password,
                twitter_id=twitter_id,
                google_id=google_id,
                facebook_id=facebook_id,
            )
            return self.isertUserData(data)
        except Exception as e:
            print(f"Error on write user {e}")
            return False

    def validateIfAnUserExist(self, email: str):
        """
        Validate if an user exists on the table users
        return True if the user exists\n
        return False if the user not exists\n
        """
        try:
            # Validate if the email is not empty
            if not email:
                raise Exception("Error: email is required")
            response = self.runSelectConsult(VALIDATE_IF_USER_EXIST, (email,))[0]
            return response[0]
        except Exception as e:
            print(f"Error on validate if user exists {e}")
            return False
        pass
