from fastapi import APIRouter, Depends, HTTPException
from utils.postgres_connector import PostgresConnector
import psycopg
from models.user import UpdateUserModel
import hashlib
import json

router = APIRouter()

connection = PostgresConnector(db_name="shop_db")


@router.get("/show_all_users")
async def show_all_users(offset: int, limit: int, cursor: psycopg.cursor.Cursor = Depends(connection.get_cursor)):
    try:
        sql_command = "SELECT user_id, user_name, first_name, second_name from users OFFSET %s LIMIT %s"
        cursor.execute(sql_command, (offset, limit,))
        result = cursor.fetchall()
        cursor.close()
    except Exception as e:
        print(e)
        cursor.connection.rollback()
        cursor.close()
        raise HTTPException(status_code=400, detail="Check your data please")
    return result


@ router.get("/user_info")
async def get_user_info(id: int, cursor: psycopg.Cursor = Depends(connection.get_cursor)):
    try:
        sql_command = "SELECT user_id, user_name, first_name, second_name from users WHERE user_id = %s"
        cursor.execute(sql_command, (id,))
        result = cursor.fetchone()
        cursor.close()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="Check your data please")
    return result


@ router.get("/find_by_name")
async def find_by_name(first_name: str = None, second_name: str = None, cursor: psycopg.Cursor = Depends(connection.get_cursor)):
    try:
        first_name += "%"
        second_name += "%"
        if first_name and second_name:
            sql_command = "SELECT user_id, user_name, first_name, second_name from users WHERE first_name LIKE %s AND second_name LIKE %s"
            cursor.execute(sql_command, (first_name, second_name))
        elif first_name and not second_name:
            sql_command = "SELECT user_id, user_name, first_name, second_name from users WHERE first_name LIKE %s"
            cursor.execute(sql_command, (first_name,))
        elif first_name and second_name:
            sql_command = "SELECT user_id, user_name, first_name, second_name from users WHERE second_name LIKE %s"
            cursor.execute(sql_command, (second_name, ))

        result = cursor.fetchall()
        cursor.close()
        if result:
            return result
        return "Ничего не найдено"
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="Check your data please")


@ router.get("/find_by_login")
async def find_by_login(login, cursor: psycopg.Cursor = Depends(connection.get_cursor)):
    try:
        login += "%"
        sql_command = "SELECT user_id, user_name, first_name, second_name FROM users WHERE user_name LIKE %s"
        cursor.execute(sql_command, (login,))
        result = cursor.fetchall()
        cursor.close()
        if result:
            return result
        else:
            return []
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="Check your data please")


@ router.post("/new_user")
async def new_user(new_user: UpdateUserModel, cursor: psycopg.Cursor = Depends(connection.get_cursor)):
    user_id = -1
    try:
        sql_command: str = "INSERT INTO users (user_name, first_name, second_name, password) VALUES (%s, %s, %s, %s) RETURNING user_id, user_name, first_name, second_name"
        if new_user.password:
            password: str = hashlib.sha256(
                new_user.password.encode()).hexdigest()
        data: tuple = (new_user.user_name, new_user.first_name,
                       new_user.second_name, password)
        cursor.execute(sql_command, data)
        result = cursor.fetchone()
        user_id = result[0]
        cursor.connection.commit()
    except Exception as e:
        print(e)
        cursor.connection.rollback()
        cursor.close()
        raise HTTPException(
            status_code=400, detail="Can't create user")
    cursor.close()
    return {"message": f"User {user_id} created successfully"}


@ router.put("/update")
async def update(user_id: int, updated_user: UpdateUserModel, cursor: psycopg.Cursor = Depends(connection.get_cursor)):
    try:
        if updated_user.password:
            updated_user.password = hashlib.sha256(
                updated_user.password.encode()).hexdigest()
        print(user_id)
        updated_user_dict = UpdateUserModel.model_dump(
            updated_user, exclude_none=True)
        columns_to_update = ', '.join(
            [f"{key} = %s" for key in updated_user_dict.keys()])
        sql = f"UPDATE users SET {
            columns_to_update} WHERE user_id = %s RETURNING user_id, user_name, first_name, second_name"
        values = list(updated_user_dict.values())
        cursor.execute(sql, values + [user_id])
        result = cursor.fetchone()
        user_id = result[0]
        cursor.connection.commit()
    except Exception as e:
        print(e)
        cursor.connection.rollback()
        cursor.close()
        raise HTTPException(
            status_code=400, detail="Can't create user")
    cursor.close()
    return {"message": "User updated successfully"}


@ router.delete("/delete")
async def delete_by_id(user_id: int, cursor: psycopg.cursor.Cursor = Depends(connection.get_cursor)):
    try:
        id_in_tuple: tuple = (user_id,)
        sql_command = "DELETE FROM users WHERE user_id=%s"
        cursor.execute(sql_command, id_in_tuple)
        cursor.connection.commit()
    except Exception as e:
        print(e)
        cursor.connection.rollback()
        cursor.close()
        raise HTTPException(
            status_code=400, detail="Can't delete user")
    cursor.close()
    return {"message": "User deleted successfully"}
