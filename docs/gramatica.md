# Gramática, FIRST, FOLLOW y Tabla LL(1) - SmartRule

## 1. Gramática Libre de Contexto

**Símbolo inicial:** `Prog`

### Gramática completa

```
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
AsigOrCall    -> IGUAL Factor | Factor | ε
```

### Terminales
`WHEN, THEN, ELSE, AND, OR, NOT, TRUE, FALSE, NUM, ID, OP_REL, IGUAL, COMA, PUNTO_COMA, $`

### No Terminales
`Prog, Regla, ElsePart, Cond, OrExpr, OrTail, AndExpr, AndTail, NotExpr, RelExpr, Factor, ListaAcciones, AccionTail, Accion, AsigOrCall`

## 2. Análisis de la gramática

### Eliminación de recursión izquierda
No hay recursión izquierda directa. Se usa recursión por la derecha en `OrTail`, `AndTail`, `AccionTail`, `Prog` para facilitar el análisis LL(1).

### Factorización
Se factorizaron producciones donde era necesario (ej. `AsigOrCall` para distinguir asignación `=`, llamada con argumento o sin argumento).

### Ambigüedad
La gramática es no ambigua. Se respeta precedencia: `NOT` > `AND` > `OR`. Comparaciones relacionales no se encadenan.

## 3. Conjuntos FIRST

Ejecutar para ver cálculo completo:
```bash
python -m src.utils.first_follow
```

Valores esperados aproximados:

- FIRST(Prog) = {WHEN, ε}
- FIRST(Regla) = {WHEN}
- FIRST(ElsePart) = {ELSE, ε}
- FIRST(Cond) = {NOT, NUM, ID, TRUE, FALSE}
- FIRST(OrExpr) = {NOT, NUM, ID, TRUE, FALSE}
- FIRST(OrTail) = {OR, ε}
- FIRST(AndExpr) = {NOT, NUM, ID, TRUE, FALSE}
- FIRST(AndTail) = {AND, ε}
- FIRST(NotExpr) = {NOT, NUM, ID, TRUE, FALSE}
- FIRST(RelExpr) = {NUM, ID, TRUE, FALSE}
- FIRST(Factor) = {NUM, ID, TRUE, FALSE}
- FIRST(ListaAcciones) = {ID}
- FIRST(AccionTail) = {COMA, ε}
- FIRST(Accion) = {ID}
- FIRST(AsigOrCall) = {IGUAL, NUM, ID, TRUE, FALSE, ε}

## 4. Conjuntos FOLLOW

- FOLLOW(Prog) = {$}
- FOLLOW(Regla) = {WHEN, $}
- FOLLOW(ElsePart) = {PUNTO_COMA}
- FOLLOW(Cond) = {THEN}
- FOLLOW(OrExpr) = {THEN}
- FOLLOW(OrTail) = {THEN}
- FOLLOW(AndExpr) = {OR, THEN}
- FOLLOW(AndTail) = {OR, THEN}
- FOLLOW(NotExpr) = {AND, OR, THEN}
- FOLLOW(RelExpr) = {AND, OR, THEN}
- FOLLOW(Factor) = {OP_REL, AND, OR, THEN, COMA, PUNTO_COMA, ELSE, IGUAL, NUM, ID, TRUE, FALSE}
- FOLLOW(ListaAcciones) = {PUNTO_COMA, ELSE}
- FOLLOW(AccionTail) = {PUNTO_COMA, ELSE}
- FOLLOW(Accion) = {COMA, PUNTO_COMA, ELSE}
- FOLLOW(AsigOrCall) = {COMA, PUNTO_COMA, ELSE}

## 5. Tabla LL(1)

La tabla se construye con FIRST y FOLLOW. El parser descendente recursivo implementado sigue directamente estas producciones sin conflictos.

Para visualizar la tabla completa:
```bash
python -m src.utils.first_follow
```

## 6. Justificación LL(1)

- Para cada no-terminal y terminal en FIRST de alguna producción, hay una única producción.
- Cuando hay ε en FIRST, se usa FOLLOW para decidir.
- No hay conflictos por recursión izquierda ni ambigüedad.
- La gramática es LL(1).
