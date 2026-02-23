# KalmyPT
Solución a la prueba técnica para Kalmy

# Decisiones tecnológicas

## Patrón de arquitectura

Descartados: 
MVC → No aplica bien en APIs, porque no hay una vista como en una app web.
Arquitectura Hexagonal → demasiado compleja para este scope, y es una arquitectura que nunca he usado, solo leido. Se que usa para integrar más servicios de forma sencilla pero se me aclaro que para el scope de este proyecto no necesario.
Clean Architecture → misma razón que la hexagonal, pero esta si la he usado para apps moviles + MVVM.
Monolito sin capas → No creo poder poner todo en main.py y que sea facil de hacer el API y las pruebas.
Factory Pattern → Nunca lo he usado, pero sé que es útil cuando hay múltiples tipos de objetos, pero pregunté si era necesario pensar a futuro y se me aclaro que el scope de esta prueba es que tengan la misma estructura todos los items.

Patron elegido: 
Arquitectura en capas + repository + service
Es facil de implementar, permite separar las responsabilidad para un escalamiento sencillo.
Lo hace ideal para el scope de este proyecto, no es tan complejo .

