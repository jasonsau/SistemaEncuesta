DELIMITER //
CREATE OR REPLACE PROCEDURE procedure_check_permissions(IN id_user INT, IN name_route VARCHAR(50), OUT bool_check BOOLEAN)
BEGIN
    DECLARE route_permission_var longtext;
    DECLARE done INT DEFAULT FALSE;
    DECLARE cursor_permissions  CURSOR FOR
        SELECT permission.route_permission from encuestas_userroles as user_rol
                                                    inner join encuestas_roles as rol on user_rol.rol_user_rol_id = rol.id_rol
                                                    inner join encuestas_rolpermissions er on rol.id_rol = er.rol_rol_permission_id
                                                    inner join encuestas_permissions as permission on permission.id_permission = er.permission_rol_permission_id
        where user_user_rol_id = id_user;


    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    OPEN cursor_permissions;
    SET bool_check = false;

    loop_check: LOOP
        FETCH cursor_permissions INTO route_permission_var;
        IF done THEN
            LEAVE loop_check;
        END IF;
        IF route_permission_var = name_route THEN
            SET bool_check = true;
        END IF;
    END LOOP loop_check;
    select bool_check as result_check;
end//
DELIMITER ;

call procedure_check_permissions(2, 'home', @bool_check);