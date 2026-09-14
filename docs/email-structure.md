# Email Structure

Galería de elementos disponibles para construir emails. Cada elemento se escribe en Markdown y se convierte automáticamente a HTML seguro para email.

<!-- TODO: Agregar screenshots de cada elemento cuando la API funcione -->

---

## Paragraph

Bloque de texto plano. Es el **fallback** — cuando nada específico coincide, el texto se convierte en un párrafo.

### Sintaxis

```markdown
Tu texto aquí. Puedes usar **negrita**, *cursiva*, y `código inline`.
```

### Campos

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `text` | `str` | Contenido del párrafo ( admite Markdown inline) |

---

## Heading

Encabezados de sección (h1–h6). Estructuran el documento y crean jerarquía visual.

### Sintaxis

```markdown
# Heading 1
## Heading 2
### Heading 3
#### Heading 4
```

### Campos

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `level` | `int` | Nivel del encabezado (1–6) |
| `text` | `str` | Texto del encabezado |

---

## Button

Botón de llamada a la acción (CTA). Esencial para emails conversion-focused.

### Sintaxis

```markdown
[Get Started](https://example.com){button}

[Learn More](https://example.com){button.secondary}

[Shop Sale](https://example.com){button color="#dc2626"}
```

### Variantes

| Variante | Sintaxis | Descripción |
|----------|----------|-------------|
| Primary | `{button}` | Botón principal (color de marca) |
| Secondary | `{button.secondary}` | Botón secundario |
| Success | `{button.success}` | Acción positiva (verde) |
| Danger | `{button.danger}` | Acción destructiva (rojo) |
| Warning | `{button.warning}` | Acción de precaución (ámbar) |

### Campos

| Campo | Tipo | Default | Descripción |
|-------|------|---------|-------------|
| `href` | `str` | (requerido) | URL de destino |
| `text` | `str` | (requerido) | Texto del botón |
| `variant` | `str?` | `primary` | Variante de estilo |
| `color` | `str?` | `None` | Color personalizado (hex) |
| `width` | `str?` | `None` | Ancho (`"full"` para 100%) |
| `border_radius` | `str?` | `8px` | Radio del borde |

---

## List

Listas ordenadas y desordenadas. Útil para contenido estructurado.

### Sintaxis

```markdown
- Primer elemento
- Segundo elemento
- Tercer elemento

1. Paso uno
2. Paso dos
3. Paso tres
```

### Campos

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `items` | `list[str]` | Elementos de la lista |
| `ordered` | `bool` | `True` si es lista ordenada |

---

## Quote

Blockquotes. Para citar contenido o destacar texto.

### Sintaxis

```markdown
> "La mejor manera de predecir el futuro es crearlo."
>
> — Peter Drucker
```

### Campos

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `text` | `str` | Contenido de la cita |

---

## Image

Imágenes responsive y centradas. Soporta block e inline.

### Sintaxis

```markdown
![Hero banner](https://example.com/hero.jpg)

![Product](https://example.com/product.jpg){width="400"}

![Avatar](https://example.com/avatar.jpg){width="80" border-radius="50%"}
```

### Campos

| Campo | Tipo | Default | Descripción |
|-------|------|---------|-------------|
| `src` | `str` | (requerido) | URL de la imagen |
| `alt` | `str` | `""` | Texto alternativo |
| `width` | `str?` | `None` | Ancho renderizado |
| `height` | `str?` | `None` | Alto renderizado |
| `alignment` | `str?` | `center` | Alineación (`left`, `center`, `right`) |
| `border_radius` | `str?` | `None` | Radio del borde |

---

## Divider

Reglas horizontales. Separadores visuales entre secciones.

### Sintaxis

```markdown
---
```

### Campos

| Campo | Tipo | Descripción |
|-------|------|-------------|
| — | — | Sin campos (elemento vacío) |

---

## Spacer

Espaciado vertical explícito. Control preciso de la separación entre elementos.

### Sintaxis

```markdown
::: spacer
:::
```

### Campos

| Campo | Tipo | Default | Descripción |
|-------|------|---------|-------------|
| `height` | `str?` | `24px` | Altura del espacio |

---

## Columns

Layout multi-columna. Se apila automáticamente en móvil.

### Sintaxis

```markdown
::: columns

::: column
Contenido de la columna izquierda.
:::

::: column
Contenido de la columna derecha.
:::

:::
```

### Campos

| Campo | Tipo | Default | Descripción |
|-------|------|---------|-------------|
| `columns` | `list[ColumnCell]` | (requerido) | Lista de columnas |
| `gap` | `str?` | `16px` | Espacio entre columnas |

---

## ColumnCell

Una columna individual dentro de un bloque Columns.

### Campos

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `children` | `list[EmailStructure]` | Elementos dentro de la columna |

---

## Table

Tablas GFM con alineación de columnas. Para datos estructurados.

### Sintaxis

```markdown
| Nombre | Rol        | Estado  |
| ------ | ---------- | ------- |
| Alice  | Engineer   | Active  |
| Bob    | Designer   | Active  |
| Carol  | Manager    | Away    |
```

### Campos

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `headers` | `list[str]` | Encabezados de columna |
| `rows` | `list[list[str]]` | Filas de datos |
| `alignment` | `list[str]?` | Alineación por columna (`left`, `center`, `right`) |

---

## Code

Bloques de código con syntax highlighting. Útil para contenido técnico.

### Sintaxis

```markdown
```python
def hello():
    print("Hello, world!")
```
```

### Campos

| Campo | Tipo | Default | Descripción |
|-------|------|---------|-------------|
| `code` | `str` | (requerido) | Contenido del código |
| `language` | `str?` | `None` | Lenguaje para syntax highlighting |

---

## Link

Enlaces. Referencias a recursos externos.

### Sintaxis

```markdown
[Visita nuestro sitio](https://example.com)
```

### Campos

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `href` | `str` | URL de destino |
| `text` | `str` | Texto del enlace |
