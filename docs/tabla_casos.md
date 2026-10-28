# Tabla de Casos de Prueba - SmartRule

| ID | Descripción | Entrada | Resultado esperado | Resultado obtenido | Observación |
|---|-------------|---------|-------------------|-------------------|-------------|
| 1 | Regla simple con relacional | `WHEN temperatura > 28 THEN encender;` | ACEPTA | ACEPTA |  |
| 2 | Condición con AND | `WHEN a > 1 AND b < 2 THEN accion1;` | ACEPTA | ACEPTA |  |
| 3 | Condición con OR | `WHEN a > 1 OR b < 2 THEN accion1;` | ACEPTA | ACEPTA |  |
| 4 | Condición con NOT | `WHEN NOT activo THEN apagar;` | ACEPTA | ACEPTA |  |
| 5 | Regla con ELSE | `WHEN x > 0 THEN encender ELSE apagar;` | ACEPTA | ACEPTA |  |
| 6 | Múltiples acciones separadas por coma | `WHEN x == 1 THEN a, b, c;` | ACEPTA | ACEPTA |  |
| 7 | Acción con asignación | `WHEN x > 0 THEN y = 5;` | ACEPTA | ACEPTA |  |
| 8 | Acción con argumento | `WHEN x > 0 THEN encender luces;` | ACEPTA | ACEPTA |  |
| 9 | Acción sin argumento | `WHEN x > 0 THEN reset;` | ACEPTA | ACEPTA |  |
| 10 | Valores TRUE/FALSE | `WHEN sistema == TRUE THEN iniciar;` | ACEPTA | ACEPTA |  |
| 11 | Múltiples reglas | `WHEN a > 1 THEN x; WHEN b < 2 THEN y;` | ACEPTA | ACEPTA |  |
| 12 | Condición sin operador relacional (factor solo) | `WHEN activo THEN encender;` | ACEPTA | ACEPTA |  |
| 13 | Falta THEN | `WHEN x > 1 encender;` | RECHAZA | RECHAZA: Error sintáctico (token 5, línea 1, columna 12): se esperaba THEN, se encontró 'encender' | Error sintáctico (token 5, línea 1, columna 12): se esperaba THEN, se encontró 'encender' |
| 14 | Falta condición | `WHEN THEN encender;` | RECHAZA | RECHAZA: Error sintáctico (token 2, línea 1, columna 6): se esperaba un factor (NUM, ID, TRUE o FALSE), se encontró 'THEN' | Error sintáctico (token 2, línea 1, columna 6): se esperaba un factor (NUM, ID, TRUE o FALSE), se encontró 'THEN' |
| 15 | Falta punto y coma | `WHEN x > 1 THEN encender` | RECHAZA | RECHAZA: Error sintáctico (token 7, línea 2, columna 1): se esperaba ';' al final de la regla, se encontró fin de la entrada | Error sintáctico (token 7, línea 2, columna 1): se esperaba ';' al final de la regla, se encontró fin de la entrada |
| 16 | Falta WHEN | `x > 1 THEN encender;` | RECHAZA | RECHAZA: Error sintáctico (token 1, línea 1, columna 1): se esperaba la palabra reservada WHEN o el fin de la entrada, se encontró 'x' | Error sintáctico (token 1, línea 1, columna 1): se esperaba la palabra reservada WHEN o el fin de la entrada, se encontró 'x' |
| 17 | Coma sobrante | `WHEN x > 1 THEN a,, b;` | RECHAZA | RECHAZA: Error sintáctico (token 8, línea 1, columna 19): se esperaba el nombre de una acción (ID), se encontró ',' | Error sintáctico (token 8, línea 1, columna 19): se esperaba el nombre de una acción (ID), se encontró ',' |
| 18 | Falta operando tras operador relacional | `WHEN temperatura > THEN encender;` | RECHAZA | RECHAZA: Error sintáctico (token 4, línea 1, columna 20): se esperaba un factor (NUM, ID, TRUE o FALSE), se encontró 'THEN' | Error sintáctico (token 4, línea 1, columna 20): se esperaba un factor (NUM, ID, TRUE o FALSE), se encontró 'THEN' |
| 19 | Lista de acciones vacía | `WHEN x > 1 THEN ;` | RECHAZA | RECHAZA: Error sintáctico (token 6, línea 1, columna 17): se esperaba el nombre de una acción (ID), se encontró ';' | Error sintáctico (token 6, línea 1, columna 17): se esperaba el nombre de una acción (ID), se encontró ';' |
| 20 | Falta acción después de ELSE | `WHEN x > 1 THEN a ELSE ;` | RECHAZA | RECHAZA: Error sintáctico (token 8, línea 1, columna 24): se esperaba el nombre de una acción (ID), se encontró ';' | Error sintáctico (token 8, línea 1, columna 24): se esperaba el nombre de una acción (ID), se encontró ';' |
| 21 | Coma al final sin acción | `WHEN x > 1 THEN a,;` | RECHAZA | RECHAZA: Error sintáctico (token 8, línea 1, columna 19): se esperaba el nombre de una acción (ID), se encontró ';' | Error sintáctico (token 8, línea 1, columna 19): se esperaba el nombre de una acción (ID), se encontró ';' |
| 22 | Falta acción después de coma | `WHEN x > 1 THEN ,a;` | RECHAZA | RECHAZA: Error sintáctico (token 6, línea 1, columna 17): se esperaba el nombre de una acción (ID), se encontró ',' | Error sintáctico (token 6, línea 1, columna 17): se esperaba el nombre de una acción (ID), se encontró ',' |
| 23 | Falta valor tras IGUAL | `WHEN x > 1 THEN y = ;` | RECHAZA | RECHAZA: Error sintáctico (token 8, línea 1, columna 21): se esperaba un factor (NUM, ID, TRUE o FALSE), se encontró ';' | Error sintáctico (token 8, línea 1, columna 21): se esperaba un factor (NUM, ID, TRUE o FALSE), se encontró ';' |
| 24 | Operador relacional mal formado o incompleto | `WHEN x > = 1 THEN y;` | RECHAZA | RECHAZA: Error sintáctico (token 4, línea 1, columna 10): se esperaba un factor (NUM, ID, TRUE o FALSE), se encontró '=' | Error sintáctico (token 4, línea 1, columna 10): se esperaba un factor (NUM, ID, TRUE o FALSE), se encontró '=' |
| 25 | Entrada vacía | `` | ACEPTA | ACEPTA |  |
| 26 | Solo espacios | `` | ACEPTA | ACEPTA |  |
| 27 | Regla mínima con una sola acción | `WHEN a > 1 THEN x;` | ACEPTA | ACEPTA |  |
| 28 | Múltiples punto y coma | `WHEN a > 1 THEN x;;` | RECHAZA | RECHAZA: Error sintáctico (token 8, línea 1, columna 19): se esperaba la palabra reservada WHEN o el fin de la entrada, se encontró ';' | Error sintáctico (token 8, línea 1, columna 19): se esperaba la palabra reservada WHEN o el fin de la entrada, se encontró ';' |
| 29 | Regla mal formada con doble WHEN | `WHEN a > 1 THEN x; WHEN` | RECHAZA | RECHAZA: Error sintáctico (token 9, línea 2, columna 1): se esperaba un factor (NUM, ID, TRUE o FALSE), se encontró fin de la entrada | Error sintáctico (token 9, línea 2, columna 1): se esperaba un factor (NUM, ID, TRUE o FALSE), se encontró fin de la entrada |
| 30 | Falta cierre tras múltiples reglas | `WHEN a > 1 THEN x; WHEN b > 2 THEN y` | RECHAZA | RECHAZA: Error sintáctico (token 14, línea 2, columna 1): se esperaba ';' al final de la regla, se encontró fin de la entrada | Error sintáctico (token 14, línea 2, columna 1): se esperaba ';' al final de la regla, se encontró fin de la entrada |
| 31 | Acción con ID ID asignación | `WHEN x > 0 THEN encender luces = 100;` | ACEPTA | ACEPTA |  |
| 32 | Condición con NOT anidado | `WHEN NOT NOT activo THEN encender;` | ACEPTA | ACEPTA |  |
