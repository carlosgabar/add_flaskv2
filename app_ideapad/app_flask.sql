PGDMP                       }         	   app_flask    17.2    17.2 &    �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                           false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                           false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                           false            �           1262    16571 	   app_flask    DATABASE     �   CREATE DATABASE app_flask WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'Spanish_Venezuela.1252';
    DROP DATABASE app_flask;
                     postgres    false            �            1259    16572    administrador    TABLE     m   CREATE TABLE public.administrador (
    id_user character varying(20),
    password character varying(20)
);
 !   DROP TABLE public.administrador;
       public         heap r       postgres    false            �            1259    16575    curso_id_curso_seq    SEQUENCE     ~   CREATE SEQUENCE public.curso_id_curso_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 99999
    CACHE 1;
 )   DROP SEQUENCE public.curso_id_curso_seq;
       public               postgres    false            �            1259    16576    curso    TABLE     �   CREATE TABLE public.curso (
    id_curso integer DEFAULT nextval('public.curso_id_curso_seq'::regclass) NOT NULL,
    nombre character varying(100)
);
    DROP TABLE public.curso;
       public         heap r       postgres    false    218            �            1259    16580    sec_curso_trabajador    SEQUENCE     }   CREATE SEQUENCE public.sec_curso_trabajador
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 +   DROP SEQUENCE public.sec_curso_trabajador;
       public               postgres    false            �            1259    16581    curso_trabajador    TABLE     �   CREATE TABLE public.curso_trabajador (
    id_ct integer DEFAULT nextval('public.sec_curso_trabajador'::regclass) NOT NULL,
    id_curso integer,
    id_trabajador integer,
    status character varying DEFAULT 'activo'::character varying
);
 $   DROP TABLE public.curso_trabajador;
       public         heap r       postgres    false    220            �            1259    16588    h_curso    TABLE     n   CREATE TABLE public.h_curso (
    id_curso_original integer,
    cant_horas integer,
    id_vcurso integer
);
    DROP TABLE public.h_curso;
       public         heap r       postgres    false            �            1259    16591    sec_h_curso    SEQUENCE     t   CREATE SEQUENCE public.sec_h_curso
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 "   DROP SEQUENCE public.sec_h_curso;
       public               postgres    false            �            1259    16592    sec_idtarea    SEQUENCE     t   CREATE SEQUENCE public.sec_idtarea
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 "   DROP SEQUENCE public.sec_idtarea;
       public               postgres    false            �            1259    16593 
   sec_vcurso    SEQUENCE     s   CREATE SEQUENCE public.sec_vcurso
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 !   DROP SEQUENCE public.sec_vcurso;
       public               postgres    false            �            1259    16594    tarea    TABLE     �   CREATE TABLE public.tarea (
    id_tarea integer DEFAULT nextval('public.sec_idtarea'::regclass) NOT NULL,
    id_curso integer NOT NULL,
    descripcion text
);
    DROP TABLE public.tarea;
       public         heap r       postgres    false    224            �            1259    16600 
   trabajador    TABLE     �   CREATE TABLE public.trabajador (
    id_trabajador integer NOT NULL,
    nombre character varying(100),
    apellido character varying(100),
    clave character varying(15),
    cedula integer,
    departamento character varying(50)
);
    DROP TABLE public.trabajador;
       public         heap r       postgres    false            �            1259    16603    v_curso    TABLE     �  CREATE TABLE public.v_curso (
    id_vcurso integer DEFAULT nextval('public.sec_vcurso'::regclass) NOT NULL,
    fecha_inicio timestamp without time zone,
    fecha_fin date,
    minimo integer,
    maximo integer,
    descripcion text,
    status text DEFAULT 'progreso'::text,
    hora time without time zone,
    canthoras integer,
    id_curso_original integer,
    ponente character varying(100),
    localidad character varying(100),
    salon character varying(100)
);
    DROP TABLE public.v_curso;
       public         heap r       postgres    false    225            �          0    16572    administrador 
   TABLE DATA           :   COPY public.administrador (id_user, password) FROM stdin;
    public               postgres    false    217   �,       �          0    16576    curso 
   TABLE DATA           1   COPY public.curso (id_curso, nombre) FROM stdin;
    public               postgres    false    219   �,       �          0    16581    curso_trabajador 
   TABLE DATA           R   COPY public.curso_trabajador (id_ct, id_curso, id_trabajador, status) FROM stdin;
    public               postgres    false    221   �-       �          0    16588    h_curso 
   TABLE DATA           K   COPY public.h_curso (id_curso_original, cant_horas, id_vcurso) FROM stdin;
    public               postgres    false    222   4.       �          0    16594    tarea 
   TABLE DATA           @   COPY public.tarea (id_tarea, id_curso, descripcion) FROM stdin;
    public               postgres    false    226   n.       �          0    16600 
   trabajador 
   TABLE DATA           b   COPY public.trabajador (id_trabajador, nombre, apellido, clave, cedula, departamento) FROM stdin;
    public               postgres    false    227   �.       �          0    16603    v_curso 
   TABLE DATA           �   COPY public.v_curso (id_vcurso, fecha_inicio, fecha_fin, minimo, maximo, descripcion, status, hora, canthoras, id_curso_original, ponente, localidad, salon) FROM stdin;
    public               postgres    false    228   f/       �           0    0    curso_id_curso_seq    SEQUENCE SET     A   SELECT pg_catalog.setval('public.curso_id_curso_seq', 52, true);
          public               postgres    false    218            �           0    0    sec_curso_trabajador    SEQUENCE SET     C   SELECT pg_catalog.setval('public.sec_curso_trabajador', 10, true);
          public               postgres    false    220            �           0    0    sec_h_curso    SEQUENCE SET     :   SELECT pg_catalog.setval('public.sec_h_curso', 33, true);
          public               postgres    false    223            �           0    0    sec_idtarea    SEQUENCE SET     9   SELECT pg_catalog.setval('public.sec_idtarea', 8, true);
          public               postgres    false    224            �           0    0 
   sec_vcurso    SEQUENCE SET     9   SELECT pg_catalog.setval('public.sec_vcurso', 13, true);
          public               postgres    false    225            D           2606    16611    curso curso_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public.curso
    ADD CONSTRAINT curso_pkey PRIMARY KEY (id_curso);
 :   ALTER TABLE ONLY public.curso DROP CONSTRAINT curso_pkey;
       public                 postgres    false    219            F           2606    16613 &   curso_trabajador curso_trabajador_pkey 
   CONSTRAINT     g   ALTER TABLE ONLY public.curso_trabajador
    ADD CONSTRAINT curso_trabajador_pkey PRIMARY KEY (id_ct);
 P   ALTER TABLE ONLY public.curso_trabajador DROP CONSTRAINT curso_trabajador_pkey;
       public                 postgres    false    221            J           2606    16615    tarea tarea_pkey 
   CONSTRAINT     ^   ALTER TABLE ONLY public.tarea
    ADD CONSTRAINT tarea_pkey PRIMARY KEY (id_tarea, id_curso);
 :   ALTER TABLE ONLY public.tarea DROP CONSTRAINT tarea_pkey;
       public                 postgres    false    226    226            L           2606    16617    trabajador trabajador_pkey 
   CONSTRAINT     c   ALTER TABLE ONLY public.trabajador
    ADD CONSTRAINT trabajador_pkey PRIMARY KEY (id_trabajador);
 D   ALTER TABLE ONLY public.trabajador DROP CONSTRAINT trabajador_pkey;
       public                 postgres    false    227            H           2606    16619 (   curso_trabajador unique_curso_trabajador 
   CONSTRAINT     v   ALTER TABLE ONLY public.curso_trabajador
    ADD CONSTRAINT unique_curso_trabajador UNIQUE (id_curso, id_trabajador);
 R   ALTER TABLE ONLY public.curso_trabajador DROP CONSTRAINT unique_curso_trabajador;
       public                 postgres    false    221    221            N           2606    16621    v_curso v_curso_pkey 
   CONSTRAINT     Y   ALTER TABLE ONLY public.v_curso
    ADD CONSTRAINT v_curso_pkey PRIMARY KEY (id_vcurso);
 >   ALTER TABLE ONLY public.v_curso DROP CONSTRAINT v_curso_pkey;
       public                 postgres    false    228            O           2606    16622 &   h_curso h_curso_id_curso_original_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.h_curso
    ADD CONSTRAINT h_curso_id_curso_original_fkey FOREIGN KEY (id_curso_original) REFERENCES public.curso(id_curso) NOT VALID;
 P   ALTER TABLE ONLY public.h_curso DROP CONSTRAINT h_curso_id_curso_original_fkey;
       public               postgres    false    222    219    4676            P           2606    16627    h_curso h_curso_id_vcurso_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.h_curso
    ADD CONSTRAINT h_curso_id_vcurso_fkey FOREIGN KEY (id_vcurso) REFERENCES public.v_curso(id_vcurso) NOT VALID;
 H   ALTER TABLE ONLY public.h_curso DROP CONSTRAINT h_curso_id_vcurso_fkey;
       public               postgres    false    228    222    4686            Q           2606    16632    tarea tarea_id_curso_fkey    FK CONSTRAINT        ALTER TABLE ONLY public.tarea
    ADD CONSTRAINT tarea_id_curso_fkey FOREIGN KEY (id_curso) REFERENCES public.curso(id_curso);
 C   ALTER TABLE ONLY public.tarea DROP CONSTRAINT tarea_id_curso_fkey;
       public               postgres    false    226    4676    219            R           2606    16637 &   v_curso v_curso_id_curso_original_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.v_curso
    ADD CONSTRAINT v_curso_id_curso_original_fkey FOREIGN KEY (id_curso_original) REFERENCES public.curso(id_curso) NOT VALID;
 P   ALTER TABLE ONLY public.v_curso DROP CONSTRAINT v_curso_id_curso_original_fkey;
       public               postgres    false    4676    219    228            �      x�+-.M,���44261����� =�      �     x�}��N�0���S�	P�?�vDb��I����z��$%����:X n�/�gqL;:QTk��ه$��:z�zSm<�x<�w�����\|m��NR��>��}�����y˨L��r �?�'U�s�匜��#�^����	�4��]��2-ث�_�f�\5ń�2�l�l(�c�'U�0�SZD+bB���ʢu��)@�r�z~UU�w�Y��Ěx$�3�ېX�,�j ��2�Zel3�3n�XM�2c����1����,/[;�7��[������F)��A��      �   L   x�3�4�4��02�L��K�ɬJL��
�b��L0E�8�0E�A& �)��%�!Q#�0E8-0����� �2/�      �   *   x�35��44�2�4�4�@�1�	�m�i��8��b���� t�p      �   f   x�M�1�0��>EO����t��EBI��8?	�e(r���-c_�\\w�fX:���ȋod_-�95�m��ب�~U̘��V�E���:��A%C      �   r   x�-�A
�0��c�-�T�D_���bp�P%=��u�{�ev�Β	6}��n�ĔB ������(RIP����H<�aʵ'x���Tǘe����k?�o
�I�a�E�u9����"(      �   z  x�œAN�0EדS�E�$nCv܃ʹ"#�6v�Eo��J��@B)��x����w	�.�F��
��V������'��AL�O�\kwP��Q�Ϣ�b���v�F!������d{Y	���aoُ�b]�X�����m�A!���;f�L.x�sb���W�'���u����)��_<.,��-��T��1�Q��S��h���~5`"G�O���8Gz{%8��S��Ǽr�w;'ט5��_3'��"�̊��'Jt�ⳮ�
�''�.D��,d��}�G�)
\%�Q(��Y�f>�4�^���)�|�cH���H�������=r�!�=.̝ҳ=W&
S�v6V�4�nbS�%^ ^�c��(w�'���wEQ����     