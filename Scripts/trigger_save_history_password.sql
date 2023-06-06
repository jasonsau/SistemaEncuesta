DELIMITER //
CREATE OR REPLACE TRIGGER trigger_save_history_password
    AFTER UPDATE ON encuestas_users
    FOR EACH ROW
BEGIN
    IF (NEW.password_user <> OLD.password_user) THEN
        INSERT INTO encuestas_historypassword(
            date_created_history_password,
            password_history_password,
            user_history_password_id
        ) VALUES (
                     NOW(),
                     OLD.password_user,
                     NEW.id_user
                 );
    END IF;
end;
DELIMITER ;
