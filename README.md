Drinkit – Die Getränkeverwaltung vom AStA am KIT
================================================
Wird benutzt um das Guthaben/die Schulden von den Menschen zu erfassen die sich in die Liste am Getränkekühlschrank eingetragen haben, Erinnerungsmails zu verschicken und neue Strichlisten zu drucken.

Das System basiert auf dem Django-Framework und benutzt Reportlab für das generieren der Strichliste.

Installation
------------
1. Virtualenv anlegen: `pyvenve venv`
2. Virtualenv aktivieren: `source venv/bin/activate`
3. Abhängigkeiten installieren: `pip3 install -r venv_requirements.txt`
4. private_settings anlegen: `cp drinkit_site/private_settings.py.sample drinkit_site/private_settings.py`
5. Im private_settings.py den Debug-Modus ausschalten
6. Im private_settings.py einen neuen SECRET_KEY genenerieren
7. Im private_settings.py den Datenbankzugang konfigurieren
8. Wenn die Software jenseits des AStA am KIT betrieben werden soll, dann in der settings.py die Optionen ALLOWED_HOSTS und EMAIL_HOST anpassen.
9. Datenbankstruktur anlegen: `./manage.py migrate`
10. Static Files generieren: `./manage.py collectstatic`
11. Webserver so konfigurieren, dass er die wsgi.py per WSGI aufruft, und die Dateien im static Ordner statisch unter dem Pfad <domain>/static/ ausliefert. Pro-Tipp: Webserver so einrichten, dass er seine Konfiguration beim aktualisieren der `drinkit_site/settings.py` neu lädt (damit man für das Aktualisieren keine Root-Rechte braucht).

Updates
-------
Wenn eine neue Django-Version erscheint sollte man folgendes tun:

1. Virtualenv aktivieren: `source venv/bin/activate`
2. Updates auflisten: `pip list -o`
3. Updates installieren: `pip3 install --upgrade -r venv_requirements.txt`
4. Static Files generieren: `./manage.py collectstatic`
5. Dem Webserver mitteilen dass sich was geändert hat: `touch drinkit_site/settings.py`
6. Virtualenv deaktivieren: `deactivate`
7. Wenn man Lust hat noch die ``venv_requirements.txt`` aktualisieren, committen und pushen

Bei Fragen oder Problemen
-------------------------
Das Ding wurde 2015 von Michael Tänzer (aka Mimi) geschrieben. Der ist hoffentlich noch unter neo@nhng.de erreichbar.

Lizenz
------
Wie es sich für dieses Projekt gehört, ist es so genannte Beer-Ware. Soll heißen, dass ihr damit machen könnt was auch immer ihr wollt, und wenn wir uns treffen und ihr das Projekt nützlich findet dann könnt ihr mir ja ein Bier ausgeben wenn ihr wollt. Da man in Deutschland Software nicht so einfach als Public Domain deklarieren kann, steht Drinkit formal unter der CC0-Lizenz, die dem noch am nächsten kommt. Die benutzten Libraries/Module unterliegen allerdings zum großen Teil anderen Lizenzen. Dazu gehört auch die Library StickyTableHeaders (MIT-Lizenz) die aus Gründen des einfacheren Deployments direkt mit Drinkit ausgeliefert wird.

Verbesserungsvorschläge, insbesondere in Form von Pull-Requests, werden gern entgegen genommen.