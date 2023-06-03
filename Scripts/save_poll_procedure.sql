DELIMITER  //
CREATE OR REPLACE PROCEDURE procedure_save_poll(IN json_poll JSON, OUT id_poll INT)
BEGIN
    DECLARE json_poll_general JSON DEFAULT JSON_OBJECT();
    DECLARE json_poll_questions JSON DEFAULT JSON_ARRAY();
    DECLARE json_poll_questions_options JSON DEFAULT JSON_ARRAY();
    DECLARE len_json_poll_questions INT DEFAULT 0;
    DECLARE len_json_poll_questions_options INT DEFAULT 0;

    set json_poll_general = JSON_EXTRACT(json_poll, '$.general');
    set json_poll_questions = JSON_EXTRACT(json_poll, '$.questions');
    set len_json_poll_questions = JSON_LENGTH(json_poll_questions);

    INSERT INTO encuestas_polls (
        date_created_poll,
        title_poll,
        object_poll,
        description_poll,
        instructions_poll,
        date_start_poll,
        date_end_poll,
        token_poll,
        limit_sample_poll,
        user_poll_id
    ) VALUES (
                 SYSDATE(),
                 JSON_VALUE(json_poll_general, '$.name_poll'),
                 JSON_VALUE(json_poll_general, '$.objective_poll'),
                 '',
                 JSON_VALUE(json_poll_general, '$.instructions_poll'),
                 JSON_VALUE(json_poll_general, '$.date_start_poll'),
                 JSON_VALUE(json_poll_general, '$.date_end_poll'),
                 JSON_VALUE(json_poll_general, '$.token_poll'),
                 JSON_VALUE(json_poll_general, '$.limit_sample_poll'),
                 JSON_VALUE(json_poll_general, '$.user_poll_id')
             );
    set @id_poll = LAST_INSERT_ID();
    while len_json_poll_questions > 0 do
            INSERT INTO encuestas_questions(
                title_question,
                type_question_question_id,
                poll_question_id
            ) VALUES(
                        JSON_VALUE(
                                JSON_EXTRACT(
                                        json_poll_questions,
                                        CONCAT('$[', len_json_poll_questions-1, ']')
                                    ),
                                '$.title_question'
                            ),
                        JSON_VALUE(
                                JSON_EXTRACT(
                                        json_poll_questions,
                                        CONCAT('$[', len_json_poll_questions-1, ']')
                                    ),
                                '$.type_question'
                            ),
                        @id_poll
                    );
            set @id_question = LAST_INSERT_ID();

            set json_poll_questions_options = JSON_EXTRACT(
                    json_poll_questions,
                    CONCAT('$[', len_json_poll_questions-1, '].options')
                );

            set len_json_poll_questions_options = JSON_LENGTH(json_poll_questions_options);

            while len_json_poll_questions_options > 0 do
                    INSERT encuestas_optionsquestion(
                        name_option_question,
                        value_option_question,
                        title_option_question,
                        description_option_question,
                        question_option_question_id,
                        id_option
                    ) VALUES (
                                 JSON_VALUE(
                                         JSON_EXTRACT(
                                                 json_poll_questions_options,
                                                 CONCAT('$[', len_json_poll_questions_options - 1, ']')),
                                         '$.name_option'
                                     ),
                                 JSON_VALUE(
                                         JSON_EXTRACT(
                                                 json_poll_questions_options,
                                                 CONCAT('$[', len_json_poll_questions_options - 1, ']')),
                                         '$.value_option'
                                     ),
                                 JSON_VALUE(
                                         JSON_EXTRACT(
                                                 json_poll_questions_options,
                                                 CONCAT('$[', len_json_poll_questions_options - 1, ']')),
                                         '$.title_option'
                                     ),
                                 '',
                                 @id_question,
                                 JSON_VALUE(
                                         JSON_EXTRACT(
                                                 json_poll_questions_options,
                                                 CONCAT('$[', len_json_poll_questions_options - 1, ']')),
                                         '$.id_question'
                                     )
                             );

                    set len_json_poll_questions_options = len_json_poll_questions_options - 1;
                end while;

            set len_json_poll_questions = len_json_poll_questions - 1;
        end while;
end//
DELIMITER ;
