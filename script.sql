
/*Types Questions*/
INSERT encuestas_typequestion(id_type_question, name_type_question, description_type_question)
VALUES (1, 'Texto', 'Respuesta libre'),
    (2, 'Opcion Multiple', 'Respuesta de opcion multiple'),
    (3, 'Opcion unica', 'Respuesta de una sola opcion');

/*Personas*/

INSERT encuestas_persons(id_person, name_person, email_person, birth_date_person, img_person, genre_person, active_person)
VALUES (1, 'Jason Saul Martinez Argueta', 'ma17092@ues.edu.sv', '1998-10-10', 'https://scontent.fsal3-1.fna.fbcdn.net/v/t1.0-9/118003644_10224136183191788_917898764577970446_o.jpg?_nc_cat=102&ccb=2', 'M', 1);

INSERT INTO encuestas_roles(id_rol, name_rol, code_rol, description_rol, active_rol)
VALUES(1, 'Usuario normal', 'UN' ,'Usuario normal de la aplicacion puede crear encuestas y lo relacionado a ello', true);
INSERT INTO encuestas_roles(id_rol, name_rol, code_rol, description_rol, active_rol)
VALUES(2, 'Usuario Administrador', 'UA', 'Usuario que tiene el control de las acciones de los usuarios normales', true);

INSERT INTO encuestas_userroles(id_user_rol, user_user_rol_id, rol_user_rol_id)
VALUES(3, 2, 2);

INSERT INTO encuestas_permissions(id_permission, name_permission, description_permission, active_permission, route_permission)
VALUES(1, 'Crear encuesta', 'Permite crear una encuesta', true, 'create-poll');
INSERT INTO encuestas_permissions(id_permission, name_permission, description_permission, active_permission, route_permission)
VALUES(2, 'Home', 'Home de encuestas', true, 'home');
INSERT INTO encuestas_permissions(id_permission, name_permission, description_permission, active_permission, route_permission)
VALUES(3, 'Home admin', 'Home de admin', true, 'home-admin');


INSERT INTO encuestas_rolpermissions(id_rol_permission, rol_rol_permission_id, permission_rol_permission_id)
VALUES (1, 1, 1);
INSERT INTO encuestas_rolpermissions(id_rol_permission, rol_rol_permission_id, permission_rol_permission_id)
VALUES (2, 1, 2);
INSERT INTO encuestas_rolpermissions(id_rol_permission, rol_rol_permission_id, permission_rol_permission_id)
VALUES (3, 2, 3);