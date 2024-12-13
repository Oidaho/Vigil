# ./VK-Vigil/database/scripts.py
from .db import db_instance


def delete_expired_warns():
    with db_instance.atomic():
        db_instance.execute_sql("DELETE FROM warns WHERE expired <= NOW();")


def delete_expired_queue():
    with db_instance.atomic():
        db_instance.execute_sql("DELETE FROM queue WHERE expired <= NOW();")


# TODO: Edit according to the future structure of the application.
def set_conversation_default_settings():
    with db_instance.atomic():
        db_instance.execute_sql("""
        CREATE OR REPLACE FUNCTION setup_conversation_settings()
        RETURNS TRIGGER AS $$
        BEGIN
            IF (NEW.mark != 'LOG') THEN
                INSERT INTO delays(bpid, setting, delay)
                VALUES (NEW.id, 'slow_mode', 1),
                    (NEW.id, 'account_age', 7),
                    (NEW.id, 'menu_session', 5);

                INSERT INTO delays(bpid, setting, delay)
                VALUES (NEW.id, 'green_zone', 1),
                    (NEW.id, 'yellow_zone', 7),
                    (NEW.id, 'red_zone', 30);

                INSERT INTO settings(bpid, name, status, destination, points)
                VALUES (NEW.id, 'photo', 'active', 'filter', 1),
                    (NEW.id, 'video', 'active', 'filter', 1),
                    (NEW.id, 'audio', 'active', 'filter', 1),
                    (NEW.id, 'audio_message', 'active', 'filter', 1),
                    (NEW.id, 'link', 'active', 'filter', 1),
                    (NEW.id, 'poll', 'active', 'filter', 1),
                    (NEW.id, 'wall', 'active', 'filter', 1),
                    (NEW.id, 'doc', 'active', 'filter', 1),
                    (NEW.id, 'app_action', 'active', 'filter', 1),
                    (NEW.id, 'graffiti', 'active', 'filter', 1),
                    (NEW.id, 'sticker', 'active', 'filter', 1),
                    (NEW.id, 'forward', 'active', 'filter', 1),
                    (NEW.id, 'reply', 'active', 'filter', 1),
                    (NEW.id, 'geo', 'active', 'filter', 1);

                INSERT INTO settings(bpid, name, status, destination, points)
                VALUES (NEW.id, 'curse_words', 'inactive', 'system', 1),
                    (NEW.id, 'account_age', 'inactive', 'system', 10),
                    (NEW.id, 'slow_mode', 'inactive', 'system', 2),
                    (NEW.id, 'open_pm', 'inactive', 'system', 2),
                    (NEW.id, 'link_filter', 'inactive', 'system', 3),
                    (NEW.id, 'hard_link_filter', 'inactive', 'system', 1);
            END IF;
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;

        CREATE TRIGGER setup_peer_settings
        AFTER INSERT ON peers
        FOR EACH ROW
        EXECUTE FUNCTION setup_peer_settings();
        """)
