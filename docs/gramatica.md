# Gramática, FIRST, FOLLOW y Tabla LL(1) - SmartRule

## 1. Gramática Libre de Contexto

**Símbolo inicial:** `Prog`

### Gramática completa (fuente: src/gramatica.py)

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
Accion        -> ID AccionResto
AccionResto   -> IGUAL Factor | ID ArgResto | NUM | TRUE | FALSE | ε
ArgResto      -> IGUAL Factor | ε
```

### Terminales
`WHEN, THEN, ELSE, AND, OR, NOT, TRUE, FALSE, NUM, ID, OP_REL, IGUAL, COMA, PUNTO_COMA, EOF ($)`

### No Terminales
`Prog, Regla, ElsePart, Cond, OrExpr, OrTail, AndExpr, AndTail, NotExpr, RelExpr, RelExprTail, Factor, ListaAcciones, AccionTail, Accion, AccionResto, ArgResto`

## 2. Análisis de la gramática

### Recursión izquierda
No hay recursión izquierda directa. Se usa recursión por la derecha en `OrTail`, `AndTail`, `AccionTail`, `Prog` para facilitar el análisis LL(1).

### Factorización
Se factorizaron producciones donde era necesario. Se reemplazó `AsigOrCall` por `Accion -> ID AccionResto` con `AccionResto` y `ArgResto` para eliminar conflictos FIRST/FIRST, permitiendo distinguir:
- Asignación directa: `variable = valor` (`AccionResto -> IGUAL Factor`)
- Acción con objetivo y asignación: `encender luces = 100` (`AccionResto -> ID ArgResto`, `ArgResto -> IGUAL Factor`)
- Llamada con argumento: `encender luces` o `accion NUM/TRUE/FALSE` 
- Llamada sin argumento: `accion` (deriva ε)

### Ambigüedad
La gramática es no ambigua. Se respeta precedencia: `NOT` > `AND` > `OR`. Comparaciones relacionales no se encadenan.

## 3. Conjuntos FIRST (salida real del verificador)

```
FIRST(Accion) = { ID }
FIRST(AccionResto) = { FALSE, ID, IGUAL, NUM, TRUE, epsilon }
FIRST(AccionTail) = { COMA, epsilon }
FIRST(AndExpr) = { FALSE, ID, NOT, NUM, TRUE }
FIRST(AndTail) = { AND, epsilon }
FIRST(ArgResto) = { IGUAL, epsilon }
FIRST(Cond) = { FALSE, ID, NOT, NUM, TRUE }
FIRST(ElsePart) = { ELSE, epsilon }
FIRST(Factor) = { FALSE, ID, NUM, TRUE }
FIRST(ListaAcciones) = { ID }
FIRST(NotExpr) = { FALSE, ID, NOT, NUM, TRUE }
FIRST(OrExpr) = { FALSE, ID, NOT, NUM, TRUE }
FIRST(OrTail) = { OR, epsilon }
FIRST(Prog) = { WHEN, epsilon }
FIRST(Regla) = { WHEN }
FIRST(RelExpr) = { FALSE, ID, NUM, TRUE }
FIRST(RelExprTail) = { OP_REL, epsilon }
```

## 4. Conjuntos FOLLOW (salida real del verificador)

```
FOLLOW(Accion) = { COMA, ELSE, PUNTO_COMA }
FOLLOW(AccionResto) = { COMA, ELSE, PUNTO_COMA }
FOLLOW(AccionTail) = { ELSE, PUNTO_COMA }
FOLLOW(AndExpr) = { OR, THEN }
FOLLOW(AndTail) = { OR, THEN }
FOLLOW(ArgResto) = { COMA, ELSE, PUNTO_COMA }
FOLLOW(Cond) = { THEN }
FOLLOW(ElsePart) = { PUNTO_COMA }
FOLLOW(Factor) = { AND, COMA, ELSE, OP_REL, OR, PUNTO_COMA, THEN }
FOLLOW(ListaAcciones) = { ELSE, PUNTO_COMA }
FOLLOW(NotExpr) = { AND, OR, THEN }
FOLLOW(OrExpr) = { THEN }
FOLLOW(OrTail) = { THEN }
FOLLOW(Prog) = { $ }
FOLLOW(Regla) = { $, WHEN }
FOLLOW(RelExpr) = { AND, OR, THEN }
FOLLOW(RelExprTail) = { AND, OR, THEN }
```

## 5. Tabla LL(1) y verificación

```
Entradas en tabla LL(1): 59
Sin conflictos detectados.
```

Para reproducir:
```bash
python -m src.utils.first_follow
```

La gramática cumple con las condiciones LL(1): para cada no-terminal y terminal en FIRST de alguna producción hay una única producción, y cuando hay ε en FIRST se usa FOLLOW. No hay conflictos FIRST/FIRST ni FIRST/FOLLOW.

## 6. Extensión creativa

**Nombre:** Soporte para cláusula `ELSE`, operador `NOT` y acciones flexibles (asignación o llamada con argumento).

**Justificación:** Amplía las reglas de automatización con alternativas y mayor expresividad en condiciones y acciones.

**Producciones que lo implementan:**
- `ElsePart -> ELSE ListaAcciones | ε` (cláusula ELSE opcional)
- `NotExpr -> NOT NotExpr | RelExpr` (negación, con mayor precedencia)
- `Accion -> ID AccionResto` 
- `AccionResto -> IGUAL Factor | ID ArgResto | NUM | TRUE | FALSE | ε` (asignación, acción con objetivo+asignación, llamada con argumento, llamada sin argumento)
- `ArgResto -> IGUAL Factor | ε`

**Tests que lo cubren:**
- `tests/test_parser.py`: `test_regla_con_else`, `test_regla_con_not`, `test_multiples_acciones`, `test_asignacion`, `test_accion_sin_argumento`, `test_true_false`
- `tests/test_integracion.py`: casos con `ELSE`, `NOT` anidado, múltiples acciones
- `tests/test_ast_forma.py`: verifica precedencia `NOT > AND > OR` en el AST
- `tests/test_casos.py`: casos con `ELSE`, `NOT`, asignaciones y acciones con argumento
- `tests/test_errores_tarea4.py`: mensajes contextuales relacionados a acciones
