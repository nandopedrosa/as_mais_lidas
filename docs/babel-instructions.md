Flask-Babel instructions:

Execute these commands on the root of your application (where the README file is)

==== Initial Settings ====

1. Initial text extraction: pybabel extract -F babel.cfg -o messages.pot app 

2. Generating a language catalog: pybabel init -i messages.pot -d app/translations -l pt

3. Then you can edit the translations with PoeEdit

4. After you have done that, you have to compile to publish the texts: pybabel compile -d app/translations

==== Updating ====

If you already have a language catalog (translations/.po files), when  you update your texts, you have to:

1. Extract your template file (.pot) again: pybabel extract -F babel.cfg -o messages.pot app

2. Update your translations: pybabel update -i messages.pot -d app/translations 

AND DON'T FORGET TO ALWAYS COMPILE: pybabel compile -d app/translations

=== LAZY GETTEXT ===

Note: if you want to extract with LAZY_GETTEXT, you have to inform the -K parameter. Like this:

pybabel extract -F babel.cfg -k lazy_gettext -o messages.pot app
