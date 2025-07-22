Project: REALM is a community project dedicated to the development of REALM MMORPG.<BR><BR>

REALM is planned to be an open world fantasy role-playing adventure. At the moment the world is in a pre-development state.<br>
This means that it is constantly being reworked, torn down and rebuilt, it's full of bugs and emtpy place-holder objects, and so on.
<BR>
<BR>The Auth Server, Realm Server, and World Servers along with their Databases have been extensively developed with structures in place for implementing features easily.
<BR>
Right now the focus is on the authentication, user account front end and account creation, realm selection, character selection, and world placement.<BR>
<BR>
Once this has been expanded upon, the next focus will be the UI Design and Manager scripts. Here are some features planned for REALM:<BR>
<BR>
Dynamic Changing Interface (DCI) - The interface will change based on current class.<BR>
Dynamic Input Manager (DIM) - The user input for casting/attacking/etc will also change based on the Class.<BR>
Spell and Ability Fusion (FUSE) - A manager to allow spell fusion to melee and other weapons and attacks.<BR>
Dynamic Building Plots - (PLOT) - A system to handle dynamic building plot locaitons based on terrain features.<BR>
Arkitect - A sophisticated and advanced building UI and system for players to create buildings and contructs on Plots. <BR>
Open World Building - Players will be able to create empires (similar to guilds in other MMOs), large structures such as castles, and create community settlements that can progress. <BR>
<BR>
<BR>
We will add more to the list as features are confirmed and their mechanics and have more details.

## Setup

To install the Python dependencies for the Realm Server:

```bash
cd "Realm Server 1.12"
pip install -r requirements.txt
```

This installs `flask`, `pymysql`, `sqlalchemy` and `pytest`.
