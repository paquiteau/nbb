===============
Next Bus Bot
===============

A bot/ cli tool that simply gives you the waiting times for next buses at your favorite bus stop.

It works only for the IDFM/RATP Network, relying on the api ``lines/v4``. For now only a handfull of bus stops on the Plateau de Saclay are registered, but you can add your own


.. warning::

   I am not responsible if you arrive late at your work.
   For serious travel planning, use your favorite app.

Example
-------
::

   $ nbb mdv
   Next buses at Mare du Vivier:
   - ⏰  6 min. (12:29)  9️⃣ 🚍 ▶ Centre Commercial Ulis 2
   - ⏰ 27 min. (12:50)  9️⃣ 🚍 ▶ Gare de Jouy en Josas
   - ⏰ 35 min. (12:58)  9️⃣ 🚍 ▶ Centre Commercial Ulis 2
   - ⏰ 53 min. (13:16)  9️⃣ 🚍 ▶ Christ de Saclay


Installation
============

Pip Installation
----------------

::

   $ pip install next-bus-bot


Developer Installation
----------------------

1. clone the repo ::

   $ git clone git@github.com:paquiteau/nbb/

2. create your venv with your favorite tool
3. Install locally the package with bells and whistles ::

   $ (venv) pip install -e .[dev,test]


TODO
----
 - automatic aliasing of stops (based on initials)
 - support for direction filtering
 - Add support for a bot front-end (slack, discord, IRC, etc).
 - Extend the useful bus stops.

Configuration
=============

nbb can be configured via its command line argument, or via a config file `nbb_conf.toml`, it uses `TOML https://toml.io/en/` syntax formatting. Suitable location for the config file are, loaded in this order:

 1. `nbb/nbb_conf.toml`
 2. `~/.config/nbb_conf.toml`
 3. `nbb_conf.toml` in current directory.
 4. `nbb --config <file>`


An example (and default) config file is available in `nbb/nbb_conf`, and a example config is:

.. code-block:: toml

    [cli]
    # Default parameters for the CLI
    pretty = true     # Emoji in the terminal
    compact = false    # More condensed output
    verbose = false    # More verbose output, only for debugging.

    [stop.places]
    # List of bus stops, with their name and their ID
    # You can find the ID of a stop by looking at the URL of the stop on the IDFM website
    # https://data.iledefrance-mobilites.fr/explore/dataset/zones-de-correspondance/custom/?disjunctive.zdctype

    # The name of the step as a key does not matter,
    # it should only be consistent between the stops, stops.aliases and stop.directions sections.
    #
    # The first stop defined is the default one.

    [stop.aliases]
    # Aliases for the stops defined in stop.places
    "Mare du Vivier" = ["CEA Porte Sud", "Neurospin", "nsp", "mdv"]
    "Moulon" = ["ens"]
    "Raoul Dautry" = ["CEA Porte Est"]
    "Place Marguerite Perey" = ["Inria"]


    [stop.direction_filter]
    # Direction filter for the stops defined in stop.places.

    # For each stop you can filter the direction
    "Mare du Vivier" = ["Gare du Guichet", "Centre Commercial Ulis 2"]      # Only keep the buses that have either 'gare du guichet'  or  'Centre commercial ulis2' as destination.
    "Moulon" = ["Gare du Guichet", "Centre Commercial Ulis 2"]      # Only keep the gare du guichet  and Centre commercial ulis2
