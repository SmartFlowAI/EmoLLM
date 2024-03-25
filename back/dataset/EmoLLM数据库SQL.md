# 建库SQL语句：

```sql
-- Database: EmoLLM

-- DROP DATABASE IF EXISTS "EmoLLM";

CREATE DATABASE "EmoLLM"
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'Chinese (Simplified)_China.936'
    LC_CTYPE = 'Chinese (Simplified)_China.936'
    LOCALE_PROVIDER = 'libc'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;
```

## 1、创建Users表：

```sql
-- Table: public.Users

-- DROP TABLE IF EXISTS public."Users";

CREATE TABLE IF NOT EXISTS public."Users"
(
    user_id integer NOT NULL DEFAULT nextval('users_id_seq'::regclass),
    phone_number "char" NOT NULL,
    name "char" NOT NULL,
    gender boolean NOT NULL,
    school "char" NOT NULL,
    create_time time with time zone,
    llog_in_time time with time zone,
    email "char",
    user_state bigint DEFAULT 1,
    CONSTRAINT "Users_pkey" PRIMARY KEY (user_id),
    CONSTRAINT phone_number UNIQUE (phone_number)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public."Users"
    OWNER to postgres;

COMMENT ON COLUMN public."Users".user_id
    IS '用户id';

COMMENT ON COLUMN public."Users".phone_number
    IS '电话号码';

COMMENT ON COLUMN public."Users".name
    IS '昵称';

COMMENT ON COLUMN public."Users".gender
    IS '性别，0代表男，1代表女';

COMMENT ON COLUMN public."Users".school
    IS '学校';

COMMENT ON COLUMN public."Users".create_time
    IS '用户创建时间';

COMMENT ON COLUMN public."Users".llog_in_time
    IS '用户最后一次登陆时间';

COMMENT ON COLUMN public."Users".email
    IS '预留字段，为以后可能的收集做准备';

COMMENT ON COLUMN public."Users".user_state
    IS '0表示已删除，1表示正常状态，2表示用户被禁用';
```

## 2、创建Characters表：

```sql
-- Table: public.Characters

-- DROP TABLE IF EXISTS public."Characters";

CREATE TABLE IF NOT EXISTS public."Characters"
(
    character_id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    user_id integer NOT NULL,
    image bytea,
    description "char",
    character_name "char" NOT NULL,
    character_state boolean,
    CONSTRAINT "Characters_pkey" PRIMARY KEY (character_id),
    CONSTRAINT user_id FOREIGN KEY (user_id)
        REFERENCES public."Users" (user_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public."Characters"
    OWNER to postgres;

COMMENT ON COLUMN public."Characters".character_id
    IS '模型id';

COMMENT ON COLUMN public."Characters".user_id
    IS '用户id';

COMMENT ON COLUMN public."Characters".image
    IS '用户与模型的聊天背景';

COMMENT ON COLUMN public."Characters".description
    IS '用户对自定义模型的描述';

COMMENT ON COLUMN public."Characters".character_name
    IS '模型名称';

COMMENT ON COLUMN public."Characters".character_state
    IS '模型状态，0表示角色已被用户删除，1表示未删除';
```

## 3、创建Sessions表：

```sql
-- Table: public.Sessions

-- DROP TABLE IF EXISTS public."Sessions";

CREATE TABLE IF NOT EXISTS public."Sessions"
(
    session_id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    user_id integer NOT NULL,
    character_id integer NOT NULL,
    start_time time with time zone,
    end_time time with time zone,
    session_state boolean,
    CONSTRAINT "Sessions_pkey" PRIMARY KEY (session_id),
    CONSTRAINT character_id FOREIGN KEY (character_id)
        REFERENCES public."Characters" (character_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID,
    CONSTRAINT user_id FOREIGN KEY (user_id)
        REFERENCES public."Users" (user_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public."Sessions"
    OWNER to postgres;

COMMENT ON COLUMN public."Sessions".session_id
    IS '会话id';

COMMENT ON COLUMN public."Sessions".user_id
    IS '用户id';

COMMENT ON COLUMN public."Sessions".character_id
    IS '模型id';

COMMENT ON COLUMN public."Sessions".start_time
    IS '会话开始时间';

COMMENT ON COLUMN public."Sessions".end_time
    IS '会话终止时间';

COMMENT ON COLUMN public."Sessions".session_state
    IS '会话状态，0表示已被用户删除，1表示未删除';
```

## 4、创建Messages表：

```sql
-- Table: public.Messages

-- DROP TABLE IF EXISTS public."Messages";

CREATE TABLE IF NOT EXISTS public."Messages"
(
    message_id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    session_id integer NOT NULL,
    type integer NOT NULL,
    message_text "char",
    message_time time with time zone,
    massage_state boolean,
    CONSTRAINT message_id PRIMARY KEY (message_id),
    CONSTRAINT session_id FOREIGN KEY (session_id)
        REFERENCES public."Sessions" (session_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public."Messages"
    OWNER to postgres;

COMMENT ON COLUMN public."Messages".message_id
    IS '消息id';

COMMENT ON COLUMN public."Messages".session_id
    IS '会话id';

COMMENT ON COLUMN public."Messages".type
    IS '消息种类，0为模型的text消息，1为用户的text消息';

COMMENT ON COLUMN public."Messages".message_text
    IS '消息内容';

COMMENT ON COLUMN public."Messages".message_time
    IS '消息时间';

COMMENT ON COLUMN public."Messages".massage_state
    IS '消息状态，0表示已被用户删除，1表示未删除';
```

