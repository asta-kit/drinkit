Drinkit – Die Getränkeverwaltung vom AStA am KIT
================================================
Wird benutzt um das Guthaben/die Schulden von den Menschen zu erfassen die sich in die Liste am Getränkekühlschrank eingetragen haben, Erinnerungsmails zu verschicken und neue Strichlisten zu drucken.

Das System basiert auf dem Django-Framework und benutzt Reportlab für das generieren der Strichliste.

Updates
-------
Wenn eine neue Django-Version erscheint sollte man folgendes tun:

1. Virtualenv aktivieren: `source venv/bin/activate`
2. Updates auflisten: `pip list -o`
3. Updates installieren: `pip install -U Django`
4. Dem Webserver mitteilen dass sich was geändert hat: `touch drinkit_site/settings.py`
5. Virtualenv deaktivieren: `deactivate`
6. Wenn man Lust hat noch die ``venv_requirements.txt`` aktualisieren, committen und pushen

Bei Fragen oder Problemen
-------------------------
Das Ding wurde 2015 von Michael Tänzer (aka Mimi) geschrieben. Der ist hoffentlich noch unter neo@nhng.de erreichbar.
