
/*Types Questions*/
INSERT encuestas_typequestion(id_type_question, name_type_question, description_type_question)
VALUES (1, 'Texto', 'Respuesta libre'),
    (2, 'Opcion Multiple', 'Respuesta de opcion multiple'),
    (3, 'Opcion unica', 'Respuesta de una sola opcion')

/*Personas*/

INSERT encuestas_persons(id_person, name_person, email_person, birth_date_person, img_person, genre_person, active_person)
VALUES (1, 'Jason Saul Martinez Argueta', 'ma17092@ues.edu.sv', '1998-10-10', 'https://scontent.fsal3-1.fna.fbcdn.net/v/t1.0-9/118003644_10224136183191788_917898764577970446_o.jpg?_nc_cat=102&ccb=2', 'M', 1);
