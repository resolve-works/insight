CREATE OR REPLACE TRIGGER set_file_owner
    BEFORE INSERT ON private.files FOR EACH ROW
    EXECUTE FUNCTION set_owner ();

CREATE OR REPLACE TRIGGER set_prompt_owner
    BEFORE INSERT ON private.prompts FOR EACH ROW
    EXECUTE FUNCTION set_owner ();

CREATE OR REPLACE TRIGGER set_document_owner
    BEFORE INSERT ON private.documents FOR EACH ROW
    EXECUTE FUNCTION set_owner ();

CREATE OR REPLACE TRIGGER set_file_updated_at
    BEFORE UPDATE ON private.files FOR EACH ROW
    EXECUTE FUNCTION set_updated_at ();

CREATE OR REPLACE TRIGGER set_prompt_updated_at
    BEFORE UPDATE ON private.prompts FOR EACH ROW
    EXECUTE FUNCTION set_updated_at ();

CREATE OR REPLACE TRIGGER set_document_updated_at
    BEFORE UPDATE ON private.documents FOR EACH ROW
    EXECUTE FUNCTION set_updated_at ();

