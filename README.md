# Analizador Sintáctico para DSL "SmartRule"

Proyecto de Teoría de la Computación - Analizador Léxico y Sintáctico LL(1)

## 1. Descripción del lenguaje

**SmartRule** es un lenguaje de dominio específico (DSL) para definir reglas de automatización en sistemas IoT/smart home. Permite definir reglas condicionales con operadores lógicos, comparaciones relacionales y acciones a ejecutar.

### Características
- Reglas tipo `WHEN <condición> THEN <acción(es)> [ELSE <acción(es)>];`
- Condiciones con operadores relacionales: `>`, `<`, `>=`, `<=`, `==`, `!=`
- Operadores lógicos: `AND`, `OR`, `NOT`
- Acciones: asignaciones `identificador = valor` o llamadas a acción `identificador [argumento]`
- Valores: números enteros, identificadores (sensores/actuadores/variables)
- Múltiples acciones separadas por coma `,`

### Ejemplos válidos
```text
WHEN temperatura > 28 AND humedad < 40 THEN encender ventilador;
WHEN luz == 0 OR movimiento == TRUE THEN encender luces, alarma = 1 ELSE apagar luces;
WHEN NOT puerta_abierta THEN activar_alarma;
```

### Ejemplos inválidos (detectados)
```text
WHEN temperatura > THEN encender ventilador;  # falta operando
temperatura > 28 THEN encender luces;          # falta WHEN
WHEN temperatura > 28 encender luces;          # falta THEN
```

## 2. Arquitectura (Limpia)

```
src/
├── lexer/      # Analizador léxico (basado en el provisto)
├── ast/        # Nodos del Árbol Sintáctico Abstracto (AST)
├── parser/     # Parser LL(1) descendente recursivo
└── utils/      # Utilidades (FIRST/FOLLOW, visualización)
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
RelExpr     -> Factor OP_REL Factor | Factor
Factor      -> NUM | ID | TRUE | FALSE
ListaAcciones -> Accion AccionTail
AccionTail    -> COMA Accion AccionTail | ε
Accion        -> ID AsigOrCall
AsigOrCall    -> IGUAL Factor | Factor | ε
```

Donde `IGUAL` representa `=`. Ver `docs/gramatica.md` para detalles completos, FIRST/FOLLOW, tabla LL(1).

## 4. Requisitos

- Python 3.10+ (probado en entorno local)
- Sin dependencias externas obligatorias (solo librería estándar)

## 5. Ejecución

### Probar con ejemplos incluidos
```bash
python main.py --archivo ejemplos/validos_1.sr
```

### Modo interactivo
```bash
python main.py
```

### Ejecutar pruebas
```bash
python -m pytest tests/ -v
```

## 6. Archivos importantes

- `main.py` - Punto de entrada CLI
- `docs/gramatica.md` - Gramática, FIRST, FOLLOW, tabla LL(1), análisis de ambigüedad/recursión
- `docs/informe_latex/` - Informe en LaTeX listo para compilar
- `tests/` - Suite de pruebas (>=25 casos según rúbrica)

## 7. Autoría y aclaraciones

- El lexer parte del analizador léxico proporcionado (`anlizador_lexico1.ipynb`), adaptado y extendido.
- Parser implementado desde cero con enfoque LL(1) descendente recursivo (sin generadores automáticos).
- Árbol sintáctico/AST construido explícitamente.
- Mensajes de error sintácticos claros con posición/causa.
