en tabla ciclos_programados:

```sql
  CHECK (costo > 0),
  CONSTRAINT fechainicio_check CHECK (fecha_inicio < fecha_fin)
```

en tabla exámenes:

```sql
  CONSTRAINT puntaje_check CHECK (puntaje >= -112.5),
```


en tabla pagos:
```sql
  CONSTRAINT monto_check CHECK (monto > 0),
```


en tabla usuarios:
```sql
  CONSTRAINT chk_longitud_contrasenia
  CHECK (LENGTH(contrasenia) >= 8);
```

