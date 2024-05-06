# cs50w-project2
## Descripción 
Se ha hecho una aplicación web de subastas con temática del juego Dungeons and Dragons. Dentro de esta el usuario podrá crear listados de subastas, agregar a su watchlist, ofertar por las subastas, ver las distintas categorías, entre otras funciones relacionadas con el filtrado de las subastas. 
## Tecnologías utilizadas
Para el proyecto se ha hecho de uso de django, modelos de django, sqlite3, sass y boostrap.
## ¿Por qué no he hecho uso de django forms?
Como Django es una tecnología todavía nueva para mí, se me hizo fácil entender como hacer con los campos de foreign keys con los formularios de django, por lo cual preferí hacer mis propios formularios desde cer.
## Modelos
He hecho uso de 5 modelos:
### User
Se utiliza al abstract user brindado por Django para llevar el registro de usuarios
### Listing
Lleva el registro de todos los listados hechos por el usuario, podemos destacar que tiene dos campos foreign key para los users y las ofertas; y un campo many to many para la watchlist
### Offers
Se lleva registro de todas las ofertas hechas en las distintas listas.
### Comments
Lleva registro de todos los comentarios realizados en las distintas listas
### Winners
Lleva un registro de los ganadores de las distintas listas.
## Categories
Al usuario se le solicita elegir una categoría, sin embargo el valor predeterminado del selector es "No category" que devuelve un string falsy, lo que se toma como None en views, por lo cual la categoría resulta opcional.
