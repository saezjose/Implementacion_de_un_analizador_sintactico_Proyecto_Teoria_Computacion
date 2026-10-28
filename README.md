# Analizador Sintáctico para DSL "SmartRule"

Proyecto de Teoría de la Computación - Analizador Léxico y Sintáctico LL(1)

## 1. Descripción del lenguaje

**SmartRule** es un lenguaje de dominio específico (DSL) para definir reglas de automatización en sistemas IoT/smart home. Permite definir reglas condicionales con operadores lógicos, comparaciones relacionales y acciones a ejecutar.

### Características
- Reglas tipo `WHEN <condición> THEN <acción(es)> [ELSE <acción(es)>];`
- Condiciones con operadores relacionales: `>`, `<`, `>=`, `<=`, `==`, `!=`
- Operadores lógicos: `AND`, `OR`, `NOT`
- Acciones: asignaciones `identificador = valor` o llamadas a acción `identificador [argumento]` o `identificador identificador = valor`
- Valores: números enteros, identificadores, `TRUE`, `FALSE`
- Múltiples acciones separadas por coma `,`

### Formato de entrada
- Archivos con extensión `.sr`
- Palabras reservadas en mayúsculas: `WHEN`, `THEN`, `ELSE`, `AND`, `OR`, `NOT`, `TRUE`, `FALSE`
- Punto y coma `;` obligatorio al final de cada regla

### Ejemplo
**Entrada:**
```text
WHEN temperatura > 28 AND humedad < 40 THEN encender ventilador;
```

**Salida:**
```text
============================================================
ANALIZADOR SINTACTICO SMART RULE (LL(1))
============================================================

Entrada:
WHEN temperatura > 28 AND humedad < 40 THEN encender ventilador;

[OK] ANALISIS LEXICO EXITOSO
[OK] ANALISIS SINTACTICO EXITOSO

Se reconocieron 1 regla(s) valida(s).
```

## 2. Arquitectura

```
src/
├── lexer/      # Analizador léxico
├── ast/        # Nodos del Árbol Sintáctico Abstracto (AST)
├── parser/     # Parser LL(1) descendente recursivo
└── utils/      # Utilidades (FIRST/FOLLOW, visualización, exportadores)
```

## 3. Gramática Libre de Contexto (GLC)

```bnf
Prog        -> Regla Prog | ε
Regla       -> WHEN Cond THEN ListaAcciones ElsePart PUNTO_COMA
ElsePart    -> ELSE ListaAcciones | ε
Cond        -> OrExpr
OrExpr      -> AndExpr OrTail
OrTail      -> OR AndExpr OrTail | ε
AndExpr     -> NotExpr AndTail
AndTail     -> AND NotExpr AndTail | ε
NotExpr     -> NOT NotExpr | RelExpr
RelExpr     -> Factor RelExprTail
RelExprTail -> OP_REL Factor | ε
Factor      -> NUM | ID | TRUE | FALSE
ListaAcciones -> Accion AccionTail
AccionTail    -> COMA Accion AccionTail | ε
Accion        -> ID AsigOrCall
AsigOrCall    -> IGUAL Factor | ID AsigTail | NUM | TRUE | FALSE | ε
AsigTail      -> IGUAL Factor | ε
```

Ver `docs/gramatica.md` para detalles completos, FIRST/FOLLOW, tabla LL(1).

## 4. Requisitos

- Python 3.10+
- Sin dependencias externas obligatorias (solo librería estándar)

## 5. Ejecución

### Probar con ejemplos incluidos
```bash
python main.py -f ejemplos/validos_1.sr
```

### Mostrar tokens
```bash
python main.py -f ejemplos/validos_1.sr -t
```

### Mostrar AST
```bash
python main.py -f ejemplos/validos_1.sr -a
```

### Reportar todos los errores (modo pánico)
```bash
python main.py -f ejemplos/invalidos_1.sr -e
```

### Modo interactivo
```bash
python main.py
```

### Calcular FIRST, FOLLOW y verificar tabla LL(1)
```bash
python -m src.utils.first_follow
```

### Ejecutar pruebas
```bash
python -m unittest discover -s tests -v
```

## 6. Archivos importantes

- `main.py` - Punto de entrada CLI
- `src/gramatica.py` - Gramática única fuente de verdad
- `docs/gramatica.md` - Gramática, FIRST, FOLLOW, tabla LL(1), análisis
- `docs/informe_latex/` - Informe en LaTeX
- `tests/` - Suite de pruebas

## 7. Autoría y aclaraciones

- El analizador léxico fue tomado como base del cuaderno `analizador_lexico1.ipynb`, adaptado y extendido.
- Parser implementado desde cero con enfoque LL(1) descendente recursivo (sin generadores automáticos).
- Árbol sintáctico/AST construido explícitamente.
- Mensajes de error con formatos exactos: `Error sintáctico (token N, línea L, columna C): ...` y `Error léxico (línea L, columna C): símbolo no reconocido 'S'`.
