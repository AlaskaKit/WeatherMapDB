--
-- PostgreSQL database dump
--

-- Dumped from database version 13.0
-- Dumped by pg_dump version 13.0

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: sorted_weather; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.sorted_weather (
    city_id integer NOT NULL,
    city_name character varying(100) NOT NULL,
    weather_description character varying(50) NOT NULL,
    temperature real NOT NULL,
    pressure integer NOT NULL,
    humidity integer NOT NULL,
    visibility integer NOT NULL,
    wind_speed real NOT NULL,
    wind_dir integer NOT NULL,
    clouds_all integer NOT NULL
);


ALTER TABLE public.sorted_weather OWNER TO postgres;

--
-- Name: unsorted_weather; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.unsorted_weather (
    city_id integer NOT NULL,
    city_name character varying(100) NOT NULL,
    weather_description character varying(50) NOT NULL,
    temperature real NOT NULL,
    pressure integer NOT NULL,
    humidity integer NOT NULL,
    visibility integer NOT NULL,
    wind_speed real NOT NULL,
    wind_dir integer NOT NULL,
    clouds_all integer NOT NULL
);


ALTER TABLE public.unsorted_weather OWNER TO postgres;

--
-- Data for Name: sorted_weather; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.sorted_weather (city_id, city_name, weather_description, temperature, pressure, humidity, visibility, wind_speed, wind_dir, clouds_all) FROM stdin;
264371	Athens	scattered clouds	17.45	1022	59	10000	2.6	160	40
745042	Istanbul	broken clouds	15.05	1023	59	10000	5.7	20	75
\.


--
-- Data for Name: unsorted_weather; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.unsorted_weather (city_id, city_name, weather_description, temperature, pressure, humidity, visibility, wind_speed, wind_dir, clouds_all) FROM stdin;
524894	Moscow	light rain	3.61	1030	93	10000	1	0	90
5128581	New York	mist	8.91	1016	93	2012	2.1	0	90
264371	Athens	scattered clouds	17.45	1022	59	10000	2.6	160	40
745042	Istanbul	broken clouds	15.05	1023	59	10000	5.7	20	75
\.


--
-- Name: sorted_weather sorted_weather_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sorted_weather
    ADD CONSTRAINT sorted_weather_pkey PRIMARY KEY (city_id);


--
-- Name: unsorted_weather unsorted_weather_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.unsorted_weather
    ADD CONSTRAINT unsorted_weather_pkey PRIMARY KEY (city_id);


--
-- PostgreSQL database dump complete
--

