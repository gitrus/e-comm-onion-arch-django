# e-comm-onion-arch-django
Example of python onion arch project(django): Ecomm

This project demonstrates a modular monolith architecture using Django and Django-Ninja.
A modular monolith in this context means that services are divided into modules within a single repository.
For example, the order service is a module, the product service is a module, etc.It is modular monolith on django + django-ninja.
The project uses onion architecture, so all layers are provided through a dependency injector.

To achieve modularity, encapsulation techniques are used:
- Each module has its own api and urls.py
- Each module does not share its repository layer and models (database models) with other modules
- Each module has its own set of tests. These tests check behavior, so the same part of the system can be tested twice among different modules to ensure encapsulation

However, modules can use the service layer from other modules. This usage is encapsulated into a local repository to:
- Provide a contract for using other services
- Encapsulate the calls to other services as it would be in real services


[IN PROGRESS] Use cases:
- get  available product list
- CRUD for order (almost done)
- authentication through jwt token + related user entity
