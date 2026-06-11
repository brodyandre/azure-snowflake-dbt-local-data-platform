-- Schemas alinhados com as camadas do laboratorio local e com necessidades operacionais.

use database LOCAL_DATA_PLATFORM;

create schema if not exists RAW;
create schema if not exists STAGING;
create schema if not exists INTERMEDIATE;
create schema if not exists MARTS;
create schema if not exists CONTROL;
