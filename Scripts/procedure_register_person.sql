DELIMITER //
CREATE OR REPLACE PROCEDURE procedure_register_person(
    IN json_data JSON,
    IN password_var VARCHAR(250)
)
BEGIN
    DECLARE id_rol_var INT;
    SELECT id_rol INTO id_rol_var from encuestas_roles where code_rol = 'UN';
    START TRANSACTION;
    INSERT INTO encuestas_persons(name_person, birth_date_person, img_person, email_person, genre_person, active_person)
    VALUES (
               JSON_VALUE(JSON_EXTRACT(json_data, '$.person'), '$.name_person'),
               JSON_VALUE(JSON_EXTRACT(json_data, '$.person'), '$.birth_date_person'),
               JSON_VALUE(JSON_EXTRACT(json_data, '$.person'), '$.img_person'),
               JSON_VALUE(JSON_EXTRACT(json_data, '$.person'), '$.email_person'),
               JSON_VALUE(JSON_EXTRACT(json_data, '$.person'), '$.genre_person'),
               true
           );
    set @id_person = LAST_INSERT_ID();

    INSERT INTO encuestas_users(username_user, password_user, person_user_id, fails_login_user, active_person, password)
    VALUES (
               JSON_VALUE(JSON_EXTRACT(json_data, '$.user'), '$.username_user'),
               password_var,
               @id_person,
               0,
               true,
               password_var
           );
    set @id_user = LAST_INSERT_ID();

    INSERT INTO encuestas_userroles(rol_user_rol_id, user_user_rol_id)
    VALUES(
              id_rol_var,
              @id_user
          );
    COMMIT;
end//
DELIMITER ;
